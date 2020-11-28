"""
Author: Mario Uriel Romero Martinez
Contact: marioma3@cisco.com
Purpose: To create,update and generate a report of Security Group Tags on ISE"

"""


from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
from tkinter import filedialog
from authentication import authentication
import csv
from ise import *



def authenticate():
    global conn,header
    conn=None
    header=None

    ise=iseadd.get()
    usnam=un.get()
    pasw=pw.get()


    if ise != "" or usnam!="" or pasw != "":
        conn,header=authentication(ise,usnam,pasw)
        messagebox.showinfo("Authentication","Credentials were save")

    else:
        messagebox.showwarning("Empty Fields","Provide complete information")

def login():

    global label1,label2,label3,label4,entry1,entry2,entry3,b1,b2


    label1=Label(root,text="Provide ISE credentials",relief="solid",width=20,font=("arial",19,"bold"))
    label1.place(x=90,y=53)

    label2=Label(root,text="ISEAddress:",width=20,font=("arial",10,"bold"))
    label2.place(x=80,y=130)

    entry1=Entry(root,textvar=iseadd)
    entry1.place(x=240,y=130)

    label3=Label(root,text="Username:",width=20,font=("arial",10,"bold"))
    label3.place(x=80,y=170)

    entry2=Entry(root,textvar=un)
    entry2.place(x=240,y=170)

    label4=Label(root,text="Password:",width=20,font=("arial",10,"bold"))
    label4.place(x=80,y=210)

    entry3=Entry(root,textvar=pw,show='*')
    entry3.place(x=240,y=210)

    b1=Button(root,text="Accept",width=12,bg='blue',fg='white',command=authenticate)
    b1.place(x=150,y=380)
    b2=Button(root,text="Exit",width=12,bg='red',fg='white',command=exit1)
    b2.place(x=280,y=380)

def report():

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

    if 'b3' in globals():
        b3.destroy()

    if 'conn' in globals():
        listsgtids=get_sgtsids(conn,header)
        #csv_report=open(asksaveasfilename())

        if get_sgt_info(conn,header,listsgtids):
            messagebox.showinfo("Report Generated","The report was created succesfully")
        else:
            messagebox.showerror("Error trying to generate the report")


    
    else:
        messagebox.showwarning("Warning", "Verify login authorization")




def readcsv():

    listaux=[]
    
    if 'conn' in globals():
        csvfile= filedialog.askopenfilename(initialdir="/",title="CREATE-Select the csv file",filetypes = (("csv files","*.csv"),("all files","*.*")))
        try:
            with open(csvfile,'r') as csvf:
                reader=csv.reader(csvf)

                for row in reader:
                    listaux.append({"@description":row[1],"@name":row[0],"generationId":"0","value":row[2]})
        except Exception as e:
            print("Error trying to open/read file ", e)
            messagebox.showerror(f"Error trying to open/read file {e}")


        if bulk_sgt(conn,header,"create",listaux):
            messagebox.showinfo("Successful Operation","SGTs were created successfully on ISE")

        else:
            messagebox.showerror("Error", "SGTs were not created,Verify authentication credentials")
    
    else:
        messagebox.showwarning("Warning", "Verify authentication credentials")

def updatecsv():
    listaux=[]
    
    if 'conn' in globals():
        csvfile= filedialog.askopenfilename(initialdir="/",title="UPDATE-Select the csv file",filetypes = (("csv files","*.csv"),("all files","*.*")))
        try:
            with open(csvfile,'r') as csvf:
                reader=csv.reader(csvf)

                for row in reader:
                    #sgt=i.split(',')
          
                    listaux.append({"@description":row[2],"@name":row[1],"@id":row[0],"propogateToApic":False,"value":row[3]})

        except Exception as e:
            print("Error trying to open/read file ", e)
            messagebox.showerror(f"Error trying to open/read file {e}")



        if bulk_sgt(conn,header,"update",listaux):
            messagebox.showinfo("Successful Operation","SGTs were updated successfully on ISE")

        else:
            messagebox.showerror("Error", "SGTs were not updated,Verify authentication credentials")
    
    else:
        messagebox.showwarning("Warning", "Verify authentication credentials")


#def postonesgt():
#    pass

def exit1():
    exit()


# def createonesgt():
#     label1=Label(root,text="SGT Name:",width=20,font=("arial",10,"bold"))
#     label1.place(x=80,y=130)

#     entry1=Entry(root,textvar=sgtname)
#     entry1.place(x=240,y=130)

#     label2=Label(root,text="SGT Description:",width=20,font=("arial",10,"bold"))
#     label2.place(x=80,y=170)

#     entry2=Entry(root,textvar=sgtdescr)
#     entry2.place(x=240,y=170)

#     label3=Label(root,text="SGT Value (TAG):",width=20,font=("arial",10,"bold"))
#     label3.place(x=80,y=210)

#     entry3=Entry(root,textvar=sgtv,show='*')
#     entry3.place(x=240,y=210)

#     b1=Button(root,text="Create",width=12,bg='green',fg='white',command=postonesgt)
#     b1.place(x=150,y=380)
#     b2=Button(root,text="Exit",width=12,bg='red',fg='white',command=exit1)
#     b2.place(x=280,y=380)
    
def updatebulksgt():
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

    updatecsv()


def createbulksgt():
    #global b3

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

    #b3=Button(root,text="Select the *.csv file",width=22,bg='blue',fg='white',command=readcsv)
    #b3.place(x=150,y=80)
    readcsv()
   

root= Tk()
root.geometry("500x500")
root.title("P&G ISE SGT")

iseadd=StringVar()
un=StringVar()
pw=StringVar()

sgtname=StringVar()
sgtdescr=StringVar()
sgtv=StringVar()

pmenu = Menu(root)
root.config(menu=pmenu)

login_menu = Menu(pmenu, tearoff=0)
pmenu.add_cascade(label="Login", menu=login_menu)
login_menu.add_command(label="Authenticate",command=login)

add_menu = Menu(pmenu, tearoff=0)
pmenu.add_cascade(label="Add SGTs", menu=add_menu)
#add_menu.add_command(label="Add SGTs one by one",command=createonesgt)
#add_menu.add_separator()
add_menu.add_command(label="Add a group of SGTs from a csv file",command=createbulksgt)

update_menu = Menu(pmenu, tearoff=0)
pmenu.add_cascade(label="Update SGTs", menu=update_menu)
#update_menu.add_command(label="Update SGTs one by one",command=createonesgt)
#update_menu.add_separator()
update_menu.add_command(label="Update a group of SGTs from a csv file",command=updatebulksgt)

report_menu = Menu(pmenu, tearoff=0)
pmenu.add_cascade(label="Generate SGT report", menu=report_menu)
report_menu.add_command(label="Create CSV File",command=report)

C = Canvas(root, height=500, width=500)
C.pack()
filename = PhotoImage(file = "ise26.png")
C.create_image(0,0,anchor=NW,image=filename)



root.mainloop()
