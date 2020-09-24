"""
Sign-Up & Log-In V1
Python & SQLite
Developer: Hesham Saeed
Date: 1 September, 2020

What can this app do?
- The user can register specific data to become a member of our site.
- This data will be recorded in the database.
- The registered user can log-in the site by typing his code and password.

specific data: (First Name - Last Name - #code - #Password - Adress - Age)
code :- Generate Random Code For Every User As Id."""

import sqlite3
import string
import random
import time
# ============================================================================ #
# Create Database & Tables
db = sqlite3.connect("app.db")

cr = db.cursor()

cr.execute("""
CREATE TABLE IF NOT EXISTS 
members(fname TEXT NOT NULL, lname TEXT NOT NULL, adress TEXT, age INTEGER NOT NULL,
code TEXT PRIMARY KEY NOT NULL, password TEXT NOT NULL)""")


def c_c():
    """"C_C Fuction For Save All And Close Database"""
    db.commit()
    db.close()


def gen_code():
    """This Function Do: Generate Random Code From [A-z0-9]"""
    all_chars_degits = string.ascii_letters + string.digits
    code = ""
    while len(code) < 10:
        code += all_chars_degits[random.randint(0, 61)]
    return code


# ============================================================================ #
# Create Welcome Message & Our Commands
print("""-------------------------------------------------
Hello Gust!
For Sign-Up Please Write => (sign-up or sign or s or 1).
For Log-In Please Write  => (log-in or log or l or 2).
Thanks!
-------------------------------------------------""")

# User Input Command & Our Commands
user_input = input("Write Here: ").strip().lower()
sign_commands = ["sign-up", "sign", "s", "1"]
log_commands = ["log-in", "log", "l", "2"]
# ============================================================================ #


def sign_up():
    """This Function Do: Add Member To Our Database And Check Some Rules"""
    print("-" * 50)
    # Input [1]
    u_fname = input("Enter First Name: ").strip().lower()
    u_lname = input("Enter Last Name: ").strip().lower()

    # Check [1]
    if len(u_fname) == 0 or len(u_fname) > 20 or len(u_lname) == 0 or len(u_lname) > 20:
        print("Please Enter Your Name As Real Name, \nFirst Name = ", end="")
        print("Limit With 20 Characters And Last Name = Limit With20 Characters")
    else:
        # Input [2]
        u_adress = input("Enter Adress: ").strip().lower()
        u_age = int(input("Enter Age: "))
        # Check [2]
        if u_age < 18 or u_age > 90:
            print("You Must Be From 18 To 90 Years")
        else:
            # Input [3] Form Code Generator Fuction
            u_code = gen_code()
            cr.execute(f"SELECT code FROM members WHERE code = '{u_code}'")
            s_code = cr.fetchone()
            # Check [3] Loop To Get Uniq Code
            while s_code is not None:
                u_code = gen_code()
                cr.execute(f"SELECT code FROM members WHERE code = '{u_code}'")
                s_code = cr.fetchone()
            # Input [4]
            u_pass = input("Enter Password: ").strip()
            # Check [4]
            if len(u_pass) >= 8 and len(u_pass) <= 24:
                # [Final] Insert If All Rules Is Good
                cr.execute(
                    "INSERT INTO members VALUES(?, ?, ?, ?, ?, ?)",
                    (u_fname, u_lname, u_adress, u_age, u_code, u_pass)
                )
                # Print The Data As Writer [Nice One!]
                print("-" * 50)
                txt1 = f"Name: {u_fname.capitalize()} {u_lname.capitalize()}\n"
                txt2 = f"Addres: {u_adress.capitalize()}\nAge: {u_age} Year\n"
                txt3 = f"Your Code: {u_code}\nYour Password: {u_pass}\n"
                txt4 = f"Thank You {u_fname.capitalize()} For Sign-Up!\n"
                all_txt = txt1 + txt2 + txt3 + txt4
                for i in all_txt:
                    print(i, end="", flush=True)
                    time.sleep(0.1)
                print("-" * 50)
            else:
                print("Password Must Be From 8 To 24 No Less No More!")
    c_c()


def log_in():
    """This Function Do: Log-In Member To Our App And Check Some Rules"""
    # Input [1]
    u_code = input("Enter Code: ").strip()
    u_pass = input("Enter Password: ").strip()
    # Fetch Code
    cr.execute(
        f"SELECT code FROM members WHERE code = '{u_code}' AND password = '{u_pass}'")
    fetch_code = cr.fetchone()
    # Check [1]
    if fetch_code is not None:
        cr.execute(f"SELECT * FROM members WHERE code = '{u_code}'")
        fetch_all_data = cr.fetchone()
        # Print The Data As Writer [Nice One!]
        print("-" * 50)
        txt0 = "<--Your Profile-->\n"
        txt1 = f"Welcome {fetch_all_data[0].capitalize()} {fetch_all_data[1].capitalize()}.\n"
        txt2 = f"Live In {fetch_all_data[2].upper()}.\n"
        txt3 = f"Age Is {fetch_all_data[3]} Year.\n"
        all_txt = txt0 + txt1 + txt2 + txt3
        for i in all_txt:
            print(i, end="", flush=True)
            time.sleep(0.1)
        print("-" * 50)
    else:
        print("You Are Haker Or What ! Go Away :)")
    c_c()


# ============================================================================ #
# Check User-Command
if user_input in sign_commands:  # For Sign-Up

    sign_up()


elif user_input in log_commands:  # For Log-In

    log_in()


# For False Input
else:
    print("-" * 50)
    print("Please Focus And Enter A Real Command !")
    print("Our Command For Sign-Up => ", sign_commands)
    print("Our Command For Log-In => ", log_commands)
    print("-" * 50)
    c_c()
