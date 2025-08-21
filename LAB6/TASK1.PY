class Student:
    def __init__(self, name, roll_no, marks):
        self.name = name
        self.roll_no = roll_no
        self.marks = float(marks)

    def details(self):
        print(f"Student Name: {self.name}")
        print(f"Student Roll No: {self.roll_no}")
        print(f"Student Marks: {self.marks}")

    def grade(self):
        if self.marks >= 90:
            return "A"
        elif self.marks >= 80:
            return "B"
        elif self.marks >= 70:
            return "C"
        elif self.marks >= 60:
            return "D"
        else:
            return "Fail"

# Input from user
name = input("Enter Student Name: ")
roll_no = input("Enter Student Roll No: ")
marks = input("Enter Student Marks: ")

# Create Student object
student = Student(name, roll_no, marks)

# Call methods
student.details()
print(f"Student Grade: {student.grade()}")
