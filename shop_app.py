from tkinter import *

import mysql.connector

class ShopApp :
    def __init__(self,root) :
        self.root=root
        root.title('Deliver app')
        # frame for login page
        self.home_frame=Frame(self.root,height=400,width=500,bg='cornsilk')
        self.home_frame.propagate(0)
        self.home_frame.pack()

        # label about the app
        self.home_lbl1=Label(self.home_frame,text='Welcome to ABC shop',width=20,height=1,font=('Courier',-30,'bold'),fg='blue',bg='yellow')
        self.home_lbl2=Label(self.home_frame,text='You can get your food here!',width=35,height=1,font=('arial',-14,'bold'),fg='violet',bg='cornsilk')
        self.home_lbl1.pack(side=TOP,pady=10)
        self.home_lbl2.pack(side=TOP,pady=10)

        # login and class button
        self.b_login=Button(self.home_frame,text='login',width=14,height=2,bg='white',fg='blue',activebackground='green',activeforeground='red',command=self.callnext)
        self.b_close=Button(self.home_frame,text='Close',width=14,height=2,bg='red',fg='white',activebackground='green',activeforeground='red',command=quit)
        self.b_close.pack(side=BOTTOM,pady=15)
        self.b_login.pack(side=BOTTOM,pady=5)

    def callnext(self) :
        self.home_frame.destroy()
        Login()

class Login(ShopApp) :
    def __init__(self) :
        # connect to mySQL database - student_data
        self.conn=mysql.connector.connect(host='localhost',database='student_data',user='root',password='2077')
        # prepare a cursor
        self.cursor=self.conn.cursor()
        # executing query
        self.cursor.execute('Select Roll_no, Id, Items from student')

        # get all rows and store in data instance
        self.data={}
        for row in self.cursor.fetchall() :
            if not row[1]==None :
                self.data[row[0]]=list(row)
                self.data[row[0]].pop(0)

        self.cursor.close()
        self.conn.close()

        self.login_page()

    def login_page(self) :
        '''This method is for login page'''
        self.login_frame=Frame(height=400,width=500,bg='aquamarine')
        self.login_frame.propagate(0)
        self.login_frame.pack()
        
        # Entry box and label
        self.user_lbl=Label(self.login_frame,text='Enter the Username :')
        self.id_lbl=Label(self.login_frame,text='Enter the Order id :')
        self.user_ent=Entry(self.login_frame,width=25,fg='blue',bg='white',font=('Arial',14))
        self.id_ent=Entry(self.login_frame,width=25,fg='blue',bg='white',font=('Arial',14))

        self.user_lbl.place(x=50,y=100)  # username label
        self.user_ent.place(x=200,y=100) # username entry
        self.id_lbl.place(x=50,y=150)  # id label
        self.id_ent.place(x=200,y=150)  # id entry

        # Next button 
        self.next_b=Button(self.login_frame,text='Next',width=14,height=2,bg='Orange',fg='white',activebackground='green',activeforeground='red',command=self.display)
        self.next_b.place(x=360,y=338)

        # cancel button
        self.login_cancel=Button(self.login_frame,text='Cancel',width=14,height=2,bg='red',fg='white',activebackground='green',activeforeground='red',command=quit)
        self.login_cancel.pack(side=BOTTOM,pady=20)

    def display(self) :
        # retrieve the values from entry objects
        self.username=self.user_ent.get()
        self.id=self.id_ent.get()

        # check for username and password
        if self.username=='' or self.id=='' :
            self.error_login=Label(self.login_frame,text='Enter username and id!',font=('arial',-14),fg='red',bg='aquamarine')
            self.error_login.place(x=150,y=300)
        else :
            if self.username in self.data :
                if self.data[self.username][0]==self.id :
                    self.login_frame.destroy()
                    ShowData(self.username,self.data)
                else :
                    try : self.error_login.destroy() 
                    except : pass
                    self.error_login=Label(self.login_frame,text='incorrect order id!',font=('arial',-14),fg='red',bg='aquamarine')
                    self.error_login.place(x=150,y=300)
            else :
                try : self.error_login.destroy() 
                except : pass
                self.error_login=Label(self.login_frame,text='Order not found!',font=('arial',-14),fg='red',bg='aquamarine')
                self.error_login.place(x=150,y=300)

class ShowData :
    def __init__(self,username,data) :
        self.data_frame=Frame(height=400,width=500,bg='aquamarine')
        self.data_frame.propagate(0)
        self.data_frame.pack()

        # connect to mySQL database - student_data
        self.conn=mysql.connector.connect(host='localhost',database='student_data',user='root',password='2077')
        # prepare a cursor
        self.cursor=self.conn.cursor()
        # executing query
        self.cursor.execute('Select Items from stock')

        # get all rows and store in instance
        self.itemlst=[]
        for i in self.cursor.fetchall() :
            self.itemlst+=i

        self.cursor.close()
        self.conn.close()

        # Label 
        self.show_lbl=Label(self.data_frame,text='Your Order',font='Calibri 16',fg='green',bg='white')
        self.show_lbl.place(x=50,y=50)

        self.username=username

        # Text box of to show selected items
        self.show_order=Text(self.data_frame,width=14,height=10,wrap=WORD)
        self.show_order.place(x=50,y=100)

        # index of items
        self.itemsIndex=data[self.username][1].split(',')

        for i in self.itemsIndex :
            self.show_order.insert(END,self.itemlst[int(i)]+'\n') 

        # connect to mySQL database - student_data
        self.conn=mysql.connector.connect(host='localhost',database='student_data',user='root',password='2077')
        # prepare a cursor
        self.cursor=self.conn.cursor()
        # executing query
        try :
            self.cursor.execute("update student set Id='', Items='' where Roll_no='%s'"%(self.username))
            self.conn.commit()
        except :
            # rollback if there is any error
            self.conn.rollback()
        finally :
            # close connection
            self.cursor.close()
            self.conn.close()

root=Tk()
obj=ShopApp(root)
root.mainloop()