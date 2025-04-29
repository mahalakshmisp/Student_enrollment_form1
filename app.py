# app.py - Full Flask Project for Student Management

from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)


students_file = 'students.csv'
courses_file = 'courses.csv'
enrollments_file = 'enrollments.csv'
payments_file = 'payments.csv'
instructors_file = 'instructors.csv'
feedback_file = 'feedback.csv'


def load_data(file, columns):
    return pd.read_csv(file) if os.path.exists(file) else pd.DataFrame(columns=columns)


students_df = load_data(students_file, ["Student ID", "Full Name", "DOB", "Gender", "Phone", "Email", "Address", "Course", "Enroll Date", "Payment Status"])
courses_df = load_data(courses_file, ["Course ID", "Course Name", "Description", "Duration", "Fee", "Instructor", "Start Date", "End Date"])
enrollments_df = load_data(enrollments_file, ["Enrollment ID", "Student ID", "Course ID", "Enrollment Date", "Status", "Feedback"])
payments_df = load_data(payments_file, ["Invoice No", "Student Name", "Course Name", "Amount Due", "Amount Paid", "Balance", "Payment Date", "Method", "Status"])
instructors_df = load_data(instructors_file, ["Instructor ID", "Name", "Contact", "Courses", "Availability", "Rate"])
feedback_df = load_data(feedback_file, ["Course Name", "Student Name", "Rating", "Comments", "Date"])

@app.route('/')
def dashboard():
    total_students = len(students_df)
    active_courses = len(courses_df)
    monthly_revenue = payments_df["Amount Paid"].sum() if not payments_df.empty else 0

    chart_data = enrollments_df["Course ID"].value_counts()
    chart_labels = [courses_df[courses_df["Course ID"] == cid]["Course Name"].values[0] if not courses_df[courses_df["Course ID"] == cid].empty else cid for cid in chart_data.index]

    return render_template("dashboard.html",
                           total_students=total_students,
                           active_courses=active_courses,
                           monthly_revenue=monthly_revenue,
                           chart_labels=chart_labels,
                           chart_data=chart_data.tolist())

@app.route('/students')
def students():
    return render_template("students.html", students=students_df.to_dict(orient='records'))

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        new_student = request.form.to_dict()
        students_df.loc[len(students_df)] = new_student
        students_df.to_csv(students_file, index=False)
        return redirect(url_for('students'))
    return render_template("add_student.html", courses=courses_df["Course Name"].tolist())

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        new_feedback = request.form.to_dict()
        feedback_df.loc[len(feedback_df)] = new_feedback
        feedback_df.to_csv(feedback_file, index=False)
        return redirect(url_for('dashboard'))  # or wherever you want to go after submission
    return render_template("feedback_form.html")

# Add this route to your app.py to handle instructor form submission
@app.route('/instructors', methods=['GET', 'POST'])
def add_instructor():
    if request.method == 'POST':
        new_instructor = request.form.to_dict()
        instructors_df.loc[len(instructors_df)] = new_instructor
        instructors_df.to_csv(instructors_file, index=False)
        return redirect(url_for('dashboard'))  # Redirect to dashboard or any other page
    return render_template("instructor_form.html")

@app.route('/payments', methods=['GET', 'POST'])
def add_payment():
    if request.method == 'POST':
        new_payment = request.form.to_dict()
        payments_df.loc[len(payments_df)] = new_payment
        payments_df.to_csv(payments_file, index=False)
        return redirect(url_for('dashboard'))
    return render_template("payment_form.html")

# Add this route to your app.py to handle attendance form submission

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    if request.method == 'POST':
        date = request.form['Date']
        attendance_records = {'Date': date}
        for key, value in request.form.items():
            if key.startswith('attendance_'):
                student_id = key.split('_')[1]
                attendance_records[student_id] = value

        try:
            existing_attendance = pd.read_csv('attendance.csv')
        except FileNotFoundError:
            existing_attendance = pd.DataFrame()

        new_row = pd.DataFrame([attendance_records])
        updated_attendance = pd.concat([existing_attendance, new_row], ignore_index=True)
        updated_attendance.to_csv('attendance.csv', index=False)

        return redirect(url_for('dashboard'))

    return render_template("attendance_form.html", students=students_df.to_dict(orient='records'))

# Add this route to your app.py to handle enrollment form submission

@app.route('/enrollments', methods=['GET', 'POST'])
def enroll():
    if request.method == 'POST':
        new_enrollment = request.form.to_dict()
        enrollments_df.loc[len(enrollments_df)] = new_enrollment
        enrollments_df.to_csv(enrollments_file, index=False)
        return redirect(url_for('dashboard'))

    return render_template("enrollment_form.html", 
                           students=students_df.to_dict(orient='records'), 
                           courses=courses_df.to_dict(orient='records'))

# Add this route to your app.py to handle course form submission

@app.route('/courses', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        new_course = request.form.to_dict()
        courses_df.loc[len(courses_df)] = new_course
        courses_df.to_csv(courses_file, index=False)
        return redirect(url_for('dashboard'))
    return render_template("course_form.html")



if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host="0.0.0.0", port=5000)
