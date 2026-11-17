import sqlite3
import streamlit as st

DB_NAME = "students.db"

# Database connection
def create_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn

# Create table
def create_table():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


# CREATE
def add_student(name, age):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO students (name, age) VALUES (?, ?)",
        (name, age)
    )

    conn.commit()
    conn.close()


# READ
def get_students():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()

    conn.close()
    return data


# UPDATE
def update_student(student_id, name, age):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE students SET name=?, age=? WHERE id=?",
        (name, age, student_id)
    )

    conn.commit()
    conn.close()


# DELETE
def delete_student(student_id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id=?",
        (student_id,)
    )

    conn.commit()
    conn.close()


# Create database table
create_table()


# STREAMLIT UI
st.title("Student Management System")

menu = st.sidebar.selectbox(
    "Select Operation",
    ["Create", "Read", "Update", "Delete"]
)


# CREATE
if menu == "Create":

    st.header("Add Student")

    name = st.text_input("Enter Student Name")
    age = st.number_input("Enter Student Age", min_value=1, step=1)

    if st.button("Add Student"):

        if name.strip():
            add_student(name, age)
            st.success("Student Added Successfully!")
        else:
            st.error("Please enter student name")


# READ
elif menu == "Read":

    st.header("Student Records")

    students = get_students()

    if students:
        st.table(students)
    else:
        st.info("No Students Found")


# UPDATE
elif menu == "Update":

    st.header("Update Student")

    students = get_students()

    if students:

        student_ids = [student[0] for student in students]

        student_id = st.selectbox(
            "Select Student ID",
            student_ids
        )

        selected_student = next(
            s for s in students if s[0] == student_id
        )

        name = st.text_input(
            "Enter New Name",
            value=selected_student[1]
        )

        age = st.number_input(
            "Enter New Age",
            min_value=1,
            value=selected_student[2]
        )


