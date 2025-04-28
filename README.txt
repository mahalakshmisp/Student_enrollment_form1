# Student Management System (Flask Project)

## Project Structure:
/project-folder
│
├── app.py                  # Flask application logic
├── students.csv            # Student data
├── courses.csv             # Courses data
├── enrollments.csv         # Enrollment records
├── payments.csv            # Payment details
├── instructors.csv         # Instructor profiles
├── feedback.csv            # Course feedback
│
├── /templates
│   ├── dashboard.html      # Dashboard with chart
│   ├── students.html       # Student information table
│   └── add_student.html    # Form to add new students
│
└── /static
    └── style.css           # CSS styling

## How to Run
1. Install Flask and Pandas:
   pip install flask pandas

2. Run the application:
   python app.py

3. Visit http://127.0.0.1:5000/ in your browser.

## Notes:
- All data is stored in CSV files.
- You can add more routes and templates as needed.
- Modify the CSS in /static/style.css for customization.
