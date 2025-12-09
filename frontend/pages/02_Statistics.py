# Statistics page

import streamlit as st
import requests
import pandas as pd
import plotly.express as px

def get_classes_without_prerequisites():
    url = f"{st.secrets["api"]["base_url"]}/stats/classes-without-prereqs"
    response = requests.get(url=url)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_sections_by_day(year, semester):
    url = f"{st.secrets["api"]["base_url"]}/stats/sections-by-day"
    request_json = {
        "year": year,
        "semester": semester
    }
    response = requests.get(url=url, json=request_json)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_top_classes_by_duration(year, semester, limit):
    url = f"{st.secrets["api"]["base_url"]}/stats/top-classes-by-avg-duration"
    request_json = {
        "year": year,
        "semester": semester,
        "limit": int(limit)
    }
    response = requests.get(url=url, json=request_json)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_top_rooms_by_utilization(year, semester, limit):
    url = f"{st.secrets["api"]["base_url"]}/stats/top-rooms-by-utilization"
    request_json = {
        "year": year,
        "semester": semester,
        "limit": int(limit)
    }
    response = requests.get(url=url, json=request_json)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_multi_room_classes(year, semester, limit, orderby):
    url = f"{st.secrets["api"]["base_url"]}/stats/multi-room-classes"
    request_json = {
        "year": year,
        "semester": semester,
        "limit": int(limit),
        "orderby": orderby
    }
    response = requests.get(url=url, json=request_json)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_top_departments_by_sections(year, semester, limit):
    url = f"{st.secrets["api"]["base_url"]}/stats/top-departments-by-sections"
    request_json = {
        "year": year,
        "semester": semester,
        "limit": int(limit)
    }
    response = requests.get(url=url, json=request_json)

    if response.status_code == 200:
        return response.json()
    else:
        return None

st.title("RUMAD 2.0")
st.header("Statistics")

if st.session_state["logged_in"]:
    st.write(f"Hi, {st.session_state["name"]}! Check out these stats!\n\n\n")
    # CLASSES WITHOUT PREREQUISITES
    st.subheader("Classes without prerequisites")

    # For class in classes without prereqs, write a bullet
    classes_without_prerequisites = get_classes_without_prerequisites()

    if classes_without_prerequisites:
        for c in classes_without_prerequisites:
            st.markdown(f"- {c["fullcode"]}")
    else:
        st.write("No classes without prerequisites.")

    # SECTIONS BY DAY OF WEEK
    st.subheader("Sections by day of week")
    year = st.text_input("Year", value="2025", help="Enter a year like 2025")
    semester = st.text_input("Semester", value="Fall", help="Enter a semester from Fall, Spring, V1, V2")

    if st.button("Plot Sections by Day of Week"):
        if not (year and semester):
            st.error("Please enter year and semester.")
        else:
            data = get_sections_by_day(year, semester)

        if not data:
            st.write("No sections available for this year and semester combination.")
        else:
            df = pd.DataFrame(data)

            day_order = ["L", "M", "W", "J", "V", "S", "D"]
            df["day"] = pd.Categorical(df["day"], categories=day_order, ordered=True)
            df = df.sort_values(by=["day"])

            fig_sections_by_day_of_week = px.bar(
                df,
                x="day",
                y="sections",
                labels={"day": "Day of the Week", "sections": "Number of sections"},
                title=f"Sections by Day of Week for {semester} {year}",
            )

            fig_sections_by_day_of_week.update_layout(xaxis=dict(dtick=1))
            st.plotly_chart(fig_sections_by_day_of_week, use_container_width=True)

    # TOP CLASSES BY AVERAGE DURATION
    st.subheader("Top Classes By Average Duration")
    limit_top_classes_by_duration = st.number_input("Limit top classes", value=1, min_value=1, max_value=10, step=1, help="Limit the number of classes displayed up to 10.")

    if st.button("Plot Top Classes by Duration"):
        if not (year and semester and limit_top_classes_by_duration and 0 < int(limit_top_classes_by_duration) <= 10):
            st.error("Please enter year, semester, and limit within 1 and 10.")
        else:
            data = get_top_classes_by_duration(year, semester, limit_top_classes_by_duration)

        if not data:
            st.write("No classes available for this year and semester combination.")
        else:
            df_top_classes_by_duration = pd.DataFrame(data)
            df_top_classes_by_duration["fullcode"] = pd.Categorical(df_top_classes_by_duration["fullcode"], categories=df_top_classes_by_duration["fullcode"].values, ordered=True)
            df_top_classes_by_duration = df_top_classes_by_duration.sort_values(by=["avg_minutes"], ascending=False)

            fig_top_classes_by_duration = px.bar(
                df_top_classes_by_duration,
                x="fullcode",
                y="avg_minutes",
                labels={"fullcode": "Class Code", "avg_minutes": "Average Minutes"},
                title=f"Top {limit_top_classes_by_duration} Classes by Average Duration for {semester} {year}"
            )

            fig_top_classes_by_duration.update_layout(xaxis=dict(dtick=1))
            st.plotly_chart(fig_top_classes_by_duration, use_container_width=True)

    # TOP ROOMS BY AVERAGE UTILIZATION
    st.subheader("Top Rooms by Average Duration")
    limit_top_rooms_by_utilization = st.number_input("Limit top rooms", value=5, min_value=1, max_value=10, help="Limit the number of rooms displayed up to 10.")

    if st.button("Plot Top Rooms by Utilization"):
        if not (year and semester and limit_top_rooms_by_utilization and 0 < int(limit_top_rooms_by_utilization) <= 10):
            st.error("Please enter year, semester, and limit within 1 and 10.")
        else:
            data = get_top_rooms_by_utilization(year, semester, limit_top_rooms_by_utilization)

        if not data:
            st.write("No rooms available for this year and semester combination.")
        else:
            df_top_rooms_by_utilization = pd.DataFrame(data)
            # Concatename building and room number
            df_top_rooms_by_utilization["fullname"] = df_top_rooms_by_utilization["building"] + " " + df_top_rooms_by_utilization["room_number"]
            df_top_rooms_by_utilization["fullname"] = pd.Categorical(df_top_rooms_by_utilization["fullname"], categories=df_top_rooms_by_utilization["fullname"].values)
            df_top_rooms_by_utilization = df_top_rooms_by_utilization.sort_values(by=["utilization"], ascending=False)

            fig_top_rooms_by_utilization = px.bar(
                df_top_rooms_by_utilization,
                x="fullname",
                y="utilization",
                labels={"fullname": "Room", "utilization": "Utilization"},
                title=f"Top {limit_top_rooms_by_utilization} Rooms by Utilization for {semester} {year}"
            )

            fig_top_rooms_by_utilization.update_layout(xaxis=dict(dtick=1))
            st.plotly_chart(fig_top_rooms_by_utilization, use_container_width=True)

    # MULTI-ROOM CLASSES
    st.subheader("Distinct Rooms per Class")
    limit_multiroom_classes = st.number_input("Limit Multi-Room Classes", value=5, min_value=1, max_value=10, help="Limit the number of classes displayed up to 10.")
    order_input = st.selectbox("Sorting Order", ["Ascending", "Descending"], index=1)

    orderby = {"Ascending": "asc", "Descending": "desc"}
    order = {"Ascending":True, "Descending":False}

    if st.button("Plot Distinct Rooms per Class"):
        if not (year and semester and order_input and limit_multiroom_classes and 0 < int(limit_multiroom_classes) <= 10):
            st.error("Please enter year, semester, and limit within 1 and 10.")
        else:
            data = get_multi_room_classes(year, semester, limit_multiroom_classes, orderby[order_input])

        if not data:
            st.write("No rooms available for this year and semester combination.")
        else:
            df_multi_room_classes = pd.DataFrame(data)
            df_multi_room_classes["fullcode"] = pd.Categorical(df_multi_room_classes["fullcode"], categories=df_multi_room_classes["fullcode"].values)
            df_multi_room_classes = df_multi_room_classes.sort_values(by=["distinct_rooms"], ascending=order[order_input])

            fig_multi_room_classes = px.bar(
                df_multi_room_classes,
                x="fullcode",
                y="distinct_rooms",
                labels={"fullcode": "Class", "distinct_rooms": "Distinct Rooms"},
                title=f"Distinct Rooms per class for {semester} {year}"
            )

            fig_multi_room_classes.update_layout(xaxis=dict(dtick=1))
            st.plotly_chart(fig_multi_room_classes, use_container_width=True)

    # TOP DEPARTMENTS BY SECTIONS
    st.subheader("Top Departments by Sections")
    limit_top_departments_by_sections = st.number_input("Limit Departments", value=1, min_value=1, max_value=10, help="Limit the number of departments displayed up to 10.")

    if st.button("Plot Top Departments by Sections"):
        if not (year and semester and limit_top_departments_by_sections and 0 < int(limit_top_departments_by_sections) <= 10):
            st.error("Please enter year, semester, and limit within 1 and 10.")
        else:
            data = get_top_departments_by_sections(year, semester, limit_top_departments_by_sections)

        if not data:
            st.write("No departments available for this year and semester combination.")
        else:
            df_top_departments_by_sections = pd.DataFrame(data)
            df_top_departments_by_sections["department"] = pd.Categorical(df_top_departments_by_sections["department"].values)
            df_top_departments_by_sections = df_top_departments_by_sections.sort_values(by=["sections"], ascending=False)

            fig_top_departments_by_sections = px.bar(
                df_top_departments_by_sections,
                x="department",
                y="sections",
                labels={"department": "Department", "sections": "Sections"},
                title=f"Top {limit_top_departments_by_sections} Departments by Sections for {semester} {year}"
            )

            fig_top_departments_by_sections.update_layout(xaxis=dict(dtick=1))
            st.plotly_chart(fig_top_departments_by_sections, use_container_width=True)

else:
    st.error("You must be logged in to access this page.")