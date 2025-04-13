import psycopg2
import csv
import pandas as pd
from tabulate import tabulate 

conn = psycopg2.connect(host="localhost", dbname = "lab10", user = "postgres", password = "1",port=5432)

cur = conn.cursor()

check = True
command = ''
temp = ''

name_var = ''
surname_var = ''
phone_var = ''
id_var = ''

start = True
back = True

name_upd = ''
surname_upd = ''
phone_upd = ''

filepath = ''

while check:
    print("""
1. "i" or "I" = INSERT
2. "u" or "U" = UPDATE 
3. "q" or "Q" = QUERY 
4. "d" or "D" = DELETE 
5. "c" or "C" = CLOSE
6. "s" or "S" = SEE table.
    """)
    command = str(input())
    
    if command == "i" or command == "I":
        print('"csv" upload csv file or "con" typing from console: ')
        command = ''
        temp = str(input())
        if temp == "con":
            name_var = str(input("Name: "))
            surname_var = str(input("Surname: "))
            phone_var = str(input("Phone: "))
            cur.execute("INSERT INTO phonebook (name, surname, phone) VALUES (%s, %s, %s)", (name_var, surname_var, phone_var))
            conn.commit()


        if temp == "csv":
            filepath = input("Enter a file path with proper extension: ")
            with open(str(filepath), 'r') as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    cur.execute("INSERT INTO phonebook (name, surname, phone) VALUES (%s, %s, %s)", (row[0], row[1], row[2]))
            conn.commit()   


    if command == "d" or command == "D":
        command = ''
        idd = str(input('"name" or "phone": '))
        if idd == "name":
            name = str(input("name that you want to delete: "))
            cur.execute("DELETE FROM phonebook WHERE name = %s", (name,))
            conn.commit()
        if idd == "phone":
            phone = str(input("phone that you want to delete: "))
            cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
            conn.commit()
    

    if command == 'u' or command == 'U':
        command = ''
        temp = str(input('"name", "surname" or "phone": '))
        if temp == "name":
            name_var = str(input("name that you want to change: "))
            name_upd = str(input("new name: "))
            cur.execute("UPDATE phonebook SET name = %s WHERE name = %s", (name_upd, name_var))
            conn.commit()

        if temp == "surname":
            surname_var = str(input("surname that you want to change: "))
            surname_upd = str(input("new surname: "))
            cur.execute("UPDATE phonebook SET surname = %s WHERE surname = %s", (surname_upd, surname_var))
            conn.commit()

        if temp == "phone":
            phone_var = str(input("phone number that you want to change: "))
            phone_upd = str(input("new phone number: "))
            cur.execute("UPDATE phonebook SET phone = %s WHERE phone = %s", (phone_upd, phone_var))
            conn.commit()

    if command == "q" or command == "Q":
        command = ''
        temp = str(input('"id", "name", "surname" or "phone": '))
        if temp == "id":
            id_var = str(input("id of the user: "))
            cur.execute("SELECT * FROM phonebook WHERE user_id = %s", (id_var, ))
            rows = cur.fetchall()
            print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"]))
                
        if temp == "name":
            name_var = str(input("name of the user: "))
            cur.execute("SELECT * FROM phonebook WHERE name = %s", (name_var, ))
            rows = cur.fetchall()
            print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"]))
        
        if temp == "surname":
            surname_var = str(input("surname of the user: "))
            cur.execute("SELECT * FROM phonebook WHERE surname = %s", (surname_var, ))
            rows = cur.fetchall()
            print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"]))
            
            
        if temp == "phone":
            phone_var = str(input("phone number of the user: "))
            cur.execute("SELECT * FROM phonebook WHERE phone = %s", (phone_var, ))
            rows = cur.fetchall()
            print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"]))

    
    if command == "s" or command == "S":
        command = ''
        cur.execute("SELECT * from phonebook;")
        rows = cur.fetchall()
        print(tabulate(rows, headers=["ID", "Name", "Surname", "Phone"], tablefmt='fancy_grid'))

    if command == "c" or command == "C":
        command = ''
        check = False
        

conn.commit()
cur.close()
conn.close()