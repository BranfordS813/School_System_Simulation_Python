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
        # Each entry: {'title': str, 'score': float, 'weight': float}
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
            new_assignments: A list of dicts, e.g., [{'title': 'Midterm', 'score': 92.0, 'weight': 0.3}]
        """
        # Ensure we have the latest data from the file before updating
        self.load_grades() 
        
        for new_a in new_assignments:
            found = False
            for i, existing_a in enumerate(self.assignment_entries):
                # Check if an assignment with the same title already exists (case-insensitive)
                if existing_a['title'].lower() == new_a['title'].lower():
                    # Update existing entry with new score and weight
                    # Validate that score and weight keys exist before update
                    if 'score' in new_a and 'weight' in new_a:
                         self.assignment_entries[i]['score'] = new_a['score']
                         self.assignment_entries[i]['weight'] = new_a['weight']
                         print(f"Updated: {new_a['title']} (Score: {new_a['score']}, Weight: {new_a['weight']})")
                         found = True
                         break
            
            if not found:
                # If the title is new, append it
                # Ensure all required keys are present before appending
                if 'title' in new_a and 'score' in new_a and 'weight' in new_a:
                    self.assignment_entries.append(new_a)
                    print(f"Added New Assignment: {new_a['title']} (Score: {new_a['score']}, Weight: {new_a['weight']})")
                else:
                    print(f"[GB WARNING] Skipping assignment due to missing fields: {new_a}")
        
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
        print("\n" + "="*70)
        print(f"GRADE REPORT: {self.course_name} for {self.student_name} (ID: {self.student_id})")
        print("="*70)

        if not self.assignment_entries:
            print("No assignments recorded yet.")
            print("="*70)
            return

        print(f"{'TITLE':<30}{'SCORE':<10}{'WEIGHT':<10}{'CONTRIBUTION':<20}")
        print("-" * 70)
        
        for entry in self.assignment_entries:
            title = str(entry.get('title', 'N/A'))
            score = float(entry.get('score', 0.0))
            weight = float(entry.get('weight', 0.0))
            
            # Contribution is (Score / 100) * Weight, expressed as a raw grade component
            contribution = (score / 100.0) * weight
            
            print(f"{title:<30}{score:>7.2f}% {weight:>7.2f} {contribution*100:>15.2f} points")
            
        print("-" * 70)
        
        current_final_grade, total_weight, score_percent_completed = self.calculate_weighted_score()

        print(f"Total Weight Applied: {total_weight:.2f} ({(total_weight * 100):.0f}%)")
        print(f"Grade Based on Completed Work: {score_percent_completed:.2f}%")
        print(f"Current Course Grade (out of 100% total): {current_final_grade:.2f}%")
        print("="*70)

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
                print("Continuing with existing entries. New entries will be appended or will require manual update via add_grades_to_json().")

        newly_entered_assignments = []
        while True:
            title = input("Enter Assignment Title (or 'done' to finish): ")
            if title.lower() == 'done':
                break

            try:
                score = float(input(f"Enter score for {title} (e.g., 90.5): "))
                # Convert weight to float, allowing for percentage input (e.g., 30 -> 0.3)
                weight_input = input(f"Enter weight for {title} (as decimal e.g., 0.3, or percentage e.g., 30): ")
                
                weight = float(weight_input)
                if weight > 1.0: # Assume if > 1, it was entered as a percentage (e.g., 30)
                    weight /= 100.0

                newly_entered_assignments.append({
                    'title': title,
                    'score': score,
                    'weight': weight
                })
                print(f"Queued: {title} (Score: {score}, Weight: {weight})")
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

# if __name__ == '__main__':
#     # --- Example Usage ---
    
#     # 1. Initialize GradeBook for a student
#     gb = GradeBook("Data Structures 101", "A9001", "Leia Organa")
    
#     # 2. Add some grades programmatically
#     new_grades = [
#         {'title': 'Homework 1', 'score': 95.0, 'weight': 0.10},
#         {'title': 'Midterm Exam', 'score': 82.5, 'weight': 0.30},
#     ]
#     gb.add_grades_to_json(new_grades)

#     # 3. Display the current report
#     gb.display_grades()
    
#     # 4. Update an existing grade (Homework 1 - maybe it was regraded)
#     print("\n--- UPDATING A GRADE (Homework 1) ---")
#     gb.add_grades_to_json([{'title': 'Homework 1', 'score': 98.0, 'weight': 0.10}])
#     gb.display_grades()
    
#     # 5. Add a new assignment
#     print("\n--- ADDING NEW ASSIGNMENT (Final Project) ---")
#     gb.add_grades_to_json([{'title': 'Final Project', 'score': 90.0, 'weight': 0.50}])
#     gb.display_grades()

#     # 6. Calculate the final score only (useful for automation)
#     score, weight_used, score_completed = gb.calculate_weighted_score()
#     print(f"\n[PROGRAMMATIC CALC] Weighted Sum: {score:.2f}% | Total Weight Used: {weight_used:.2f}")

#     # 7. Remove an assignment
#     print("\n--- REMOVING ASSIGNMENT (Midterm Exam) ---")
#     gb.remove_assignment("Midterm Exam")
#     gb.display_grades()
    
#     # 8. Clean up (Optional: delete the created JSON file)
#     # gb.delete_json_file()
