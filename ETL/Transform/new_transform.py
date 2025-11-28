import pandas as pd


# Funtions to transform each source file
def transform_room(rooms_src_path):
    df = pd.read_csv(rooms_src_path, na_values=[""])
    df = df.dropna()

    # Make sure records are sorted by rid
    df = df.sort_values("rid").reset_index(drop=True)

    df.to_csv("ETL/Transform/new_transformed_data/room.csv", index=False)


def transform_meeting(meeting_src_path):
    df = pd.read_csv(meeting_src_path, na_values=[""])
    df = df.dropna()

    # Change ccode to strings of 3 length with zeros at front
    df["ccode"] = (df["ccode"].astype("string").str.zfill(3))

    # Rename column names to match table diagrams
    df = df.rename(columns={
        "start": "starttime",
        "start": "starttime",
        "end": "endtime",
        "day": "cdays",
    })

    # Convert time columns from string to time type
    df["starttime"] = pd.to_datetime(df["starttime"], format="%H:%M:%S")
    df["endtime"] = pd.to_datetime(df["endtime"], format="%H:%M:%S")

    # Remove meetings in the time gap
    start_gap = pd.to_datetime("10:15:00", format="%H:%M:%S")
    to_be_moved_start = pd.to_datetime("12:00:00", format="%H:%M:%S")
    target_start = pd.to_datetime("12:30:00", format="%H:%M:%S")

    mask = ~((df["cdays"] == "MJ") & (df["starttime"] >= start_gap) & (df["starttime"] < to_be_moved_start))
    df = df[mask].reset_index(drop=True)

    # Shift MJ meetings starting at 12:00 pm onwards
    mask = (df["cdays"] == "MJ") & (df["starttime"] >= to_be_moved_start)
    if mask.any():
        # Get the index of the first row to be shifted
        first_seen_index = df.loc[mask, "starttime"].idxmin()

        # Calculate the time delta to shift values
        shift = target_start - df.at[first_seen_index, "starttime"]
        df.loc[mask, "starttime"] = df.loc[mask, "starttime"] + shift
        df.loc[mask, "endtime"] = df.loc[mask, "endtime"] + shift

    # Remove MJ meetings that end after 7:45 pm
    end_limit = pd.to_datetime("19:45:00", format="%H:%M:%S")
    mask = ~((df["cdays"] == "MJ") & (df["endtime"] > end_limit))
    df = df[mask].sort_values("mid").reset_index(drop=True)

    # Return formatting to hh:mm:ss
    df["starttime"] = df["starttime"].dt.strftime("%H:%M:%S")
    df["endtime"] = df["endtime"].dt.strftime("%H:%M:%S")

    df.to_csv("ETL/Transform/new_transformed_data/meeting.csv", index=False)


def transform_class(courses_src_path):
    df = pd.read_csv(courses_src_path, na_values=[""])

    # Rename columns to match table diagram
    df = df.rename(columns={
        "classid": "cid",
        "classes.name": "cname",
        "classes.code": "ccode",
        "description": "cdesc",
        "syllabus": "csyllabus",
    })

    # Change ccode to strings of 4 length with zeros at front
    # so dummy record's VARCHAR mathes the other records
    df["ccode"] = (df["ccode"].astype("string").str.zfill(4))

    # Reorder columns to match table diagram
    column_order = ["cid", "cname", "ccode", "cdesc", "term", "years", "cred", "csyllabus"]
    df = df[column_order]

    # Ensure classes data starts with id 2
    mask = df["cid"] >= 2
    df = df[mask].sort_values("cid").reset_index(drop=True)

    df.to_csv("ETL/Transform/new_transformed_data/class.csv", index=False)


def transform_requisite(requisites_src_path):
    df = pd.read_csv(requisites_src_path, na_values=[""])
    df = df.dropna()

    # Rename columns to match table diagram
    df = df.rename(columns={
        "cid": "classid",
        "requisiteid": "reqid",
        "preReq": "prereq",
    })

    # Change prereq values from integer to boolean
    df["prereq"] = df["prereq"].astype(bool)

    # Ensure referenced classes exist
    transformed_class_path = "ETL/Transform/new_transformed_data/class.csv"
    valid_ids = pd.read_csv(transformed_class_path, usecols=["cid"])["cid"].to_list()
    mask = (df["classid"].isin(valid_ids)) & (df["reqid"].isin(valid_ids))
    df = df[mask].sort_values(["classid", "reqid"]).reset_index(drop=True)

    df.to_csv("ETL/Transform/new_transformed_data/requisite.csv", index=False)


def transform_sections(sections_src_path):
    df = pd.read_csv(sections_src_path, na_values=[""])
    df = df.dropna()

    # Rename columns to match table diagram
    df = df.rename(columns={
        "room_id": "roomid",
        "class_id": "cid",
        "meeting_id": "mid",
        "year": "years",
    })

    # Reorder columns to match table diagram
    column_order = ["sid", "roomid", "cid", "mid", "semester", "years", "capacity"]
    df = df[column_order]

    # Sections must be taught in a valid classroom and meeting, and the class must exist
    transformed_room_path = "ETL/Transform/new_transformed_data/room.csv"
    transformed_meeting_path = "ETL/Transform/new_transformed_data/meeting.csv"
    transformed_class_path = "ETL/Transform/new_transformed_data/class.csv"

    existing_room_ids = pd.read_csv(transformed_room_path, usecols=["rid"])["rid"].to_list()
    existing_meting_ids = pd.read_csv(transformed_meeting_path, usecols=["mid"])["mid"].to_list()
    existing_class_ids = pd.read_csv(transformed_class_path, usecols=["cid"])["cid"].to_list()

    mask = (df["roomid"].isin(existing_room_ids)) & (df["mid"].isin(existing_meting_ids)) & (
        df["cid"].isin(existing_class_ids))
    df = df[mask].reset_index(drop=True)

    # Sections cannot be in overcapacity
    room_capacities = pd.read_csv(transformed_room_path, usecols=["rid", "capacity"]).set_index("rid")[
        "capacity"].to_dict()

    mask = (df["capacity"] <= df["roomid"].map(room_capacities))
    df = df[mask].reset_index(drop=True)

    # Courses must be taught in the correct years and semester
    class_years = pd.read_csv(transformed_class_path, usecols=["cid", "years"]).set_index("cid")["years"].to_dict()
    class_terms = pd.read_csv(transformed_class_path, usecols=["cid", "term"]).set_index("cid")["term"].to_dict()

    valid_year_sections = set()
    valid_semester_sections = set()

    for _, row in df.iterrows():
        cid = row["cid"]
        section_years = row["years"]
        section_semester = row["semester"]

        class_year = class_years.get(cid)
        class_term = class_terms.get(cid)

        if (class_year == "Every Year"
                or (int(section_years) % 2 == 0 and (class_year == "Even Years" or class_year == "According to Demand"))
                or (int(section_years) % 2 != 0 and (
                        class_year == "Odd Years" or class_year == "According to Demand"))):
            valid_year_sections.add(row["sid"])

        if (class_term == "According to Demand"
                or (section_semester == "Fall" and "First Semester" in str(class_term))
                or (section_semester == "Spring" and "Second Semester" in str(class_term))):
            valid_semester_sections.add(row["sid"])

    mask = (df["sid"].isin(valid_year_sections.intersection(valid_semester_sections)))
    df = df[mask].reset_index(drop=True)

    # A class can not have different sections at the same hour in the same semester and year
    # In the event of conflicts, keep the section with the lowest sid
    # Adding a starttime column to help with checking conflicts
    meeting_starttimes = pd.read_csv(transformed_meeting_path, usecols=["mid", "starttime"]).set_index("mid")[
        "starttime"].to_dict()
    df["starttime"] = df["mid"].map(meeting_starttimes)

    # Aggregate to find the idxmin sid for each (cid, semester, years, starttime) group
    aggregate = (df.groupby(["cid", "semester", "years", "starttime"])["sid"].idxmin())

    df = df.loc[aggregate.values].reset_index(drop=True)

    # Multiple sections cannot be taught in the same room at the same time
    # In the event of conflicts, keep the section with the lowest sid
    aggregate = (df.groupby(["roomid", "semester", "years", "starttime"])["sid"].idxmin())

    df = df.loc[aggregate.values].reset_index(drop=True)
    df = df.drop(columns=["starttime"])
    df = df.sort_values("sid").reset_index(drop=True)

    df.to_csv("ETL/Transform/new_transformed_data/section.csv", index=False)


def main():
    # Paths to source files to be transformed
    courses_src_path = "ETL/Extract/extracted_data/courses.csv"
    meeting_src_path = "ETL/Extract/extracted_data/meeting.csv"
    requisites_src_path = "ETL/Extract/extracted_data/requisites_requisites.csv"
    rooms_src_path = "ETL/Extract/extracted_data/rooms.csv"
    sections_src_path = "ETL/Extract/extracted_data/sections.csv"

    transform_room(rooms_src_path)
    transform_meeting(meeting_src_path)
    transform_class(courses_src_path)
    transform_requisite(requisites_src_path)
    transform_sections(sections_src_path)


if __name__ == "__main__":
    main()