#!/usr/bin/env python3

import csv 
import json
import pandas as pd


data = [
    [101, "Computer Science", 3, "Yes", "15.0"],
    [102, "Economics", 3.5, "No", "12.5"],
    [103, "Mathematics", 4, "Yes", "18.0"],
    [104, "Data Science", 2.8, "No", "10.5"],
    [105, "Psychology", 3, "Yes", "14.0"]
]

headers = ["student_id", "major", "GPA", "is_cs_major", "credits_taken"]

with open("raw_survey_data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(data)

courses = [
    {
        "course_id": "DS2002",
        "section": "001",
        "title": "Data Science Systems",
        "level": 200,
        "instructors": [
            {"name": "Austin Rivera", "role": "Primary"},
            {"name": "Heywood Williams-Tracy", "role": "TA"}
        ]
    },
    {
        "course_id": "ECON4190",
        "section": "001",
        "title": "Industrial Organization",
        "level": 400,
        "instructors": [
            {"name": "Federico Ciliberto", "role": "Primary"},
            {"name": "Braden Wagner", "role": "TA"}
        ]
    },
    {
        "course_id": "DS3001",
        "section": "002",
        "title": "Foundations of Machine Learning",
        "level": 200,
        "instructors": [
            {"name": "Michael Freenor", "role": "Primary"}
        ]
    }
]

with open("raw_course_catalog.json", "w") as f:
    json.dump(courses, f, indent=4)

df = pd.read_csv("raw_survey_data.csv")

df['is_cs_major'] = df['is_cs_major'].map({'Yes': True, 'No': False})

df = df.astype({'GPA': 'float64', 'credits_taken': 'float64'})

df.to_csv("clean_survey_data.csv", index=False)

with open("raw_course_catalog.json", "r") as f:
    courses = json.load(f)

df_normalized = pd.json_normalize(
    courses,
    record_path=['instructors'],
    meta=['course_id', 'title', 'level', 'section'],
    errors='ignore'
)

df_normalized.to_csv("clean_course_catalog.csv", index=False)

