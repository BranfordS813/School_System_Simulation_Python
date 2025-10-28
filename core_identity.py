class CoreIdentity():
    """
        A parent class that defines the identifying information of an individual within an 
        Alien school system database.
    """
    # Let's add some default values. don't forget from chapter 8 that default values are 
    # to be added last within the arguments of a definition.
    def __init__(self, 
                 unique_system_id, 
                 dob, first_name, last_name, 
                 gender, species, home_planet,
                 middle_name="", preferred_name=""):
        """Initialize attributes"""
        # Attributes
        self.unique_system_id = unique_system_id
        """dob is entered as a list in day/month/year format, as based on the indivdiual's planet"""
        self.dob = dob
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.species = species
        self.home_planet = home_planet
        self. middle_name = middle_name
        self.preferred_name = preferred_name 

    # Methods

    # Print Person's full name 
    def full_name(self):
        """A simple funciton that returns the full name of an individual"""
        indiv_full_name = "--- Person's Full Name ---"
        if self.middle_name:
            indiv_full_name += f"\n{self.first_name} {self.middle_name} {self.last_name}"
        else:
            indiv_full_name += f"\n{self.first_name} {self.last_name}"

        if self.preferred_name:
            indiv_full_name += f"\nPrefers to be called by {self.preferred_name}"
          
        return indiv_full_name
    
    def full_name_simple(self):
        """a simpler definition for the person's full name that skips the preferred_name logic
        """
        # Initialize variable: 
        indiv_full_name_simp = ""
        
        if self.middle_name:
            indiv_full_name_simp += f"{self.first_name} {self.middle_name} {self.last_name}"
        else:
            indiv_full_name_simp += f"{self.first_name} {self.last_name}"

        return indiv_full_name_simp

    # New method added:
    def get_id_string(self):
        """
        Returns a formatted string containing the individual's simplified full name 
        and their unique system ID for quick identification.
        """
        name = self.full_name_simple()
        return f"{name} (ID: {self.unique_system_id})"
    
    # Print Person's full Registration --> call a method that belongs to an object.
    def full_registration(self):
        """A simple function that returns the full registration of an individual with
            all of the attributes of the CoreIdentity Class
        """
        print(100 * "=")
        print("📃Full Registration Info")
        print(100 * "=")
        # To use the method as an object, use dot notation with self
        self.full_name()

        #print other identifiers
        print(f"Unique ID: {self.unique_system_id}")
        print(f"Date of Birth (DOB): {self.dob}")
        print(f"Species: {self.species}")
        print(f"Home Planet: {self.home_planet}")

    # Helper function - Calculate individual's age (earth years) compared to native years
    
    def age_adjust(self, current_year):
        """
        Calculates an individual's age in their home planet's native years and the equivalent 
        age in Earth years, based on planetary orbital and rotational factors.

        The calculation uses three main steps:
        1. Determine the Planet's Current Year (Planet Year Offset + Current Earth Year).
        2. Determine the Planet Age (Planet Current Year - Birth Year).
        3. Convert to Earth Age (Planet Age * Planetary Rotation Factor).

        If the home planet is not found in the registry, the function returns 
        "-- Unknown --" for the age values.

        :param current_year: The current Earth year (e.g., 2025).
        :return: Tuple (individual_earth_age, individual_hp_age) 
                 If successful: rounded float ages. 
                 If data missing: string values "-- Unknown --".
        """
        # Import exhaustive list of registered planets and age conversion factors: 
        from planet_data_model import Planets_Rot
        from planet_data_model_2 import Planets_Year

        # We assume the last element of the DOB list is the birth year in the planet's native cycle.
        # dob: [day, month, year]
        birth_year = self.dob[-1]

        # Use an AND condition to check if the home planet is in *both* required dictionaries
        if self.home_planet in Planets_Year and self.home_planet in Planets_Rot:
            
            # 1. Obtaining planet offset
            planet_year_offset = Planets_Year[self.home_planet]
            planet_rot_factor = Planets_Rot[self.home_planet]

            # 2. Calculating current planet year (Person's home planet)
            current_planet_year = current_year + planet_year_offset

            # 3. Calculating Persons age (in their home planet years)
            individual_hp_age = current_planet_year - birth_year

            # 4. Calculating Person's age (in earth years via conversion)
            individual_earth_age = individual_hp_age * planet_rot_factor

            # Print statement
            simple_name = self.full_name_simple() # Use the proper method call

            print(15 * "-")
            # Rounding for clean display
            print(f"{simple_name}'s age on {self.home_planet} is {individual_hp_age:.2f} native years.")
            print(f"{simple_name}'s age in Earth years is {individual_earth_age:.2f} Earth years.")
            print(15 * "-")
            
            return round(individual_earth_age, 2), round(individual_hp_age, 2)
            
        else: 
            print(15 * "-")
            print("Age cannot be calculated due to Person's home planet not in registry.")
            print("Please provide home planet. If home planet cannot be provided, please fill")
            print("out form F-8294 and report to Administrator office No. 423.")
            print("Until then, age will be given as -- Unknown --")
            print(15 * "-")
            
            # Explicitly define and return the unknown string output as requested by the user
            individual_hp_age = "-- Unknown --"
            individual_earth_age = "-- Unknown --"
            return individual_earth_age, individual_hp_age
