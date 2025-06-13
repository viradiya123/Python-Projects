class School:
    def __init__(self, name, level, numberOfStudents):
        self._name = name
        self._level = level
        self._numberOfStudents = numberOfStudents

    # Getters
    def get_name(self):
        return self._name

    def get_level(self):
        return self._level

    def get_numberOfStudents(self):  
        return self._numberOfStudents  

    # Setter
    def set_numberOfStudents(self, new_number):
        if isinstance(new_number, int):
            self._numberOfStudents = new_number
        else:
            raise TypeError("Number of students must be an integer")

    # __repr__ method
    def __repr__(self):
        return "School Name: {}\nLevel: {}\nTotal Students: {}".format(
            self._name, self._level, self._numberOfStudents
        )

# Primary school
class Primary(School):  
    def __init__(self, name, numberOfStudents, pickupPolicy):
        super().__init__(name, "Primary", numberOfStudents)  
        self._pickupPolicy = pickupPolicy

    def get_pickupPolicy(self):
        return self._pickupPolicy

    def __repr__(self):
        base = super().__repr__() 
        return base + "\nPickup Policy: {}".format(self._pickupPolicy)

# Middle school
class Middle(School):
    def __init__(self, name, numberOfStudents):
        super().__init__(name, "Middle", numberOfStudents)

# High school
class High(School):
    def __init__(self, name, numberOfStudents, sportsTeams):
        super().__init__(name, "High", numberOfStudents)
        self._sportsTeams = sportsTeams

    def get_sportsTeams(self):
        return self._sportsTeams

    def __repr__(self):
        base = super().__repr__()
        return base + "\nSports Teams: {}".format(", ".join(self._sportsTeams))


# Object creation
s1 = School("Greenwood", "middle", 400)
print(s1)

# Getter
print(s1.get_numberOfStudents())

# Setter
s1.set_numberOfStudents(450)
print(s1.get_numberOfStudents())

# Primary school
p1 = Primary("SunRise", 300, "Pickup after 3:00 PM")
print(p1)

# High school
h1 = High("GEC Patan", 1500, ["Cricket", "Football"])
print(h1)
