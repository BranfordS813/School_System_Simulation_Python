import json
import os
from typing import List, Dict, Union, Tuple

class GradeBook:
    """
    Manages assignment scores and weights for a single student in a single course,
    with methods for persistent storage to a JSON file and grade calculation.
    """
    def __init__(self, course_name: str, student_id: str, student_name: str):
        """Initializes the GradeBook, immediately attempting to load existing data."""
        self.course_name = course_name
        self.student_id = student_id
        self.student_name = student_name
        # Internal storage for assignments
        # FIX: Explicitly updated the docstring and type hint to include 'type' (the assignment type).
        # Each entry: {'title': str, 'type': str, 'score': float, 'weight': float}
        self.assignment_entries: List[Dict[str, Union[str, float]]] = []
        # Try to load existing grades if the file exists
        self.load_grades()

    def get_filename(self) -> str:
        """Generates the standardized filename for the JSON persistence."""
        # Example: Quantum_Theory_Koriandr_Starr_S456.json
        safe_course = self.course_name.replace(" ", "_")
        safe_name = self.student_name.replace(" ", "_").replace(".", "")
        return f"{safe_course}_{safe_name}_{self.student_id}.json"

    def save_grades(self):
        """Saves the current assignment_entries to the persistent JSON file."""
        filename = self.get_filename()
        try:
            with open(filename, 'w') as f:
                json.dump(self.assignment_entries, f, indent=4)
            print(f"[GB] Successfully saved assignments to {filename}.")
        except Exception as e:
            print(f"[GB ERROR] Failed to save grades to {filename}: {e}")

    def load_grades(self):
        """Loads existing assignments from the persistent JSON file into memory."""
        filename = self.get_filename()
        if os.path.exists(filename):
            try:
                with open(filename, 'r') as f:
                    self.assignment_entries = json.load(f)
            # We assume JSON loading is fine, but the old data might be missing 'type'.
            # When new data with 'type' is saved, this is implicitly fixed.
                print(f"[GB] Successfully loaded existing grades from {filename}.")
            except json.JSONDecodeError:
                print(f"[GB WARNING] JSON file {filename} is corrupt or empty. Starting fresh.")
                self.assignment_entries = []
            except Exception as e:
                print(f"[GB ERROR] Failed to load grades from {filename}: {e}")
        else:
            print(f"[GB] No existing grade file found for {self.student_name}. Starting new entry.")

    def add_grades_to_json(self, new_assignments: List[Dict[str, Union[str, float]]]):
        """
        Updates existing assignments (by title) or adds new ones to the GradeBook, 
        then saves the result to the JSON file.
        
        Args:
            new_assignments: A list of dicts, e.g., 
                [{'title': 'Midterm', 'type': 'Exam', 'score': 92.0, 'weight': 0.3}]
        """
        # Ensure we have the latest data from the file before updating
        self.load_grades() 
        
        for new_a in new_assignments:
            found = False
            for i, existing_a in enumerate(self.assignment_entries):
                # Check if an assignment with the same title already exists (case-insensitive)
                if existing_a['title'].lower() == new_a['title'].lower():
                    # Update existing entry with new score, type, and weight
                    if all(key in new_a for key in ['score', 'weight', 'type']):
                        self.assignment_entries[i]['score'] = new_a['score']
                        self.assignment_entries[i]['weight'] = new_a['weight']
                        self.assignment_entries[i]['type'] = new_a['type'] # Included 'type' update
                        print(f"Updated: {new_a['title']} (Type: {new_a['type']}, Score: {new_a['score']}, Weight: {new_a['weight']})")
                        found = True
                        break
            
            if not found:
                # If the title is new, append it
                # Ensure all required keys are present before appending
                if all(key in new_a for key in ['title', 'score', 'weight', 'type']):
                    self.assignment_entries.append(new_a)
                    print(f"Added New Assignment: {new_a['title']} (Type: {new_a['type']}, Score: {new_a['score']}, Weight: {new_a['weight']})")
                else:
                    # FIX: Warn about missing 'type' if it's not present, alongside score/weight.
                    print(f"[GB WARNING] Skipping assignment due to missing fields (must have title, type, score, weight): {new_a}")
        
        # Save the combined and updated list back to the file
        self.save_grades()

    # --- NEW FEATURE 1: Grade Calculation ---
    def calculate_weighted_score(self) -> Tuple[float, float, float]:
        """
        Calculates the student's current weighted score and total weight accounted for.
        Assumes scores are out of 100.
        
        Returns:
            Tuple[float, float, float]: (Current Weighted Score, Total Weight Applied, Score % of Completed Work)
        """
        total_weighted_sum = 0.0
        total_weight_applied = 0.0
        
        for entry in self.assignment_entries:
            try:
                score = float(entry.get('score', 0.0))
                weight = float(entry.get('weight', 0.0))
                
                # Calculate contribution: (score / 100) * weight
                weighted_contribution = (score / 100.0) * weight
                total_weighted_sum += weighted_contribution
                total_weight_applied += weight
                
            except (TypeError, ValueError) as e:
                print(f"[GB CALC ERROR] Skipping entry '{entry.get('title', 'Unknown')}' due to invalid data: {e}")
        
        # Calculate the score percentage based on completed weight (if weight is > 0)
        score_percent_completed = 0.0
        if total_weight_applied > 0:
            # Score is the weighted sum divided by the total weight applied, normalized back to 100%
            score_percent_completed = (total_weighted_sum / total_weight_applied) * 100.0
        
        # The Current Weighted Score represents the final grade if no more assignments are given (out of 1.0)
        # We present this as a percentage: total_weighted_sum * 100
        current_final_grade_percentage = total_weighted_sum * 100.0

        return current_final_grade_percentage, total_weight_applied, score_percent_completed

    # --- NEW FEATURE 2: Assignment Removal ---
    def remove_assignment(self, title_to_remove: str) -> bool:
        """
        Removes an assignment by its title (case-insensitive) and saves the change.
        
        Args:
            title_to_remove: The title of the assignment to remove.
            
        Returns:
            True if the assignment was found and removed, False otherwise.
        """
        original_length = len(self.assignment_entries)
        
        # Create a new list without the matching assignment(s)
        self.assignment_entries = [
            a for a in self.assignment_entries 
            if a.get('title', '').lower() != title_to_remove.lower()
        ]
        
        new_length = len(self.assignment_entries)
        
        if new_length < original_length:
            print(f"[GB SUCCESS] Removed assignment(s) with title '{title_to_remove}'.")
            self.save_grades()
            return True
        else:
            print(f"[GB WARNING] Assignment '{title_to_remove}' not found.")
            return False

    # --- NEW FEATURE 3: Display Reporting ---
    def display_grades(self):
        """
        Prints a formatted report of all assignments and the calculated grade.
        """
        print("\n" + "="*80)
        print(f"GRADE REPORT: {self.course_name} for {self.student_name} (ID: {self.student_id})")
        print("="*80)

        if not self.assignment_entries:
            print("No assignments recorded yet.")
            print("="*80)
            return

        # FIX: Added 'TYPE' column to the display
        print(f"{'TITLE':<30}{'TYPE':<10}{'SCORE':<10}{'WEIGHT':<10}{'CONTRIBUTION':<20}")
        print("-" * 80)
        
        for entry in self.assignment_entries:
            title = str(entry.get('title', 'N/A'))
            # FIX: Safely retrieve 'type' and default if not present (for old data)
            type_val = str(entry.get('type', 'N/A')) 
            score = float(entry.get('score', 0.0))
            weight = float(entry.get('weight', 0.0))
            
            # Contribution is (Score / 100) * Weight, expressed as a raw grade component
            contribution = (score / 100.0) * weight
            
            # FIX: Included 'type' in the print formatting
            print(f"{title:<30}{type_val:<10}{score:>7.2f}% {weight:>7.2f} {contribution*100:>15.2f} points")
            
        print("-" * 80)
        
        current_final_grade, total_weight, score_percent_completed = self.calculate_weighted_score()

        print(f"Total Weight Applied: {total_weight:.2f} ({(total_weight * 100):.0f}%)")
        print(f"Grade Based on Completed Work: {score_percent_completed:.2f}%")
        print(f"Current Course Grade (out of 100% total): {current_final_grade:.2f}%")
        print("="*80)

    # --- Original Interactive Method (Minor Update to use display_grades) ---
    def start_interactive_entry(self):
        """
        Interactive method to prompt the user for assignment details.
        It respects existing loaded grades and allows the user to clear them or append.
        """
        print("\n--- Starting Interactive Assignment Entry ---")
        
        # If loading grades was successful, ask the user if they want to clear them first
        if self.assignment_entries:
            self.display_grades() # Show current state
            print(f"Currently, {len(self.assignment_entries)} assignments are loaded from the file.")
            response = input("Do you want to clear these existing entries and start fresh? (yes/no): ").lower()
            if response == 'yes':
                self.assignment_entries = []
                print("Existing entries cleared from memory.")
            else:
                # If they say no, load the grades again to ensure we have the disk version
                self.load_grades()
                print("Continuing with existing entries. New entries will be appended or will require manual update via add_grades_to_json().")

        newly_entered_assignments = []
        while True:
            title = input("Enter Assignment Title (or 'done' to finish): ")
            if title.lower() == 'done':
                break
            
            # NOTE: The Assignment Type prompt is missing here, but it is likely handled in teacher.py.
            # FIX: Adding the missing prompt for interactive input here just in case this method is used directly.
            assignment_type = input(f"Enter Assignment Type for {title} (e.g., Homework, Quiz, Exam, Project): ")

            try:
                score = float(input(f"Enter score for {title} (e.g., 90.5): "))
                # Convert weight to float, allowing for percentage input (e.g., 30 -> 0.3)
                weight_input = input(f"Enter weight for {title} (as decimal e.g., 0.3, or percentage e.g., 30): ")
                
                weight = float(weight_input)
                if weight > 1.0: # Assume if > 1, it was entered as a percentage (e.g., 30)
                    weight /= 100.0

                newly_entered_assignments.append({
                    'title': title,
                    'type': assignment_type, # FIX: Added assignment type to the dictionary
                    'score': score,
                    'weight': weight
                })
                print(f"Queued: {title} (Type: {assignment_type}, Score: {score}, Weight: {weight})")
            except ValueError:
                print("Invalid input for score or weight. Please try again.")

        # Use the existing add_grades_to_json to handle updates/appends and save
        if newly_entered_assignments:
            self.add_grades_to_json(newly_entered_assignments)

        print("--- Interactive Entry Finished ---")
        self.display_grades()


    def delete_json_file(self):
        """Deletes the persistent JSON file for this GradeBook instance."""
        filename = self.get_filename()
        try:
            os.remove(filename)
            self.assignment_entries = [] # Clear memory after deleting file
            print(f"[GB SUCCESS] Successfully deleted the GradeBook file: {filename}")
        except FileNotFoundError:
            print(f"[GB WARNING] GradeBook file not found: {filename}")
        except Exception as e:
            print(f"[GB ERROR] An error occurred during file deletion: {e}")
