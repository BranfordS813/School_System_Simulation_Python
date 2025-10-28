from core_identity import CoreIdentity # Parent class
from student import Student # We need the Student class type for the roster
from gradebook import GradeBook
from student_roster import StudentRoster

class Teacher(CoreIdentity):
    """
    A child class representing faculty members within the Alien school system.
    It inherits core identity attributes and adds faculty-specific attributes 
    and methods (like managing grades and generating reports).
    """

    def __init__(self, 
                 # New Teacher Attributes
                 staff_id, department, courses_taught, 
                 
                 # Parent Attributes (Mandatory)
                 unique_system_id, dob, first_name, last_name, 
                 gender, species, home_planet,
                 
                 # Parent Attributes (Optional/Default)
                 middle_name="", preferred_name=""):
        
        # 1. Initialize Parent Class Attributes
        super().__init__(unique_system_id, 
                         dob, first_name, last_name, 
                         gender, species, home_planet,
                         middle_name, preferred_name)
        
        # 2. Initialize New Teacher Attributes
        self.staff_id = staff_id # Staff ID
        self.department = department # Academic department
        self.courses_taught = courses_taught # List of courses taught

        # List to hold Student objects taught by this teacher.
        self.student_roster = [] 
        # Removed redundant assignment of GradeBook and StudentRoster classes
        # as they are imported at the module level.

    def instructor_name_simp(self):
        """a simple definition that returns the first and last name of the instructor"""
        simple_name_message = f"{self.first_name} {self.last_name}"
        return simple_name_message

    def course_statement(self):
        """A simple definition that lists the courses taught by the teacher"""
        taught_courses = self.courses_taught
        # Print statment
        print(100 * "=")
        print(f"Courses taught by instructor {self.first_name} {self.last_name}:")
        print(100 * "=")

        for course in taught_courses:
            print(f"{course}")

    def course_simp(self): 
        """An even more simple definition that gives back the list of the courses taught
            by the teacher
        """
        taught_courses_simp = self.courses_taught
        return taught_courses_simp

    def add_student_to_roster(self, student_object):
        """Adds a student object to the teacher's roster (in-memory)."""
        if isinstance(student_object, Student):
            self.student_roster.append(student_object)
            print(f"Roster Update: {student_object.full_name_simple()} added to {self.full_name_simple()}'s roster.")
        else:
            print(f"Error: Can only add Student objects to the roster.")

    def faculty_summary(self):
        """Prints a summary of the teacher's faculty status."""
        print(50 * "=")
        print(f"🧑‍🏫 Faculty Profile: {self.full_name_simple()} ({self.preferred_name or 'N/A'})")
        print(50 * "=")
        print(f"Staff ID: {self.staff_id}")
        print(f"Department: {self.department}")
        print(f"Courses Taught: {', '.join(self.courses_taught)}")
        print(f"Total Students on Roster: {len(self.student_roster)}")

    
    # --- Roster Management Method (No change needed here) --- #

    def manage_class_roster(self, course_name: str, year: int, semester: str):
        """
        Initializes and manages the StudentRoster object for a specific course/term.
        """
        
        # Automatically pull teacher context
        instructor_name = self.instructor_name_simp()
        instructor_id = self.staff_id
        
        # 1. Instantiate the Roster, which auto-loads existing data from file
        course_roster = StudentRoster(
            course_name=course_name,
            instructor_name=instructor_name,
            instructor_id=instructor_id,
            year=year,
            semester=semester
        )
        
        # 2. Start the interactive entry process (which handles saving the file)
        course_roster.start_interactive_entry()
        
        return course_roster

        
    # --- GRADE MANAGEMENT METHODS (UPDATED) --- #

    # **REMOVED setup_student_course** - The Student object now manages its own grade data.
    
    def enter_assignment_grade(self, student_obj: Student, course_name: str, assignment_name: str, score: float, weight: float):
        """
        Teacher method to record a grade and its weight for a specific student 
        and course, using the method created in the student.py file.
        """
        if course_name not in student_obj.enrolled_courses:
             print(f"Warning: {student_obj.full_name_simple()} is not officially enrolled in {course_name}.")

        print(f"\n--- Entering Grade for {student_obj.full_name_simple()} in {course_name} ---")
        
        # This calls the new method in student.py
        student_obj.add_assignment_grade(
            course_name=course_name, 
            assignment_name=assignment_name, 
            score=score, 
            weight=weight
        )
        # Note: You would likely integrate this with your persistent GradeBook later.

    
    def calculate_and_report_grade(self, student_obj: Student, course_name: str):
        """
        Teacher triggers the final weighted grade calculation for the student in one course,
        which updates the student's internal 'report_card' attribute.
        """
        print(f"\n--- Calculating Final Grade for {student_obj.full_name_simple()} in {course_name} ---")
        final_percentage = student_obj.calculate_final_course_grade(course_name)
        
        # Optional: Print the result of the update
        letter_grade = student_obj.report_card.get(course_name, "N/A")
        print(f"Final Grade Calculated: {final_percentage:.2f}% ({letter_grade}).")
        print("Student's internal report card has been updated.")
        
        return letter_grade

    def bulk_add_grades_from_gradebook(self, student_obj: Student, course_name: str, gradebook: GradeBook):
        """
        Utility to loop through a single GradeBook instance and push all recorded
        assignments into the student's detailed grade list.
        """
        print(f"\n--- Bulk Adding Assignments from {gradebook.get_filename()} to {student_obj.full_name_simple()} ---")
        
        # FIX 1: The correct attribute name is assignment_entries
        if not gradebook.assignment_entries: 
            print("GradeBook is empty. No assignments transferred.")
            return

        # FIX 2: The correct attribute name is assignment_entries
        for assignment in gradebook.assignment_entries:
            # We assume the GradeBook structure now includes 'weight'
            try:
                self.enter_assignment_grade(
                    student_obj=student_obj,
                    course_name=course_name,
                    # FIX 3: GradeBook uses 'title' not 'name' for the assignment name
                    assignment_name=assignment['title'], 
                    score=assignment['score'], 
                    weight=assignment['weight']
                )
            except KeyError as e:
                # Catching if required keys ('score', 'title', 'weight') are missing
                print(f"Error: Assignment missing required field: {e}. Skipping entry: {assignment}")
