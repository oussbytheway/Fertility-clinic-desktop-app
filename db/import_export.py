import openpyxl
import json
import sys
import pandas as pd
import tkinter as tk
from db.data_base import Patient, Rappel, Motifs, Status
from datetime import datetime, date
from tkinter import filedialog, messagebox


class Import():
    def import_patient(session):
        # Create a Tkinter root window
        root = tk.Tk()
        root.withdraw()  # hide the root window

        # Prompt the user to choose a file
        file_path = filedialog.askopenfilename()
        if file_path == '':
            print('Exit import')
        else:
            # Open the file as a binary file
            with open(file_path, 'rb') as file:
                # Load the XLSX file into a Pandas DataFrame
                df = pd.read_excel(file)

            # Convert the DataFrame to a JSON string
            json_data = df.to_json(orient='records')

            data = json.loads(json_data)

            # restrictions
            err = None
            required_columns = ["nom_complet", "email", "tel", "description"]
            # columns
            missing_columns = []
            intruder_columns = []
            for d in data:
                for k in d.keys():
                    if k not in required_columns:
                        intruder_columns.append(k)
                for col in required_columns:
                    if col not in d.keys():
                        missing_columns.append(col)
            if missing_columns or intruder_columns:
                error = "Veuillez vérifier les colonnes. \n\n"
                if missing_columns:
                    error += f"Colonnes manquantes: {set(missing_columns)}. \n\n"
                if intruder_columns:
                    error += f"Colonnes intruses: {set(intruder_columns)}."
                messagebox.showwarning(title="Erreur", message=error)
                err = True
            else:
                if err is None:
                    for dict in data:
                        new = Patient(**dict)
                        session.add(new)
                    session.commit()
                    messagebox.showinfo(
                        title="Import réussi", message='Ajout des patients réussi!')

    def import_rappel(session):

        # Create a Tkinter root window
        root = tk.Tk()
        root.withdraw()  # hide the root window

        # Prompt the user to choose a file
        file_path = filedialog.askopenfilename()
        if file_path == '':
            print('Exit import')
        else:
            # Open the file as a binary file
            with open(file_path, 'rb') as file:
                # Load the XLSX file into a Pandas DataFrame
                df = pd.read_excel(file)

            # Convert the DataFrame to a JSON string
            json_data = df.to_json(orient='records')

            data = json.loads(json_data)

            # restrictions
            err = None
            required_columns = ["patient", "motif", "date", "commentaire"]
            # columns
            missing_columns = []
            intruder_columns = []
            for d in data:
                for k in d.keys():
                    if k not in required_columns:
                        intruder_columns.append(k)
                for col in required_columns:
                    if col not in d.keys():
                        missing_columns.append(col)
            if missing_columns or intruder_columns:
                error = "Veuillez vérifier les colonnes. \n\n"
                if missing_columns:
                    error += f"Colonnes manquantes: {set(missing_columns)}. \n\n"
                if intruder_columns:
                    error += f"Colonnes intruses: {set(intruder_columns)}."
                messagebox.showwarning(title="Erreur", message=error)
                err = True
            else:

                # motifs
                allowed_motifs = [Motifs.motif(1), Motifs.motif(
                    2), Motifs.motif(3), Motifs.motif(4), Motifs.motif(5)]
                k = 1
                for row in data:
                    motif = row["motif"]
                    k += 1
                    if motif not in allowed_motifs:
                        error = f"Le motif doit être l'un des suivants : " + \
                            ", ".join(allowed_motifs)
                        error += f"\n\nErreur: {motif} \n\nLigne: {k}"
                        messagebox.showwarning(title="Erreur", message=error)
                        err = True
                        break  # Stop checking the rest of the rows if there's an error
                j = 1
                for d in data:
                    p = session.query(Patient).filter(
                        Patient.nom_complet == d['patient'])
                    pt = d['patient']
                    j += 1
                    if p.count() == 0:
                        error = f'Le patient n\'existe pas dans votre base de données.\n\nErreur: {pt}\n\nLigne: {j}'
                        messagebox.showwarning(title="Erreur", message=error)
                        err = True
                        break

                format = '%Y-%m-%d'
                i = 1
                for d in data:
                    da = str(d['date'])
                    i += 1
                    try:
                        datetime.strptime(da, format)

                    except ValueError:
                        error = f'Date invalide.\n\nErreur: {da}\n\nLigne: {i}'
                        messagebox.showwarning(title="Erreur", message=error)
                        err = True
                        break

                if err is None:
                    for dict in data:
                        dict["date"] = datetime.strptime(
                            dict["date"], '%Y-%m-%d').date()

                        patient = session.query(Patient).filter(
                            Patient.nom_complet == dict["patient"]).first()  # get patient from name
                        if patient is None:
                            dict["patient"] = '(PATIENT SUPPRIMÉ)'
                        else:
                            dict["patient"] = patient.id

                        if dict["motif"] == Motifs.motif(1):
                            dict["motif"] = Motifs.motif1
                        elif dict["motif"] == Motifs.motif(2):
                            dict["motif"] = Motifs.motif2
                        elif dict["motif"] == Motifs.motif(3):
                            dict["motif"] = Motifs.motif3
                        elif dict["motif"] == Motifs.motif(4):
                            dict["motif"] = Motifs.motif4
                        elif dict["motif"] == Motifs.motif(5):
                            dict["motif"] = Motifs.motif4

                        new = Rappel(**dict)
                        session.add(new)
                    session.commit()
                    messagebox.showinfo(
                        title="Import réussi", message='Ajout des rappels réussi!')


class Export():
    def export_rappel(session):
        # create a new workbook
        wb = openpyxl.Workbook()

        # select the active worksheet
        ws = wb.active

        # write headers to the first row
        ws.append(['id', 'patient', 'motif', 'date',
                   'status', 'commentaire', 'creation'])

        # write data to the worksheet
        rappels = session.query(Rappel).all()

        for r in rappels:
            # motif name
            if r.motif == Motifs.motif1:
                motif = Motifs.motif(1)
            elif r.motif == Motifs.motif2:
                motif = Motifs.motif(2)
            elif r.motif == Motifs.motif3:
                motif = Motifs.motif(3)
            elif r.motif == Motifs.motif4:
                motif = Motifs.motif(4)
            elif r.motif == Motifs.motif5:
                motif = Motifs.motif(5)

            # patient name
            id = int(r.patient)
            patient = session.query(Patient).get(id)
            if patient is None:
                patient = '(PATIENT SUPPRIMÉ)'
            else:
                patient = patient.nom_complet

            # status
            if r.status == Status.notyet:
                status = Status.notyet_()
            elif r.status == Status.delayed:
                status = Status.delayed_()
            elif r.status == Status.done:
                status = Status.done_()

            # dates

            date_string = str(r.created)
            datetime_object = datetime.strptime(
                date_string, "%Y-%m-%d %H:%M:%S.%f")
            creation = datetime_object.strftime("%Y-%m-%d %H:%M:%S")

            d = r.created.strftime("%Y-%m-%d")

            ws.append([r.id, patient, motif, str(d),
                       status, r.commentaire, str(creation)])
        today = date.today()
        # save the workbook to disk
        wb.save(f'rappels({today}).xlsx')

        messagebox.showinfo(
            title="Export réussi",
            message=f"Les données ont été exportées avec succès dans le fichier 'rappels({today}).xlsx'"
        )

    def export_patient(session):
        # create a new workbook
        wb = openpyxl.Workbook()

        # select the active worksheet
        ws = wb.active

        # write headers to the first row
        ws.append(['id', 'nom_complet', 'email', 'tel',
                   'description', 'creation'])

        # write data to the worksheet
        patients = session.query(Patient).all()

        for p in patients:

            # date

            date_string = str(p.created)
            try:
                datetime_object = datetime.strptime(
                    date_string, "%Y-%m-%d %H:%M:%S")
            except:
                datetime_object = datetime.strptime(
                    date_string, "%Y-%m-%d %H:%M:%S.%f")
            creation = datetime_object.strftime("%Y-%m-%d %H:%M:%S")

            ws.append([p.id, p.nom_complet, p.email, p.tel,
                       p.description, str(creation)])
        today = date.today()
        # save the workbook to disk
        wb.save(f'patients({today}).xlsx')

        messagebox.showinfo(
            title="Export réussi",
            message=f"Les données ont été exportées avec succès dans le fichier 'patients({today}).xlsx'"
        )
