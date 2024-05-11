import tkinter as tk
import mysql.connector
from tkinter import ttk, messagebox
from tkinter import *

def verify_login(username, password):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="pythondatabase"
    )


# ------------------------------------ Query the database to check if the username and password match ---------------------------------
    mycursor = mydb.cursor()
    query = "SELECT * FROM users WHERE username = %s AND password = %s"
    mycursor.execute(query, (username, password))
    result = mycursor.fetchone()

    mycursor.close()
    mydb.close()

    if result:
        return True
    else:
        return False

#-------------------------------------------------------- Main program ----------------------------------------------------------------

def mainprogram():
    global listBox
    root = tk.Tk()
    root.geometry("800x500") 
    root.title('Student registration')


    global e1,e2,e3,e4

    tk.Label(root, text="Student Registation", fg="red", font=('Arial', 30)).place(x=300, y=5)
    tk.Label(root, text="ID").place(x=10, y=10)
    Label(root, text="Course").place(x=10, y=40)
    Label(root, text="Name").place(x=10, y=70)
    Label(root, text="Year").place(x=10, y=100)

    e1 = Entry(root)
    e1.place(x=140, y=10)

    e2 = Entry(root)
    e2.place(x=140, y=40)

    e3 = Entry(root)
    e3.place(x=140, y=70)

    e4 = Entry(root)
    e4.place(x=140, y=100)

    Button(root, text="Add",command = Add,height=3, width= 13).place(x=30, y=130)
    Button(root, text="update",command = update,height=3, width= 13).place(x=140, y=130)
    Button(root, text="Delete",command = delete,height=3, width= 13).place(x=250, y=130)
    Button(root, text="Search", command=search, height=3, width=13).place(x=360, y=130)

    cols = ('id', 'course', 'name','year')
    listBox = ttk.Treeview(root, columns=cols, show='headings' )
    for col in cols:
        listBox.heading(col, text=col)
        listBox.grid(row=1, column=0, columnspan=2)
        listBox.place(x=10, y=200)
    show()
    listBox.bind('<Double-Button-1>',GetValue)

    root.mainloop()

# ----------------------------------------------------- Attempting to login -----------------------------------------------------------

def login_attempt():
    username = username_entry.get()
    password = password_entry.get()

    if verify_login(username, password):
        print("Login successful")
        login_window.destroy()
        mainprogram()
    else:
        print("Invalid username or password")

def GetValue(event):
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)
    e4.delete(0, END)
    row_id = listBox.selection()[0]
    select = listBox.set(row_id)
    e1.insert(0,select['id'])
    e2.insert(0,select['course'])
    e3.insert(0,select['name'])
    e4.insert(0,select['year'])

# ------------------------------------------------------------------ Adding --------------------------------------------------------------------

def Add():
    studid = e1.get()
    studname = e2.get()
    coursename = e3.get()
    feee = e4.get()
    mysqldb=mysql.connector.connect(host="localhost",
                                    user="root",
                                    password="1234",
                                    database="pythondatabase")
    mycursor=mysqldb.cursor()
    try:
        sql = "INSERT INTO  people (id,course,name,year) VALUES (%s, %s, %s, %s)"
        val = (studid,studname,coursename,feee)
        mycursor.execute(sql, val)
        mysqldb.commit()
        lastid = mycursor.lastrowid
        messagebox.showinfo("information", "Employee inserted successfully...")
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)
        e1.focus_set()
        show()
    except Exception as e:
        print(e)
        mysqldb.rollback()
        mysqldb.close()

# ----------------------------------------------------------- Update ------------------------------------------------------------------------------

def update():
    studid = e1.get()
    studname = e2.get()
    coursename = e3.get()
    feee = e4.get()
    mysqldb=mysql.connector.connect(host="localhost",
                                    user="root",
                                    password="1234",
                                    database="pythondatabase")
    mycursor=mysqldb.cursor()
    try:
        sql = "Update  people set course= %s,name= %s,year= %s where id= %s"
        val = (studname,coursename,feee,studid)
        mycursor.execute(sql, val)
        mysqldb.commit()
        lastid = mycursor.lastrowid
        messagebox.showinfo("information", "Record Updateddddd successfully...")
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)
        e1.focus_set()
        show()
    except Exception as e:
        print(e)
        mysqldb.rollback()
        mysqldb.close()

# ---------------------------------------------------------------- delete -------------------------------------------------------------------------

def delete():
    studid = e1.get()
    mysqldb=mysql.connector.connect(host="localhost",
                                    user="root",
                                    password="1234",
                                    database="pythondatabase")
    mycursor=mysqldb.cursor()
    try:
        sql = "delete from people where id = %s"
        val = (studid,)
        mycursor.execute(sql, val)
        mysqldb.commit()
        lastid = mycursor.lastrowid
        messagebox.showinfo("information", "Record Deleteeeee successfully...")
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)
        e1.focus_set()
        show()
    except Exception as e:
        print(e)
        mysqldb.rollback()
        mysqldb.close()
#--------------------------------------------------------------------- Search ------------------------------------------------------------------------

def search():
    id = e1.get()
    if not id:
        messagebox.showerror("Error", "Please enter ID number to search.")
        return
    
    mysqldb = mysql.connector.connect(host="localhost", user="root", password="1234", database="pythondatabase")
    mycursor = mysqldb.cursor()
    try:
        mycursor.execute("SELECT id, name, course, year FROM people WHERE id = %s", (id,))
        record = mycursor.fetchone()
        if record:
            e1.delete(0, END)
            e2.delete(0, END)
            e3.delete(0, END)
            e4.delete(0, END)
            e1.insert(0, record[0])
            e2.insert(0, record[1])
            e3.insert(0, record[2])
            e4.insert(0, record[3])
        else:
            messagebox.showinfo("Information", "No record found with ID number: {}".format(id))
    except Exception as e:
        print(e)
        messagebox.showerror("Error", "An error occurred while searching.")
    finally:
        mysqldb.close()


# -------------------------------------------------------------------- show -----------------------------------------------------------------------

def show():
    mysqldb = mysql.connector.connect(host="localhost", 
                                        user="root", 
                                        password="1234", 
                                        database="pythondatabase")
    for record in listBox.get_children():
        listBox.delete(record)
                
    mycursor = mysqldb.cursor()
    mycursor.execute("SELECT id,course,name,year FROM people")
    records = mycursor.fetchall()
    print(records)
    for i, (id,stname, course,fee) in enumerate(records, start=1):
        listBox.insert("", "end", values=(id, stname, course, fee))
        mysqldb.close()

#------------------------------------------------------------------ Window ------------------------------------------------------------------------

login_window = tk.Tk()
login_window.title("DBMS login Page")
login_window.geometry("300x200")

tk.Label(login_window, text="Username").pack()
username_entry = tk.Entry(login_window)
username_entry.pack()

tk.Label(login_window, text="Password").pack()
password_entry = tk.Entry(login_window, show="*")
password_entry.pack()

login_button = tk.Button(login_window, text="Login", command=login_attempt)
login_button.pack()

tk.mainloop()
