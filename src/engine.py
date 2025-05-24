# src/engine.py

from experta import *
import pandas as pd

class Student(Fact):
    pass

class Advisor(KnowledgeEngine):
    def __init__(self, student_info, combination, policies_file):
        super().__init__()
        self.student_info = student_info
        self.combination = combination
        self.policies_file = policies_file
        self.recommendation = []
        self.explanation = []
        self.max_credits = 0

    @Rule(Student(CGPA=P(lambda x: x < 2.0)))
    def low_credit_limit(self):
        self.max_credits = int(self.policies_file.loc[self.policies_file["Condition"] == 'CGPA<2.0', 'Value'].values[0])
        self.explanation.append(f"Max Credits limit is {self.max_credits} because CGPA < 2.0")

    @Rule(Student(CGPA=P(lambda x: 2.0 <= x < 3.0)))
    def medium_credit_limit(self):
        self.max_credits = int(self.policies_file.loc[self.policies_file["Condition"] == '2.0<=CGPA<3.0', 'Value'].values[0])
        self.explanation.append(f"Max Credits limit is {self.max_credits} because 2.0 <= CGPA < 3.0")

    @Rule(Student(CGPA=P(lambda x: x >= 3.0)))
    def high_credit_limit(self):
        self.max_credits = int(self.policies_file.loc[self.policies_file["Condition"] == 'CGPA>=3.0', 'Value'].values[0])
        self.explanation.append(f"Max Credits limit is {self.max_credits} because CGPA >= 3.0")

    @Rule(Student(CGPA=MATCH.cgpa, Passed=MATCH.passed, Failed=MATCH.failed, Semester=MATCH.semester))
    def recommend_courses(self, cgpa, passed, failed, semester):
        total_credits = 0
        for _, row in self.combination.iterrows():
            code = row['CourseCode']
            name = row['CourseName']
            credit_hours = row['CreditHours']
            prerequisites = str(row['Prerequisites']).split(',') if pd.notna(row['Prerequisites']) else []
            co_requisites = str(row['CoRequisites']).split(',') if 'CoRequisites' in row and pd.notna(row['CoRequisites']) else []
            offered = row['semester']

            if code in passed:
                continue
            if offered not in (semester, 'Both'):
                continue
            if not all(req.strip() in passed for req in prerequisites if req.strip()):
                self.explanation.append(f"{code} not recommended: missing prerequisite(s): {', '.join(prerequisites)}")
                continue
            if not all(co.strip() in passed or co.strip() in failed for co in co_requisites if co.strip()):
                self.explanation.append(f"{code} not recommended: co-requisites not satisfied")
                continue

            if total_credits + credit_hours > self.max_credits:
                continue

            if code in failed:
                self.explanation.append(f"{code} prioritized: previously failed")

            self.recommendation.append({
                'Course code': code,
                'Course Name': name,
                'Credit Hours': credit_hours
            })
            total_credits += credit_hours
            self.explanation.append(f"{code} recommended")
