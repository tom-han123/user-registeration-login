import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
import csv
import pyodbc

class Signin(QMainWindow):
    def __init__(self):
        super(Signin, self).__init__()
        loadUi("signin.ui", self)
        self.loginbtn.clicked.connect(self.login_function)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signup.clicked.connect(self.to_signup)
        self.label_1 = QtWidgets.QLabel(self)
        self.label_1.move(220, 300)
        self.label_1.setStyleSheet("color:#fff;font-size:12px;")

    #CSV
    # def login_function(self):
    #     email = self.email.text()
    #     password = self.password.text()
    #     if email != "" and password != "":
    #         self.label_1.setText("")
    #         datasets = {}
    #         with open('user.csv', 'r') as f:
    #             csvreader = csv.reader(f)
    #             for row in csvreader:
    #                 datasets[row[0]] = row[1]
    #
    #         if email in datasets.keys():
    #             if datasets[email] == password:
    #                 print('Welcome ' + email)
    #             else:
    #                 self.label_1.setText("Incorrect Password!")
    #                 self.label_1.adjustSize()
    #         else:
    #             self.label_1.setText("User doesn\'t exist!")
    #             self.label_1.adjustSize()
    #     else:
    #         self.label_1.setText(" Please fill the form!")
    #         self.label_1.adjustSize()

    #Microsoft SQL Server
    def login_function(self):
        email = self.email.text()
        password = self.password.text()

        con_str = ("Driver={SQL Server};"
                   "Server=DESKTOP-5SPMEFM;"
                   "Database=authentication_db;"
                   "Trusted_Connection=yes;")
        query1 = 'SELECT email, password FROM user_registeration WHERE email=\'' + email + '\';'

        if email != "" and password != "":
            self.label_1.setText("")
            with pyodbc.connect(con_str) as con1:
                cursor1 = con1.cursor()
                cursor1.execute(query1)
                value = cursor1.fetchall()

            if value:
                if value[0][1] == password:
                    print('Welcome ' + email)
                else:
                    self.label_1.setText("Incorrect Password!")
                    self.label_1.adjustSize()
            else:
                self.label_1.setText("User doesn\'t exist!")
                self.label_1.adjustSize()
        else:
            self.label_1.setText(" Please fill the form!")
            self.label_1.adjustSize()

    def to_signup(self):
        signup = Signup()
        widget.addWidget(signup)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class Signup(QMainWindow):
    def __init__(self):
        super(Signup, self).__init__()
        loadUi("signup.ui", self)
        self.signupbtn.clicked.connect(self.signup_function)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confrim_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signin.clicked.connect(self.to_signin)
        self.label_1 = QtWidgets.QLabel(self)
        self.label_1.move(250, 210)
        self.label_1.setStyleSheet("color:#fff;font-size:12px;")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.move(190, 390)
        self.label_2.setStyleSheet("color:#fff;font-size:12px;")

    #CSV
    # def signup_function(self):
    #     email = self.email.text()
    #     password = self.password.text()
    #     con_pass = self.confrim_password.text()
    #     if email is None or password == "" or con_pass == "":
    #         self.label_1.setText("")
    #         self.label_2.setText("")
    #         self.label_2.setText(" Please fill the form!")
    #         self.label_2.adjustSize()
    #     elif email.count("@gmail.com") == 1:
    #         if password == con_pass:
    #             self.label_1.setText("")
    #             datasets = {}
    #             with open('user.csv', 'r') as f:
    #                 csvreader = csv.reader(f)
    #                 for row in csvreader:
    #                     datasets[row[0]] = row[1]
    #             if email in datasets.keys():
    #                 self.label_1.setText("Email already exist!")
    #                 self.label_1.adjustSize()
    #             else:
    #                 with open('user.csv', 'a', newline='\n') as f:
    #                     writer = csv.writer(f)
    #                     writer.writerow((email, password))
    #                 print("Successfully logged in with email: ", email, "and password:", password)
    #         else:
    #             self.label_1.setText("")
    #             self.label_2.setText("The two password doesn\'t match each other!")
    #             self.label_2.adjustSize()
    #     else:
    #         self.label_1.setText("Invalid Email Address!")
    #         self.label_1.adjustSize()

    def signup_function(self):
        email = self.email.text()
        password = self.password.text()
        con_pass = self.confrim_password.text()
        if email is None or password == "" or con_pass == "":
            self.label_1.setText("")
            self.label_2.setText("")
            self.label_2.setText(" Please fill the form!")
            self.label_2.adjustSize()
        elif email.count("@gmail.com") == 1:
            if password == con_pass:
                self.label_1.setText("")
                con_str = ("Driver={SQL Server};"
                           "Server=DESKTOP-5SPMEFM;"
                           "Database=authentication_db;"
                           "Trusted_Connection=yes;")
                query = 'INSERT INTO user_registeration(email, password) VALUES(?, ?)'

                query1 = 'SELECT * FROM user_registeration WHERE email=\'' + email + '\';'

                with pyodbc.connect(con_str) as con1:
                    cursor1 = con1.cursor()
                    cursor1.execute(query1)
                    data = cursor1.fetchall()

                if data:
                    self.label_1.setText("Email already exist!")
                    self.label_1.adjustSize()
                else:
                    with pyodbc.connect(con_str) as con:
                        cursor = con.cursor()
                        cursor.execute(query, (email, password))
                    print("Successfully logged in with email: ", email, "and password:", password)
            else:
                self.label_1.setText("")
                self.label_2.setText("The two password doesn\'t match each other!")
                self.label_2.adjustSize()
        else:
            self.label_1.setText("Invalid Email Address!")
            self.label_1.adjustSize()

    def to_signin(self):
        signin = Signin()
        widget.addWidget(signin)
        widget.setCurrentIndex(widget.currentIndex() + 1)


app = QApplication(sys.argv)
mainwindow = Signup()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(480)
widget.setFixedHeight(620)
widget.show()
app.exec()