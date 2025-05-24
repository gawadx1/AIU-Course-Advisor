# src/editor.py

import pandas as pd

class CourseEditor:
    def __init__(self, core_file_path, elective_file_path):
        self.core_courses = pd.read_csv(core_file_path)
        self.elective_courses = pd.read_csv(elective_file_path)

    def get_combined_courses(self):
        return pd.concat([self.core_courses, self.elective_courses], ignore_index=True)

    def list_all_courses(self):
        return self.get_combined_courses()[['CourseCode', 'CourseName', 'CreditHours']]

    def find_course(self, code):
        combined = self.get_combined_courses()
        return combined[combined['CourseCode'] == code]

    def add_course(self, course_data, is_core=True):
        df = self.core_courses if is_core else self.elective_courses
        df.loc[len(df)] = course_data

    def save_courses(self, core_path=None, elective_path=None):
        if core_path:
            self.core_courses.to_csv(core_path, index=False)
        if elective_path:
            self.elective_courses.to_csv(elective_path, index=False)
