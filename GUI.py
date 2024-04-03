# Imports
import os
import random
import string
from tkinter import *

# Main Screen
master = Tk()
master.title('FinTrack')


# Functions

def generate_password(length=12):
    small_alphabets = string.ascii_lowercase
    capital_alphabets = string.ascii_uppercase
    numbers = string.digits
    special_characters = string.punctuation

    all_characters = small_alphabets + capital_alphabets + numbers + special_characters

    password = ''
    for i in range(length):
        password += random.choice(all_characters)

    notif.config(fg="green", text="Generated Password " + password)


def finish_register():
    name = temp_name.get()
    surname = temp_surname.get()
    mobile = temp_mobile.get()
    password = temp_password.get()
    reg_deposit = temp_deposit.get()
    all_accounts = os.listdir()

    if name == "" or surname == "" or mobile == "":
        notif.config(fg="red", text="All fields required * ")
        return

    for name_check in all_accounts:
        if name == name_check:
            notif.config(fg="red", text="Account already exists")
            return
        else:
            new_file = open(name, "w")
            new_file.write(name + '\n')
            new_file.write(surname + '\n')
            new_file.write(mobile + '\n')
            new_file.write(password + '\n')
            new_file.write(reg_deposit)
            new_file.write('\nDeposit: R' + reg_deposit)
            new_file.close()
            notif.config(fg="green", text="Account has been created")


def register():
    # Vars
    global temp_name
    global temp_surname
    global temp_mobile
    global temp_password
    global temp_deposit
    global notif
    temp_name = StringVar()
    temp_surname = StringVar()
    temp_mobile = StringVar()
    temp_password = StringVar()
    temp_deposit = StringVar()

    # Register Screen
    register_screen = Toplevel(master)
    register_screen.title('Register')

    # Labels
    Label(register_screen, text="Please enter your details below to register", font=('Arial', 12)).grid(row=0,
                                                                                                        sticky=N,
                                                                                                        pady=10)
    Label(register_screen, text="Name", font=('Arial', 12)).grid(row=1, sticky=W)
    Label(register_screen, text="Surname", font=('Arial', 12)).grid(row=2, sticky=W)
    Label(register_screen, text="Mobile", font=('Arial', 12)).grid(row=3, sticky=W)
    Label(register_screen, text="Password", font=('Arial', 12)).grid(row=4, sticky=W)
    Label(register_screen, text="Deposit", font=('Arial', 12)).grid(row=6, sticky=W)
    notif = Label(register_screen, font=('Arial', 12))
    notif.grid(row=7, sticky=N, pady=10)

    # Entries
    Entry(register_screen, textvariable=temp_name).grid(row=1, column=0)
    Entry(register_screen, textvariable=temp_surname).grid(row=2, column=0)
    Entry(register_screen, textvariable=temp_mobile).grid(row=3, column=0)
    Entry(register_screen, textvariable=temp_password).grid(row=4, column=0)
    Entry(register_screen, textvariable=temp_deposit).grid(row=6, column=0)

    # Buttons
    Button(register_screen, text="Generate Password", command=generate_password, font=('Arial', 12)).grid(row=5,
                                                                                                          sticky=N,
                                                                                                          pady=10)
    Button(register_screen, text="Register", command=finish_register, font=('Arial', 12)).grid(row=8,
                                                                                               sticky=N,
                                                                                               pady=10)


def login_session():
    global login_name
    all_accounts = os.listdir()
    login_name = temp_login_name.get()
    login_password = temp_login_password.get()

    for name in all_accounts:
        if name == login_name:
            file = open(name, "r")
            file_data = file.read()
            file_data = file_data.split('\n')
            password = file_data[3]

            # Account Dashboard
            if login_password == password:
                login_screen.destroy()
                account_dashboard = Toplevel(master)
                account_dashboard.title('Dashboard')

                # Labels
                Label(account_dashboard, text="Account Dashboard", font=('Arial', 12)).grid(row=0, sticky=N, pady=10)
                Label(account_dashboard, text="Welcome " + name, font=('Arial', 12)).grid(row=1, sticky=N, pady=5)

                # Buttons
                Button(account_dashboard, text="Personal Details", font=('Arial', 12), width=30,
                       command=personal_details).grid(row=2, sticky=N, padx=10)
                Button(account_dashboard, text="Deposit", font=('Arial', 12), width=30, command=deposit).grid(row=3,
                                                                                                              sticky=N,
                                                                                                              padx=10,
                                                                                                              pady=5)
                Button(account_dashboard, text="Withdraw", font=('Arial', 12), width=30, command=withdraw).grid(row=4,
                                                                                                                sticky=N,
                                                                                                                padx=10,
                                                                                                                pady=5)

                Button(account_dashboard, text="Balance", font=('Arial', 12), width=30, command=view_balance).grid(
                    row=5, sticky=N, padx=10, pady=5)
                Button(account_dashboard, text="Statement", font=('Arial', 12), width=30,
                       command=view_statement).grid(row=6, sticky=N, padx=10)
                Label(account_dashboard).grid(row=7, sticky=N, pady=10)
                return
            else:
                login_notif.config(fg="red", text="Password incorrect!!")
                return
    login_notif.config(fg="red", text="No account found !!")


def deposit():
    # Vars
    global amount
    global deposit_notif
    global current_balance_label

    amount = StringVar()

    file = open(login_name, "r")
    file_data = file.read()
    user_details = file_data.split('\n')
    details_balance = user_details[4]

    # Deposit Screen
    deposit_screen = Toplevel(master)
    deposit_screen.title('Deposit')

    # Label
    Label(deposit_screen, text="Deposit", font=('Arial', 12)).grid(row=0, sticky=N, pady=10)
    current_balance_label = Label(deposit_screen, text="Current Balance: R" + details_balance, font=('Arial', 12))
    current_balance_label.grid(row=1, sticky=W)
    Label(deposit_screen, text="Amount", font=('Arial', 12)).grid(row=2, sticky=W)
    deposit_notif = Label(deposit_screen, font=('Arial', 12))
    deposit_notif.grid(row=4, sticky=N, pady=5)

    # Entry
    Entry(deposit_screen, textvariable=amount).grid(row=2, column=1)

    # Button
    Button(deposit_screen, text="Deposit", font=('Arial', 12), command=finish_deposit).grid(row=3, sticky=W, pady=5)


def finish_deposit():
    if amount.get() == "":
        deposit_notif.config(text='Amount is required!', fg="red")
        return
    if float(amount.get()) <= 0:
        deposit_notif.config(text='Negative currency is not accepted', fg='red')
        return

    file = open(login_name, 'r+')
    file_data = file.read()
    user_details = file_data.split('\n')
    current_balance = user_details[4]
    updated_balance = current_balance
    updated_balance = float(updated_balance) + float(amount.get())
    file_data = file_data.replace(current_balance, str(updated_balance))
    file_data += '\nDeposit: R' + amount.get()

    file.seek(0)
    file.truncate(0)
    file.write(file_data)
    file.close()

    current_balance_label.config(text="Current Balance: R" + str(updated_balance), fg="green")
    deposit_notif.config(text='Balance Updated', fg='green')


def withdraw():
    # Vars
    global withdraw_amount
    global withdraw_notif
    global current_balance_label
    withdraw_amount = StringVar()

    file = open(login_name, "r")
    file_data = file.read()
    user_details = file_data.split('\n')
    details_balance = user_details[4]
    file_data += '\nWithdraw: R' + withdraw_amount.get()

    # Deposit Screen
    withdraw_screen = Toplevel(master)
    withdraw_screen.title('Withdraw')

    # Label
    Label(withdraw_screen, text="Withdraw", font=('Arial', 12)).grid(row=0, sticky=N, pady=10)
    current_balance_label = Label(withdraw_screen, text="Current Balance: R" + details_balance, font=('Arial', 12))
    current_balance_label.grid(row=1, sticky=W)
    Label(withdraw_screen, text="Amount", font=('Arial', 12)).grid(row=2, sticky=W)
    withdraw_notif = Label(withdraw_screen, font=('Arial', 12))
    withdraw_notif.grid(row=4, sticky=N, pady=5)

    # Entry
    Entry(withdraw_screen, textvariable=withdraw_amount).grid(row=2, column=1)

    # Button
    Button(withdraw_screen, text="Withdraw", font=('Arial', 12), command=finish_withdraw).grid(row=3, sticky=W, pady=5)


def finish_withdraw():
    if withdraw_amount.get() == "":
        withdraw_notif.config(text='Amount is required!', fg="red")
        return
    if float(withdraw_amount.get()) <= 0:
        withdraw_notif.config(text='Negative currency is not accepted', fg='red')
        return

    file = open(login_name, 'r+')
    file_data = file.read()
    details = file_data.split('\n')
    current_balance = details[4]

    if float(withdraw_amount.get()) > float(current_balance):
        withdraw_notif.config(text='Insufficient Funds!', fg='red')
        return

    updated_balance = float(current_balance) - float(withdraw_amount.get())
    file_data = file_data.replace(current_balance, str(updated_balance))
    file_data += '\nWithdraw: R' + withdraw_amount.get()  # Append withdrawal transaction to file

    file.seek(0)
    file.truncate(0)
    file.write(file_data)
    file.close()

    current_balance_label.config(text="Current Balance: R" + str(updated_balance), fg="green")
    withdraw_notif.config(text='Balance Updated', fg='green')


def view_balance():
    file = open(login_name, 'r')
    file_data = file.read()
    user_details = file_data.split('\n')
    balance = user_details[4]
    file.close()

    balance_screen = Toplevel(master)
    balance_screen.title('Balance')
    Label(balance_screen, text="Your current balance is: R" + balance, font=('Arial', 12)).pack()

def view_statement():
    file_name = login_name

    with open(file_name, 'r') as file:  # Use with statement to close file automatically
        file_data = file.read()
        details = file_data.splitlines()  # Use splitlines() to avoid empty lines

    # Statement Screen
    statement_screen = Toplevel(master)
    statement_screen.title('Statement')

    if len(details) > 5:
        transactions = details[5:]  # Get the transaction history
        transactions = [transaction for transaction in transactions if transaction.strip()]  # Remove empty transactions
    else:
        transactions = []  # No transactions available

    if transactions:  # Check if transactions list is not empty
        for transaction in transactions:
            if transaction.startswith("Deposit"):
                Label(statement_screen, text='Credited Amount: ' + transaction.split()[1],
                      font=('Arial', 12)).pack()  # Use pack() and split() to display amount
            elif transaction.startswith("Withdraw"):
                Label(statement_screen, text='Debited Amount: ' + transaction.split()[1],
                      font=('Arial', 12)).pack()
    else:
        Label(statement_screen, text='No transaction history available.',
              font=('Arial', 12)).pack()
    os.system(file_name)


def personal_details():
    # Vars
    file = open(login_name, 'r')
    file_data = file.read()
    user_details = file_data.split('\n')
    details_name = user_details[0]
    details_surname = user_details[1]
    details_mobile = user_details[2]
    details_password = user_details[3]
    details_balance = user_details[4]

    # Personal details screen
    personal_details_screen = Toplevel(master)
    personal_details_screen.title('Personal Details')

    # Labels
    Label(personal_details_screen, text="Personal Details", font=('Arial', 12)).grid(row=0, sticky=N, pady=10)
    Label(personal_details_screen, text="Name: " + details_name, font=('Arial', 12)).grid(row=1, sticky=W)
    Label(personal_details_screen, text="Surname: " + details_surname, font=('Arial', 12)).grid(row=2, sticky=W)
    Label(personal_details_screen, text="Mobile: " + details_mobile, font=('Arial', 12)).grid(row=3, sticky=W)
    Label(personal_details_screen, text="Password: " + details_password, font=('Arial', 12)).grid(row=4, sticky=W)
    Label(personal_details_screen, text="Balance: R" + details_balance, font=('Arial', 12)).grid(row=5, sticky=W)


def login():
    # Vars
    global temp_login_name
    global temp_login_password
    global login_notif
    global login_screen
    temp_login_name = StringVar()
    temp_login_password = StringVar()

    # Login Screen
    login_screen = Toplevel(master)
    login_screen.title('Login')

    # Labels
    Label(login_screen, text="Login to your account", font=('Arial', 12)).grid(row=0, sticky=N, pady=10)
    Label(login_screen, text="Name", font=('Arial', 12)).grid(row=1, sticky=W)
    Label(login_screen, text="Password", font=('Arial', 12)).grid(row=2, sticky=W)
    login_notif = Label(login_screen, font=('Arial', 12))
    login_notif.grid(row=4, sticky=N)

    # Entry
    Entry(login_screen, textvariable=temp_login_name).grid(row=1, column=1, padx=5)
    Entry(login_screen, textvariable=temp_login_password, show="*").grid(row=2, column=1, padx=5)

    # Button
    Button(login_screen, text="Login", command=login_session, width=15, font=('Arial', 12)).grid(row=3, column=1,
                                                                                                 sticky=W, pady=5,
                                                                                                 padx=5)


# Labels
Label(master, text="FinTrack Bank", font=('Arial', 14)).grid(row=0, sticky=N, pady=10)
Label(master, text="You'll never walk alone!", font=('Arial', 13)).grid(row=1, sticky=N)

# Buttons
Button(master, text="Register", font=('Arial', 12), width=20, command=register).grid(row=3, sticky=N)
Button(master, text="Login", font=('Arial', 12), width=20, command=login).grid(row=4, sticky=N, pady=10)

master.mainloop()
