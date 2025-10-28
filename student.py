from core_identity import CoreIdentity
from level_tup import Level

class Student(CoreIdentity):
    """
    A child class focusing on students within an Alien school system.
    It imports attributes and methods from its parent CoreIdentity Class 
    but contains its own methods, including viewing grades, checking enrollment, 
    and viewing extra information like extracurriculars and SSL hours.
    """
    
    # --- Helper Function for Grading (Pure Python) ---
    def _calculate_letter_grade(self, percentage):
        """Converts a final percentage score to a letter grade based on a standard scale."""
        if percentage >= 90:
            return 'A'
        elif percentage >= 80:
            return 'B'
        elif percentage >= 70:
            return 'C'
        elif percentage >= 60:
            return 'D'
        else:
            return 'F'

    def __init__(self, 
                 # New Student Attributes (Mandatory)
                 grade_index, school, entry_year,
                 sid, rfid, log_un, 
                 log_pas, enroll_status, 
                 # Core_Identity Parent Attributes (Mandotry)
                 unique_system_id, 
                 dob, first_name, last_name, 
                 gender, species, home_planet,
                 # Enrolled Courses (New, Optional/Default)
                 enrolled_courses=None, 
                 # Parent Attributes (Optional/Default) 
                 middle_name="", preferred_name=""
                 ):

        # Initialize parent class attributes
        super().__init__(unique_system_id, 
                         dob, first_name, last_name, 
                         gender, species, home_planet,
                         middle_name, preferred_name)
                         
        # Initialize New Student Attributes
        self.school = school
        self.entry_year = entry_year
        self.sid = sid
        self.rfid = rfid
        self.log_un = log_un
        self.log_pas = log_pas
        self.enroll_status = enroll_status
        
        # --- Critical Grade/Enrollment Attributes ---
        # The list of courses the student is currently taking (e.g., ['XenoMath', 'Quantum Theory'])
        self.enrolled_courses = enrolled_courses if enrolled_courses is not None else []
        # Initializing for single letter grades (The Report Card view)
        self.report_card = {}
        # Initializing for detailed assignment grades (The Portal View/Master Book Data)
        self._detailed_grades = {}
        
        # --- Extracurricular Attributes ---
        self.extra = []
        self.ssl = 500 # Set a new attribute for SSL hours
        self.gpa = 5.0 # Set a new attribute for GPA (lets say the system has 0 - 5.0)
        self.c_gpa = 5.0 # Set a new attrigbute for cumualtive GPA 
        self.library = [] # Set library material check out (as list)

        # Initialize grade level index (for set_grade function)
        self.set_grade(grade_index)
    

    def set_grade(self, index):
        """
        Sets the student's grade level (Form/Program) by looking up the provided 
        integer index in the external 'Level' tuple. This is run during initialization.
        """
        try:
            # Look up the level name using the index
            self.grade_level = Level[index]
            print(f"Level set to: {self.grade_level}")
        except IndexError:
            self.grade_level = "Invalid Level Index"
            print(f"Error: Index {index} is out of range for the defined school levels.")

    def state_school(self): 
        """a simple definition that states the school that the student is from"""
        school_message = f"{self.full_name_simple()} currently attends {self.school} \
            \nYear of Entry: {self.entry_year}"
        return school_message
    
    def state_sid_rfid(self):
        """a simple definition that states the student's RFID and Student ID (sid) number"""
        id_message = f"{self.full_name_simple()}'s School related Identification numbers: \
            \nRFID number - Needed for school events, security/hallpass, library checkouts: \
            \n{self.rfid} \
            \nStudent Id (sID) number: Needed for registrar, grades and testing, Administration and Financial Aid: \
            \n{self.sid}"
        return id_message
    
    def state_sid_simp(self):
        """a much more simplified definition that retursn the sid of a student"""
        sid_simp = self.sid 
        return sid_simp
    
    def state_form(self):
        """
        A simple definition that states the student's grade (called form/level in the school system).
        This method reports the grade level that was set during initialization.
        """
        form_message = f"{self.full_name_simple()}'s current grade level: {self.grade_level}"
        return form_message
    
    def academic_summary(self, current_year):
        """Prints a detailed summary of the student's academic standing and identification."""
        print(50 * "-")
        print(f"Student Summary for {self.full_name_simple()} (Level: {self.grade_level})\
            \nAcademic Year: {current_year}")
        print(f"Enrollment: {self.enroll_status} | SID: {self.sid}")
        print(f"Current GPA: {self.gpa:.2f} | Cumulative GPA: {self.c_gpa:.2f}")
        print(f"SSL Hours Completed: {self.ssl}")
        print(50 * "-")

    # --- Course Enrollment Management (NEW SECTION) ---
    def register_course(self, course_name):
        """Adds a course to the student's enrolled list if not already registered."""
        if course_name not in self.enrolled_courses:
            self.enrolled_courses.append(course_name)
            self._detailed_grades[course_name] = [] # Initialize grade structure
            print(f"[Enrollment] {self.full_name_simple()} successfully enrolled in {course_name}.")
        else:
            print(f"[Enrollment Warning] {self.full_name_simple()} is already enrolled in {course_name}.")

    def drop_course(self, course_name):
        """Removes a course from the student's enrolled list."""
        if course_name in self.enrolled_courses:
            self.enrolled_courses.remove(course_name)
            # Optionally remove related grade data
            if course_name in self._detailed_grades:
                del self._detailed_grades[course_name]
            if course_name in self.report_card:
                del self.report_card[course_name]
            print(f"[Enrollment] {self.full_name_simple()} successfully dropped {course_name}.")
        else:
            print(f"[Enrollment Warning] {self.full_name_simple()} is not enrolled in {course_name}.")


    # --- Extracurricular and Service Management (NEW SECTION) ---
    def add_extracurricular(self, activity_name):
        """Adds an activity to the student's extracurricular list."""
        if activity_name not in self.extra:
            self.extra.append(activity_name)
            print(f"[Activity Log] Added '{activity_name}' to {self.first_name}'s activities.")
        else:
            print(f"[Activity Log] {activity_name} is already listed.")

    def log_ssl_hours(self, hours):
        """Adds Service-Learning (SSL) hours to the student's total."""
        try:
            hours = float(hours)
            if hours > 0:
                self.ssl += hours
                print(f"[SSL Log] Added {hours:.1f} SSL hours. New total: {self.ssl:.1f} hours.")
            else:
                print("[SSL Log Error] Hours must be a positive number.")
        except ValueError:
            print("[SSL Log Error] Invalid input. Please enter a number for hours.")

    def view_extracurriculars(self):
        """Displays the student's list of extracurricular activities and SSL hours."""
        print(50 * "~")
        print(f"Extracurricular and Service Summary for {self.full_name_simple()}:")
        print(f"SSL Hours Completed: {self.ssl:.1f}")
        if self.extra:
            print("Activities:")
            for activity in self.extra:
                print(f"- {activity}")
        else:
            print("No extracurricular activities logged.")
        print(50 * "~")


    # --- Grade Management Methods (The Portal View Data Setter) ---
    def add_assignment_grade(self, course_name, assignment_name, score, weight):
        """
        Adds a single assignment grade and its weight to the student's detailed record.
        This data is used for grade calculation and the Master Gradebook.
        """
        if course_name not in self._detailed_grades:
            print(f"[Grade Error] Cannot add assignment. Student is not enrolled in {course_name}. Use register_course() first.")
            return

        # Ensure that score is between 0 and 100 and weight is between 0.0 and 1.0
        score = max(0, min(100, score))
        weight = max(0.0, min(1.0, weight))
        
        # Check if the assignment already exists and update it, otherwise append new
        found = False
        for assignment in self._detailed_grades[course_name]:
            if assignment['assignment'] == assignment_name:
                assignment['score'] = score
                assignment['weight'] = weight
                found = True
                print(f"[Student Grade Update] {assignment_name} updated for {course_name}.")
                break
        
        if not found:
            self._detailed_grades[course_name].append({
                'assignment': assignment_name,
                'score': score,
                'weight': weight,
            })
            print(f"[Student Grade Record] Added {assignment_name} for {course_name}.")


    def calculate_final_course_grade(self, course_name):
        """
        Calculates the weighted final grade percentage and letter grade for a specific course.
        Updates the student's self.report_card attribute.
        """
        if course_name not in self._detailed_grades or not self._detailed_grades[course_name]:
            self.report_card[course_name] = "N/A"
            return 0.0

        total_score = 0
        total_weight = 0

        for assignment in self._detailed_grades[course_name]:
            # Calculate weighted score: (Score * Weight)
            weighted_score = assignment['score'] * assignment['weight']
            total_score += weighted_score
            total_weight += assignment['weight']

        if total_weight == 0:
            final_percentage = 0.0
        else:
            # Final grade is Total Weighted Score / Total Weight
            final_percentage = (total_score / total_weight)
        
        # Convert to letter grade and update the report card attribute
        final_letter = self._calculate_letter_grade(final_percentage)
        self.report_card[course_name] = final_letter

        return final_percentage
    
    def update_gpa(self):
        """
        Calculates the overall GPA for all courses currently in the report card.
        (Simplified 5.0 scale conversion: A=5.0, B=4.0, C=3.0, D=2.0, F=0.0)
        """
        gpa_map = {'A': 5.0, 'B': 4.0, 'C': 3.0, 'D': 2.0, 'F': 0.0, 'N/A': 0.0}
        total_gpa_points = 0
        graded_courses_count = 0
        
        # Ensure all grades are calculated before running GPA
        for course in self.enrolled_courses:
            # Running this ensures the report_card is up-to-date
            self.calculate_final_course_grade(course) 

        for grade in self.report_card.values():
            if grade in gpa_map:
                total_gpa_points += gpa_map[grade]
                if grade != 'N/A':
                    graded_courses_count += 1
        
        if graded_courses_count > 0:
            # Update current GPA (assuming this only covers the current grading period)
            self.gpa = total_gpa_points / graded_courses_count
            print(f"[Academic Update] Current GPA calculated and set to: {self.gpa:.2f}")
        else:
            self.gpa = 5.0 # Default/Placeholder if no grades are recorded
            print("[Academic Update] No graded courses to calculate current GPA.")


    # --- Data Retrieval Methods (The Instructor & Student Views) ---
    def get_grades_for_master_book(self):
        """
        Flattens ALL assignment data across ALL courses into a single list of dictionaries.
        This is the method the CourseManager uses to build the Master Gradebook.
        """
        master_list = []
        for course_name, assignments in self._detailed_grades.items():
            for assignment in assignments:
                # Copy the assignment data and add the course name
                entry = assignment.copy()
                entry['course'] = course_name
                master_list.append(entry)
        return master_list


    def view_report_card(self):
        """
        Displays the student's final letter grade for all courses (The Report Card view).
        """
        print(50 * "=")
        print(f"OFFICIAL REPORT CARD: {self.full_name_simple()} ({self.grade_level})")
        # Run GPA calculation before displaying the summary
        self.update_gpa() 
        print(f"Current GPA: {self.gpa:.2f}")
        print(50 * "=")
        if not self.report_card:
            print("No final grades available yet.")
            return

        for course, grade in self.report_card.items():
            print(f"- {course.ljust(25)} : {grade}")
        
        print(50 * "=")


    def view_course_grades(self, course_name):
        """
        Displays the detailed assignment results for a single course (The Portal view).
        """
        print(50 * "-")
        print(f"Detailed Grades for: {course_name} (SID: {self.sid})")
        print(50 * "-")

        if course_name not in self._detailed_grades or not self._detailed_grades[course_name]:
            print(f"No detailed assignments found for {course_name}.")
            return

        for assignment in self._detailed_grades[course_name]:
            score = assignment['score']
            weight = assignment['weight']
            assignment_name = assignment['assignment']
            print(f"  {assignment_name.ljust(30)} | Score: {score}/100 | Weight: {weight*100}%")

        # Calculate and display the current running grade
        final_percentage = self.calculate_final_course_grade(course_name)
        final_letter = self.report_card.get(course_name, "N/A")
        
        print(50 * "-")
        print(f"Current Final Grade: {final_percentage:.2f}% ({final_letter})")
        print(50 * "-")


    # Updated library item checkout function based on previous idea (expanded by Gemini)
    def lib_checkout(self):
        """
        A simple function for when a student wants to check out materials from the library.
        Prompts for a comma-separated list, stores items in the object's list, 
        and appends them to a student-specific .txt file for the librarian.
        """
        print(50 * "-")
        print("Library and Media Loan Checkout:")
        
        # 1. Get input as a string
        request_string = input("\nPlease enter list of items to checkout (comma-separated): ")
        
        # 2. Split the string into a clean list of items
        request_items = [item.strip() for item in request_string.split(',') if item.strip()]
        
        if not request_items:
            print("No items entered. Checkout cancelled.")
            return

        # 3. Update the student's in-memory list (the library attribute)
        self.library.extend(request_items)

        # 4. Use the open() and write() methods to create/append to a .txt file
        # Note: In a real-world web/cloud environment, this would be a database call.
        file_path = f"{self.sid}_library_checkouts.txt"
        try:
            with open(file_path, "a") as lib:
                for item in request_items:
                    # Write each item on a new line for easy reading
                    lib.write(f"{item}\n")

            print(50 * "-")
            print(f"Summary of checked out items (also recorded in {file_path}): ")
            for item in request_items:
                    print(f"- {item}")
        except Exception as e:
            # Added more generic error handling for file issues
            print(f"An error occurred during file writing: {e}")
            
        print(50 * "-")
