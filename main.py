import streamlit as st 
import sqlite3 
import matplotlib.pyplot as plt

#Setup database

# Setup database
conn = sqlite3.connect("student_performance.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS students (
    username TEXT PRIMARY KEY,
    password TEXT,
    name TEXT,
    adm_no TEXT,
    std_class TEXT,
    section TEXT,
    roll_no TEXT
)
""")

conn.commit()
Sample data for demonstration

sample_attendance = {'Jan': 92, 'Feb': 95, 'Mar': 88, 'Apr': 90} sample_marks = {'Math': 85, 'Science': 90, 'English': 78, 'Social': 88} sample_tests = ['Test 1 - Math: 80', 'Test 2 - Science: 85', 'Test 3 - English: 75'] sample_notes = ['Please improve handwriting.', 'Complete the pending homework.'] sample_tips = ['Practice Maths daily.', 'Read Science chapters thoroughly.']

Streamlit app

st.set_page_config(page_title="Dev Memorial Public School - Student Performance", layout="wide") st.title("Dev Memorial Public School - Student Performance App")

Session state

if 'logged_in' not in st.session_state: st.session_state.logged_in = False if 'user' not in st.session_state: st.session_state.user = None

Registration

def register(): st.subheader("Register") username = st.text_input("Username") password = st.text_input("Password", type="password") name = st.text_input("Full Name") adm_no = st.text_input("Admission No.") std_class = st.text_input("Class") section = st.text_input("Section") roll_no = st.text_input("Roll No.")

if st.button("Register"):
    try:
        c.execute("INSERT INTO students VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (username, password, name, adm_no, std_class, section, roll_no))
        conn.commit()
        st.success("Registration successful! You can now login.")
    except sqlite3.IntegrityError:
        st.error("Username already exists.")

Login

def login(): st.subheader("Login") username = st.text_input("Username") password = st.text_input("Password", type="password")

if st.button("Login"):
    c.execute("SELECT * FROM students WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    if user:
        st.session_state.logged_in = True
        st.session_state.user = user
        st.experimental_rerun()
    else:
        st.error("Invalid credentials")

Dashboard

def dashboard(): user = st.session_state.user st.success(f"Welcome, {user[2]} ({user[3]})")

tabs = st.tabs(["Attendance", "Marks", "Test Records", "Notes", "Improvement Tips"])

with tabs[0]:
    st.subheader("Attendance Record")
    fig, ax = plt.subplots()
    ax.bar(sample_attendance.keys(), sample_attendance.values(), color='skyblue')
    ax.set_ylabel('Percentage')
    ax.set_title('Monthly Attendance')
    st.pyplot(fig)

with tabs[1]:
    st.subheader("Marks Overview")
    fig, ax = plt.subplots()
    ax.pie(sample_marks.values(), labels=sample_marks.keys(), autopct='%1.1f%%')
    ax.set_title('Subject-wise Marks')
    st.pyplot(fig)

with tabs[2]:
    st.subheader("Test Records")
    for test in sample_tests:
        st.write(f"- {test}")

with tabs[3]:
    st.subheader("Notes from Teachers to Parents")
    for note in sample_notes:
        st.info(note)

with tabs[4]:
    st.subheader("Improvement Tips")
    for tip in sample_tips:
        st.success(tip)

Main logic

if not st.session_state.logged_in: login() st.markdown("---") st.write("Don't have an account?") with st.expander("Register here"): register() else: dashboard()

