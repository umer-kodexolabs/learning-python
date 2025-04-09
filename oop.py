class Person:
    def __init__(self, fname, lname, age,gender, country, city):
        self.fname = fname
        self.lname = lname
        self.age = age
        self.gender = gender
        self.country = country
        self.city = city
        self.skills = []

    def person_info(self):
        pronoun = ""
        if self.gender.lower() == "male":
            pronoun = "He"
        else:
            pronoun = "She"
        return f"{self.fname} {self.lname} is {self.age} years old. {pronoun} lives in {self.country}, {self.city}"
    

    def add_skills(self, skill):
        self.skills.append(skill)
        return f"{skill} added"

    def introduce(self):
        return f"Hi, I'am {self.fname} {self.lname}."

    def get_skills(self):
        return self.skills




class Student(Person):
    def __init__(self, fname, lname, age, gender, country, city,grade=None):
        super().__init__(fname, lname, age, gender, country, city)
        self.grade = grade 

    # Method Overriding: We override the person_info method to include grade
    def person_info(self):
        return (f"{self.fname}  is {self.age} years old, lives in {self.city}, {self.country}, and is in {self.grade} grade.")

    # Method Overloading: Overloading the introduce method by adding an extra argument (can use *args or default arguments)
    def introduce(self, greeting="Hello"):
         return (f"{greeting}, I'm {self.fname} {self.lname} and I'm in {self.grade} grade.")

    
    def study(self):
        return (f"{self.fname} is studying in {self.grade} grade")



person = Person("Muhammad", "Umer", 18, "Male", "Pk", "Karachi")
print(person.get_skills())
print(person.add_skills("Typescript"))
print(person.add_skills("React"))
print(person.add_skills("Node Js"))
print(person.get_skills())
print(person.introduce())
print(person.person_info())


# Student Class
student = Student("Muhammad", "Umer", 18, "Male", "Pk", "Karachi", "7th",  )
print(student.get_skills())
print(student.add_skills("Typescript"))
print(student.add_skills("React"))
print(student.add_skills("Node Js"))
print(student.get_skills())
print(student.person_info())
print(student.introduce())
print(student.study())







