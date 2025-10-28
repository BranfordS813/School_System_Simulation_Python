import json # New required import for JSON serialization
from student import Student 
from typing import List, Dict, Any, Union

class CourseManager:
    """
    A Central Data Manager for managing student objects and generating course-wide reports.
    It holds all active Student objects for a specific course.
    """
    def __init__(self, course_name: str):
        self.course_name = course_name
        self.students: List[Student] = [] # This list will hold Student objects

    def enroll_student(self, student_object: Student):
        """Adds a student object to the course roster."""
        self.students.append(student_object)
        print(f"Enrolled: {student_object.full_name_simple()} in {self.course_name}.")

    def find_student_by_id(self, student_id: str) -> Union[Student, None]:
        """
        Finds and returns a Student object from the roster by their unique system ID (sid).
        Returns the Student object if found, otherwise returns None.
        """
        for student in self.students:
            if student.sid == student_id:
                return student
        print(f"Warning: Student with ID '{student_id}' not found in course roster for {self.course_name}.")
        return None

    def generate_master_gradebook(self) -> List[Dict[str, Any]]:
        """
        Generates a master gradebook as a single flat list of dictionaries,
        where each dictionary represents one single grade entry from any student.
        """
        master_gradebook = []

        # 1. Iterate over every student enrolled in the course
        for student in self.students:
            
            # 2. Get the student's individual, flat list of detailed grades
            student_grades = student.get_grades_for_master_book() 

            # 3. Iterate over each individual grade entry (row)
            for grade_entry in student_grades:
                # 4. Create a new dictionary entry for the master book
                master_row = grade_entry.copy()
                
                # Crucial step: Add the student's identifier to the row
                master_row['Student Name'] = student.full_name_simple()
                master_row['Student ID'] = student.sid
                
                # 5. Append the complete row to the master list
                master_gradebook.append(master_row)

        print(f"Master Gradebook for '{self.course_name}' generated with {len(master_gradebook)} total entries.")
        return master_gradebook

    def export_master_gradebook_json(self, filepath: str):
        """
        Generates the master gradebook and exports it to a JSON file at the specified filepath.
        The data is saved with an indent of 4 for readability.
        """
        try:
            gradebook_data = self.generate_master_gradebook()
            
            with open(filepath, 'w') as f:
                json.dump(gradebook_data, f, indent=4)
                
            print(f"Success: Master gradebook exported to '{filepath}'.")
        except Exception as e:
            print(f"Error exporting gradebook to JSON: {e}")
            
    def generate_final_grade_report(self) -> List[Dict[str, str]]:
        """
        Generates a summary report of the final calculated grades (percentage and letter grade)
        for all students in the course, using the data stored in the student's report_card.
        """
        final_report = []
        
        print(f"\n--- Generating Final Grade Report for {self.course_name} ({len(self.students)} Students) ---")
        
        for student in self.students:
            # Assumes the student's report_card holds the final grade result under the course name
            final_grade_data = student.report_card.get(self.course_name)
            
            report_entry = {
                'Student Name': student.full_name_simple(),
                'Student ID': student.sid,
                'Course': self.course_name,
            }
            
            if final_grade_data and isinstance(final_grade_data, dict):
                # We expect final_grade_data to be a dictionary like {'percentage': 92.5, 'letter_grade': 'A-'}
                report_entry['Final Grade Percentage'] = f"{final_grade_data.get('percentage', 'N/A'):.2f}%"
                report_entry['Final Letter Grade'] = final_grade_data.get('letter_grade', 'N/A')
            else:
                report_entry['Final Grade Percentage'] = 'Pending'
                report_entry['Final Letter Grade'] = 'Pending'

            final_report.append(report_entry)

        return final_report
