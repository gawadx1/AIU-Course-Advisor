# app/app.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from src.engine import Advisor, Student
from src.editor import CourseEditor
from src.explanation import ExplanationLogger

class InferenceEngineMain:
    def __init__(self, core_path, elective_path, policies_path):
        self.editor = CourseEditor(core_path, elective_path)
        self.policies = pd.read_csv(policies_path)
        self.combined_courses = self.editor.get_combined_courses()
        self.logger = ExplanationLogger()

    def run_inference(self, student_info):
        advisor = Advisor(student_info, self.combined_courses, self.policies)
        advisor.explanation = self.logger.explanations
        advisor.reset()
        advisor.declare(Student(**student_info))
        advisor.run()
        return advisor.recommendation, self.logger.get_all()

# --- Streamlit UI ---
st.set_page_config(page_title="Course Recommendation Advisor")
st.title("📘 Course Recommendation Advisor")

menu = st.sidebar.radio("Choose Mode", ["Run Advisor", "Edit Course Files"])

# Load default paths
core_file = "data/Cyber Security Track Courses Updated.csv"
elective_file = "data/Elective courses.csv"
policies_file = "data/policies.csv"

if menu == "Edit Course Files":
    st.subheader("🛠️ Course Knowledge Base Editor")
    st.markdown("Upload and preview course files to update the system's knowledge base.")

    uploaded_core = st.file_uploader("Upload Core Courses CSV", type="csv")
    uploaded_electives = st.file_uploader("Upload Elective Courses CSV", type="csv")

    if uploaded_core:
        core_df = pd.read_csv(uploaded_core)
        core_df.to_csv("data/Cyber Security Track Courses Updated.csv", index=False)
        st.success("Core courses updated.")
        st.dataframe(core_df)

    if uploaded_electives:
        elective_df = pd.read_csv(uploaded_electives)
        elective_df.to_csv("data/Elective courses.csv", index=False)
        st.success("Elective courses updated.")
        st.dataframe(elective_df)

else:
    st.sidebar.header("Student Information")
    cgpa = st.sidebar.number_input("Enter CGPA", min_value=0.0, max_value=4.0, step=0.01)
    semester = st.sidebar.selectbox("Current Semester", ["FALL", "SPRING"])

    all_courses = pd.concat([
        pd.read_csv(core_file),
        pd.read_csv(elective_file)
    ], ignore_index=True)

    course_codes = all_courses['CourseCode'].dropna().unique().tolist()

    passed_courses = st.sidebar.multiselect("Select Passed Courses", course_codes)
    failed_courses = st.sidebar.multiselect("Select Failed Courses", course_codes)

    if st.sidebar.button("Run Advisor"):
        student_info = {
            'CGPA': cgpa,
            'Passed': passed_courses,
            'Failed': failed_courses,
            'Semester': semester.upper()
        }

        engine = InferenceEngineMain(core_file, elective_file, policies_file)
        recs, expls = engine.run_inference(student_info)

        st.subheader("📚 Recommended Courses")
        if recs:
            st.dataframe(pd.DataFrame(recs))
        else:
            st.info("No courses recommended based on current information.")

        st.subheader("🧠 Explanation")
        for e in expls:
            st.markdown(f"- {e}")
