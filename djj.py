import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import mysql.connector
import random
import csv

# Constants
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
PERIODS = 8
MAX_PERIODS_PER_TEACHER = 48

#databse connection
con=mysql.connector.connect(
    host="localhost",
    user="root",
    password="123Asd#123",
    database="timetable"
)
cursor=con.cursor()
# Create main window
root = tk.Tk()
root.title("QTECH-Timetable")
root.geometry("800x500")

# Create a parent frame to hold both sections
main_frame = tk.Frame(root)
main_frame.pack(pady=10, padx=10)

# Create data entry frame to hold all data entry frames 
dataentry_frame=tk.Frame(main_frame)
dataentry_frame.grid(row=0, column=0, pady=10, padx=10) 

# function to aad department 
def add_department():
    Dept_id=dept_id_entry.get().strip()
    Dept_name=dept_name_entry.get().strip()
    

    if Dept_id and Dept_name :
        try:
            query = "INSERT INTO timetable.department (Department_id, Department_name) VALUES(%s, %s)"
            cursor.execute(query, (Dept_id, Dept_name))
            con.commit()
            messagebox.showinfo("Success","Department Add Successfully!")

            #clear the entry after adding
            dept_id_entry.delete(0, tk.END)
            dept_name_entry.delete(0, tk.END)
            
            #update_departments()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")
    else :
        messagebox.showwarning("Input Error","All field are requierd")


# function to aad department 
def del_department():
    Dept_id=dept_id_entry.get().strip()
    

    if Dept_id :
        try:
            query = " DELETE FROM timetable.department WHERE  Department_id = %s"
            cursor.execute(query, (Dept_id,))
            con.commit()
            if cursor.rowcount > 0:
                messagebox.showinfo("Success", "Department deleted successfully!")
            else:
                messagebox.showwarning("Not Found", "Department ID not found.")


            #clear the entry after adding
            dept_id_entry.delete(0, tk.END)
            

            #update_departments()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")
    else :
        messagebox.showwarning("Input Error","All field are requierd")


# Department Frame
dept_frame = tk.Frame(dataentry_frame, relief="groove", borderwidth=2)
dept_frame.grid(row=0, column=0, padx=20, pady=10, sticky="w")

tk.Label(dept_frame, text="........ADD DEPARTMENT........").grid(row=0, column=0, columnspan=2, pady=5)

tk.Label(dept_frame, text="DEPARTMENT ID:").grid(row=1, column=0, sticky="w", pady=5)
dept_id_entry = tk.Entry(dept_frame)
dept_id_entry.grid(row=1, column=1, padx=10, sticky="w")

tk.Label(dept_frame, text="DEPARTMENT NAME:").grid(row=2, column=0, sticky="w", pady=5)
dept_name_entry = tk.Entry(dept_frame)
dept_name_entry.grid(row=2, column=1, padx=10, sticky="w")


tk.Button(dept_frame, text="ADD DEPARTMENT", command= add_department).grid(row=4, column=0, pady=10)
tk.Button(dept_frame, text="DELETE DEPARTMENT", command= del_department).grid(row=4, column=1, pady=10)


# function to aad teacher    
def add_teacher():
    Teacher_id=teacher_id_entry.get().strip()
    Teacher_name=teacher_name_entry.get().strip()

    if Teacher_id and Teacher_name:
        try:
            query = "INSERT INTO timetable.teachers (Teacher_id, Teacher_name) VALUES(%s, %s)"
            cursor.execute(query, (Teacher_id, Teacher_name))
            con.commit()
            messagebox.showinfo("Success","Taecher Add Successfully!")

            #clear the entry after adding
            teacher_id_entry.delete(0, tk.END)
            teacher_name_entry.delete(0, tk.END)

            #update_departments()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")
    else :
        messagebox.showwarning("Input Error","All field are requierd")

# function to delete teacher    
def del_teacher():
    Teacher_id=teacher_id_entry.get().strip()
    

    if Teacher_id :
        try:
            query = "DELETE FROM timetable.teachers WHERE  Teacher_id = %s"
            cursor.execute(query, (Teacher_id,))
            con.commit()
            messagebox.showinfo("Success","Taecher Add Successfully!")

            #clear the entry after adding
            teacher_id_entry.delete(0, tk.END)
           
            #update_departments()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")
    else :
        messagebox.showwarning("Input Error","All field are requierd")

# Teacher Frame
teacher_frame = tk.Frame(dataentry_frame, relief="groove", borderwidth=2)
teacher_frame.grid(row=0, column=1, padx=20, pady=10, sticky="w")

tk.Label(teacher_frame, text="........ADD TEACHER........").grid(row=0, column=0, columnspan=2, pady=5)

tk.Label(teacher_frame, text="TEACHER ID:").grid(row=1, column=0, sticky="w", pady=5)
teacher_id_entry = tk.Entry(teacher_frame)
teacher_id_entry.grid(row=1, column=1, padx=10, sticky="w")

tk.Label(teacher_frame, text="TEACHER NAME:").grid(row=2, column=0, sticky="w", pady=5)
teacher_name_entry = tk.Entry(teacher_frame)
teacher_name_entry.grid(row=2, column=1, padx=10, sticky="w")

tk.Button(teacher_frame, text="ADD TEACHER", command=add_teacher, bg="GREEN").grid(row=3, column=0, pady=10)
tk.Button(teacher_frame, text="DELETE TEACHER", command=del_teacher, bg= "RED").grid(row=3, column=1, pady=10)

# function to aad subject    
def add_subject():
    Subject_id = subject_id_entry.get().strip()
    Subject_name = subject_name_entry.get().strip()
    Semester = semester_entry.get().strip()
    Periods = periods_entry.get().strip()
    Labs = labs_entry.get().strip()
    Department_name = department_var.get().strip()
    Teacher_name = teacher_var.get().strip()

       # Ensure that a valid department and teacher is selected
    if Department_name == "" or Department_name == "Select Department":
        messagebox.showwarning("Input Error", "Please select a valid department.")
        return

    if Teacher_name == "" or Teacher_name == "Select Teacher":
        messagebox.showwarning("Input Error", "Please select a valid teacher.")
        return

    if Subject_id and Subject_name and Semester and Periods and Department_name and Labs and Teacher_name:
        try:
            query = "INSERT INTO timetable.subjects (Subject_id, Subject_name, Semester, Department_name, Teacher_name, No_periods, No_lab) VALUES(%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (Subject_id, Subject_name, Semester, Department_name, Teacher_name, Periods, Labs))
            con.commit()
            messagebox.showinfo("Success", "Subject Added Successfully!")

            # Clear entries after adding
            subject_id_entry.delete(0, tk.END)
            subject_name_entry.delete(0, tk.END)
            semester_entry.delete(0, tk.END)
            periods_entry.delete(0, tk.END)
            labs_entry.delete(0, tk.END)

            department_var.set("Select Department")  # Reset dropdown
            teacher_var.set("Select Teacher")  # Reset dropdown

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")
    else:
        messagebox.showwarning("Input Error", "All fields are required.")


# function to delete SUBJECT    
def del_subject():
    Subject_id=subject_id_entry.get().strip()
    

    if Subject_id :
        try:
            query = "DELETE FROM timetable.subjects WHERE  Subject_id = %s"
            cursor.execute(query, (Subject_id,))
            con.commit()
            messagebox.showinfo("Success","Taecher Deleted Successfully!")

            #clear the entry after adding
            subject_id_entry.delete(0, tk.END)
           
            #update_departments()
        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")
    else :
        messagebox.showwarning("Input Error","All field are requierd")



#update department combo box 

def update_departments():
    cursor.execute("SELECT DISTINCT Department_name FROM timetable.department")
    departments = [row[0] for row in cursor.fetchall()]

    # Insert a placeholder
    departments.insert(0, "Select Department")
    department_menu["values"] = departments  
    department_var.set("Select Department")  # Set default to placeholder


#update teacher combobox
def update_teachers():
    cursor.execute("SELECT DISTINCT Teacher_name FROM timetable.teachers")
    teachers = [row[0] for row in cursor.fetchall()]

    # Insert a placeholder
    teachers.insert(0, "Select Teacher")
    teacher_menu["values"] = teachers  
    teacher_var.set("Select Teacher")  # Set default to placeholder

# Sujects Frame
subject_frame = tk.Frame(dataentry_frame, relief="groove", borderwidth=2)
subject_frame.grid(row=0, column=2, padx=20, pady=10, sticky="w")

tk.Label(subject_frame, text="........ADD SUBJECT........").grid(row=0, column=1, columnspan=2, pady=5)

tk.Label(subject_frame, text="SUBJECT ID:").grid(row=1, column=0, sticky="w", pady=5)
subject_id_entry = tk.Entry(subject_frame)
subject_id_entry.grid(row=1, column=1, padx=10, sticky="w")

tk.Label(subject_frame, text="SUBJECT NAME:").grid(row=1, column=2, sticky="w", pady=5)
subject_name_entry = tk.Entry(subject_frame)
subject_name_entry.grid(row=1, column=3, padx=10, sticky="w")

tk.Label(subject_frame, text="SEMESTER NAME:").grid(row=2, column=0, sticky="w", pady=5)
semester_entry = tk.Entry(subject_frame)
semester_entry.grid(row=2, column=1, padx=10, sticky="w")

tk.Label(subject_frame, text="NO OF PERIODS:").grid(row=2, column=2, sticky="w", pady=5)
periods_entry = tk.Entry(subject_frame)
periods_entry.grid(row=2, column=3, padx=10, sticky="w")


tk.Label(subject_frame, text="NO OF LABS:").grid(row=2, column=4, sticky="w", pady=5)
labs_entry = tk.Entry(subject_frame)
labs_entry.grid(row=2, column=5, padx=10, sticky="w")

tk.Label(subject_frame, text="DEPARTMENT NAME:").grid(row=3, column=0, sticky="w", pady=5)
department_var = tk.StringVar()
department_menu = ttk.Combobox(subject_frame, textvariable=department_var, values=[],  state="readonly")
department_menu.grid(row=3, column=1, padx=10, sticky="w")

tk.Label(subject_frame, text="TEACHER NAME:").grid(row=3, column=2, sticky="w", pady=5)
teacher_var = tk.StringVar()
teacher_menu = ttk.Combobox(subject_frame, textvariable=teacher_var, values=[],  state="readonly")
teacher_menu.grid(row=3, column=3, padx=10, sticky="w")


tk.Button(subject_frame, text="ADD SUBJECT", command=add_subject).grid(row=4, column=0, pady=10)
tk.Button(subject_frame, text="DELETE SUBJECT", command=del_subject).grid(row=4, column=3, pady=10)



def update_departments1():
    cursor.execute("SELECT DISTINCT Department_name FROM timetable.department")
    departments = [row[0] for row in cursor.fetchall()]
    
    department1_menu["values"]=departments  # Clear existing options

    if departments:
        department_var.set(departments[0])  # Select the first department by default
        

# generate department wise timetable Frame
genrate_frame = tk.Frame(dataentry_frame, relief="groove", borderwidth=2)
genrate_frame.grid(row=1, column=0, padx=20, pady=10, sticky="w")

# Function of genrate time table 

def generate_timetable():
    global department_timetable_data
    selected_department = department_var.get()
    selected_semester = semester_var.get()

    if not selected_department or not selected_semester:
        messagebox.showwarning("Selection Error", "Please select a department and semester.")
        return

    cursor.execute("""
        SELECT Subject_name, Teacher_name, No_periods  
        FROM subjects
        WHERE Department_name=%s AND Semester=%s
    """, (selected_department, selected_semester))
    data = cursor.fetchall()

    if not data:
        messagebox.showwarning("No Data", "No subjects found for the selected department and semester!")
        return

    subject_teacher_list = [
        (subject, teacher, no_periods) for subject, teacher, no_periods  in data
    ]

    teacher_periods = {}  
    subject_periods = {}  
    department_timetable_data = {}  

    random.seed(100)  

    for i, day in enumerate(DAYS):
        assigned_teachers = {}
        j = 0

        while j < PERIODS:
            random.shuffle(subject_teacher_list)

            for subject, teacher,  no_periods in subject_teacher_list:
                if teacher not in assigned_teachers:
                    assigned_teachers[teacher] = 0

                    max_periods_for_subject = no_periods
                    current_subject_periods = subject_periods.get(subject, 0)
                    current_teacher_periods = teacher_periods.get(teacher, 0)
                # Schedule theoretical subjects in periods 1-4
                elif (
                    current_subject_periods < max_periods_for_subject
                    and current_teacher_periods < MAX_PERIODS_PER_TEACHER
                    and assigned_teachers[teacher] < 2
                    and j < 4  # Ensuring theory subjects are scheduled before practical starts
                ):
                    timetable[i][j].set(f"{subject} ({teacher})")

                    subject_periods[subject] = current_subject_periods + 1
                    teacher_periods[teacher] = current_teacher_periods + 1
                    assigned_teachers[teacher] += 1
                    department_timetable_data.setdefault(teacher, []).append((i, j, f"{subject} (Theory)"))

                    j += 3
                    break
            else:
                j += 1  

    messagebox.showinfo("Success", "Department timetable generated successfully!")


tk.Label(genrate_frame, text="........GENERATE DEPARMENT WISE TIMETALE........").grid(row=0, column=0, columnspan=2, pady=5)

tk.Label(genrate_frame, text="DEPARTMENT NAME:").grid(row=1, column=0, sticky="w", pady=5)
department_var = tk.StringVar()
department1_menu = ttk.Combobox(genrate_frame, textvariable=department_var, values=[])
department1_menu.grid(row=1, column=1, padx=10, sticky="w")

tk.Label(genrate_frame, text="SEMESTER NAME:").grid(row=2, column=0, sticky="w", pady=5)
semester_var = tk.StringVar()
semester_menu = ttk.Combobox(genrate_frame, textvariable=semester_var, values=[])
semester_menu.grid(row=2, column=1, padx=10, sticky="w")

tk.Button(genrate_frame, text="GENRATE TIMETABLE", command=generate_timetable).grid(row=3, column=0, pady=10)


def update_semester():
    cursor.execute("SELECT DISTINCT Semester FROM timetable.subjects")
    semesters = [row[0] for row in cursor.fetchall()]
    
    semester_menu["values"]=semesters  # Clear existing options

    if semesters:
        semester_var.set(semesters[0])  # Select the first department by default
        # update_semesters()  # Call the function if needed


# generate  teacher wise timetable Frame
genrate1_frame = tk.Frame(dataentry_frame, relief="groove", borderwidth=2)
genrate1_frame.grid(row=1, column=2, padx=20, pady=10, sticky="w")

tk.Label(genrate1_frame, text="........GENERATE TEACHER WISE TIMETALE........").grid(row=0, column=0, columnspan=2, pady=5)

tk.Label(genrate1_frame, text="TEACHER NAME:").grid(row=1, column=0, sticky="w", pady=5)
teacher_var = tk.StringVar()
teacher1_menu = ttk.Combobox(genrate1_frame, textvariable=teacher_var, values=[])
teacher1_menu.grid(row=1, column=1, padx=10, sticky="w")

tk.Label(genrate1_frame, text="SEMESTER NAME:").grid(row=2, column=0, sticky="w", pady=5)
semester_var = tk.StringVar()
semester1_menu = ttk.Combobox(genrate1_frame, textvariable=semester_var, values=[])
semester1_menu.grid(row=2, column=1, padx=10, sticky="w")

tk.Button(genrate1_frame, text="GENRATE TIMETABLE", command=add_subject).grid(row=3, column=0, pady=10)


def update_semester1():
    cursor.execute("SELECT DISTINCT Semester FROM timetable.subjects")
    semesters = [row[0] for row in cursor.fetchall()]
    
    semester1_menu["values"]=semesters  # Clear existing options

    if semesters:
        semester_var.set(semesters[0])  # Select the first department by default
        # update_semesters()  # Call the function if needed



#update teacher combobox
def update_teachers1():
    cursor.execute("SELECT DISTINCT Teacher_name FROM timetable.teachers")
    teachers = [row[0] for row in cursor.fetchall()]
    
    teacher1_menu["values"]=teachers  # Clear existing options

    if teachers:
        teacher_var.set(teachers[0])  # Select the first department by default
        # update_semesters()  # Call the function if needed


# generate department wise timetable Frame
timetable_frame = tk.Frame(main_frame, relief="groove", borderwidth=2)
timetable_frame.grid(row=3, column=0, padx=10, pady=10)




#Timetable data storage
timetable = [[tk.StringVar() for _ in range(PERIODS)] for _ in range(len(DAYS))]


tk.Label(timetable_frame, text="Day/Period", width=12, height=2, borderwidth=1, relief="solid").grid(row=0,column=0,sticky="w")
for i in range(PERIODS):
    tk.Label(timetable_frame, text=f"Period{i+1}", width=20, height=2, borderwidth=1, relief="solid").grid(row=0, column=i+1, sticky="w")
for i, day in enumerate(DAYS):
    tk.Label(timetable_frame, text=day, width=12, height=2, borderwidth=1, relief="solid").grid(row=i+1,column=0,sticky="w")
    for j in range(PERIODS):
        timetable[i][j]=tk.StringVar()
        entry= tk.Entry(timetable_frame,textvariable=timetable[i][j], width=20)
        entry.grid(row=i+1,column=j+1,sticky="w")  




update_semester1()
update_semester()
update_teachers()
update_teachers1()
update_departments()
update_departments1()
root.mainloop()
