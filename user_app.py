from tkinter import *

import mysql.connector

class OrderApp :
    def __init__(self,root) :
        self.root=root
        root.title('Order')
        # frame for login page
        self.home_frame=Frame(self.root,height=400,width=500,bg='cornsilk')
        self.home_frame.propagate(0)
        self.home_frame.pack()

        # label about the app
        self.home_lbl1=Label(self.home_frame,text='Welcome to E token app',width=23,height=1,font=('Courier',-30,'bold'),fg='white',bg='green')
        self.home_lbl2=Label(self.home_frame,text='Order anywhere from this app!',width=35,height=1,font=('arial',-14,'bold'),fg='violet',bg='cornsilk')
        self.home_lbl1.pack(side=TOP,pady=10)
        self.home_lbl2.pack(side=TOP,pady=10)

        # login and class button
        self.b_login=Button(self.home_frame,text='login',width=14,height=2,bg='white',fg='blue',activebackground='green',activeforeground='red',command=self.callLogin)
        self.b_close=Button(self.home_frame,text='Close',width=14,height=2,bg='red',fg='white',activebackground='green',activeforeground='red',command=quit)
        self.b_close.pack(side=BOTTOM,pady=15)
        self.b_login.pack(side=BOTTOM,pady=5)
    
    def callLogin(self) :
        '''This method destroys the current frame and calls the next frame'''
        self.home_frame.destroy()
        Login()

class Login(OrderApp) :
    def __init__(self) :
        # connect to mySQL database - student_data
        self.conn=mysql.connector.connect(host='localhost',database='student_data',user='root',password='2077')
        # prepare a cursor
        self.cursor=self.conn.cursor()
        # executing query
        self.cursor.execute('Select Roll_no, Password from student')

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
        self.user_lbl=Label(self.login_frame,text='Enter the Username :',bg='aquamarine')
        self.pass_lbl=Label(self.login_frame,text='Enter the Password :',bg='aquamarine')
        self.user_ent=Entry(self.login_frame,width=25,fg='blue',bg='white',font=('Arial',14))
        self.pass_ent=Entry(self.login_frame,width=25,fg='blue',bg='white',font=('Arial',14),show='*')

        self.user_lbl.place(x=50,y=100)  # username label
        self.user_ent.place(x=200,y=100) # username entry
        self.pass_lbl.place(x=50,y=150)  # password label
        self.pass_ent.place(x=200,y=150)  # password entry

        # Next button 
        self.next_b=Button(self.login_frame,text='Next',width=14,height=2,bg='Orange',fg='white',activebackground='green',activeforeground='red',command=self.display)
        self.next_b.place(x=360,y=338)

        # cancel button
        self.login_cancel=Button(self.login_frame,text='Cancel',width=14,height=2,bg='red',fg='white',activebackground='green',activeforeground='red',command=quit)
        self.login_cancel.pack(side=BOTTOM,pady=20)

    def display(self) :
        # retrieve the values from entry objects
        self.username=self.user_ent.get()
        self.password=self.pass_ent.get()

        # check for username and password
        if self.username=='' or self.password=='' :
            try : self.error_login.destroy() 
            except : pass
            self.error_login=Label(self.login_frame,text='Enter username and password',font=('arial',-14,),fg='red',bg='aquamarine')
            self.error_login.place(x=150,y=300)
        else :
            if self.username in self.data :
                if self.data[self.username]==self.password :
                    self.login_frame.destroy()
                    ItemSelection(self.username)
                else :
                    try : self.error_login.destroy() 
                    except : pass
                    self.error_login=Label(self.login_frame,text='incorrect password!',font=('arial',-14,),fg='red',bg='aquamarine')
                    self.error_login.place(x=150,y=300)
            else :
                try : self.error_login.destroy() 
                except : pass
                self.error_login=Label(self.login_frame,text='Username does not exist!',font=('arial',-14,),fg='red',bg='aquamarine')
                self.error_login.place(x=150,y=300)

class ItemSelection() :
    def __init__(self,username) :
        # connect to mySQL database - student_data
        self.conn=mysql.connector.connect(host='localhost',database='student_data',user='root',password='2077')
        # prepare a cursor
        self.cursor=self.conn.cursor()
        # executing query
        self.cursor.execute('Select * from stock')

        # get purchase items from database and store in items
        self.items=[]
        for row in self.cursor.fetchall() :
            self.items.append(list(row))

        self.cursor.close()
        self.conn.close()

        # call select method for items selection
        self.select()
        self.username=username

    def select(self) :
        self.selection_frame=Frame(height=400,width=500,bg='aquamarine')
        self.selection_frame.propagate(0)
        self.selection_frame.pack()

        # create label 
        self.select_lbl=Label(self.selection_frame,text='Select one or more items you want below',font='Calibri 14')
        self.select_lbl.pack(side=TOP,pady=10)

        self.show_Items=Label(self.selection_frame,text='Items',font='Arial 20 bold')
        self.show_price=Label(self.selection_frame,text='Price',font='Arial 20 bold')
        self.show_Items.place(x=20,y=80)
        self.show_price.place(x=220,y=80)

        # create list box with names and price
        self.select_lst=Listbox(self.selection_frame,font='Arial 12 bold',fg='blue',bg='yellow',height=10,selectmode=MULTIPLE)
        self.select_lst.pack(side=LEFT,padx=15)
        self.item_price=Listbox(self.selection_frame,font='Arial 12 bold',fg='blue',bg='white',height=10)
        self.item_price.pack(side=LEFT)
        
        for i in self.items :
            self.select_lst.insert(END,i[0])
        for i in self.items :
            self.item_price.insert(END,i[1])

        self.select_lst.bind('<<ListboxSelect>>',self.on_select)


    def call_frame(self) :
        self.selection_frame.destroy()
        Purchase(self.indexes,self.items,self.username)
        
    def on_select(self,event) :
        '''This method stores the selected items in the Listbox'''
        # know the indexes of the selected items  
        self.indexes=self.select_lst.curselection()
        if len(self.indexes)>0 :
            # Next button
            try : self.next.destroy()
            except : pass
            self.next=Button(self.selection_frame,text='next',width=14,height=2,bg='green',fg='black',activebackground='green',activeforeground='red',command=self.call_frame)
            self.next.pack(side=BOTTOM,padx=10,pady=10)
        else :
            try : self.next.destroy()
            except : pass

class Purchase(Login) :
    def __init__(self,indexes,items,username) :
        self.purchase_frame=Frame(height=400,width=500,bg='cornsilk')
        self.purchase_frame.propagate(0)
        self.purchase_frame.pack()
        
        # Label 
        self.show_lbl=Label(self.purchase_frame,text='You selected',font='Calibri 16',fg='green',bg='white')
        self.show_lbl.place(x=50,y=50)

        self.username=username
        # Text box of to show selected items
        self.indexes=indexes
        self.items=items

        self.show_order=Text(self.purchase_frame,width=14,height=10,wrap=WORD)
        self.show_order.place(x=50,y=100)

        for i in self.indexes :
            self.show_order.insert(END,self.items[i][0]+'\n')
        
        self.cost=0
        for i in self.indexes :
            self.cost+=self.items[i][1]

        # show price label
        self.cost_lbl=Label(self.purchase_frame,text='Total cost :',font='Arial 20')
        self.cost_lbl.place(x=200,y=100)
        self.cost_lbl=Label(self.purchase_frame,text=f'Rs.{self.cost}',font='Arial 20 bold')
        self.cost_lbl.place(x=350,y=100)

        # paid button
        self.var1=IntVar()
        self.paid_b=Checkbutton(self.purchase_frame,text='paid',width=14,height=2,variable=self.var1,command=self.payment)
        self.paid_b.pack(side=BOTTOM,pady=20)

        # purchase button
        self.purchase_b=Button(self.purchase_frame,text='Purchase',width=14,height=2,bg='orange',fg='black',command=self.order_id)
        self.purchase_b.place(x=340,y=340)

        self.purchased=''
        for i in self.indexes :
            self.purchased+=str(i)+','

        self.purchased=self.purchased[0:len(self.purchased)-1]  # removing last comma

        # close window button
        self.b_close=Button(self.purchase_frame,text='Close',width=14,height=2,bg='red',fg='white',activebackground='green',activeforeground='red',command=quit)
        self.b_close.place(x=50,y=340)
        
        self.pay=0
    def payment(self) :
        x=self.var1.get()
        if x==1 :
            self.pay=1
    
    def order_id(self) :
        '''This method verifies the payment and add order id to the customer'''
        if self.pay==1 :
            self.id=''
            from random import randint
            str='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
            for i in range(8) :
                self.id+=str[randint(0,35)]

            try : self.error_lbl.destroy() 
            except : pass
            self.id_lbl=Label(self.purchase_frame,text=f'Order id: {self.id}',font='arial 16')
            self.id_lbl.place(x=220,y=240)

            # destroy lable if purchased
            self.purchase_b.destroy()
            self.purchased_lbl=Label(self.purchase_frame,text='Purchased!',font='arial 16')
            self.purchased_lbl.place(x=340,y=345)

            # connect to mySQL database - student_data
            self.conn=mysql.connector.connect(host='localhost',database='student_data',user='root',password='2077')
            # prepare a cursor
            self.cursor=self.conn.cursor()
            # executing query
            # prepare SQL query string to update a Id and Items
            try :
                self.cursor.execute("update student set Id='%s', Items='%s' where Roll_no='%s'"%(self.id,self.purchased,self.username))
                self.conn.commit()
            except :
                # rollback if there is any error
                self.conn.rollback()
            finally :
                # close connection
                self.cursor.close()
                self.conn.close()
            
        else :
            self.error_lbl=Label(self.purchase_frame,text='Please make purchase',font='arial 16')
            self.error_lbl.place(x=220,y=250)

root=Tk()
start=OrderApp(root)
root.mainloop()