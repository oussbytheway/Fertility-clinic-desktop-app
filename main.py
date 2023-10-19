import sys
import time
import datetime
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget, QDesktopWidget
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.uic import loadUi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.data_base import Admin, Patient, Rappel, Motifs, Status
from display import Today
from db.import_export import Import, Export


# ?                           User Experience:

def setFont(label, size):
    # Set the font to Roboto with a size of 14
    font = QFont("Segoe UI", size)
    label.setFont(font)


def setButton(list, type):
    colors = ['#87CEFA', '#fba88f', '#D8BFD8', '#98FB98']
    n = 0
    for color in colors:
        if type == 1:
            btn = list[n]
            btn.setStyleSheet(
                "QPushButton{ text-align: center; min-width: 100px; color: #28282b; background:"+f"{color}"+"} QPushButton:hover{ background: #1A1A1A; color: #fefefe;}")
            n = n + 1

        else:
            btn = list[n]
            btn.setStyleSheet(
                "QToolButton{ text-align: center; min-width: 100px; color: #28282b; background:"+f"{color}"+"} QToolButton:hover{ background: #1A1A1A; color: #fefefe;}")
            n = n + 1


def setIcons(logo, admin_pic, home_btn, patients_btn, rappels_btn):

    logo_icon = QPixmap('icons/logo.png')  # logo
    logo_icon = logo_icon.scaled(
        50, 50, QtCore.Qt.KeepAspectRatio)  # logo resized
    logo.setPixmap(logo_icon)  # logo display

    admin_icon = QPixmap('icons/admin.jpg')  # admin picture
    admin_icon = admin_icon.scaled(
        40, 40, QtCore.Qt.KeepAspectRatio)  # admin picture resized
    admin_pic.setPixmap(admin_icon)  # admin picture display

    home_icon = QPixmap('icons/home.png')
    home_icon = QIcon(home_icon)
    home_btn.setIcon(home_icon)
    home_icon_size = QtCore.QSize(
        home_btn.width() - 48, home_btn.height() - 48)
    home_btn.setIconSize(home_icon_size)

    patients_icon = QPixmap('icons/patients.png')
    patients_icon = QIcon(patients_icon)
    patients_btn.setIcon(patients_icon)
    patients_icon_size = QtCore.QSize(
        patients_btn.width() - 48, patients_btn.height() - 48)
    patients_btn.setIconSize(patients_icon_size)

    rappels_icon = QPixmap('icons/rappel.png')
    rappels_icon = QIcon(rappels_icon)
    rappels_btn.setIcon(rappels_icon)
    rappels_icon_size = QtCore.QSize(
        rappels_btn.width() - 48, rappels_btn.height() - 48)
    rappels_btn.setIconSize(rappels_icon_size)


class BackButton():
    def __init__(self, widget):
        window = Home()
        widget.insertWidget(2, window)
        widget.setCurrentIndex(2)


# load the database
engine = create_engine('sqlite:///db/ma_bdd.db', echo=True)

# create a session to access database
Session = sessionmaker(bind=engine)
session = Session()

# auth window, for verifying the admin info


class Authentication(QDialog):
    # main method of Authentication
    def __init__(self):
        super(Authentication, self).__init__()
        loadUi('templates/authentication.ui', self)  # load the auth UI
        # ? UX/UI
        flat = QPixmap('icons/auth_bg.png')
        self.auth_flat.setPixmap(flat)
        setFont(self.auth_title, 20)
        setFont(self.username_label, 8)
        setFont(self.username, 10)
        setFont(self.password_label, 8)
        setFont(self.password, 10)
        setFont(self.auth_btn, 8)
        setFont(self.error, 12)
        self.auth_title.setStyleSheet("color: #000")
        self.username_label.setStyleSheet("color: #000")
        self.password_label.setStyleSheet("color: #000")
        self.error.setStyleSheet("color: #FF0000")
        self.username.setStyleSheet(""" QLineEdit {
                                        color: #000; 
                                        }

                                        QLineEdit:focus {
                                        border: 1px solid #000; 
                                        }""")
        self.password.setStyleSheet(""" QLineEdit {
                                        color: #000; 
                                        }

                                        QLineEdit:focus {
                                        border: 1px solid #000;
                                        }""")

        self.auth_btn.setStyleSheet(""" QPushButton {
                                        background: #28282b;
                                        border: none;
                                        color: #fefefe;
                                        text-align: center;
                                        }
                                        QPushButton:hover {
                                        background: #555;  
                                        }""")
        self.auth_btn.setCursor(QtCore.Qt.PointingHandCursor)

        # mask the password caracters
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)

        # click the button with the Enter key
        self.username.returnPressed.connect(self.auth_btn.click)
        self.password.returnPressed.connect(self.auth_btn.click)
        # connecting the auth button the admin verification function
        self.auth_btn.clicked.connect(self.verify_admin)

    # admin verification function
    def verify_admin(self):
        # ? UI/UX
        self.username.setStyleSheet(""" QLineEdit {
                                        color: #000; 
                                        }

                                        QLineEdit:focus {
                                        border: 1px solid #000; 
                                        }""")
        self.password.setStyleSheet(""" QLineEdit {
                                        color: #000; 
                                        }

                                        QLineEdit:focus {
                                        border: 1px solid #000;
                                        }""")

        username = self.username.text()  # username input
        password = self.password.text()  # password input
        # condition
        if len(username) == 0 or len(password) == 0:  # at leat one input empty
            self.error.setText("Vous avez oublié un champ")
            if len(username) != 0:
                self.password.setStyleSheet("""
                                            QLineEdit{
                                            border: 1px solid #ff0000;
                                            }""")
            elif len(password) != 0:
                self.username.setStyleSheet("""
                                        QLineEdit{
                                        border: 1px solid #ff0000; 
                                        }""")
            else:
                self.username.setStyleSheet("""
                                            QLineEdit{
                                            border: 1px solid #ff0000; 
                                            }""")
                self.password.setStyleSheet("""
                                                QLineEdit{
                                                border: 1px solid #ff0000;
                                                }""")
        else:
            # actual admin info from database
            admin = session.query(Admin).first()
            # actual admin username from row to managable string
            admin_username = str(admin.username)

            if admin_username == username:  # if the input username is compatible with the actual username
                # if the input password is compatible with the actual password
                if password == str(admin.password):
                    self.error.setText(
                        f"Content de vous revoir {admin_username}")  # welcome text
                    # directing the user to click the auth_btn
                    self.auth_btn.setText("Cliquez ici")
                    self.error.setStyleSheet("color: #3d8b3d;")
                    self.username.setStyleSheet("""
                                            QLineEdit{
                                            border: 1px solid #3d8b3d; 
                                            }""")
                    self.password.setStyleSheet("""
                                                    QLineEdit{
                                                    border: 1px solid #3d8b3d;
                                                    }""")
                    self.auth_btn.setStyleSheet(""" QPushButton {
                                    background: #3d8b3d;
                                    color: #1A1A1A;
                                    text-align: center;
                                    }
                                    QPushButton:hover {
                                    background: #3d8b3d;                                 
                                    }""")
                    # connecting the auth_btn to the gotohome function
                    self.auth_btn.clicked.connect(self.gotohome)
                else:
                    self.username.setStyleSheet("""
                                            QLineEdit{
                                            border: 1px solid #98FB98; 
                                            }""")
                    self.password.setStyleSheet("""
                                            QLineEdit{
                                            border: 1px solid #ff0000;
                                            }""")
                    self.error.setText("Mot de passe incorrecte")
            else:
                self.error.setText("Nom d'utilisateur invalide")

    # home widget display function
    def gotohome(self):
        home = Home()  # the home widget class
        widget.addWidget(home)  # adding it to the widgetstack
        # incrementing the stack index, home widget now has the index 1
        widget.setCurrentIndex(widget.currentIndex()+1)


class Home(QDialog):
    def __init__(self):
        super(Home, self).__init__()
        loadUi('templates/home.ui', self)  # load the home UI
        # ? UX/UI
        setFont(self.home_label, 15)
        setFont(self.patient_count, 17)
        setFont(self.p_label, 12)
        setFont(self.rappel_count, 17)
        setFont(self.r_label, 12)
        setFont(self.a_label, 12)
        setFont(self.admin_username, 16)
        setIcons(self.logo, self.admin_pic, self.home_btn,
                 self.patients_btn, self.rappels_btn)
        # Get the user's screen width
        bar_width = app.desktop().availableGeometry().width() - 40
        self.top_bar.setFixedWidth(bar_width)
        bar_height = app.desktop().availableGeometry().height()
        self.side_bar.setFixedHeight(bar_height)
        self.info_box1.move(bar_width - 1100, self.info_box1.y())
        self.info_box2.move(bar_width - 700, self.info_box2.y())
        self.info_box3.move(bar_width - 300, self.info_box3.y())
        self.top_bar_color.setStyleSheet("background: #1A1A1A")
        self.side_bar.setStyleSheet("background: #1A1A1A")
        self.home_btn.setStyleSheet(""" QPushButton {
                                        border: none;
                                        background: #B0E0E6;
                                        }
                                        
                                    """)
        self.patients_btn.setStyleSheet("""
                                        QPushButton {
                                        border: none;
                                        }
                                        QPushButton:hover {
                                        background: #B0E0E6;
                                        }""")
        self.rappels_btn.setStyleSheet("""
                                        QPushButton {
                                        border: none;
                                        }
                                        QPushButton:hover {
                                        background: #B0E0E6;
                                        }""")

        self.home_label.setStyleSheet("color: #fefefe")
        # patient card
        patient_card_icon = QPixmap(
            'icons/patient_card.png')
        patient_card_icon = patient_card_icon.scaled(
            50, 50, QtCore.Qt.KeepAspectRatio)
        self.patient_card_icon.setPixmap(
            patient_card_icon)
        patient_count = session.query(Patient).filter().count()
        self.patient_count.setText(str(patient_count))
        # rappel card
        rappel_card_icon = QPixmap(
            'icons/rappel_card.png')
        rappel_card_icon = rappel_card_icon.scaled(
            60, 60, QtCore.Qt.KeepAspectRatio)
        self.rappel_card_icon.setPixmap(
            rappel_card_icon)
        today = datetime.date.today()
        rappel_count = session.query(Rappel).filter(
            Rappel.date == today).count()
        self.rappel_count.setText(str(rappel_count))
        # admin card
        admin_card_icon = QPixmap(
            'icons/admin_card.png')
        admin_card_icon = admin_card_icon.scaled(
            60, 60, QtCore.Qt.KeepAspectRatio)
        self.admin_card_icon.setPixmap(
            admin_card_icon)

        admin_username = session.query(Admin).first().username
        self.admin_username.setText(str(admin_username))

        # connecting the patients button the patients window display function
        self.patients_btn.clicked.connect(self.gotopatients)
        # connecting the rappels button the rappels window display function
        self.rappels_btn.clicked.connect(self.gotorappels)
        self.display.clicked.connect(self.gototoday)

        # keyboard shortcuts
        self.rappels_btn.setShortcut('Ctrl+r')
        self.patients_btn.setShortcut('Ctrl+p')
        self.display.setShortcut('Alt+r')

    # patients window display function

    def gotopatients(self):
        p = Patients()  # calling the patients class to define widget
        widget.insertWidget(2, p)  # adding it to the stack in index n 2
        widget.setCurrentIndex(2)  # setting current index to 2

    # rappels window display function
    def gotorappels(self):
        r = Rappels()  # calling the rappels class to define widget
        widget.insertWidget(2, r)  # adding it to the stack in index n 3
        widget.setCurrentIndex(2)  # setting current index to 3

    def gototoday(self):

        # create the widget
        window = Today(widget)

        # add the widget to the stack and set it as the current widget
        widget.insertWidget(2, window)
        widget.setCurrentIndex(2)

        # Get the user's screen geometry
        screen_geometry = app.desktop().availableGeometry()

        # Set the widget's geometry to the screen geometry
        widget.setGeometry(screen_geometry)

        time.sleep(0.2)

        widget.showMaximized()  # display


class Patients(QDialog):
    def __init__(self):
        super(Patients, self).__init__()
        loadUi('templates/patients.ui', self)
        # hide create widget
        self.hidden = True
        self.hide_show()

        # ? UX/UI
        setFont(self.home_label, 15)
        setFont(self.patient_label, 15)
        setFont(self.add_label, 15)
        setFont(self.label_1, 13)
        setFont(self.label_2, 13)
        setFont(self.label_3, 13)
        setFont(self.label_4, 13)
        setFont(self.error, 13)
        setFont(self.nom, 12)
        setFont(self.email, 12)
        setFont(self.tel, 12)
        setFont(self.description, 12)
        setFont(self.patients_table, 10)
        btns = [self.create_btn, self.delete_btn,
                self.import_btn, self.export_btn]
        setButton(btns, 2)
        setIcons(self.logo, self.admin_pic, self.home_btn,
                 self.patients_btn, self.rappels_btn)
        back_icon = QPixmap('icons/back.png')
        back_icon = QIcon(back_icon)
        self.cancel_btn.setIcon(back_icon)
        back_icon_size = QtCore.QSize(
            self.cancel_btn.width() - 60, self.cancel_btn.height() - 60)
        self.cancel_btn.setIconSize(back_icon_size)

        # Get the user's screen width
        bar_width = app.desktop().availableGeometry().width() - 40
        self.top_bar.setFixedWidth(bar_width)
        bar_height = app.desktop().availableGeometry().height()
        self.side_bar.setFixedHeight(bar_height)
        self.patients_table.setFixedHeight(bar_height - 210)
        self.patients_table.setFixedWidth(bar_width - 305)
        self.create_bg.setFixedHeight(bar_height - 100)
        self.create_bg.setFixedWidth(bar_width - 100)
        btn_x = self.patients_table.width() + 160
        self.create_btn.move(btn_x, self.create_btn.y() + 50)
        self.delete_btn.move(btn_x, self.delete_btn.y() + 50)
        self.delete_id.move(btn_x, self.delete_id.y() + 50)
        self.import_btn.move(btn_x, self.import_btn.y() + 150)
        self.export_btn.move(btn_x, self.export_btn.y() + 150)
        self.top_bar_color.setStyleSheet("background: #1A1A1A")
        self.side_bar.setStyleSheet("background: #1A1A1A")
        self.home_btn.setStyleSheet(""" QPushButton {
                                        border: none;
                                        }
                                        QPushButton:hover {
                                        background: #B0E0E6;
                                        }
                                    """)
        self.patients_btn.setStyleSheet("""
                                        QPushButton {
                                        border: none;
                                        background: #B0E0E6;
                                        }
                                        """)
        self.rappels_btn.setStyleSheet("""
                                        QPushButton {
                                        border: none;
                                        }
                                        QPushButton:hover {
                                        background: #B0E0E6;
                                        }""")

        self.home_label.setStyleSheet("color: #fefefe;")
        self.add_label.setStyleSheet("color: #000;")
        self.patient_label.setStyleSheet("color: #000;")

        # keyboard shortcuts
        self.home_btn.setShortcut('Ctrl+h')
        self.rappels_btn.setShortcut('Ctrl+r')
        self.cancel_btn.setShortcut('Esc')

        # buttons
        self.home_btn.clicked.connect(self.gotohome)
        self.rappels_btn.clicked.connect(Home.gotorappels)
        self.create_btn.clicked.connect(self.create)
        self.delete_btn.clicked.connect(self.delete)
        self.import_btn.clicked.connect(self.imports)
        self.export_btn.clicked.connect(self.exports)

        # data table
        self.patients_table.setColumnWidth(0, 150)
        self.patients_table.setColumnWidth(1, 180)
        self.patients_table.setColumnWidth(2, 100)
        self.patients_table.setColumnWidth(3, 354)
        self.patients_table.setColumnWidth(4, 120)
        self.patients_table.setColumnWidth(5, 100)
        # patient data fetch from database
        self.loaddata()

    def hide_show(self):

        if self.hidden == True:
            self.create_bg.hide()
        if self.hidden == False:
            self.create_bg.show()

    def loaddata(self):
        patients = []
        row = 0

        query = session.query(Patient).all()  # get all patients data

        # patients data one by one
        for p in query:
            patient = {"nom_complet": p.nom_complet,
                       "email": p.email,
                       "tel": p.tel,
                       "description": p.description,
                       "creation": str(p.created.strftime("%Y-%m-%d %H:%M:%S")),
                       "id": str(p.id)}
            patients.append(patient)

        # filling the table
        self.patients_table.setRowCount(len(patients))
        for patient in patients:
            self.patients_table.setItem(
                row, 0, QtWidgets.QTableWidgetItem(patient["nom_complet"]))
            self.patients_table.setItem(
                row, 1, QtWidgets.QTableWidgetItem(patient["email"]))
            self.patients_table.setItem(
                row, 2, QtWidgets.QTableWidgetItem(patient["tel"]))
            self.patients_table.setItem(
                row, 3, QtWidgets.QTableWidgetItem(patient["description"]))
            self.patients_table.setItem(
                row, 4, QtWidgets.QTableWidgetItem(patient["creation"]))
            self.patients_table.setItem(
                row, 5, QtWidgets.QTableWidgetItem(patient["id"]))

            row += 1

            # edit
            self.patients_table.verticalHeader().sectionDoubleClicked.connect(
                self.edit)  # table cell click function

    def create(self):
        # showing create widget
        self.hidden = False
        self.hide_show()

        self.create_patient.clicked.connect(self.create_confirmed)
        self.hidden = True
        self.cancel_btn.clicked.connect(self.hide_show)

    def create_confirmed(self):
        # fetching input info
        nom_complet = self.nom.text()
        email = self.email.text()
        tel = self.tel.text()
        description = self.description.toPlainText()

        # at least one input empty
        if nom_complet == '' or email == '' or tel == '' or description == '':
            self.error.setText("Vous avez oublié un champ!")
            self.create_patient.clicked.connect(self.create_confirmed)
        else:
            self.error.setText("")
            # database
            patient = Patient(nom_complet, email, tel, description)
            session.add(patient)
            session.commit()
            # refreshing the patients window to contain new info
            p = Patients()  # calling the patients class to define widget
            widget.insertWidget(2, p)  # adding it to the stack in index n 2
            widget.setCurrentIndex(2)  # setting current index to 2

    def edit(self, row):

        # input data
        nom_complet = self.patients_table.item(row, 0).text()
        email = self.patients_table.item(row, 1).text()
        tel = self.patients_table.item(row, 2).text()
        description = self.patients_table.item(row, 3).text()
        created = self.patients_table.item(row, 4).text()
        creation = datetime.datetime.strptime(created, "%Y-%m-%d %H:%M:%S")

        # patient id
        id = int(self.patients_table.item(row, 5).text())

        # getting the patient with id
        patient = session.query(Patient).filter(Patient.id == id)

        # updating it
        patient = patient.update({"nom_complet": nom_complet, "email": email,
                                  "tel": tel, "description": description, "created": creation})
        session.commit()  # modification base de données

    def delete(self):
        condition = self.delete_id.text().isdigit()
        if not condition:
            self.delete_id.setText('Id ?')
        else:
            self.delete_btn.setText('Confirmer')
            self.delete_btn.clicked.connect(self.delete_confirmed)

    def delete_confirmed(self):
        id = int(str(self.delete_id.text()))
        session.query(Patient).filter(Patient.id == id).delete()
        session.commit()
        # refresh
        p = Patients()  # calling the patients class to define widget
        widget.insertWidget(2, p)  # adding it to the stack in index n 2
        widget.setCurrentIndex(2)  # setting current index to 2

    def gotohome(self):
        widget.setCurrentIndex(1)

    def imports(self):
        Import.import_patient(session)

    def exports(self):
        Export.export_patient(session)


class Rappels(QDialog):
    def __init__(self):
        super(Rappels, self).__init__()
        loadUi('templates/rappels.ui', self)
        # hide create widget
        self.hidden = True
        self.hide_show()
        # ? UX/UI
        setFont(self.home_label, 15)
        setFont(self.rappel_label, 15)
        setFont(self.add_label, 15)
        setFont(self.label_1, 13)
        setFont(self.label_2, 13)
        setFont(self.label_3, 13)
        setFont(self.label_4, 13)
        setFont(self.error, 13)
        setFont(self.motif_dropdown, 12)
        setFont(self.patient_dropdown, 12)
        setFont(self.rappel_date, 12)
        setFont(self.rappel_comment, 12)
        setFont(self.rappels_table, 10)
        btns = [self.create_btn, self.delete_btn,
                self.import_btn, self.export_btn]
        setButton(btns, 2)
        setIcons(self.logo, self.admin_pic, self.home_btn,
                 self.patients_btn, self.rappels_btn)
        back_icon = QPixmap('icons/back.png')
        back_icon = QIcon(back_icon)
        self.cancel_btn.setIcon(back_icon)
        back_icon_size = QtCore.QSize(
            self.cancel_btn.width() - 60, self.cancel_btn.height() - 60)
        self.cancel_btn.setIconSize(back_icon_size)

        # Get the user's screen width
        bar_width = app.desktop().availableGeometry().width() - 40
        self.top_bar.setFixedWidth(bar_width)
        bar_height = app.desktop().availableGeometry().height()
        self.side_bar.setFixedHeight(bar_height)
        self.rappels_table.setFixedHeight(bar_height - 210)
        self.rappels_table.setFixedWidth(bar_width - 305)
        self.create_bg.setFixedHeight(bar_height - 100)
        self.create_bg.setFixedWidth(bar_width - 100)
        btn_x = self.rappels_table.width() + 160
        self.create_btn.move(btn_x, self.create_btn.y() + 50)
        self.delete_btn.move(btn_x, self.delete_btn.y() + 50)
        self.delete_id.move(btn_x, self.delete_id.y() + 50)
        self.import_btn.move(btn_x, self.import_btn.y() + 150)
        self.export_btn.move(btn_x, self.export_btn.y() + 150)
        self.top_bar_color.setStyleSheet("background: #1A1A1A")
        self.side_bar.setStyleSheet("background: #1A1A1A")
        self.home_btn.setStyleSheet(""" QPushButton {
                                        border: none;
                                        }
                                        QPushButton:hover {
                                        background: #B0E0E6;
                                        }
                                    """)
        self.patients_btn.setStyleSheet("""
                                        QPushButton {
                                        border: none;
                                        }
                                        QPushButton:hover {
                                        background: #B0E0E6;
                                        }""")
        self.rappels_btn.setStyleSheet("""
                                        QPushButton {
                                        border: none;
                                        background: #B0E0E6;
                                        }
                                        """)

        self.home_label.setStyleSheet("color: #fefefe;")
        self.add_label.setStyleSheet("color: #000;")
        self.rappel_label.setStyleSheet("color: #000;")

        # keyboard shortcuts
        self.home_btn.setShortcut('Ctrl+h')
        self.patients_btn.setShortcut('Ctrl+p')
        self.cancel_btn.setShortcut('Esc')

        # buttons
        self.patients_btn.clicked.connect(Home.gotopatients)
        self.home_btn.clicked.connect(Patients.gotohome)
        self.create_btn.clicked.connect(self.create)
        self.delete_btn.clicked.connect(self.delete)
        self.import_btn.clicked.connect(self.imports)
        self.export_btn.clicked.connect(self.exports)

        # data table
        self.rappels_table.setColumnWidth(0, 160)
        self.rappels_table.setColumnWidth(1, 180)
        self.rappels_table.setColumnWidth(2, 100)
        self.rappels_table.setColumnWidth(3, 100)
        self.rappels_table.setColumnWidth(4, 300)
        self.rappels_table.setColumnWidth(5, 160)
        self.rappels_table.setColumnWidth(6, 50)
        # rappel data fetch from database
        self.loaddata()

    def loaddata(self):
        rappels = []
        row = 0

        query = session.query(Rappel).all()  # get all rappels data

        # patients data one by one
        for r in query:
            rappel = {"patient": r.patient,
                      "motif": r.motif,
                      "date": r.date,
                      "status": r.status,
                      "commentaire": r.commentaire,
                      "creation": r.created.strftime("%Y-%m-%d %H:%M:%S"),
                      "id": r.id}
            rappels.append(rappel)

        # filling the table
        self.rappels_table.setRowCount(len(rappels))
        for rappel in rappels:
            # patient name
            id = int(rappel["patient"])
            patient = session.query(Patient).get(id)
            if patient is None:
                patient = '(PATIENT SUPPRIMÉ)'
            else:
                patient = patient.nom_complet

            # motif name
            if rappel["motif"] == Motifs.motif1:
                motif = Motifs.motif(1)
            elif rappel["motif"] == Motifs.motif2:
                motif = Motifs.motif(2)
            elif rappel["motif"] == Motifs.motif3:
                motif = Motifs.motif(3)
            elif rappel["motif"] == Motifs.motif4:
                motif = Motifs.motif(4)
            elif rappel["motif"] == Motifs.motif5:
                motif = Motifs.motif(5)

            # status
            if rappel["status"] == Status.notyet:
                status = Status.notyet_()
            elif rappel["status"] == Status.delayed:
                status = Status.delayed_()
            elif rappel["status"] == Status.done:
                status = Status.done_()

            self.rappels_table.setItem(
                row, 0, QtWidgets.QTableWidgetItem(str(patient)))
            self.rappels_table.setItem(
                row, 1, QtWidgets.QTableWidgetItem(str(motif)))
            self.rappels_table.setItem(
                row, 2, QtWidgets.QTableWidgetItem(str(rappel["date"])))
            self.rappels_table.setItem(
                row, 3, QtWidgets.QTableWidgetItem(str(status)))
            self.rappels_table.setItem(
                row, 4, QtWidgets.QTableWidgetItem(str(rappel["commentaire"])))
            self.rappels_table.setItem(
                row, 5, QtWidgets.QTableWidgetItem(str(rappel["creation"])))
            self.rappels_table.setItem(
                row, 6, QtWidgets.QTableWidgetItem(str(rappel["id"])))

            row += 1

    def hide_show(self):

        if self.hidden == True:
            self.create_bg.hide()
        if self.hidden == False:
            self.create_bg.show()

    def create(self):
        # get patient names for drop down
        patients = session.query(Patient).all()
        self.patient_dropdown.addItem('')
        for p in patients:
            self.patient_dropdown.addItem(p.nom_complet)

        # get motifs for drop down using list this time
        motifs = []
        n_motifs = 5  # how many motifs
        for id in range(1, n_motifs + 1):
            motifs.append(str(Motifs.motif(id)))
        self.motif_dropdown.addItem('')
        self.motif_dropdown.addItems(motifs)

        # date
        self.rappel_date.setDisplayFormat("dd.MM.yyyy")
        self.rappel_date.setDate(QDate.currentDate())
        self.rappel_date.setMinimumDate(QDate.currentDate())
        self.rappel_date.setMaximumDate(
            QDate.fromString("29.12.2099", "dd.MM.yyyy"))

        # showing create widget
        self.hidden = False
        self.hide_show()

        self.create_rappel.clicked.connect(self.create_confirmed)
        self.hidden = True
        self.cancel_btn.clicked.connect(self.hide_show)

    def create_confirmed(self):

        # fetching input info
        # nom patient
        p_name = str(self.patient_dropdown.currentText())

        # motif
        motif = str(self.motif_dropdown.currentText())

        # motif.replace('Ú', 'é')
        if motif == Motifs.motif(1):
            motif = Motifs.motif1
        elif motif == Motifs.motif(2):
            motif = Motifs.motif2
        elif motif == Motifs.motif(3):
            motif = Motifs.motif3
        elif motif == Motifs.motif(4):
            motif = Motifs.motif4
        elif motif == Motifs.motif(5):
            motif = Motifs.motif5

        # date
        date = self.rappel_date.date()  # get date
        date = date.toPyDate()  # normalize date

        # commentaire
        comment = self.rappel_comment.toPlainText()

        # at leat one input empty
        if len(comment) == 0 or p_name == '' or motif == '':
            self.error.setText("Vous avez oublié un champ")
            self.create_rappel.clicked.connect(self.create_confirmed)
        else:

            # id patient
            patient = session.query(Patient).filter(
                Patient.nom_complet == p_name).first()  # get patient from name
            p_id = patient.id

            # database
            rappel = Rappel(p_id, motif, date, comment)
            session.add(rappel)
            session.commit()

            # refreshing the patients window to contain new info
            r = Rappels()  # calling the patients class to define widget
            widget.insertWidget(2, r)  # adding it to the stack in index n 2
            widget.setCurrentIndex(2)  # setting current index to 2

    def delete(self):
        condition = self.delete_id.text().isdigit()
        if not condition:
            self.delete_id.setText('ID ?')
        else:
            self.delete_btn.setText('Confirmer')
            self.delete_btn.clicked.connect(self.delete_confirmed)

    def delete_confirmed(self):
        id = int(str(self.delete_id.text()))
        session.query(Rappel).filter(Rappel.id == id).delete()
        session.commit()
        # refresh
        r = Rappels()  # calling the patients class to define widget
        widget.insertWidget(2, r)  # adding it to the stack in index n 2
        widget.setCurrentIndex(2)  # setting current index to 2

    def imports(self):
        Import.import_rappel(session)

    def exports(self):
        Export.export_rappel(session)


# main
app = QApplication(sys.argv)  # defining the app
auth = Authentication()  # first widget

widget = QStackedWidget()  # start a widget stack
widget.addWidget(auth)  # adding auth as the first widget, index is 0


# Get the user's screen geometry
screen_geometry = app.desktop().availableGeometry()

# Set the widget's geometry to the screen geometry
widget.setGeometry(screen_geometry)

widget.showMaximized()  # display

# exit
try:
    sys.exit(app.exec())
except:
    print("Quitter")
