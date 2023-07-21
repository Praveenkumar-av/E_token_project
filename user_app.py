from tkinter import *

import mysql.connector

class Order_app :
    def __init__(self,root) :
        self.root=root
        root.title('Order')
        # frame for login page
        self.home_frame=Frame(self.root,height=400,width=500,bg='cornsilk')
        self.home_frame.propagate(0)
        self.home_frame.pack()

        # label about the app
        self.home_lbl1=Label(self.home_frame,text='Welcome to ABC app',width=20,height=1,font=('Courier',-30,'bold'),fg='blue',bg='yellow')
        self.home_lbl2=Label(self.home_frame,text='Order anywhere from this app!',width=35,height=1,font=('arial',-14,'bold'),fg='violet',bg='cornsilk')
        self.home_lbl1.pack(side=TOP,pady=10)
        self.home_lbl2.pack(side=TOP,pady=10)

        # login and clase button
        self.b_login=Button(self.home_frame,text='login',width=14,height=2,bg='white',fg='blue',activebackground='green',activeforeground='red',command=lambda:self.Destroy_frame(self.home_frame,Login))
        self.b_close=Button(self.home_frame,text='Close',width=14,height=2,bg='red',fg='white',activebackground='green',activeforeground='red',command=quit)
        self.b_close.pack(side=BOTTOM,pady=15)
        self.b_login.pack(side=BOTTOM,pady=5)
    
    def Destroy_frame(self,current,next) :
        '''This method destroys the current frame and calls the next frame'''
        current.destroy()
        next()

class Login(Order_app) :
    def __init__(self) :
        # connect to mySQL database
        self.conn=mysql.connector.connect(host='localhost',database='student_data',user='root',password='2077')
        # prepare a cursor
        self.cursor=self.conn.cursor()
        # executing query
        self.cursor.execute('Select Roll_no, Password from roll_no')

        # get all rows and store in data instance
        self.data={}
        for row in self.cursor.fetchall() :
            self.data[row[0]]=row[1]

        self.cursor.close()
        self.conn.close()

        self.login_page()

    def login_page(self) :
        '''This method is for login page'''
        self.login_frame=Frame(height=400,width=500,bg='aquamarine')
        self.login_frame.propagate(0)
        self.login_frame.pack()
        
        # Entry box and label
        self.user_lbl=Label(text='Enter the Username :')
        self.pass_lbl=Label(text='Enter the Password :')
        self.user_ent=Entry(self.login_frame,width=25,fg='blue',bg='white',font=('Arial',14))
        self.pass_ent=Entry(self.login_frame,width=25,fg='blue',bg='white',font=('Arial',14),show='*')

        self.user_lbl.place(x=50,y=100)  # username label
        self.user_ent.place(x=200,y=100) # username entry
        self.pass_lbl.place(x=50,y=150)  # password label
        self.pass_ent.place(x=200,y=150)  # password entry

        # Next button 
        self.next_b=Button(self.login_frame,text='Next',width=14,height=2,bg='brown',fg='white',activebackground='green',activeforeground='red',command=self.display)
        self.next_b.pack(side=BOTTOM,pady=10)

    def display(self) :
        # retrieve the values from entry objects
        self.username=self.user_ent.get()
        self.password=self.pass_ent.get()

        # check for username and password
        if self.username=='' or self.password=='' :
            error_login=Label(self.login_frame,text='Enter username and password',font=('arial',-14,),fg='red',bg='aquamarine')
            error_login.place(x=150,y=300)
        else :
            if self.username in self.data :
                if self.data[self.username]==self.password :
                    print('PASS')
                else :
                    try : error_login.destroy() 
                    except : pass
                    error_login=Label(self.login_frame,text='incorrect password!',font=('arial',-14,),fg='red',bg='aquamarine')
                    error_login.place(x=150,y=300)
            else :
                try : error_login.destroy() 
                except : pass
                error_login=Label(self.login_frame,text='Username does not exist!',font=('arial',-14,),fg='red',bg='aquamarine')
                error_login.place(x=150,y=300)

root=Tk()
start=Order_app(root)
root.mainloop()