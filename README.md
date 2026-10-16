# Student Grade Management System

A command-line program, written in Python, that manages student marks and grades.
Data is stored in a JSON file, so it is kept between runs.

## Features
- Add, view, search, update and delete students
- Input checks: marks must be numbers from 0 to 100, and each subject needs a mark
- Automatic average and letter grade (A 90+, B 80+, C 70+, D 60+, F below 60)
- Ranked report, sorted by average
- Class statistics: number of students, class average, highest and lowest average

## Run it
Requires Python 3.

```bash
python3 student_grade_manager.py
```

A `students.json` file is created the first time you add a student.

## Menu
1. Add Student
2. View Students
3. Search Student
4. Update Student
5. Delete Student
6. Calculate Grades
7. Generate Report
8. Class Statistics
9. Exit

## Author
Sandile Luthuli (GitHub: SANDILE027)