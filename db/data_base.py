import datetime
import enum
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, DateTime, Enum, Date
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class Admin(Base):
    __tablename__ = "Admin"

    username = Column('username', String, primary_key=True)
    password = Column('password', String)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f'Admin: {self.username}'


class Patient(Base):
    __tablename__ = "Patients"

    id = Column('id', Integer, autoincrement=True, primary_key=True)
    nom_complet = Column('nom_complet', String)
    description = Column('description', String)
    email = Column('email', String)
    tel = Column('tel', String)
    created = Column('creation', DateTime,
                     default=datetime.datetime.now())

    def __init__(self, nom_complet, email, tel, description):
        self.nom_complet = nom_complet
        self.email = email
        self.tel = tel
        self.description = description


class Motifs(enum.Enum):
    motif1 = 'Préparation de la FIV'
    motif2 = 'Suivi de stimulation ovarienne'
    motif3 = 'Consultation pré-FIV'
    motif4 = 'Suivi de grossesse'
    motif5 = "Prélèvement d'ovocytes pour la FIV" 

    def motif(id):
        if id == 1:
            return 'Préparation de la FIV'
        elif id == 2:
            return 'Suivi de stimulation ovarienne'
        elif id == 3:
            return 'Consultation pré-FIV'
        elif id == 4:
            return 'Suivi de grossesse'
        elif id == 5:
            return "Prélèvement d'ovocytes pour la FIV"


class Status(enum.Enum):
    notyet = 'Pas encore'
    done = 'Terminé'
    delayed = 'Prolongé'

    def notyet_():
        return 'Pas encore'

    def delayed_():
        return 'Terminé'

    def done_():
        return 'Prolongé'


class Rappel(Base):
    __tablename__ = "Rappels"

    id = Column('id', Integer, autoincrement=True, primary_key=True)
    patient = Column(Integer, ForeignKey('Patients.id'), nullable=False)
    motif = Column(Enum(Motifs), default=Motifs.motif1, nullable=False)
    date = Column('date', Date, default=datetime.date.today())
    status = Column(Enum(Status), default=Status.notyet, nullable=False)
    commentaire = Column('commentaire', String)
    created = Column('creation', DateTime,
                     default=datetime.datetime.now())

    def __init__(self, patient, motif, date, commentaire):
        self.patient = patient
        self.motif = motif
        self.date = date
        self.commentaire = commentaire

    def delayed(self, date):
        if date == 'demain' or date == 'Demain':
            today = datetime.date.today()
            tomorrow = today + datetime.timedelta(days=1)
            self.date = tomorrow
            self.status = Status.delayed
            return True
        elif date == 'apres demain' or date == 'Apres demain' or date == 'après demain' or date == 'Après demain':
            today = datetime.date.today()
            aftertmrw = today + datetime.timedelta(days=2)
            self.date = aftertmrw
            self.status = Status.delayed
            return True
        else:
            try:
                day = datetime.datetime.strptime(date, '%Y-%m-%d')
            except:
                return False
            self.date = day
            self.status = Status.delayed
            return True

    def done(self):
        self.status = Status.done


""" 
# engine
engine = create_engine('sqlite:///db/ma_bdd.db', echo=True)

# session
Session = sessionmaker(bind=engine)
session = Session()

# create classes
Base.metadata.create_all(bind=engine)

# add 
admin = Admin('admin', '1234')
session.add(admin)
patient = Patient('Benberkane Amine', 'aminebenberkane@gmail.com', '0799388743', 'Travaille chez Hayet Clinique de Fertilité'
                  )
session.add(patient)

# delete patient
session.query(Patient).filter(Patient.id == 3).delete()

# delete table
Base.metadata.drop_all(bind=engine, tables=[Rappel.__table__])

# Delete all objects from the Patient table
session.query(Patient).delete()

# commit
session.commit() """
