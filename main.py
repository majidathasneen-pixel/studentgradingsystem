import sqlite3

# ---------------- DATABASE CONNECTION ----------------
conn=sqlite3.connect("students.db")
cursor=conn.cursor()


# ---------------- CREATE TABLES ----------------
def create_tables():


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    cursor.execute("""
       CREATE TABLE IF NOT EXISTS students (
           student_id INTEGER PRIMARY KEY AUTOINCREMENT,
           name TEXT NOT NULL,
           age INTEGER
       )
       """)

    cursor.execute("""
       CREATE TABLE IF NOT EXISTS subjects (
           subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
           subject_name TEXT UNIQUE NOT NULL
       )
       """)

    cursor.execute("""
   CREATE TABLE IF NOT EXISTS marks (
       mark_id INTEGER PRIMARY KEY AUTOINCREMENT,
       student_id INTEGER,
       subject TEXT NOT NULL,
       marks INTEGER NOT NULL,
       grade TEXT NOT NULL,
       FOREIGN KEY(student_id) REFERENCES students(student_id)
   )
   """)


    conn.commit()
    # ---------------- USER AUTHENTICATION ----------------


def register_user():


    username = input("Enter new username: ")
    password = input("Enter new password: ")

    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print("✅ User registered successfully")
    except sqlite3.IntegrityError:
        print("❌ Username already exists")

    #conn.close()


def login_user():
    conn=sqlite3.connect("students.db")
    cursor=conn.cursor()

    username = input("Username: ")
    password = input("Password: ")

    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()

    #conn.close()

    if user:
        print("✅ Login successful")
        return True
    else:
        print("❌ Invalid username or password")
        return False


# ---------------- FUNCTIONS ----------------

def add_student():
    conn=sqlite3.connect("students.db")
    cursor=conn.cursor()
    name = input("Enter student name: ")
    age = int(input("Enter age: "))
    cursor.execute(
    "INSERT INTO students (name, age) VALUES (?, ?)",
    (name, age)
    )
    conn.commit()
    #conn.close()
    print("Student added successfully.")

def calculate_grade(marks):
    if marks >= 90:
        return "A+"
    elif marks >= 80:
        return"A"
    elif marks >= 70:
        return"B"
    elif marks >= 60:
        return"C"
    else:
        return"Fail"


def add_marks():
    conn=sqlite3.connect("students.db")
    cursor=conn.cursor()
    student_id = int(input("Enter student ID: "))
    subject = input("Enter subject name: ")
    marks = int(input("Enter marks: "))

    grade=calculate_grade(marks)
    cursor.execute(
        "INSERT INTO marks (student_id, subject, marks,grade) VALUES (?, ?, ?, ?)",
        (student_id, subject, marks,grade)
    )
    conn.commit()
    #conn.close()
    print("Marks added successfully.")


def view_students():
    cursor.execute("SELECT * FROM students")
    records = cursor.fetchall()
    print("\nStudent List:")
    for row in records:
        print(row)


def view_result():
    conn=sqlite3.connect("students.db")
    cursor=conn.cursor()
    student_id = int(input("Enter student ID: "))
    cursor.execute(
        "SELECT subject, marks FROM marks WHERE student_id=?",
        (student_id,)
    )
    records = cursor.fetchall()

    if not records:
        print("No marks found for this student.")
        return

    total = 0
    print("\nSubject Marks:")
    for subject, marks in records:
        print(subject, ":", marks)
        total += marks

    average = total / len(records)
    print("Average Marks:", average)

    if average >= 90:
        grade = "A"
    elif average >= 75:
        grade = "B"
    elif average >= 60:
        grade = "C"
    elif average >= 50:
        grade = "D"
    else:
        grade = "Fail"

    print("Grade:", grade)
    conn.close()


def update_marks():
    mark_id = int(input("Enter mark ID to update: "))
    new_marks = int(input("Enter new marks: "))
    cursor.execute(
        "UPDATE marks SET marks=? WHERE mark_id=?",
        (new_marks, mark_id)
    )
    conn.commit()
    print("Marks updated successfully.")


def delete_student():
    student_id = int(input("Enter student ID to delete: "))
    cursor.execute("DELETE FROM marks WHERE student_id=?", (student_id,))
    cursor.execute("DELETE FROM students WHERE student_id=?", (student_id,))
    conn.commit()
    print("Student record deleted successfully.")


# ---------------- MAIN MENU ----------------
def main_menu():
 while True:
     print("""
     ========= STUDENT GRADING SYSTEM =========
     1. Add Student
     2. Add marks
     3. View Students
     4. View Results
     5. Update Marks
     6. Delete Student
     7. Logout
     """)

     choice = input("Enter your choice: ")

     if choice == "1":
         add_student()
     elif choice == "2":
         add_marks()
     elif choice == "3":
         view_students()
     elif choice == "4":
          view_result()
     elif choice == "5":
         update_marks()
     elif choice == "6":
         delete_student()
     elif choice == "7":
         print("🔐 Logged out")
         break
     else:
         print("❌ Invalid choice")

 # ---------------- PROGRAM START ----------------


def start():
    create_tables()

    while True:
        print("""
     ===== LOGIN MENU =====
     1. Register
     2. Login
     3. Exit
     """)

        choice = input("Enter choice: ")

        if choice == "1":
            register_user()
        elif choice == "2":
            if login_user():
                main_menu()
        elif choice == "3":
            print("👋 Exiting program")
            break
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    start()
    conn.close()


