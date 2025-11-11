# Mail App
A simple Python Tkinter app for sending emails via SMTP with a clean and easy-to-use interface.

## Login Frame

1. **Enter your email address** – for example, Gmail.  
2. **Enable two-factor authentication** in your email account, then **generate an app password**.  
3. **Enter your email and the app password** to log in.

For example:

<img src="login_example.png" alt="Mail App Login Screenshot" width="600">

## Send mail

1. Click the **New Mail** button
2. Add as much **recipient** as you want
3. Add files
4. send your mail

<img src="mail_frame.png" alt="Mail App Login Screenshot" width="600">

## Features

- **Add recipients** – Add multiple recipients for your email.  
- **Remove recipients** – Remove recipients if needed.  
- **Compose emails** – Enter subject and message content.  
- **Attach files** – Add files like PDFs, images, or any other type to your email.  
- **Send emails via SMTP** – Works with Gmail using an app password.  
- **Login with app password** – Requires 2-factor authentication to generate an app password.  
- **Dynamic interface** – Shows attached files and allows removing them before sending.  

## Installation

1. Open a terminal (Git Bash, PowerShell, or CMD).  
2. Clone the repository:

```bash
git clone https://github.com/rodin04/Mail-app.git
```

3. Navigate to the project folder.
```bash
cd your_folder_path!!!
```

4. Install requirements.txt
```bash
pip install -r requirements.txt
```

## Start programm

1. Open a terminal (Git Bash, PowerShell, or CMD).
2. Navigate to the project folder.
```bash
cd your_folder_path!!!
```
3. Start python script
```bash
python mail.py
```

## Requirements

- Python 3.12+  
- Tkinter (standard library, usually included with Python)  
- reportlab 3.6+ (`reportlab==3.6.13`) – for PDF generation  
- PyPDF2 3.0+ (`PyPDF2==3.0.1`) – for reading and writing PDFs  
- Pillow 10+ (`Pillow==10.0.0`) – for image handling and screenshots  
- fpdf 1.7+ (`fpdf==1.7.2`) – alternative PDF generation  
- pyserial 3.5+ (`pyserial==3.5`) – for serial communication (if used)  
