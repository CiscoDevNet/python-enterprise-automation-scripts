from tkinter import *
from tkinter.ttk import Combobox, Progressbar
from tkinter import messagebox
from tkinter import filedialog
from os import path
from datetime import date
from nobg import *
import time
import threading

"""
Author: Mario Uriel Romero Martínez
Organization:Cisco CX BCS SD-WAN
Description: Python script to generate a report for Network Group objects from Firepower Management Center 
"""


def getobj(progressx,labelx):

    listobj=[]

    if 'token' in globals():
        
        labelx['text']="Collecting the List of Network Object Groups..."
        root.update_idletasks()
        listobj=get_nobjg(token,fmc_url,domainid)
        progressx['value']=50
        labelx['text']=f"List created {progress['value']}%"
        root.update_idletasks()
        time.sleep(1)

        labelx['text']="Collecting Network Object group info..."
        root.update_idletasks()
        get_objinfo(token,fmc_url,domainid,listobj)
        progressx['value']=75
        labelx['text']=f"Information was collected {progress['value']}%"
        root.update_idletasks()
        time.sleep(1)
        labelx['text']="Generating report..."
        root.update_idletasks()
        time.sleep(1)
        writetoexcel("netgrobj.json")
        progressx['value']=100
        labelx['text']=f"Report was created {progress['value']}%"
        root.update_idletasks()
        time.sleep(1)
     
        
        messagebox.showinfo("Report Status","Spreadsheet was created")
        
    else:
        messagebox.showwarning("Warning", "Verify authentication status")
        
        progress.stop()
        label5['text']=""



def getnetobjg():

    
    global progress,label5

    if 'label1' in globals():
        label1.destroy()
        label2.destroy()
        label3.destroy()
        label4.destroy()
        entry1.destroy()
        entry2.destroy()
        entry3.destroy()
        b1.destroy()
        b2.destroy()
    
    
    
    progress = Progressbar(root, orient = HORIZONTAL,length = 300, mode = 'determinate')
    progress.place(x=100,y=110)

    label5=Label(root,text="Creating report...",width=50,font=("arial",10,"bold"))
    label5.place(x=40,y=210)
    root.update_idletasks()
    time.sleep(1)
    getobj(progress,label5)
    
  


    


def authent():

    global token,domainid,fmc_url
    
    fmca=fmcadd.get()
    usnam=un.get()
    pasw=pw.get() 

    if fmca != "" and usnam!="" and pasw != "":
        fmc_url = f"https://{fmca}"
    dictauth=authenticate(usnam,pasw,fmc_url)

    
    token=dictauth["Token"]
    domainid=dictauth["DomainId"]
    if token!=None:
        messagebox.showinfo("Authentication response","User succesfully signed up")
    else:
        messagebox.showerror("Authetication Error", "Invalid User or password")




def exitp():
    exit()

def login():

    if 'progress' in globals():
        progress.destroy()
        label5.destroy()

    global label1,label2,label3,label4,entry1,entry2,entry3,b1,b2

    label1=Label(root,text="Log in to FMC",relief="solid",width=20,font=("arial",19,"bold"))
    label1.place(x=90,y=53)

    label2=Label(root,text="FMC Address:",width=20,font=("arial",10,"bold"))
    label2.place(x=80,y=130)

    entry1=Entry(root,textvar=fmcadd)
    entry1.place(x=240,y=130)

    label3=Label(root,text="Username:",width=20,font=("arial",10,"bold"))
    label3.place(x=80,y=170)

    entry2=Entry(root,textvar=un)
    entry2.place(x=240,y=170)

    label4=Label(root,text="Password:",width=20,font=("arial",10,"bold"))
    label4.place(x=80,y=210)

    entry3=Entry(root,textvar=pw,show='*')
    entry3.place(x=240,y=210)

    b1=Button(root,text="Accept",width=12,bg='blue',fg='white',command=authent)
    b1.place(x=150,y=380)
    b2=Button(root,text="Exit",width=12,bg='red',fg='white',command=exitp)
    b2.place(x=280,y=380)

   



root= Tk()
root.geometry("500x500")
root.title("SD-WAN vEdge Validation")

fmcadd=StringVar()
un=StringVar()
pw=StringVar()

pmenu = Menu(root)
root.config(menu=pmenu)

login_menu = Menu(pmenu, tearoff=0)
pmenu.add_cascade(label="1.Login", menu=login_menu)
login_menu.add_command(label="Authenticate",command=login)

get_menu = Menu(pmenu, tearoff=0)
pmenu.add_cascade(label="2.Get Network Object groups", menu=get_menu)
get_menu.add_command(label="Generate report",command=getnetobjg)

exit_menu = Menu(pmenu, tearoff=0)
pmenu.add_cascade(label="3.Exit", menu=exit_menu)
exit_menu.add_command(label="Exit",command=exitp)

C = Canvas(root, height=500, width=500)

filename = PhotoImage(file = "firewall_fc_256.png")
C.create_image(500/2,500/2,anchor="center",image=filename)
C.pack()


root.mainloop()






