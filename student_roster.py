# student_roster.py
import json
import os
from typing import List, Dict, Any, Union

class StudentRoster:
    """
    A module that specializes in creating a persistent roster of students for a given class.
    It handles loading and saving student identifiers to a unique JSON file defined by 
    the instructor, course, and academic term.
    """

    def __init__(self, course_name: str, instructor_name: str, instructor_id: str, year: int, semester: str):
        
        self.course_name = course_name
        self.instructor_name = instructor_name
        self.instructor_id = instructor_id
        self.year = year
        self.semester = semester
        # The roster will store a list of student dictionary identifiers (not Student objects)
        # Each dict: {'name': str, 'id': str, 'course': str}
        self.student_roster: List[Dict[str, str]] = [] 
        
        # Load existing data upon creation
        self.load_roster()

    def get_filename(self) -> str:
        """Generate file name structure for the student roster to save as a .json file."""
        name_structure = self.instructor_name.replace(" ", "_")
        # Dynamically generate file name using course and instructor data
        safe_course = self.course_name.replace(" ", "_")
        return f"{safe_course}_{name_structure}_{self.instructor_id}_{self.semester}_{self.year}.json"

    def load_roster(self):
        """Loads roster data (list of student dicts) from JSON file into self.student_roster."""

        filename_roster = self.get_filename()
        if os.path.exists(filename_roster): 
            try:
                with open(filename_roster, 'r') as f:
                    # Load the list of student identifier dictionaries
                    self.student_roster = json.load(f)
                    print(f"[Roster] Loaded {len(self.student_roster)} students for {self.course_name};")
                    print(f"         Instructor {self.instructor_name}; Semester: {self.semester}; Year: {self.year}")
            except (json.JSONDecodeError, FileNotFoundError):
                print(f"[Roster] Warning: No valid file found for {filename_roster}. Starting fresh.")
            except Exception as e:
                print(f"[Roster] An error occurred during file loading: {e}")

    def save_roster(self):
        """Saves the current self.student_roster list to the unique JSON file."""
        filename_roster = self.get_filename()
        try:
            with open(filename_roster, 'w') as f:
                # json.dump correctly serializes the list of dictionaries
                json.dump(self.student_roster, f, indent=4)
            print(f"\n[Roster] SUCCESS: Roster saved to {filename_roster}.")
        except Exception as e:
            print(f"[Roster] Error saving file {filename_roster}: {e}")

    # --- NEW FEATURE 1: Display Roster ---
    def display_roster(self):
        """Prints a formatted report of all students in the roster."""
        print("\n" + "="*50)
        print(f"Roster for: {self.course_name}")
        print(f"Instructor: {self.instructor_name} | Term: {self.semester} {self.year}")
        print("="*50)
        
        if not self.student_roster:
            print("The roster is currently empty.")
            print("="*50)
            return

        print(f"{'STUDENT NAME':<30}{'ID':<20}")
        print("-" * 50)
        
        for student in self.student_roster:
            name = student.get('name', 'N/A')
            student_id = student.get('id', 'N/A')
            print(f"{name:<30}{student_id:<20}")

        print("-" * 50)
        print(f"Total Students: {len(self.student_roster)}")
        print("="*50)

    # --- NEW FEATURE 2: Remove Student ---
    def remove_student_from_roster(self, student_id: str) -> bool:
        """
        Removes a student from the roster by their ID and saves the change.

        Args:
            student_id: The unique ID of the student to remove.
            
        Returns:
            True if the student was found and removed, False otherwise.
        """
        original_length = len(self.student_roster)
        
        # Create a new list excluding any students that match the provided ID
        self.student_roster = [
            s for s in self.student_roster 
            if s.get('id') != student_id
        ]
        
        if len(self.student_roster) < original_length:
            print(f"[Roster SUCCESS] Student with ID '{student_id}' removed from roster.")
            self.save_roster()
            return True
        else:
            print(f"[Roster WARNING] Student with ID '{student_id}' not found in roster.")
            return False

    def start_interactive_entry(self):
        """
        Manages the interactive command-line loop for adding new students 
        and updates the persistent file.
        """

        print("\n--- Starting Interactive Student Roster Entry ---")
        self.display_roster()
        
        newly_entered_students = []
        while True: 
            # Prompt for name
            student_name = input("Enter Student's Full Name (or 'done' to finish): ").strip()

            if student_name.lower() == 'done':
                break
            
            # Prompt for ID
            student_id = input(f"Enter ID number for {student_name}: ").strip()
            
            if not student_id:
                print("Student ID cannot be empty. Skipping entry.")
                continue

            # Check if student is already in the roster by ID (in memory)
            if any(s['id'] == student_id for s in self.student_roster):
                print(f"Warning: Student with ID {student_id} is already in the roster. Skipping entry.")
                continue

            # Store only the necessary identifying data as a dictionary
            new_student_data = {
                "name": student_name,
                "id": student_id,
                "course": self.course_name # Useful context for when the file is loaded elsewhere
            }
            
            # Add to the in-memory roster
            self.student_roster.append(new_student_data)
            print(f"Roster Update: {student_name} (ID: {student_id}) added to {self.course_name} roster.")

        # Save the updated roster list after the loop finished
        if self.student_roster:
            self.save_roster()

        self.display_roster()
        print("--- Interactive Entry Finished ---")

# if __name__ == '__main__':
#     # --- Example Usage ---
    
#     # 1. Initialize Roster
#     roster = StudentRoster(
#         course_name="Quantum Theory", 
#         instructor_name="Dr. Zoidberg", 
#         instructor_id="Z101", 
#         year=2345, 
#         semester="Fall"
#     )
    
#     # 2. Add students interactively (uncomment this line to test)
#     # roster.start_interactive_entry()

#     # 3. Add students programmatically (if not using interactive)
#     roster.student_roster.extend([
#         {'name': 'Fry J. Philip', 'id': 'P001', 'course': 'Quantum Theory'},
#         {'name': 'Bender B. Rodriguez', 'id': 'B102', 'course': 'Quantum Theory'},
#         {'name': 'Turanga Leela', 'id': 'T303', 'course': 'Quantum Theory'},
#     ])
#     roster.save_roster()

#     # 4. Display the roster
#     print("\n--- Current Roster ---")
#     roster.display_roster()

#     # 5. Remove a student
#     print("\n--- Removing Student P001 ---")
#     roster.remove_student_from_roster("P001")
    
#     # 6. Display updated roster
#     print("\n--- Updated Roster ---")
#     roster.display_roster()
