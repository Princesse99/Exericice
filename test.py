from tkinter import *
import os
from PIL import Image, ImageTk
from tkinter import filedialog
import socket
import threading

# Utilisez des chemins absolus
image1_path = os.path.abspath("Image/1.jpg")
image2_path = os.path.abspath("Image/2.jpg")

print(f"Image 1 path: {image1_path}")
print(f"Image 2 path: {image2_path}")

root = Tk()
root.title("Shareit")
root.geometry("450x560+500+200")
root.configure(bg="#f4fdfe")
root.resizable(False, False)

filename = None

def select_file():
    global filename
    filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                          title='Select Image File',
                                          filetypes=(('Text files', '.txt'), ('All files', '.*')))
    print(f"Selected file: {filename}")

def sender():
    if filename is None:
        print("No file selected")
        return

    s = socket.socket()
    host = socket.gethostname()
    port = 8080
    s.bind((host, port))
    s.listen(1)
    print(f"Host: {host}, Port: {port}")
    print('Waiting for any incoming connections....')
    conn, addr = s.accept()
    with open(filename, 'rb') as file:
        file_data = file.read(1024)
        while file_data:
            conn.send(file_data)
            file_data = file.read(1024)
    conn.close()
    print("Data has been transmitted successfully")

def receiver(ID, filepath):
    s = socket.socket()
    port = 8080
    s.connect((ID, port))
    with open(filepath, 'wb') as file:
        file_data = s.recv(1024)
        while file_data:
            file.write(file_data)
            file_data = s.recv(1024)
    s.close()
    print("File has been received successfully")

def Send():
    print("Opening Send window")
    window = Toplevel(root)
    window.title("Send")
    window.geometry('450x560+500+200')
    window.configure(bg="#f4fdfe")
    window.resizable(False, False)

    try:
        image_icon1 = PhotoImage(file=image1_path)
        window.iconphoto(False, image_icon1)
        print("Loaded image_icon1 successfully")
    except Exception as e:
        print(f"Error loading image_icon1: {e}")

    try:
        Sbackground = PhotoImage(file=image2_path)
        Label(window, image=Sbackground).place(x=-2, y=0)
        print("Loaded Sbackground successfully")
    except Exception as e:
        print(f"Error loading Sbackground: {e}")

    host = socket.gethostname()
    Label(window, text=f'ID: {host}', bg='white', fg='black').place(x=140, y=290)

    Button(window, text="+Select file", width=10, height=1, font="arial 14 bold", bg="#fff", fg="#000", command=select_file).place(x=16, y=15)
    Button(window, text='SEND', width=8, height=1, font='arial 14 bold', bd=2, fg="#fff", bg="#000", command=sender).place(x=17, y=60)

    window.mainloop()

def Receive():
    print("Opening Receive window")
    main = Toplevel(root)
    main.title("Receive")
    main.geometry('450x560+500+200')
    main.configure(bg="#f4fdfe")
    main.resizable(False, False)

    def select_save_file():
        global save_filename
        save_filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=(("Text files", ".txt"), ("All files", ".*")))
        print(f"Save file as: {save_filename}")
        incoming_file.delete(0, END)
        incoming_file.insert(0, save_filename)

    def start_receiver():
        ID = SenderID.get()
        filepath = incoming_file.get()
        threading.Thread(target=receiver, args=(ID, filepath)).start()

    try:
        image_icon1 = PhotoImage(file=image1_path)
        main.iconphoto(False, image_icon1)
        print("Loaded image_icon1 successfully")
    except Exception as e:
        print(f"Error loading image_icon1: {e}")

    try:
        Sbackground = PhotoImage(file=image2_path)
        Label(main, image=Sbackground).place(x=-2, y=0)
        print("Loaded Sbackground successfully")
    except Exception as e:
        print(f"Error loading Sbackground: {e}")

    Label(main, text="Receive", font=('arial,20'), bg="#f4fdfe").place(x=100, y=280)
    Label(main, text="Input sender ID", font=('arial,20'), bg="#f4fdfe").place(x=20, y=340)
    SenderID = Entry(main, width=25, fg="black", border=2, bg='white', font=('arial', 15))
    SenderID.place(x=20, y=370)
    SenderID.focus()

    Label(main, text="Filename for the incoming file:", font=('arial,20'), bg="#f4fdfe").place(x=20, y=420)
    incoming_file = Entry(main, width=25, fg="black", border=2, bg='white', font=('arial', 15))
    incoming_file.place(x=20, y=450)

    Button(main, text="Select save file", width=15, height=1, font="arial 14 bold", bg="#fff", fg="#000", command=select_save_file).place(x=20, y=500)
    Button(main, text="Receive", width=10, height=1, font="arial 14 bold", bg="#fff", fg="#000", command=start_receiver).place(x=200, y=500)

    main.mainloop()

Label(root, text="File Transfer", font=('Acumin Variable Concept', 20, 'bold'), bg="#f4fdfe").place(x=20, y=30)
Frame(root, width=400, height=2, bg="#f3f5f6").place(x=25, y=80)

send = Button(root, text="Send", bg="#762170", bd=0, command=Send)
send.place(x=50, y=100)

receive = Button(root, text="Receive", bg="#216D76", bd=0, command=Receive)
receive.place(x=50, y=150)

Label(root, text="Send", font=('Acumin Variable Concept', 17, 'bold'), bg="#f4fdfe").place(x=65, y=200)
Label(root, text="Receive", font=('Acumin Variable Concept', 17, 'bold'), bg="#f4fdfe").place(x=300, y=200)

print("Starting main loop")
root.mainloop()
print("Main loop finished")
