import sqlite3
from employee import Employee

# Creating a connection
conn = sqlite3.connect("employee.db")

# Creating a cursor to excute our commands
c = conn.cursor()

# Creating a table where we eill save the data, use "CREATE TABLE " then the name and then the values
c.execute(""" CREATE TABLE employee (
    first text,
    last text,
    pay intger
)
""")

emp_1 = Employee("me", "he", 3000)
emp_2 = Employee("you", "she", 4000)

# Adding a value to the table, this is one way to give it arguments
c.execute(" INSERT INTO employee VALUES (?, ?, ?)",
          (emp_1.first, emp_1.last, emp_1.pay))
conn.commit()

# # This is the second way to give a database some arguments
c.execute(" INSERT INTO employee VALUES (:first, :last, :pay)", {
          "first": emp_1.first, "last": emp_1.last, "pay": emp_1.pay})
conn.commit()

# Finding a value in the table, we can iterate it
c.execute(" SELECT * FROM employee WHERE last=?", (emp_1.last,))
c.execute(" SELECT * FROM employee WHERE last=:last", {"last": emp_1.last})

print(c.fetchall())


# Committing the changes
conn.commit()

# Closing the connection
conn.close()
