import streamlit as st
import sqlite3
import matplotlib.pyplot as plt

# ----------------------------
# Setup database
# ----------------------------
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

# ----------------------------
# Functions
# ----------------------------
def add_student(username, password, name, adm_no, std_class, section, roll_no):
    c.execute("INSERT OR REPLACE INTO students VALUES (?, ?, ?, ?, ?, ?, ?)",
              (username, password, name, adm_no, std_class, section, roll_no))
    conn.commit()

def get_student(username, password):
    c.execute("SELECT * FROM students WHERE username=? AND password=?", (username, password))
    return c.fetchone()

# ----------------------------
# Page 1: Login
# ----------------------------
st.title("📚 Dev Memorial Public School - Student Performance App")

menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Register":
    st.subheader("Register Student")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    name = st.text_input("Full Name")
    adm_no = st.text_input("Admission Number")
    std_class = st.text_input("Class")
    section = st.text_input("Section")
    roll_no = st.text_input("Roll Number")
    if st.button("Register"):
        add_student(username, password, name, adm_no, std_class, section, roll_no)
        st.success("✅ Registered Successfully!")

elif choice == "Login":
    st.subheader("Student Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        student = get_student(username, password)
        if student:
            st.success(f"Welcome {student[2]} 👋")
            
            # Menu after login
            tabs = st.tabs(["📄 Attendance", "📊 Marks", "📝 Test Records", "📬 Teacher Notes", "💡 Improvement Tips"])
            
            with tabs[0]:
                st.subheader("Attendance")
                st.info("Your attendance this term: 92% ✅")
                st.progress(0.92)
            
            with tabs[1]:
                st.subheader("Marks Overview")
                marks_data = {"Math": 85, "Science": 78, "English": 90, "History": 88}
                subjects = list(marks_data.keys())
                scores = list(marks_data.values())

                fig, ax = plt.subplots()
                ax.bar(subjects, scores)
                ax.set_ylabel("Marks")
                ax.set_title("Marks Chart")
                st.pyplot(fig)

            with tabs[2]:
                st.subheader("Test Records")
                st.write("""
                - **Math Test 1:** 85/100
                - **Science Test 1:** 78/100
                - **English Test 1:** 90/100
                """)

            with tabs[3]:
                st.subheader("Notes from Teacher")
                st.write("📌 Keep up the great work in English and History.")
                st.write("📌 Pay more attention to Science homework.")

            with tabs[4]:
                st.subheader("Improvement Tips")
                st.write("""
                - Revise Science chapters daily
                - Practice Math problems from NCERT
                - Read English newspapers to improve vocabulary
                """)
        else:
            st.error("❌ Invalid username or password")
