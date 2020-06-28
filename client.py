import socket
from tkinter import *
from langdetect import detect
#voice bot
import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
#voices index 0 is spanish female voice
engine.setProperty('voice', voices[0].id)


#Interface
root = Tk()
root.title("Test")
root.geometry('400x500')
#sockets
HEADER = 64
PORT = 80
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "quit"
#SERVER = socket.gethostbyname(socket.gethostname())
SERVER = '192.168.1.38'
ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def quitapp():
    send("quit")
    root.destroy()
def detectlang(text):
    lang = detect(text)
    if (lang == "en"): 
        engine.setProperty('voice', voices[1].id) 
        return 1
    elif (lang == "ja"):
        engine.setProperty('voice', voices[2].id)
        return 2
    elif (lang == "es"):
        engine.setProperty('voice', voices[0].id)
        return 0
    else: 
        print("Non valid language")
        return 1


def send(msg):
    chatWindow.insert(END, "\n" + "You said: " + msg)
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    rmsg = client.recv(2048).decode(FORMAT)
    chatWindow.insert(END, "\n" + "He/she says: " + rmsg)
    indexvoice = detectlang(rmsg)
    engine.setProperty('voice', voices[indexvoice].id)
    engine.say(rmsg)
    engine.runAndWait()


def clicksend():
    msg = messageWindow.get()
    send(msg)
    messageWindow.delete(0, END)
    messageWindow.insert(0,"")
   
main_menu = Menu(root)
main_menu.add_command(label='Quit',command=quitapp)
root.config(menu=main_menu)

chatWindow = Text(root,bd=1,bg='grey',width= 50, height= 8)
chatWindow.place(x=6, y=6, height= 385, width= 370)

messageWindow = Entry(root,bg='grey',width = 30)
messageWindow.place(x=128, y= 400, height= 88, width= 260)

button = Button(root, text='enviar', bg='#e67f77',activebackground='#ed9e98', width=12, height = 5,font=('Arial',14),command=clicksend)
button.place(x=6,y=400,height=88,width= 120)

#WIP scrollbar
scrollbar = Scrollbar(root, command=chatWindow.yview())
scrollbar.place(x=375,y=5,height=385)

root.mainloop()



#out = 0
#while not out:
    #print ("Escribe tu mensaje o quit para salir")
    #msg = input()
#    if msg == "quit":
#        out = 1
#        send(msg)
        #print("Saliendo")
#    else: 
#        send(msg)
        

