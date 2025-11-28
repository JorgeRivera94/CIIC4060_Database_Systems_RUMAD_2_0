import os
import pandas as pd
import sqlite3
import json
import xml.etree.ElementTree as ET
import re
import requests


# Extract functions

# .csv
def extract_csv(input_path, output_path):
    df = pd.read_csv(input_path)
    df.to_csv(output_path, index=False)


# .json
def extract_json(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    def safe_int(x):
        # return int or None
        try:
            return int(str(x).strip())
        except Exception:
            return None

    rows = []

    def try_add_row(building_name, item):
        rid = item.get("rid", item.get("id"))
        room_number = item.get("room_number", item.get("number"))
        capacity = item.get("capacity")

        # Normalize fields
        building = ("" if building_name is None else str(building_name).strip())
        room_number = None if room_number is None else str(room_number).strip()
        rid_i = safe_int(rid)
        cap_i = safe_int(capacity)

        # Skip rows with null values
        if not building or not room_number or rid_i is None or cap_i is None:
            return

        rows.append({
            "rid": rid_i,
            "building": building,
            "room_number": room_number,
            "capacity": cap_i
        })

    for building, items in data.items():
        if isinstance(items, list):
            for item in items:
                try_add_row(building, item)
        elif isinstance(items, dict):
            try_add_row(building, items)

    # Sorted Dataframe by rid
    df = pd.DataFrame(rows, columns=["rid", "building", "room_number", "capacity"])
    df = df.sort_values("rid").reset_index(drop=True)

    df.to_csv(output_path, index=False)


# .xml
def extract_xml(input_path, output_path):
    _ILLEGAL_XML_10 = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F]")

    with open(input_path, "r", encoding="utf-8", errors="replace") as f:
        raw = f.read()
    raw = raw.lstrip("\ufeff")
    raw = _ILLEGAL_XML_10.sub("", raw)

    # Wrap the whole thing so multiple top-level elements become children of ROOT
    wrapped = f"<ROOT>\n{raw}\n</ROOT>"
    root = ET.fromstring(wrapped)

    # This section used GenAI to help debug:
    # If your repeated unit is <Courses>, grab all of them; otherwise fall back to children
    records = root.findall("Courses") or list(root)

    rows = []
    for rec in records:
        row = {}
        # attributes (if any)
        for k, v in rec.attrib.items():
            row[f"@{k}"] = v
        # children
        for child in rec:
            if child.tag == "classes":
                # flatten nested <classes>
                for sub in child:
                    row[f"classes.{sub.tag}"] = (sub.text or "").strip()
                for k, v in child.attrib.items():
                    row[f"classes.@{k}"] = v
            else:
                row[child.tag] = (child.text or "").strip()
                for k, v in child.attrib.items():
                    row[f"{child.tag}.@{k}"] = v
        rows.append(row)

    df = pd.DataFrame(rows or [{}])
    df.to_csv(output_path, index=False)


# .db
def extract_db(input_path, output_path):
    conn = sqlite3.connect(input_path)
    cursor = conn.cursor()

    cursor.execute("Select name From sqlite_master Where type='table';")
    tables = [t[0] for t in cursor.fetchall()]

    for table in tables:
        df = pd.read_sql_query(f"Select * From {table}", conn)
        table_output_path = output_path.replace(".csv", f"_{table}.csv")
        df.to_csv(table_output_path, index=False)


# To download syllabi
def download_syllabi(url, department, code, name):
    response = requests.get(url)

    with open(f"ETL/Extract/syllabuses/{department}-{code}-{name}.pdf", "wb") as f:
        f.write(response.content)
        f.close()


# Main call to Extract the given files
def main():
    # Source and destination directories
    src_dir = "ETL/project_data/"
    dst_dir = "ETL/Extract/extracted_data/"

    for filename in os.listdir(src_dir):
        input_path = os.path.join(src_dir, filename)
        name, ext = os.path.splitext(filename)
        output_path = os.path.join(dst_dir, f"{name}.csv")

        if ext == ".csv":
            extract_csv(input_path, output_path)
        elif ext == ".json":
            extract_json(input_path, output_path)
        elif ext == ".xml":
            extract_xml(input_path, output_path)
        elif ext == ".db":
            extract_db(input_path, output_path)
        else:
            print(f"Unhandled extension {ext} for file {filename}.")

    # After converting the files to CSV
    courses_path = "ETL/Extract/extracted_data/courses.csv"
    df = pd.read_csv(courses_path)

    for row in df.itertuples():
        # As the schema for these rows is Pandas(Index, classes.code, classes.name, classid, cred, description, syllabus, term, years),
        # The mappings will be:
        url = row[6]
        department = row[2]
        code = row[1]
        name = row[5]

        if type(url) == str:
            name = name.replace(" ", "-")
            download_syllabi(url, department, code, name)


if __name__ == "__main__":
    main()