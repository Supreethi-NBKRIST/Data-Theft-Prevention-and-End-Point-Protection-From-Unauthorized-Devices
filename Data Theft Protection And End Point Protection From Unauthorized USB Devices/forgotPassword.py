import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import subprocess
import mysql.connector
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import array
import time
import random


class VideoPlayerApp:
    def __init__(self, window, video_source):
        #self.count = 0
        #self.chances = 0
        self.otp=0
        self.window = window
        self.window.title("Video Player")
        self.video_source = video_source
        self.cap = cv2.VideoCapture(self.video_source)
        self.canvas = tk.Canvas(window, width=self.cap.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()
        width=self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height=self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)-40
        window.geometry('{}x{}+{}+{}'.format(int(width), int(height), int(x), int(y)))
        def verify1():

            self.verifyButton.destroy()

            self.passLabel=tk.Label(window,text='PASSWORD',font=('Microsoft Yahei UI Light',10,'bold'),bg='black',fg='cyan')
            self.passLabel.place(x=550,y=260)
            self.passEntry=tk.Entry(window,width=30,font=('Microsoft Yahei UI Light',10,'bold'),fg='black',bg='LightSkyBlue1')
            self.passEntry.place(x=550,y=290)

            self.conpassLabel=tk.Label(window,text='CONFIRM PASSWORD',font=('Microsoft Yahei UI Light',10,'bold'),bg='black',fg='cyan')
            self.conpassLabel.place(x=550,y=320)
            self.conpassEntry=tk.Entry(window,width=30,font=('Microsoft Yahei UI Light',10,'bold'),fg='black',bg='LightSkyBlue1')
            self.conpassEntry.place(x=550,y=350)

            self.submitButton=tk.Button(window,text='Submit',font=('Open Sans',14,'bold'),bd=0,bg='cyan',fg='black',activebackground='black',activeforeground='cyan',width=10,command=change_password)
            self.submitButton.place(x=690,y=410)
            
        def change_password():
            if self.otpEntry.get()=='':
                messagebox.showerror('Error','All Fields Are Required')
            elif self.passEntry.get() !=  self.conpassEntry.get():
               messagebox.showerror('Error','Password Mismatch')
            else:
                try:
                    con = mysql.connector.connect(host='localhost',user='root',password='root',database='login')
                    cursor = con.cursor()
                except:
                    messagebox.showerror('Error','Database Connectivity issue,  Please Try Again')
                    return
                #print(self.otp)
                if self.otp == self.otpEntry.get():
                    query='update login set password=%s where email=%s'
                    cursor.execute(query,(self.passEntry.get(),self.emailEntry.get()))
                    con.commit()
                    con.close()
                    messagebox.showinfo('Success','New User Created Successfully')
                    window.destroy()
                    subprocess.run(["python", "login.py"])
                else:
                    messagebox.showinfo('Error','Invalid otp') 
                    
        def clear():
            self.emailEntry.delete(0,tk.END)
            self.usernameEntry.delete(0,tk.END)
            #self.otpEntry.delete(0,tk.END)

        def on_button_click():
            window.destroy()
            subprocess.run(["python", "admin.py"]) 

        def generate_otp(length=6):
            otp = ""
            for _ in range(length):
                otp += str(random.randint(0, 9))
            return otp

        self.otp=generate_otp()

        def verify():
            print(self.otp)
            if self.emailEntry.get()=='' :
                messagebox.showinfo('Error','All Fields are Required')
            else:      
                try:
                    con = mysql.connector.connect(host='localhost',user='root',password='root',database='login')
                    cursor = con.cursor()
                except:
                    messagebox.showerror('Error','Database Connectivity issue,  Please Try Again')
                    return          
                query = 'select * from login where email=%s'
                cursor.execute(query, (self.emailEntry.get(),))
                row = cursor.fetchone()
                if row is not None:  
                    sender_email = 'lockyourusbport@gmail.com'
                    receiver_email = self.emailEntry.get()
                    subject = 'Email Verification'
                    message = 'OTP for email verification:' + self.otp
                    smtp_server = "smtp.gmail.com"
                    smtp_port = 587
                    smtp_username = sender_email
                    smtp_password = "conj xhxx bnqw xgmx"
                    msg = MIMEMultipart()
                    msg['From'] = sender_email
                    msg['To'] = receiver_email
                    msg['Subject'] = subject
                    msg.attach(MIMEText(message, 'plain'))
                    server = smtplib.SMTP(smtp_server, smtp_port)
                    server.starttls()
                    try:
                        server.login(smtp_username, smtp_password)
                    except smtplib.SMTPAuthenticationError:
                        messagebox.showerror("Error", "Wrong SMTP password")
                    else:
                        server.send_message(msg)
                        server.quit()
                        messagebox.showinfo("Success", "OTP sent successfully")
                        self.verifyButton.destroy()

                        self.otpLabel=tk.Label(window,text='OTP',font=('Microsoft Yahei UI Light',10,'bold'),bg='black',fg='cyan')
                        self.otpLabel.place(x=550,y=200)
                        self.otpEntry=tk.Entry(window,width=30,font=('Microsoft Yahei UI Light',10,'bold'),fg='black',bg='LightSkyBlue1')
                        self.otpEntry.place(x=550,y=230)

                        self.verifyButton=tk.Button(window,text='VERIFY',font=('Open Sans',10,'bold'),bd=0,bg='cyan',fg='black',activebackground='black',activeforeground='cyan',width=10,command=verify1)
                        self.verifyButton.place(x=750,y=260)
                else:
                    messagebox.showinfo('Error','User Doesnot exists.Try with correct mail')

        self.emailLabel=tk.Label(window,text='EMAIL',font=('Microsoft Yahei UI Light',10,'bold'),bg='black',fg='cyan')
        self.emailLabel.place(x=550,y=140)
        self.emailEntry=tk.Entry(window,width=30,font=('Microsoft Yahei UI Light',10,'bold'),fg='black',bg='LightSkyBlue1')
        self.emailEntry.place(x=550,y=170)

        self.verifyButton=tk.Button(window,text='Verify',font=('Open Sans',10,'bold'),bd=0,bg='cyan',fg='black',activebackground='black',activeforeground='cyan',width=10,command=verify)
        self.verifyButton.place(x=750,y=200)

        self.clearButton=tk.Button(window,text='Clear',font=('Open Sans',14,'bold'),bd=0,bg='cyan',fg='black',activebackground='black',activeforeground='cyan',width=10,command=clear)
        self.clearButton.place(x=690,y=410)

        self.backButton = tk.Button(window, text='Back', font=('Open Sans', 16, 'bold'), bd=0, bg='cyan', fg='black',cursor='hand2', activebackground='black', activeforeground='cyan',  command=on_button_click)
        self.backButton.place(x=20, y=20)

        self.update()

    def play_video(self):
        self.cap = cv2.VideoCapture(self.video_source)

    def stop_video(self):
        self.cap.release()

    def update(self):
        ret, frame = self.cap.read()
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(10, self.update)

root = tk.Tk()
video_source = 'createuser.mp4'
app = VideoPlayerApp(root, video_source)
root.mainloop()
