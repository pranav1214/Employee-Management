from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import socket
import requests
import bs4


def f1():
	adst.deiconify()
	root.withdraw()

def f2():
	root.deiconify()
	adst.withdraw()

def f3():
	root.deiconify()
	vist.withdraw()

def f4():
	udst.deiconify()
	root.withdraw()

def f5():
	root.deiconify()
	udst.withdraw()

def f6():
	dlst.deiconify()
	root.withdraw()

def f7():
	root.deiconify()
	dlst.withdraw()

#Add Data
def f8():
	con = None
	try:
		con = connect("student_database.db")
		cur = con.cursor()
		
		rno = int(adst_entRno.get())
		if rno <= 0:
			showerror("Error", " Enter a valid Roll number")
			adst_entRno.delete(0, END)
			adst_entName.delete(0, END)
			adst_entMarks.delete(0, END)
			adst_entRno.focus()
			return
		name = adst_entName.get()
		if len(name) < 2:
			showerror("Error", " Name should have atleast 2 Letters")
			adst_entName.delete(0, END)
			adst_entMarks.delete(0, END)
			adst_entRno.focus()
			return			
		if name.isdigit():
			showerror("Error", " Name should contain letters only")
			adst_entName.delete(0, END)
			adst_entMarks.delete(0, END)
			adst_entName.focus()
			return
		marks = int(adst_entMarks.get())
		if marks <= 0 or marks > 100:
			showerror("Error", " Enter valid Marks")
			adst_entMarks.delete(0, END)
			adst_entMarks.focus()
			return
		args = (rno, name, marks)
		cursor = con.cursor()
		sql = "insert into student values('%d', '%s', '%d')"
		cursor.execute(sql%args)
		con.commit()
		showinfo("Success", "New Detail Added")
		adst_entRno.delete(0, END)
		adst_entName.delete(0, END)
		adst_entMarks.delete(0, END)	
		adst_entRno.focus()
	except ValueError as e:
		showerror("Invalid", "Name should contain letters only")
		con.rollback()
	except Exception as e:
		if "UNIQUE" in str(e):
			showerror("Invalid", "Roll Number already exists")
		else:
			showerror("Failure", "Insert Issue" )
			con.rollback()
	finally:
		if con is not None:
			con.close()

#View Data			
def f9():
	vist_stData.delete(1.0, END)
	vist.deiconify()
	root.withdraw()
	con = None
	try:
		con = connect("student_database.db")
		cur = con.cursor()
		sql = "select * from student"
		cur.execute(sql)
		data = cur.fetchall()
		msg = ""
		for d in data:
			msg = msg + " Rno= " + str(d[0]) + " Name= " + str(d[1]) + " Marks= " + str(d[2]) + "\n" 
		vist_stData.insert(INSERT, msg)
	except Exception as e:
		showerror(" Issue ", e)
	finally:
		if con is not None:
			con.close()
          
#Delete Data          
def f10():
    con=None
    try:
        con=connect("student_database.db")
        rno=int(dlst_entRno.get())
        if rno <= 0:
            showerror("Invalid","Enter a valid Roll No.")
            dlst_entRno.delete(0,END)
            dlst_entRno.focus()
            return
        args=(rno)
        cursor=con.cursor()
        sql="delete from student where rno='%d'"
        cursor.execute(sql%args)
        if cursor.rowcount >= 1:
            con.commit()
            showinfo("Success","Record Deleted")
            dlst_entRno.delete(0,END)
            dlst_entRno.focus()
        else:
            showerror("Invalid","Roll No. does not exists")
            dlst_entRno.delete(0,END)
            dlst_entRno.focus()
    except Exception as e:
        showerror("Failure", "Deletion issue, enter valid Roll no. ")
        con.rollback()
    finally:
        if con is not None:
            con.close()

#Update Data            
def f11():
    con=None
    try:
        con=connect("student_database.db")
        rno=int(udst_entRno.get())
        if rno <= 0:
            showerror("Invalid Roll No.","Enter Valid Roll Number")
            udst_entRno.delete(0,END)    
            return     
        name=udst_entName.get()
        if len(name)<2:
            showerror("Invalid Name", "Name should atleast have 2 letters")
            udst_entName.delete(0,END)
            return
        marks=int(udst_entMarks.get())
        if marks <= 0 or marks > 100:
            showerror("Invalid Marks", "Marks should be in range of 0-100")
            udst_entMarks.delete(0,END)
            return      
        cursor=con.cursor()
        sql="update student set name='%s' ,  marks='%d' where rno='%d' "
        args=(name,marks,rno)
        cursor.execute(sql%args)
        if cursor.rowcount >= 1:
            con.commit()
            showinfo("Success","Details Updated")
            udst_entRno.delete(0,END)
            udst_entName.delete(0,END)
            udst_entMarks.delete(0,END)
            udst_entRno.focus()
        else:
            showerror("Invalid","Roll Number does not exists")
    except ValueError as e:
        showerror("Invalid","Enter Valid Details, check Roll no.")
        con.rollback()
    except Exception as e:
        showerror("Failure", "INSERT Issue ")
        con.rollback()
    finally:
        if con is not None:
            con.close()   

#Charts View
def f12():
    con=None
    con=connect("student_database.db")
    cursor = con.cursor()
    
    sql="select name, marks from student "
    cursor.execute(sql)
    dbdata=cursor.fetchall()
    data=pd.DataFrame(dbdata,columns=['Name','Marks'])
    a1=data.sort_values(by="Marks",ascending=False)
    a2=a1.head()
    
    marks=a2['Marks'].tolist()
    name=a2["Name"].tolist()
    
    barlist=plt.bar(name,marks)
    barlist[0].set_color('r')
    barlist[1].set_color('g')
    barlist[2].set_color('b')
    barlist[3].set_color('r')
    barlist[4].set_color('g')
    plt.title("Batch Information")
    plt.ylabel("Marks")
    plt.show()
    
def f13():
    try:
        res = requests.get("https://ipinfo.io")
        data = res.json()
        city_name = data['city']
    except Exception as e:
        print("Error",e)
    return city_name 

def f14():
    try:
         
        a1 = "http://api.openweathermap.org/data/2.5/weather?units=metric"
        a2 = "&q=" + f13()        
        a3 = "&appid=c6e315d09197cec231495138183954bd"
        api_address =  a1 + a2  + a3
        res=requests.get(api_address)  
        data=res.json()
        loc_temp=data['main']['temp']
    except Exception as e:
        print("Temp issue ",e)
    return loc_temp  


#def f15():
#    try:
#        res = requests.get("https://www.brainyquote.com/quote_of_the_day")
#        soup = bs4.BeautifulSoup(res.text, "lxml")
#        data = soup.find('img', {'class': 'p-qotd'})
#        msg = data['alt']
#    except Exception as e:
#        print(" Quote Error ", e)
#    return msg


    


#First Window
root = Tk()
root.title("S.M.S")
root.geometry("400x550+400+100")
root.resizable(False, False)
root.configure(background='light green')

btnAdd = Button(root, text='Add', width=10, font=('arial',18,'bold'), command=f1)
btnView = Button(root, text='View', width=10, font=('arial',18,'bold'), command=f9)
btnUpdate = Button(root, text='Update', width=10, font=('arial',18,'bold'), command=f4)
btnDelete = Button(root, text='Delete', width=10, font=('arial',18,'bold'), command=f6)
btnCharts = Button(root, text='Charts', width=10, font=('arial',18,'bold'), command=f12)
lblLocation=Label(root,text="Loc: "+str(f13()),font=("arial",18,'bold'),anchor="w",width=10,bg= 'light green')
lblTemp = Label(root, text='Temp: '+str(f14()), width=10, font=('arial',18,'bold'), bg= 'light green')
#lblQuote = Label(root,text="QOTD: "+ str(f15()),font=("arial",18,'bold'),width=200,bg="light green",anchor="w", wraplength=400)

btnAdd.pack(pady=10)
btnView.pack(pady=10)
btnUpdate.pack(pady=10)
btnDelete.pack(pady=10)
btnCharts.pack(pady=10)
lblLocation.place(x=5,y=350)
lblTemp.place(x=200, y=350)
#lblQuote.place(x=5, y= 400)


#Add Student Window
adst = Toplevel(root)
adst.title("Add St.")
adst.geometry("500x400+400+100")
adst.resizable(False, False)
adst.configure(background='light blue')

adst_lblRno = Label(adst, text='Enter Rno: ', bg='lightblue', font=('arial',18,'bold'))
adst_entRno = Entry(adst, bd=5, font=('arial',18,'bold'))
adst_lblName = Label(adst, text='Enter Name: ', bg='lightblue', font=('arial',18,'bold'))
adst_entName = Entry(adst, bd=5, font=('arial',18,'bold'))
adst_lblMarks = Label(adst, text='Enter Marks: ', bg='lightblue', font=('arial',18,'bold'))
adst_entMarks = Entry(adst, bd=5, font=('arial',18,'bold'))
adst_btnSave = Button(adst, text='Save', font=('arial',18,'bold'), command=f8)
adst_btnBack = Button(adst, text='Back', font=('arial',18,'bold'), command=f2)

adst_lblRno.pack(pady=5)
adst_entRno.pack(pady=5)
adst_lblName.pack(pady=5)
adst_entName.pack(pady=5)
adst_lblMarks.pack(pady=5)
adst_entMarks.pack(pady=5)
adst_btnSave.pack(pady=5)
adst_btnBack.pack(pady=5)

adst.withdraw()


#View Student Window

vist = Toplevel(root)
vist.title("View St.")
vist.geometry("400x450+400+100")
vist.resizable(False, False)
vist.configure(background='orange')

vist_stData = ScrolledText(vist, width=30, height=10, font=('arial',15,'bold'))
vist_btnBack = Button(vist, text="Back", font=('arial',18,'bold'), command=f3)

vist_stData.pack(pady=10)
vist_btnBack.pack(pady=10)

vist.withdraw()


#Update Student Window

udst = Toplevel(root)
udst.title("Update St.")
udst.geometry("500x400+400+100")
udst.resizable(False, False)
udst.configure(background='pink')

udst_lblRno = Label(udst, text='Enter Rno: ', bg='pink', font=('arial',18,'bold'))
udst_entRno = Entry(udst, bd=5, font=('arial',18,'bold'))
udst_lblName = Label(udst, text='Enter Name: ', bg='pink', font=('arial',18,'bold'))
udst_entName = Entry(udst, bd=5, font=('arial',18,'bold'))
udst_lblMarks = Label(udst, text='Enter Marks: ', bg='pink', font=('arial',18,'bold'))
udst_entMarks = Entry(udst, bd=5, font=('arial',18,'bold'))
udst_btnSave = Button(udst, text='Save', font=('arial',18,'bold'), command=f11)
udst_btnBack = Button(udst, text='Back', font=('arial',18,'bold'), command=f5)

udst_lblRno.pack(pady=5)
udst_entRno.pack(pady=5)
udst_lblName.pack(pady=5)
udst_entName.pack(pady=5)
udst_lblMarks.pack(pady=5)
udst_entMarks.pack(pady=5)
udst_btnSave.pack(pady=5)
udst_btnBack.pack(pady=5)

udst.withdraw()



#Delete Student Window
dlst = Toplevel(root)
dlst.title("Delete St.")
dlst.geometry("500x400+400+100")
dlst.resizable(False, False)
dlst.configure(background='sky blue')



dlst_lblRno = Label(dlst, text="Enter Rno.", bg='sky blue', font=('arial',18,'bold'))
dlst_entRno = Entry(dlst, bd=5, font=('arial',18,'bold'))
dlst_btnSave = Button(dlst, text='Save', font=('arial',18,'bold'), command=f10)
dlst_btnBack = Button(dlst, text='Back', font=('arial',18,'bold'),command=f7)

dlst_lblRno.pack(pady=10) 
dlst_entRno.pack(pady=10) 
dlst_btnSave.pack(pady=10)
dlst_btnBack.pack(pady=10)

dlst.withdraw()

root.mainloop()
