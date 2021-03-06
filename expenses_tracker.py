from tkinter import *
import sqlite3
import xlsxwriter
import pandas as pd
import matplotlib.pyplot as plt


from pygame.constants import GL_CONTEXT_PROFILE_COMPATIBILITY


# Creating the database that we are going to work with, and creating the crouser
conn = sqlite3.connect(":memory:")


class DataBase:
    def __init__(self, connection):
        self.conn = connection
        self.c = self.conn.cursor()

    def create_table(self):
        # Creating our table
        self.c.execute("""CREATE TABLE expenses(
            title text,
            amount integer
        )""")

    # A function for adding a new expense to the database
    def add_expens(self, title, amount):
        with self.conn:
            self.c.execute("INSERT INTO expenses VALUES(:name, :amount)", {
                "name": title, "amount": amount})

    # Creating a function for deleting a specific expense from the database
    def delet_expenses(self, title):
        with self.conn:
            self.c.execute("DELET from expenses WHERE title=:title", {
                           "title": title})

    # A function that returns all the database in our database
    def show_expenses(self):
        self.c.execute("SELECT * from expenses")
        return self.c.fetchall()

    def database_to_excell(self):
        # Creating a new excell sheet
        workbook = xlsxwriter.Workbook("Expenses_excel.xlsx")
        worksheet = workbook.add_worksheet()

        # Writing the values from my database to the excel worksheet
        row = 0
        column = 0

        for data in self.show_expenses():
            worksheet.write(row, column, data[0])
            worksheet.write(row, column + 1, data[1])
            row += 1
        workbook.close()


class TkinterWinodw:

    def __init__(self):
        self.root = Tk()
        self.root.geometry("400x500")
        self.title_variable = StringVar()
        self.amoutn_variable = StringVar()
        self.data_base = DataBase(conn)

        self.count = 1

        # Creating the intro label
        self.intro_label = Label(
            self.root, text="Create Expense!", font=("Arial", 20))
        self.intro_label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

        # Creating the expenses title label and entry
        self.expenses_label = Label(
            self.root, text="Expense title", font=("Arial", 10))
        self.expenses_label.grid(row=1, column=0, pady=10, padx=10)

        self.expenses_entry = Entry(
            self.root, textvariable=self.title_variable, width=20, borderwidth=4)
        self.expenses_entry.grid(row=1, column=1, pady=10)

        # Creating the Amount  label and entry
        self.amount_label = Label(
            self.root, text="Amount", font=("Arial", 10))
        self.amount_label.grid(row=2, column=0, pady=10, padx=10)

        self.amount_entry = Entry(
            self.root, textvariable=self.amoutn_variable, width=20, borderwidth=4)
        self.amount_entry.grid(row=2, column=1, pady=10)

        # Creating the add button for adding expense
        self.add_button = Button(
            self.root, text="Add", command=self.add)
        self.add_button.grid(row=3, column=1, pady=10, sticky=E)

        # Creating the show eexpenses button
        self.show_button = Button(
            self.root, text="Show expenses", command=self.show)
        self.show_button.grid(row=3, column=0, padx=10)

        self.root.mainloop()

    def add(self):

        # Getting the expense information
        title = self.expenses_entry.get()
        amount = int(self.amount_entry.get())

        if self.count == 1:
            self.data_base.create_table()

        # Adding it to the data base
        self.data_base.add_expens(title, amount)

        # Emptying the entrys
        self.title_variable.set(" ")
        self.amoutn_variable.set(" ")

        self.count += 1

    def show(self):
        self.root.destroy()

        # Creting another window for displaying the expenses
        window_2 = Tk()
        window_2.geometry("400x500")

        # Getting all the expenses
        expenses = self.data_base.show_expenses()

        # This is to control the rows
        antal_labels = len(expenses)
        rows = 1

        # Creating frames for the labels
        headers_frame = Frame(window_2, bg="blue")
        headers_frame.grid(row=0, column=0, columnspan=2)

        # A frame for the body
        body_frame = Frame(window_2)
        body_frame.grid(row=1, column=0, pady=10)

        # List for my labels
        labels_title = []
        labels_amount = []

        # Creting the titles for each sector
        expenses_label = Label(
            headers_frame, text="Expenses", fg="White", bg="Blue", font=("Arial", 20))
        expenses_label.grid(row=0, column=0, padx=5, pady=5)

        amount_label = Label(headers_frame, text="Amount",
                             fg="White", bg="Blue", font=("Arial", 20))
        amount_label.grid(row=0, column=1, pady=5)

        # displaying the title of the expense
        for expense in expenses:
            label = Label(body_frame, text=expense[0], font=("Arial", 15))
            label.grid(row=rows, column=0, padx=5, pady=5)

            if rows < antal_labels:
                rows += 1

            labels_title.append(label)

        # Reseting the rows
        rows = 1

        for expense in expenses:
            label = Label(body_frame, text=str(
                expense[1]) + " " + "kr", bg="grey", fg="White", font=("Arial", 15))
            label.grid(row=rows, column=1, padx=10)

            if rows < antal_labels:
                rows += 1

            labels_amount.append(label)

        self.data_base.database_to_excell()

        def back():
            window_2.destroy()
            main_window = TkinterWinodw()

        # A button to go back to the start window
        back_button = Button(window_2, text="Back",
                             bg="Grey", command=back)
        back_button.grid(row=2, column=0, sticky=W)

        self.show_graph()

    def show_graph(self):
        df = pd.read_excel(
            "C:\\Users\\abdullrauf.alhariri\\Desktop\\HelloWorld\\Expenses_excel.xlsx", engine="openpyxl")

        df.plot(kind="bar")
        plt.show()


window = TkinterWinodw()
