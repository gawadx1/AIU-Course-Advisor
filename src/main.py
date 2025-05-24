# src/main.py

from engine import Advisor, Student
from editor import CourseEditor
from explanation import ExplanationLogger
from experta import *
import pandas as pd

class InferenceEngineMain:
    def __init__(self, core_path, elective_path, policies_path):
        self.editor = CourseEditor(core_path, elective_path)
        self.policies = pd.read_csv(policies_path)
        self.combined_courses = self.editor.get_combined_courses()
        self.logger = ExplanationLogger()

    def run_inference(self, student_info):
        advisor = Advisor(student_info, self.combined_courses, self.policies)
        advisor.explanation = self.logger.explanations  # Connect the logger

        advisor.reset()
        advisor.declare(Student(**student_info))
        advisor.run()

        recommendations = advisor.recommendation
        explanations = self.logger.get_all()

        return recommendations, explanations


# Example usage
if __name__ == '__main__':
    core_file = "Cyber Security Track Courses Updated.csv"
    elective_file = "Elective courses.csv"
    policies_file = "policies.csv"

    print("Enter Student Information")
    cgpa = float(input("Enter CGPA: "))
    passed = input("Enter passed courses (comma-separated): ").split(',')
    failed = input("Enter failed courses (comma-separated): ").split(',')
    semester = input("Enter semester (FALL/SPRING): ").upper()

    student_info = {
        'CGPA': cgpa,
        'Passed': [course.strip() for course in passed if course.strip()],
        'Failed': [course.strip() for course in failed if course.strip()],
        'Semester': semester
    }

    engine = InferenceEngineMain(core_file, elective_file, policies_file)
    recs, expls = engine.run_inference(student_info)

    print("\nRecommended Courses:")
    for r in recs:
        print(r)

    print("\nExplanations:")
    for e in expls:
        print(e)
