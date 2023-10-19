import webbrowser
import datetime
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QColor, QIcon, QFont, QPixmap
from PyQt5.QtWidgets import QDialog
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.data_base import Patient, Rappel, Motifs, Status
from PyQt5.QtCore import Qt, QSize


# ? User Experrience


def setButton(list, type):
    if len(list) == 4:
        colors = ['#fba88f', '#87CEFA', '#D8BFD8', '#98FB98']
    elif len(list) == 3:
        colors = ['#fba88f', '#87CEFA', '#D8BFD8']
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


def setFont(label, size):
    # Set the font to Roboto with a size of 14
    font = QFont("Segoe UI", size)
    label.setFont(font)


# load the database
engine = create_engine('sqlite:///db/ma_bdd.db', echo=True)

# create a session to access database
Session = sessionmaker(bind=engine)
session = Session()


class Today(QDialog):
    def __init__(self, widget):
        super(Today, self).__init__()
        loadUi('display/today.ui', self)  # load the home UI
        # ? UI/UX
        setFont(self.message, 15)
        setFont(self.label_patient, 10)
        setFont(self.label_motif, 10)
        setFont(self.label_commentaire, 10)
        setFont(self.label_status, 8)
        setFont(self.label_creation, 8)
        setFont(self.today_btn, 10)
        setFont(self.demain_btn, 10)
        setFont(self.after_btn, 10)
        setFont(self.date_btn, 10)
        setFont(self.tel_btn, 10)
        setFont(self.done_btn, 10)
        setFont(self.delay_btn, 10)
        setFont(self.delay_date, 10)
        setFont(self.list_rappels, 12)
        btns = [self.email_btn, self.tel_btn, self.done_btn, self.delay_btn]
        setButton(btns, 2)
        back_icon = QPixmap('icons/back.png')
        back_icon = QIcon(back_icon)
        self.cancel_btn.setIcon(back_icon)
        back_icon_size = QtCore.QSize(
            self.cancel_btn.width() - 150, self.cancel_btn.height() - 60)
        self.cancel_btn.setIconSize(back_icon_size)

        self.message.setText("     Les rappels d'aujourdh'ui")

        # buttons
        self.demain_btn.clicked.connect(self.gototomorrow)
        self.after_btn.clicked.connect(self.gotoaftertmrw)
        self.cancel_btn.clicked.connect(self.gotohome)
        self.cancel_btn.setShortcut('Esc')
        # tooltips
        self.delay_btn.setToolTip(
            '<html><body><h3 style="color:#000;">Sélectionnez une date :</h3><p style="font-size:14px; font-family:Arial; color:#222;">yyyy-mm-dd (aaaa-mm-jj)<br>Demain. Vous pouvez également l\'écrire comme "Demain".<br>apres-demain. Vous pouvez également l\'écrire comme: Apres-demain, après-demain ou Après-Demain.</p></body></html>')

        self.widget = widget

        # load data
        # Columns
        i = f"Motif (Statut)"
        item = QtWidgets.QListWidgetItem(i)
        item.setSizeHint(QSize(400, 40))
        item.setBackground(QColor('#28282b'))
        item.setForeground(QColor('#fefefefe'))
        item.setTextAlignment(Qt.AlignCenter)
        # Disable item selection and hover color
        item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
        item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
        self.list_rappels.addItem(item)
        item = QtWidgets.QListWidgetItem('')
        item.setSizeHint(QSize(0, 0))
        self.list_rappels.addItem(item)

        # get rappels data for today
        today = datetime.date.today()
        query = session.query(Rappel).filter(Rappel.date == today)

        if query.count() == 0:
            self.message.setText("Aucun rappel !")
        else:
            self.idlist = []
            for r in query:

                if r.motif == Motifs.motif1:
                    motif = Motifs.motif(1)
                elif r.motif == Motifs.motif2:
                    motif = Motifs.motif(2)
                if r.motif == Motifs.motif3:
                    motif = Motifs.motif(3)
                elif r.motif == Motifs.motif4:
                    motif = Motifs.motif(4)
                elif r.motif == Motifs.motif5:
                    motif = Motifs.motif(5)

                if r.status == Status.delayed:
                    status = Status.delayed_()
                elif r.status == Status.notyet:
                    status = Status.notyet_()
                elif r.status == Status.done:
                    status = Status.done_()

                patient = session.query(Patient).get(r.patient)
                patient = patient.nom_complet

                id = r.id

                i = f' {motif} ({status})                                                                           %{id}'
                self.label_patient.setText('  Patient')
                self.label_motif.setText('  Motif')
                self.label_commentaire.setText('  Commentaire')
                self.label_creation.setText('  Créé le')
                self.label_status.setText('  Statut')
                item = QtWidgets.QListWidgetItem(i)
                item.setSizeHint(QSize(400, 70))
                item.setTextAlignment(Qt.AlignVCenter)
                self.list_rappels.addItem(item)
            self.list_rappels.itemDoubleClicked.connect(self.show_rappel)

    def show_rappel(self, item):
        id = item.text().split('%')[1]
        r = session.query(Rappel).get(id)

        p_id = r.patient
        p = session.query(Patient).get(p_id)
        email = p.email
        tel = p.tel

        patient = p.nom_complet

        if r.motif == Motifs.motif1:
            motif = Motifs.motif(1)
        elif r.motif == Motifs.motif2:
            motif = Motifs.motif(2)
        if r.motif == Motifs.motif3:
            motif = Motifs.motif(3)
        elif r.motif == Motifs.motif4:
            motif = Motifs.motif(4)
        elif r.motif == Motifs.motif5:
            motif = Motifs.motif(5)

        if r.status == Status.delayed:
            status = Status.delayed_()
        elif r.status == Status.notyet:
            status = Status.notyet_()
        elif r.status == Status.done:
            status = Status.done_()

        comment = r.commentaire

        created = r.created.strftime("%Y-%m-%d %H:%M:%S")

        self.label_patient.setText(str(patient))
        self.label_motif.setText(str(motif))
        self.label_commentaire.setText(str(comment))
        self.label_status.setText(f'Créé le:    {str(created)}')
        self.label_creation.setText(f'Statut:    {str(status)}')

        # method buttons
        self.email_btn.clicked.connect(lambda: self.send_email(email))
        self.tel_btn.clicked.connect(lambda: self.call(tel))
        delay_date = self.delay_date.text()
        self.delay_btn.clicked.connect(lambda: self.delay(delay_date))

    def delay(self, date):
        if self.delay_btn.text() != 'Confirmez':
            if date == '':
                self.delay_date.setText('??')
            else:
                delay_date = self.delay_date.text()
                self.delay_btn.setText('Confimez')
                self.delay_btn.clicked.connect(lambda: self.delay(delay_date))
        else:
            response = Rappel.delayed(date)
            if response == True:
                # calling the patients class to define widget
                t = Today(self.widget)
                # adding it to the stack in index n 2
                self.widget.insertWidget(2, t)
                self.widget.setCurrentIndex(2)
            else:
                self.delay_date.setText('Invalide')

    def send_email(self, email):

        url = "mailto:" + email
        webbrowser.open(url)
        print('email done')

    def call(self, tel):
        url = "tel:" + tel
        webbrowser.open(url)
        print('phone call done')

    def gototomorrow(self):
        # calling the patients class to define widget
        t = Tomorrow(self.widget)
        self.widget.insertWidget(2, t)  # adding it to the stack in index n 2
        self.widget.setCurrentIndex(2)  # setting current index to 2

    def gotoaftertmrw(self):
        # calling the patients class to define widget
        a = Aftertmrw(self.widget)
        self.widget.insertWidget(2, a)  # adding it to the stack in index n 2
        self.widget.setCurrentIndex(2)  # setting current index to 2

    def gotohome(self):
        self.widget.setCurrentIndex(1)
        print('hoome')


class Tomorrow(QDialog):
    def __init__(self, widget):
        super(Tomorrow, self).__init__()
        loadUi('display/tomorrow.ui', self)  # load the home UI
        # ? UI/UX
        setFont(self.message, 15)
        setFont(self.label_patient, 10)
        setFont(self.label_motif, 10)
        setFont(self.label_commentaire, 10)
        setFont(self.label_status, 8)
        setFont(self.label_creation, 8)
        setFont(self.today_btn, 10)
        setFont(self.demain_btn, 10)
        setFont(self.after_btn, 10)
        setFont(self.date_btn, 10)
        setFont(self.tel_btn, 10)
        setFont(self.done_btn, 10)
        setFont(self.list_rappels, 12)
        btns = [self.email_btn, self.tel_btn, self.done_btn]
        setButton(btns, 2)
        back_icon = QPixmap('icons/back.png')
        back_icon = QIcon(back_icon)
        self.cancel_btn.setIcon(back_icon)
        back_icon_size = QtCore.QSize(
            self.cancel_btn.width() - 150, self.cancel_btn.height() - 60)
        self.cancel_btn.setIconSize(back_icon_size)

        self.message.setText("     Les rappels de demain")

        # buttons
        self.today_btn.clicked.connect(self.gototoday)
        self.after_btn.clicked.connect(self.gotoaftertmrw)
        self.cancel_btn.clicked.connect(self.gotohome)
        self.cancel_btn.setShortcut('Esc')

        self.widget = widget

        # load data
        # Columns
        i = f"Motif (Statut)"
        item = QtWidgets.QListWidgetItem(i)
        item.setSizeHint(QSize(400, 40))
        item.setBackground(QColor('#28282b'))
        item.setForeground(QColor('#fefefefe'))
        item.setTextAlignment(Qt.AlignCenter)
        # Disable item selection and hover color
        item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
        item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
        self.list_rappels.addItem(item)
        item = QtWidgets.QListWidgetItem('')
        item.setSizeHint(QSize(0, 0))
        self.list_rappels.addItem(item)

        # get all rappels data
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        query = session.query(Rappel).filter(Rappel.date == tomorrow)

        if query.count() == 0:
            self.message.setText("Aucun rappel !")
        else:
            for r in query:

                if r.motif == Motifs.motif1:
                    motif = Motifs.motif(1)
                elif r.motif == Motifs.motif2:
                    motif = Motifs.motif(2)
                if r.motif == Motifs.motif3:
                    motif = Motifs.motif(3)
                elif r.motif == Motifs.motif4:
                    motif = Motifs.motif(4)
                elif r.motif == Motifs.motif5:
                    motif = Motifs.motif(5)

                if r.status == Status.delayed:
                    status = Status.delayed_()
                elif r.status == Status.notyet:
                    status = Status.notyet_()
                elif r.status == Status.done:
                    status = Status.done_()

                patient = session.query(Patient).get(r.patient)
                patient = patient.nom_complet

                id = r.id

                i = f' {motif} ({status})                                                                   %{id}'
                self.label_patient.setText('  Patient')
                self.label_motif.setText('  Motif')
                self.label_commentaire.setText('  Commentaire')
                self.label_creation.setText('  Créé le')
                self.label_status.setText('  Statut')
                item = QtWidgets.QListWidgetItem(i)
                item.setSizeHint(QSize(400, 70))
                item.setTextAlignment(Qt.AlignCenter)
                self.list_rappels.addItem(item)
        self.list_rappels.itemDoubleClicked.connect(self.show_rappel)

    def show_rappel(self, item):
        id = item.text().split('%')[1]
        r = session.query(Rappel).get(id)

        p_id = r.patient
        p = session.query(Patient).get(p_id)
        email = p.email
        tel = p.tel
        self.email_btn.clicked.connect(lambda: self.send_email(email))
        self.tel_btn.clicked.connect(lambda: self.call(tel))
        patient = p.nom_complet

        if r.motif == Motifs.motif1:
            motif = Motifs.motif(1)
        elif r.motif == Motifs.motif2:
            motif = Motifs.motif(2)
        if r.motif == Motifs.motif3:
            motif = Motifs.motif(3)
        elif r.motif == Motifs.motif4:
            motif = Motifs.motif(4)
        elif r.motif == Motifs.motif5:
            motif = Motifs.motif(5)

        if r.status == Status.delayed:
            status = Status.delayed_()
        elif r.status == Status.notyet:
            status = Status.notyet_()
        elif r.status == Status.done:
            status = Status.done_()

        comment = r.commentaire

        created = r.created.strftime("%Y-%m-%d %H:%M:%S")

        self.label_patient.setText(str(patient))
        self.label_motif.setText(str(motif))
        self.label_commentaire.setText(str(comment))
        self.label_status.setText(f'Créé le:    {str(created)}')
        self.label_creation.setText(f'Statut:    {str(status)}')

    def send_email(self, email):

        url = "mailto:" + email
        webbrowser.open(url)
        print('email done')

    def call(self, tel):
        url = "tel:" + tel
        webbrowser.open(url)
        print('phone call done')

    def gototoday(self):
        t = Today(self.widget)  # calling the patients class to define widget
        self.widget.insertWidget(2, t)  # adding it to the stack in index n 2
        self.widget.setCurrentIndex(2)  # setting current index to 2

    def gotoaftertmrw(self):
        # calling the patients class to define widget
        a = Aftertmrw(self.widget)
        self.widget.insertWidget(2, a)  # adding it to the stack in index n 2
        self.widget.setCurrentIndex(2)  # setting current index to 2

    def gotohome(self):
        self.widget.setCurrentIndex(1)
        print('hoome')


class Aftertmrw(QDialog):
    def __init__(self, widget):
        super(Aftertmrw, self).__init__()
        loadUi('display/aftertmrw.ui', self)  # load the home UI

        # ? UI/UX
        setFont(self.message, 15)
        setFont(self.label_patient, 10)
        setFont(self.label_motif, 10)
        setFont(self.label_commentaire, 10)
        setFont(self.label_status, 8)
        setFont(self.label_creation, 8)
        setFont(self.today_btn, 10)
        setFont(self.demain_btn, 10)
        setFont(self.after_btn, 10)
        setFont(self.date_btn, 10)
        setFont(self.tel_btn, 10)
        setFont(self.done_btn, 10)
        setFont(self.list_rappels, 12)
        btns = [self.email_btn, self.tel_btn, self.done_btn]
        setButton(btns, 2)
        back_icon = QPixmap('icons/back.png')
        back_icon = QIcon(back_icon)
        self.cancel_btn.setIcon(back_icon)
        back_icon_size = QtCore.QSize(
            self.cancel_btn.width() - 150, self.cancel_btn.height() - 60)
        self.cancel_btn.setIconSize(back_icon_size)

        self.message.setText("     Les rappels d'après demain")

        # buttons
        self.today_btn.clicked.connect(self.gototoday)
        self.demain_btn.clicked.connect(self.gototomorrow)
        self.cancel_btn.clicked.connect(self.gotohome)
        self.cancel_btn.setShortcut('Esc')

        self.widget = widget

       # load data
        # Columns
        i = f"Motif (Statut)"
        item = QtWidgets.QListWidgetItem(i)
        item.setSizeHint(QSize(400, 40))
        item.setBackground(QColor('#28282b'))
        item.setForeground(QColor('#fefefefe'))
        item.setTextAlignment(Qt.AlignCenter)
        # Disable item selection and hover color
        item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
        item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
        self.list_rappels.addItem(item)
        item = QtWidgets.QListWidgetItem('')
        item.setSizeHint(QSize(0, 0))
        self.list_rappels.addItem(item)

        # get all rappels data
        today = datetime.date.today()
        aftertmrw = today + datetime.timedelta(days=2)
        query = session.query(Rappel).filter(Rappel.date == aftertmrw)

        if query.count() == 0:
            self.message.setText("Aucun rappel !")
        else:
            for r in query:

                if r.motif == Motifs.motif1:
                    motif = Motifs.motif(1)
                elif r.motif == Motifs.motif2:
                    motif = Motifs.motif(2)
                if r.motif == Motifs.motif3:
                    motif = Motifs.motif(3)
                elif r.motif == Motifs.motif4:
                    motif = Motifs.motif(4)
                elif r.motif == Motifs.motif5:
                    motif = Motifs.motif(5)

                if r.status == Status.delayed:
                    status = Status.delayed_()
                elif r.status == Status.notyet:
                    status = Status.notyet_()
                elif r.status == Status.done:
                    status = Status.done_()

                patient = session.query(Patient).get(r.patient)
                patient = patient.nom_complet

                id = r.id

            i = f' {motif} ({status})                                                               %{id}'
            self.label_patient.setText('  Patient')
            self.label_motif.setText('  Motif')
            self.label_commentaire.setText('  Commentaire')
            self.label_creation.setText('  Créé le')
            self.label_status.setText('  Statut')
            item = QtWidgets.QListWidgetItem(i)
            item.setSizeHint(QSize(400, 70))
            item.setTextAlignment(Qt.AlignCenter)
            self.list_rappels.addItem(item)
        self.list_rappels.itemDoubleClicked.connect(self.show_rappel)

    def show_rappel(self, item):
        id = item.text().split('%')[1]
        r = session.query(Rappel).get(id)

        p_id = r.patient
        p = session.query(Patient).get(p_id)
        email = p.email
        tel = p.tel
        self.email_btn.clicked.connect(lambda: self.send_email(email))
        self.tel_btn.clicked.connect(lambda: self.call(tel))
        patient = p.nom_complet

        if r.motif == Motifs.motif1:
            motif = Motifs.motif(1)
        elif r.motif == Motifs.motif2:
            motif = Motifs.motif(2)
        if r.motif == Motifs.motif3:
            motif = Motifs.motif(3)
        elif r.motif == Motifs.motif4:
            motif = Motifs.motif(4)
        elif r.motif == Motifs.motif5:
            motif = Motifs.motif(5)

        if r.status == Status.delayed:
            status = Status.delayed_()
        elif r.status == Status.notyet:
            status = Status.notyet_()
        elif r.status == Status.done:
            status = Status.done_()

        comment = r.commentaire

        created = r.created.strftime("%Y-%m-%d %H:%M:%S")

        self.label_patient.setText(str(patient))
        self.label_motif.setText(str(motif))
        self.label_commentaire.setText(str(comment))
        self.label_status.setText(f'Créé le:    {str(created)}')
        self.label_creation.setText(f'Statut:    {str(status)}')

    def send_email(self, email):

        url = "mailto:" + email
        webbrowser.open(url)
        print('email done')

    def call(self, tel):
        url = "tel:" + tel
        webbrowser.open(url)
        print('phone call done')

    def gototoday(self):
        t = Today(self.widget)  # calling the patients class to define widget
        self.widget.insertWidget(2, t)  # adding it to the stack in index n 2
        self.widget.setCurrentIndex(2)  # setting current index to 2

    def gototomorrow(self):
        # calling the patients class to define widget
        t = Tomorrow(self.widget)
        self.widget.insertWidget(2, t)  # adding it to the stack in index n 2
        self.widget.setCurrentIndex(2)  # setting current index to 2

    def gotohome(self):
        self.widget.setCurrentIndex(1)
        print('hoome')
