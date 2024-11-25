from tkinter import *
from PIL import Image, ImageTk
import socket
from tkinter import filedialog
from tkinter import messagebox
import os

root = Tk()
root.title("Shareit")
root.geometry("450x500+500+200")
root.configure(bg="#f4fdfc")
root.resizable(False, False)

filename = None  # Global variable to hold the selected filename

def select_file():
    global filename
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select Image File',
                                          filetypes=[('Text files', '*.txt'), ('All files', '*.*')])
    print(f"Selected file: {filename}")  # Print the selected file path for testing

def sender():
    if filename is None:
        messagebox.showerror("Error", "Please select a file first")
        return
    
    s = socket.socket()
    host = socket.gethostname()
    port = 8080
    s.bind((host, port))
    s.listen(1)
    print(host)
    print('Incoming connections...')
    conn, addr = s.accept()
    print(f"Connected by {addr}")
    with open(filename, 'rb') as file:
        while (file_data := file.read(1024)):
            conn.send(file_data)
    print('Data transfer success...')
    conn.close()
    s.close()

def Send():
    window = Toplevel(root)
    window.title('Send')
    window.geometry('450x460+500+200')
    window.configure(bg='#f4fdfe')
    window.resizable(False, False)

    # icon
    image_icon1 = PhotoImage(file="image/send.png")
    window.iconphoto(False, image_icon1)

    host = socket.gethostbyname(socket.gethostname())
    Label(window, text=f'ID: {host}', bg='white', fg='black').place(x=140, y=290)

    Button(window, text='+ Select File', width=15, height=2, font='arial 14 bold', bg='#fff', fg='#000', command=select_file).place(x=160, y=150)
    Button(window, text='SEND', width=15, height=2, font='arial 14 bold', bg='#000', fg='#fff', command=sender).place(x=160, y=220)

    window.mainloop()

def Receive():
    main = Toplevel(root)
    main.title('Receive')
    main.geometry('450x460+500+200')
    main.configure(bg='#f4fdfe')
    main.resizable(False, False)

    def receiver():
        ID = SenderID.get()
        filename1 = incoming_file.get()

        s = socket.socket()
        port = 8080
        try:
            s.connect((ID, port))
            with open(filename1, 'wb') as file:
                while True:
                    file_data = s.recv(1024)
                    if not file_data:
                        break
                    file.write(file_data)
            print('Success')
        except Exception as e:
            print(f"Connection error: {e}")
        finally:
            s.close()

    # icon
    image_icon2 = PhotoImage(file="image/receive.png")
    main.iconphoto(False, image_icon2)

    Label(main, text="Receive", font=('arial', 20), bg='#f4fdfe').place(x=180, y=30)
    Label(main, text='Input sender ID', font=('arial', 10, 'bold'), bg='#f4fdfe').place(x=20, y=100)
    SenderID = Entry(main, width=25, fg='black', border=2, bg='white', font=('arial', 15))
    SenderID.place(x=20, y=130)
    SenderID.focus()

    Label(main, text='Filename incoming', font=('arial', 10, 'bold'), bg='#f4fdfe').place(x=20, y=180)
    incoming_file = Entry(main, width=25, fg='black', border=2, bg='white', font=('arial', 15))
    incoming_file.place(x=20, y=210)

    rr = Button(main, text='Receive', compound=LEFT, width=15, bg='#39c790', font='arial 14 bold', command=receiver)
    rr.place(x=20, y=260)

    main.mainloop()

# Utiliser Pillow pour ouvrir l'image receiver.jpg
image_path = "image/receiver.jpg"
try:
    image_icon = Image.open(image_path)
    image_icon = ImageTk.PhotoImage(image_icon)
    root.iconphoto(False, image_icon)
except Exception as e:
    print(f"Erreur en ouvrant l'image : {e}")

Label(root, text="File Transfer", font=('Acumin Variable Concept', 20, 'bold'), bg="#f4fdfe").place(x=20, y=30)
Frame(root, width=400, height=2, bg="#f3f5f6").place(x=25, y=80)

# Conserver les références des images pour éviter qu'elles soient collectées par le garbage collector
images = {}

# Utiliser Pillow pour ouvrir l'image send.png et redimensionner l'image
image_path = "image/send.png"
try:
    image_send = Image.open(image_path)
    image_send = image_send.resize((50, 50), Image.LANCZOS)  # Utiliser LANCZOS au lieu de ANTIALIAS
    images['send'] = ImageTk.PhotoImage(image_send)
    send_button = Button(root, image=images['send'], bg="#f4fdfe", bd=0, command=Send)
    send_button.place(x=180, y=150)
    
    # Ajouter un titre en dessous du bouton "Send"
    send_label = Label(root, text="Send", font=('Acumin Variable Concept', 14, 'bold'), bg="#f4fdfe")
    send_label.place(x=190, y=210)
    
except Exception as e:
    print(f"Erreur en ouvrant l'image : {e}")
    Label(root, text="Send", font=('Acumin Variable Concept', 20, 'bold'), bg="#f4fdfe").place(x=65, y=200)

# Utiliser Pillow pour ouvrir l'image receive.png et redimensionner l'image
image_path = "image/receive.png"
try:
    image_receive = Image.open(image_path)
    image_receive = image_receive.resize((50, 50), Image.LANCZOS)  # Utiliser LANCZOS au lieu de ANTIALIAS
    images['receive'] = ImageTk.PhotoImage(image_receive)
    receive_button = Button(root, image=images['receive'], bg="#f4fdfe", bd=0, command=Receive)
    receive_button.place(x=180, y=250)
    
    # Ajouter un titre en dessous du bouton "Receive"
    receive_label = Label(root, text="Receive", font=('Acumin Variable Concept', 14, 'bold'), bg="#f4fdfe")
    receive_label.place(x=190, y=310)
except Exception as e:
    print(f"Erreur en ouvrant l'image : {e}")
    Label(root, text="Receive", font=('Acumin Variable Concept', 20, 'bold'), bg="#f4fdfe").place(x=65, y=200)

root.mainloop()
