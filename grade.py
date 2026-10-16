"""Student Grade Management System

A command-line program to add, view, search, update and delete students,
calculate grades, generate a report and show class statistics.
Data is saved to students.json so it is kept between runs.
"""

import json

FILE_NAME = "students.json"


def get_grade(average):
    """Return a letter grade for an average mark."""
    if average >= 90:
        return "A"
    if average >= 80:
        return "B"
    if average >= 70:
        return "C"
    if average >= 60:
        return "D"
    return "F"


def load_students():
    """Load students from the file when the program starts."""
    try:
        with open(FILE_NAME, "r") as file:
            students = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

    # Make sure every saved student has a grade
    for details in students.values():
        details["Grade"] = get_grade(details["Average"])
    return students


def save_students():
    """Save students to the file."""
    with open(FILE_NAME, "w") as file:
        json.dump(student_list, file, indent=4)


student_list = load_students()


def get_subjects_and_marks():
    """Ask for subjects and marks until the input is valid."""
    while True:
        subjects = [s.strip() for s in input("Enter subjects (comma-separated): ").split(",") if s.strip()]

        try:
            marks = [float(m) for m in input("Enter marks (comma-separated): ").split(",")]
        except ValueError:
            print("Marks must be numbers. Try again.\n")
            continue

        if not subjects:
            print("Enter at least one subject. Try again.\n")
        elif len(subjects) != len(marks):
            print(f"You entered {len(subjects)} subjects but {len(marks)} marks. Try again.\n")
        elif any(m < 0 or m > 100 for m in marks):
            print("Marks must be between 0 and 100. Try again.\n")
        else:
            return subjects, marks


def build_record(subjects, marks):
    """Build a student record with the average and grade filled in."""
    average = sum(marks) / len(marks)
    return {
        "Subjects": subjects,
        "Marks": marks,
        "Average": average,
        "Grade": get_grade(average),
    }


def print_student(student_number, details):
    """Print one student's details."""
    print(f"Student Number: {student_number}")
    print(f"Subjects: {', '.join(details['Subjects'])}")
    print(f"Marks: {details['Marks']}")
    print(f"Average: {details['Average']:.2f}")
    print(f"Grade: {details.get('Grade', 'N/A')}")
    print()


def ask_student_number(prompt):
    return input(prompt).strip()


def add_student():
    student_number = ask_student_number("Enter student number: ")

    if not student_number:
        print("Student number cannot be empty.")
        return

    if student_number in student_list:
        print("That student number already exists. Use Update instead.")
        return

    subjects, marks = get_subjects_and_marks()
    student_list[student_number] = build_record(subjects, marks)
    save_students()
    print("Student added successfully.")


def view_students():
    if not student_list:
        print("No students found.")
        return

    print("\n===== STUDENTS =====")
    for student_number, details in student_list.items():
        print_student(student_number, details)


def search_student():
    student_number = ask_student_number("Enter student number to search: ")

    if student_number in student_list:
        print()
        print_student(student_number, student_list[student_number])
    else:
        print("Student not found.")


def update_student():
    student_number = ask_student_number("Enter student number to update: ")

    if student_number not in student_list:
        print("Student not found.")
        return

    print("\nCurrent details:")
    print_student(student_number, student_list[student_number])

    print("Enter new details:")
    subjects, marks = get_subjects_and_marks()
    student_list[student_number] = build_record(subjects, marks)
    save_students()
    print("Student updated successfully.")


def delete_student():
    student_number = ask_student_number("Enter student number to delete: ")

    if student_number not in student_list:
        print("Student not found.")
        return

    confirm = input(f"Delete {student_number}? (y/n): ").strip().lower()
    if confirm == "y":
        del student_list[student_number]
        save_students()
        print("Student deleted successfully.")
    else:
        print("Delete cancelled.")


def calculate_grades():
    if not student_list:
        print("No students found.")
        return

    print("\n===== GRADES =====")
    for student_number, details in student_list.items():
        details["Grade"] = get_grade(details["Average"])
        print(f"Student Number: {student_number}")
        print(f"Average: {details['Average']:.2f}")
        print(f"Grade: {details['Grade']}")
        print()

    save_students()


def generate_report():
    if not student_list:
        print("No students found.")
        return

    ranked = sorted(student_list.items(), key=lambda item: item[1]["Average"], reverse=True)

    print("\n===== STUDENT REPORT (highest average first) =====")
    for rank, (student_number, details) in enumerate(ranked, start=1):
        print(f"Rank: {rank}")
        print_student(student_number, details)


def class_statistics():
    if not student_list:
        print("No students found.")
        return

    averages = [details["Average"] for details in student_list.values()]

    print("\n===== CLASS STATISTICS =====")
    print(f"Number of Students: {len(student_list)}")
    print(f"Class Average: {sum(averages) / len(averages):.2f}")
    print(f"Highest Average: {max(averages):.2f}")
    print(f"Lowest Average: {min(averages):.2f}")


def print_menu():
    print("\n===== STUDENT GRADE MANAGEMENT SYSTEM =====")
    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Calculate Grades")
    print("7. Generate Report")
    print("8. Class Statistics")
    print("9. Exit")


def main():
    actions = {
        "1": add_student,
        "2": view_students,
        "3": search_student,
        "4": update_student,
        "5": delete_student,
        "6": calculate_grades,
        "7": generate_report,
        "8": class_statistics,
    }

    while True:
        print_menu()
        menu_choice = input("Choose an option: ").strip()

        if menu_choice == "9":
            print("Exiting Student Grade Management System. Goodbye!")
            break
        elif menu_choice in actions:
            actions[menu_choice]()
        else:
            print("Invalid option. Please choose between 1 and 9.")


if __name__ == "__main__":
    main()