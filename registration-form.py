import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QLineEdit,  QLineEdit, QPushButton,QMessageBox
from PyQt6.QtGui import QFont
import mysql.connector

db = mysql.connector.connect(
host = 'localhost',
user = "root",
password = "vishuofficialpassword",
database = "users")
sql = db.cursor()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.msg = QLabel("YOU HAVE BEEN HACKED :)",self)

class StartWindow(QMainWindow,QLineEdit):
    def __init__(self,sql,db):
        self.sql = sql
        self.db = db

        super().__init__()
        self.setWindowTitle("Registeration Form") #WINDOW TITLE
       
        self.note = QLabel(self)
        self.note.setText("ONLY EMAIL AND PASSWORD ARE REQUIRED FOR SIGN IN")
        self.note.resize(330,30)
        self.note.setStyleSheet('''color:red;
			font-family:Aerial;
			font-size:20;
			font-weight:bold;
 			''')
        self.note.move(600,50)

        self.nameLabel = QLabel("Name",self) #NAME LABEL
        self.nameLabel.setFont(QFont('Aerial',15))
        self.nameLabel.move(500,200)
        self.nameLabel.alignment()

        self.emailLabel = QLabel("Email",self) #EMAIL LABEL
        self.emailLabel.setFont(QFont("Aerial",15))
        self.emailLabel.move(500,275)
        
        self.pwdLabel = QLabel("Password",self) # PASSWORD LABEL
        self.pwdLabel.setFont(QFont("Aerial",15))
        self.pwdLabel.move(500,350)

        self.name = QLineEdit(self) #NAME TEXTBOX
        self.name.resize(250,30)
        self.name.move(700,200)

        self.email = QLineEdit(self) #EMAIL TEXTBOX
        self.email.resize(250,30)
        self.email.move(700,275)

        self.pwd = QLineEdit(self) #PASSWORD TEXTBOX
        self.pwd.setEchoMode(QLineEdit.EchoMode.Password)
        self.pwd.resize(250,30)
        self.pwd.move(700,350)

        self.clear = QPushButton("Clear",self)
        self.clear.setFont(QFont("Aerial",15))
        self.clear.resize(150,50)
        self.clear.move(850,450)
        self.clear.clicked.connect(self.ClearAction)

        self.signup = QPushButton("Sign Up",self)
        self.signup.move(400,450)
        self.signup.setFont(QFont("Aerial",15))
        self.signup.resize(150,50)
        self.signup.clicked.connect(self.SignUpAction)

        self.signin = QPushButton("Sign In",self)
        self.signin.setFont(QFont("Aerial",15))
        self.signin.resize(150,50)
        self.signin.move(623,450)
        self.signin.clicked.connect(self.SignInAction)

    def SignUpAction(self):
        try:
            Input = '''
                    insert into acc_info(name,email,password)
                    values(%s,%s,%s);
                      '''
            val = (self.name.text(),self.email.text(),self.pwd.text())
            self.sql.execute(Input,val)
            self.db.commit()
            SignUpMsg = QMessageBox()
            SignUpMsg.setIcon(QMessageBox.Icon.Information)
            SignUpMsg.setWindowTitle("Done")
            SignUpMsg.setText("Registration Successful!")
            SignUpMsg.setStandardButtons(QMessageBox.StandardButton.Ok)
            SignUpMsg.show()
            SignUpMsg.exec()
            self.name.setText('')
            self.email.setText('')
            self.pwd.setText('')
            
        except mysql.connector.errors.IntegrityError as e:
            SignUpError = QMessageBox()
            SignUpError.setIcon(QMessageBox.Icon.Critical)
            SignUpError.setWindowTitle("Sign Up Error")
            SignUpError.setText("Account already present.")
            SignUpError.setStandardButtons(QMessageBox.StandardButton.Ok)
            SignUpError.show()
            SignUpError.exec()
        finally:
           self.name.setText('')
           self.email.setText('')
           self.pwd.setText('')     
     
    def SignInAction(self):
        val = self.email.text(),
        Input = "select email,password from acc_info where email = %s;"
        self.sql.execute(Input,val)
        dbdata = self.sql.fetchall()
        if self.email.text() == dbdata[0][0] and self.pwd.text() == dbdata[0][1]:
            SignInMsg = QMessageBox()
            SignInMsg.setIcon(QMessageBox.Icon.Information)
            SignInMsg.setWindowTitle("Done")
            SignInMsg.setText("Sign In Successful!")
            SignInMsg.setStandardButtons(QMessageBox.StandardButton.Ok)
            SignInMsg.show()
            SignInMsg.exec()
            self.email.setText('')
            self.pwd.setText('')
            self.AppWin()
        else:
            SignInError = QMessageBox()
            SignInError.setIcon(QMessageBox.Icon.Critical)
            SignInError.setWindowTitle("Sign In Error")
            SignInError.setText("Please check email or password and try again!")
            SignInError.setStandardButtons(QMessageBox.StandardButton.Ok)
            SignInError.show()
            SignInError.exec()
            self.pwd.setText('')

    def AppWin(self):
            self.w = MainWindow()
            self.w.show()
            self.hide()
            
    def ClearAction(self):
        self.name.setText('')
        self.email.setText('')
        self.pwd.setText('')

app = QApplication(sys.argv)
w = StartWindow(sql,db)
w.show()	
app.exec()