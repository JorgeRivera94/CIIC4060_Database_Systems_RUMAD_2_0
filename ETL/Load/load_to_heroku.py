import pandas as pd
import psycopg2
from psycopg2 import sql

DATABASE_URL = "postgres://u7ve47tk2bll2p:pf62c4799770f5b46bb61127026d2ffb543bf759a1221e6f9cb86b2dc0dde73b2@c57oa7dm3pc281.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/dfcsar0vfdptop"

# Load CSVs
classes = pd.read_csv("../Transform/new_transformed_data/class.csv")
sections = pd.read_csv("../Transform/new_transformed_data/section.csv")
rooms = pd.read_csv("../Transform/new_transformed_data/room.csv")
meetings = pd.read_csv("../Transform/new_transformed_data/meeting.csv")
requisites = pd.read_csv("../Transform/new_transformed_data/requisite.csv")

# Format strings
classes["ccode"] = (classes["ccode"].astype("string").str.zfill(4))
meetings["ccode"] = (meetings["ccode"].astype("string").str.zfill(3))
rooms["room_number"] = (rooms["room_number"].astype("string").str.zfill(3))

# Format time to datetime in ISO-8601
default_date = pd.Timestamp("1900-01-01")
meetings["starttime"] = default_date + pd.to_timedelta(meetings["starttime"])
meetings["endtime"] = default_date + pd.to_timedelta(meetings["endtime"])

# Connect to Postgres
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

def insert_table(df, table_name):
    if df.empty:
        print(f"No rows to insert into {table_name}")
        return
    for _, row in df.iterrows():
        cols = list(row.index)
        vals = [row[c] for c in cols]
        insert = sql.SQL(
            "INSERT INTO {} ({}) VALUES ({}) ON CONFLICT DO NOTHING"
        ).format(
            sql.Identifier(table_name),
            sql.SQL(', ').join(map(sql.Identifier, cols)),
            sql.SQL(', ').join(sql.Placeholder() * len(cols))
        )
        cur.execute(insert, vals)
    conn.commit()
    print(f"Inserted {len(df)} rows into {table_name}")

# Load tables in order respecting foreign keys
insert_table(rooms, "room")
insert_table(meetings, "meeting")
insert_table(classes, "class")
insert_table(sections, "section")
insert_table(requisites, "requisite")

cur.close()
conn.close()