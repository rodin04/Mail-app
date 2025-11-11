# -*- coding: utf-8 -*-


from tkinter import *
from tkinter import messagebox
import smtplib
from tkinter import filedialog
import os
from tkinter import filedialog, messagebox

import serial
import time
from tkinter import *
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from PyPDF2 import PdfReader, PdfWriter

import io
from PyPDF2 import PdfReader
from PIL import Image, ImageDraw, ImageFont
from tkinter import messagebox
from PIL import ImageGrab
from datetime import datetime
import os


import smtplib
from email.message import EmailMessage

from fpdf import FPDF
import os

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os







valid = False

neue_mail_frame_bool = True

empfaenger_list = []

datei_pfad_list = []

datei_pfad_nur_name_list = []


datei_label_list = []

datei_loeschen_btn_list = []

datei_pfad = None

login_mail = None

app_pw = None


def LOGIN():
    global valid
    CHECK_IF_VALID()
    if valid:
        print("valid")
        messagebox.showinfo("Valid", "loggin was correct ✅ welcome!")
        login_frame.place_forget()
        neue_mail_button.place(relx=0.5, y=60, anchor="center")
    else:
        print("not valid")
        messagebox.showerror("Error!","Invalid mail or password. Please try again!")



def CHECK_IF_VALID():
    global valid, login_mail, app_pw
    print()
    login_mail = email_entry.get()
    app_pw = password_entry.get()

    smtp_server = "smtp.gmail.com"  # Gmail SMTP-Server
    smtp_port = 587

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(login_mail, app_pw)
        server.quit()

        print("Mail funktioniert !")
        valid = True

    except smtplib.SMTPAuthenticationError:
        valid = False
        messagebox.showerror("Error!","Invalid mail or password. Please try again!")
    except Exception as e:
        valid = False
        messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten:\n{e}")

    
    
def NEUE_MAIL():
    global neue_mail_frame_bool
    print()
    if neue_mail_frame_bool:
        neue_mail_frame_bool = False
        neue_mail_frame.place(relx=0.5, rely=0.5, anchor="center")
    elif not neue_mail_frame_bool:
        neue_mail_frame_bool = True
        neue_mail_frame.place_forget()



def ADD_EMPFAENGER():
    print()
    new_empfaenger = empfaenger_entry.get()
    if new_empfaenger == "":
        messagebox.showerror("Fehler","Bitte Empfänger eingeben!")
        return
    empfaenger_list.append(new_empfaenger)
    empfaenger_label_status.config(text=f"empfänger: {len(empfaenger_list)}")


def REM_EMPFAENGER():
    if len(empfaenger_list) >= 1:
        removed = empfaenger_list.pop()  # entfernt das letzte Element
        print(f"Entfernt: {removed}")
        empfaenger_label_status.config(text=f"empfänger: {len(empfaenger_list)}")
    else:
        messagebox.showerror("Fehler", "Keine Empfänger zum Entfernen vorhanden!")



def DATEI():
    global datei_pfad
    filetypes = [("Alle Dateien", "*.*"), ("Bilder", "*.png;*.jpg;*.jpeg;*.gif"), ("PDF", "*.pdf")]
    pfad = filedialog.askopenfilename(title="Datei auswählen", filetypes=filetypes)

    if pfad:
        datei_pfad = pfad
        datei_pfad_nur_name = os.path.basename(pfad)  # Nur den Dateinamen speichern
        datei_pfad_nur_name_list.append(datei_pfad_nur_name)
        datei_pfad_list.append(datei_pfad)
        messagebox.showinfo("Datei hinzugefügt", f"Datei:\n{pfad}")
        print(f"Datei hinzugefügt: {pfad}")
        PLOTT_DATEIEN()
    else:
        messagebox.showinfo("Abgebrochen", "Keine Datei ausgewählt.")


def PLOTT_DATEIEN():
    print("____")
    print(datei_pfad_list)

    for label in datei_label_list:
        label.destroy()

    datei_label_list.clear()

    for btn in datei_loeschen_btn_list:
        btn.destroy()

    datei_loeschen_btn_list.clear()

    y_pos = 450
    for each_data in range(len(datei_pfad_nur_name_list)):

        datei_label = Label(
        neue_mail_frame,
        text=f"{datei_pfad_nur_name_list[each_data]}",
        bg="#1e293b",
        fg="#f1f5f9",
        font=("Helvetica", 16, "bold")
        )
        datei_label.place(x=50,y=y_pos+5)
        datei_label_list.append(datei_label)

        datei_loeschen_btn = Button(
        neue_mail_frame,
        text=f"X",
        bg="#1e293b",
        fg="#dd1212",
        font=("Helvetica",12, "bold"),
        command=lambda loesch_index = each_data: datei_loeschen(loesch_index)
        )
        datei_loeschen_btn.place(x=10,y=y_pos)
        datei_loeschen_btn_list.append(datei_loeschen_btn)

        y_pos += 30

def datei_loeschen(loesch_index):
    print(loesch_index)
    datei_pfad_list.pop(loesch_index)
    datei_pfad_nur_name_list.pop(loesch_index)
    PLOTT_DATEIEN()


def SEND_MAIL():
    global login_mail, app_pw

    nachricht = nachricht_text.get("1.0", "end-1c").strip()

    if not empfaenger_list or nachricht == "":
        messagebox.showerror("Fehler", "Bitte Empfänger und zumindest Nachricht!")
        return
    
    betreff = betreff_entry.get().strip()

    msg = MIMEMultipart()
    msg['From'] = login_mail
    msg['To'] = login_mail 
    msg['Subject'] = betreff
    msg.attach(MIMEText(nachricht, 'plain'))

    for dateipfad in datei_pfad_list:
        try:
            with open(dateipfad, "rb") as f:
                part = MIMEApplication(f.read(), Name=os.path.basename(dateipfad))
            part["Content-Disposition"] = f'attachment; filename="{os.path.basename(dateipfad)}"'
            msg.attach(part)
            print(f"✅ Anhang hinzugefügt: {os.path.basename(dateipfad)}")
        except Exception as e:
            print(f"❌ Fehler beim Anhängen von {dateipfad}: {e}")

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(login_mail, app_pw)

        server.sendmail(
            from_addr=login_mail,
            to_addrs=empfaenger_list,
            msg=msg.as_string()
        )

        server.quit()
        messagebox.showinfo("Erfolg", "E-Mail erfolgreich gesendet! ✅")
        print("E-Mail erfolgreich gesendet!")

    except Exception as e:
        messagebox.showerror("Fehler", f"Fehler beim Senden: {e}")
        print(f"❌ Fehler: {e}")




window = Tk()
window.geometry("500x500")
window.config(bg="#0f172a")
window.title("Login Frame Center Example")

#LOGGIN WIDGETS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# Frame mittig im Fenster
login_frame = Frame(
    window,
    bg="#1e293b",
    bd=2,
    relief="ridge",
    width=500,
    height=300
)
login_frame.place(relx=0.5, rely=0.5, anchor="center")

# Label mittig in x-Achse, y mit Pixel
welcome_label_login = Label(
    login_frame,
    text="Willkommen zurück!",
    bg="#1e293b",
    fg="#f1f5f9",
    font=("Helvetica", 16, "bold")
)
# x=None → horizontal zentriert im Frame, y=50 Pixel von oben
welcome_label_login.place(relx=0.5, y=30, anchor="center")

# E-Mail Label
email_label = Label(
    login_frame,
    text="E-Mail",
    bg="#1e293b",
    fg="white",
    font=("Helvetica", 12)
)
email_label.place(relx=0.5, y=80, anchor="center")

# Entry für Email
email_entry = Entry(
    login_frame,
    width=30,
    font=("Helvetica", 12),
    bg="white",
    fg="black",
    relief="solid",
    bd=1
)
email_entry.place(relx=0.5, y=110, anchor="center")

# App-Passwort Label
password_label = Label(
    login_frame,
    text="App-Passwort",
    bg="#1e293b",
    fg="white",
    font=("Helvetica", 12)
)
password_label.place(relx=0.5, y=150, anchor="center")

# Entry für App-Passwort
password_entry = Entry(
    login_frame,
    width=30,
    font=("Helvetica", 12),
    show="•",
    bg="white",
    fg="black",
    relief="solid",
    bd=1
)
password_entry.place(relx=0.5, y=180, anchor="center")

# Login Button
login_button = Button(
    login_frame,
    text="Login",
    bg="#3b82f6",      # leuchtendes Blau
    fg="white",
    font=("Helvetica", 12, "bold"),
    activebackground="#2563eb",
    activeforeground="white",
    relief="flat",
    width=15,
    height=1,
    cursor="hand2",
    command=LOGIN
)
login_button.place(relx=0.5, y=230, anchor="center")


#MAIN WINDOW WIDGETS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


neue_mail_button = Button(
    window,
    text="Neue Mail",
    bg="#3b82f6",      # leuchtendes Blau
    fg="white",
    font=("Helvetica", 20, "bold"),
    activebackground="#2563eb",
    activeforeground="white",
    relief="flat",
    width=15,
    height=1,
    cursor="hand2",
    command=NEUE_MAIL
)
#neue_mail_button.place(relx=0.5, y=60, anchor="center")

neue_mail_frame = Frame(
    window,
    bg="#1e293b",
    bd=2,
    relief="ridge",
    width=800,
    height=700
)
#neue_mail_frame.place(relx=0.5, rely=0.5, anchor="center")

empfaenger_label = Label(
    neue_mail_frame,
    text="empfänger:",
    bg="#1e293b",
    fg="#f1f5f9",
    font=("Helvetica", 16, "bold")
)
# x=None → horizontal zentriert im Frame, y=50 Pixel von oben
empfaenger_label.place(x=10, y=10)

empfaenger_label_status = Label(
    neue_mail_frame,
    text="empfänger: 0",
    bg="#1e293b",
    fg="#f1f5f9",
    font=("Helvetica", 16, "bold")
)
# x=None → horizontal zentriert im Frame, y=50 Pixel von oben
empfaenger_label_status.place(x=520, y=10)

empfaenger_plus_btn = Button(
    neue_mail_frame,
    font=("Helvetica", 16, "bold"),
    text="+",
    bg="#1e293b",
    fg="#f1f5f9",
    command=ADD_EMPFAENGER)
empfaenger_plus_btn.place(x=700,y=10)

empfaenger_minus_btn = Button(
    neue_mail_frame,
    font=("Helvetica", 16, "bold"),
    text="-",
    bg="#1e293b",
    fg="#f1f5f9",
    command=REM_EMPFAENGER)
empfaenger_minus_btn.place(x=750,y=10)

empfaenger_entry = Entry(
    neue_mail_frame,
    width=30,
    font=("Helvetica", 12),
    bg="white",
    fg="black",
    relief="solid",
    bd=1
)
empfaenger_entry.place(x=160, y=15)

betreff_label = Label(
    neue_mail_frame,
    text="Betreff:",
    bg="#1e293b",
    fg="#f1f5f9",
    font=("Helvetica", 16, "bold")
)
# x=None → horizontal zentriert im Frame, y=50 Pixel von oben
betreff_label.place(x=10, y=80)

betreff_entry = Entry(
    neue_mail_frame,
    width=30,
    font=("Helvetica", 12),
    bg="white",
    fg="black",
    relief="solid",
    bd=1
)
betreff_entry.place(x=160, y=85)

nachricht_label = Label(
    neue_mail_frame,
    text="Nachricht:",
    bg="#1e293b",
    fg="#f1f5f9",
    font=("Helvetica", 16, "bold")
)
# x=None → horizontal zentriert im Frame, y=50 Pixel von oben
nachricht_label.place(x=10, y=150)


# Textbox für die Nachricht
nachricht_text = Text(
    neue_mail_frame,
    width=50,           # Anzahl Zeichen pro Zeile (Breite)
    height=15,          # Anzahl Zeilen (Höhe)
    font=("Helvetica", 12),
    bg="white",
    fg="black",
    relief="solid",
    bd=1,
    wrap="word"         # Zeilenumbruch an Wortgrenzen
)
nachricht_text.place(x=160, y=155)


datei_anhaengen_button = Button(
    neue_mail_frame,
    text="Datei anhängen",
    bg="#3b82f6",      # leuchtendes Blau
    fg="white",
    font=("Helvetica", 12, "bold"),
    activebackground="#2563eb",
    activeforeground="white",
    relief="flat",
    width=15,
    height=1,
    cursor="hand2",
    command=DATEI
)
datei_anhaengen_button.place(x=570,y=570)


send_button = Button(
    neue_mail_frame,
    text="senden",
    bg="#3b82f6",      # leuchtendes Blau
    fg="white",
    font=("Helvetica", 12, "bold"),
    activebackground="#2563eb",
    activeforeground="white",
    relief="flat",
    width=15,
    height=1,
    cursor="hand2",
    command=SEND_MAIL
)
send_button.place(x=570,y=620)





window.mainloop()
