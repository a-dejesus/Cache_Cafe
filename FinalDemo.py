 #-------------------------------------------------
### Cache Cafe
### Facial Recognition Coffee Machine using raspberry pi
### & Jetson Nano for Facial Recognition & Servo Motors for dispensing
### Creators: Abner De Jesus, Israel Diaz, Genevieve Kelleher, Andres Centeno
### CSULB College of Engineering Students
### Major: Computer Engineering
### Class: CECS 490A & 490B Senior Project
### Dates: 8/2020 - 5/2021
 #-------------------------------------------------
# import for servo motors 
import RPi.GPIO as GPIO
import serial
import time
import sys
import string

# import for TKInter
import tkinter as tk
from tkinter.font import Font
from tkinter import *
from tkinter import ttk
import tkinter.scrolledtext as scrolledtext
from tkinter import simpledialog

global flag

# Define font style and size for buttons and labels
CacheCafeFont = ("URW Chancery L", 42)
welcomeFont = ("URW Bookman L", 25)
prefferncesFont = ("URW Bookman L", 19)
buttonFont = ("URW Bookman L", 15)


# Page Container - configures all pages/windows 
class PageContainer(tk.Tk):

    def __init__(self, *args, **kwargs):
        global check
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        tk.Tk.geometry(self,'800x480')
        self.Name=StringVar()
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree,
                  PageFour, PageFive, PageSix):

            frame = F(container, self)
            self.frames[F] = frame
            frame.config(bg = "#c9ab85")
            frame.grid(row=0, column=0, sticky="nsew")
            
        # begins the program with StartPage
        self.show_frame(StartPage)

    def get_page(self,page_class):
        return self.frames[page_class]
    # show frame raises any new frame or window 
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
            
class StartPage(tk.Frame):
    ### Home Page : provides user with three different paths :
    #   Activate Facial Recognition, Create a Profile, Edit Profile
    def __init__(self, parent, controller):
        self.controller=controller
        tk.Frame.__init__(self,parent)
        #color = tk.Frame(bg = "black")
        global Name, Flav, Size, Amount
        Name=tk.StringVar()
        Flav=tk.StringVar()
        Size=tk.StringVar()
        Amount=tk.StringVar()
        welcometext=tk.StringVar()
        buttontext = tk.StringVar()
        button2text=tk.StringVar()
        # Creation and placement of labels
        header = tk.Label(self, text="Cache Cafe", font= CacheCafeFont, bg = "#c9ab85")
        header.place(x = 285, y = 90)
        welcome = tk.Label(self, textvariable = welcometext, font = welcomeFont, bg = "#c9ab85")
        welcometext.set("Welcome!")
        button2text.set("Create a New\n Profile")
        welcome.place(x = 320, y = 190)

        # Brew - If the users face is not recognized, an error message will be displayed
        # If the users face is recognized, the users profile informaion will be read
        # and the dispsenser function will be called 
        def Brew(counter):
            if counter == 100:
                welcometext.set("User Doesn't have a Profile")
                welcome.place(x=275,y=190)
                time.sleep(.1)
                tk.Tk.update_idletasks(self)
                time.sleep(3)
                welcometext.set("Welcome!")
                welcome.place(x=320,y=190)
                tk.Tk.update_idletasks(self)
                return counter
            else:
                welcometext.set("Dispensing Beverage, Please Wait")
                welcome.place(x=125,y=190)
                tk.Tk.update_idletasks(self)
                getprofilename(counter) #updates global variable name
                getprofileinfo(counter) #give values to our global dispenser variables
                dispenser() #operate our dispenser based on the dispenser variables updated in getprofileinfo
                welcometext.set("Welcome!")
                welcome.place(x=320,y=190)
                
        # ActivateCam1 - If the user chooses to activate the camera, a flag will be sent
        # to the Jetson Nano to activate the facial recognition camera
        # a message displays letting the user know their face is being detected
        def ActivateCam1():
            global flag
            # Reinstate buttons on the start page
            welcometext.set("Detecting User")
            welcome.place(x=290,y=190)
            buttontext.set("Activate Facial\n Recognition")
            ActivateF.place(x = 150, y = 270)
            button2text.set("Create a New\n Profile")
            Create.place(x = 420, y = 270)
            # Allows above tasks to be ran and set 
            tk.Tk.update_idletasks(self)
            # Sends value 2 to activate camera to scan face
            UARTtransmit(2)
            flag=UARTreceive()
            # When 30 users have Created their Profile don't allow more
            if flag==30:
                print("User max has been reached")
            else:
                return flag
        
        def message():
            # This message box prompts the user to face the camera or allows the user to cancel the activation
            # of the camera. When the user clicks the ok button, the camera will be activated
            global response
            #This creates the message box and displays our message
            response = messagebox.askokcancel(message="Please Face the Camera and \n Click ok when Ready!!!")
            if response:
                welcometext.set("Detecting User")
                welcome.place(x=290,y=190)
                buttontext.set("Activate Facial\n Recognition")
                ActivateF.place(x = 150, y = 270)
                button2text.set("Create a New\n Profile")
                Create.place(x = 420, y = 270)
                time.sleep(.1)
                #Allows above tasks to be ran and set
                tk.Tk.update_idletasks(self)
            return response
        
        def ActivateCam2():
            # ActivateCam2 - If the user chooses to Create a profile, a flag will be sent
            # to the Jetson Nano to activate the facial recognition camera
            # a message displays letting the user know their face is being detected

            global flag
            welcometext.set("Detecting User")
            welcome.place(x=290,y=190)
            buttontext.set("Activate Facial\n Recognition")
            ActivateF.place(x = 150, y = 270)
            button2text.set("Create a New\n Profile")
            Create.place(x = 420, y = 270)
            #Allows above tasks to be ran and set
            tk.Tk.update_idletasks(self)
            #Sends value 1 to activate cam and scan face. 
            UARTtransmit(1)
            flag=UARTreceive()
            #Only allow for 30 users to be created
            if flag==30:
                print("User max has been reached")
            elif flag==100:
                welcometext.set("User Already Has a Profile")
                welcome.place(x=200,y=190)
                #Allows above tasks to be ran and set
                time.sleep(.1)
                tk.Tk.update_idletasks(self)
                time.sleep(.3)
                welcometext.set("Welcome!")
                welcome.place(x=320,y=190)
                tk.Tk.update_idletasks(self)
            else:
                welcometext.set("Welcome!")
                welcome.place(x=320,y=190)
                tk.Tk.update_idletasks(self)
                return flag

        
        def ActivateCam3():
            # Activate Camera - If the user chooses to edit their profile, a flag will be sent
            # to the Jetson Nano to activate the facial recognition camera
            # a message displays letting the user know their face is being detected
            welcometext.set("Detecting User")
            welcome.place(x=290,y=190)
            buttontext.set("Activate Facial\n Recognition")
            ActivateF.place(x = 150, y = 270)
            button2text.set("Create a New\n Profile")
            Create.place(x = 420, y = 270)
            #Allows above tasks to be run and set
            tk.Tk.update_idletasks(self)
            UARTtransmit(2)
            global flag
            flag=UARTreceive()
            if flag==30:
                print("User max has been reached")
            else:
                return flag
        
        def get_user(counter):
            # Retrieves the user information 
            if counter==100:
                welcometext.set("User Not Found")
                welcome.place(x=275,y=190)
                time.sleep(.1)
                tk.Tk.update_idletasks(self)
                time.sleep(.3)
                welcometext.set("Welcome!")
                welcome.place(x=320,y=190)
                tk.Tk.update_idletasks(self)
            else:
                getprofilename(counter)
                getprofileinfo(counter)
                welcometext.set("Welcome!")
                welcome.place(x=320,y=190)
                # if a flag is recieved, save information
                if (counter<100 | counter>=0):
                    # sets info to allow previous preferences to be shown to the user
                    Name.set(name+"'s Drink:")
                    if crm1>0:
                        Flav.set("of  Vanilla Creamer")
                        Amount.set(crm1)
                    elif crm2>0:
                        Flav.set("of  Chocolate Creamer")
                        Amount.set(crm2)
                    elif crm3>0:
                        Flav.set("of  Hazelnut Creamer")
                        Amount.set(crm3)
                    elif sug>0:
                        Flav.set("of Sugar")
                        Amount.set(sug)
                    else:
                        Flav.set("0")
                        Amount.set("0")
                    if size==1:
                        Size.set("8oz Coffee with")
                    elif size==2:
                        Size.set("12oz Coffee with")
                    elif size==3:
                        Size.set("16oz Coffee with")
                    else:
                        Size.set("0")
                else:
                    Name.set("Previous Drink")
                    Flav.set("0")
                    Amount.set("0")
                    Size.set("None")
                time.sleep(.1)
                tk.Tk.update_idletasks(self)
            return Name,Flav,Amount,Size
        
        def call():
            # Calls for the information needed to show (on GUI) the users previous preferences
            test=self.controller.get_page(PageThree)
            test.Name1.set(Name.get())
            test.Flav1.set(Flav.get())
            test.Amount1.set(Amount.get())
            test.Size1.set(Size.get())

        # Create and place buttons that will pass new pages as parameters as well
        # as call definitions to be executed
        # Pages being passed as parameters depend on the users choice & the facial recognition
        ActivateF = tk.Button(self, textvariable=buttontext, font = buttonFont, bg = "#ebd5ae",
                              width = 15, command=lambda: [message(), (Brew(ActivateCam1()),
                              controller.show_frame(StartPage) if flag==100 else controller.show_frame(PageOne)) if response==True else controller.show_frame(StartPage)])
        buttontext.set("Activate Facial\n Recognition")
        ActivateF.place(x = 150, y = 270)
        
        Create = tk.Button(self, textvariable=button2text, font = buttonFont, bg = "#ebd5ae",
                           width = 15, command=lambda: [message(),(ActivateCam2(),controller.show_frame(StartPage) if flag==100 else controller.show_frame(PageTwo)) if response==True else controller.show_frame(StartPage)])
        Create.place(x = 420, y = 270)

        ChangeProf = tk.Button(self, text="Change my Coffee\n Preference", font = buttonFont,
                            bg = "#ebd5ae", width = 15, command=lambda: [message(), (get_user(ActivateCam3()),call(),controller.show_frame(StartPage) if flag==100 else controller.show_frame(PageFour)) if response==True else controller.show_frame(StartPage)])
        ChangeProf.place(x = 290, y = 380)

        
class PageOne(tk.Frame):
    
### Activate Facial Recognition Page 
    def __init__(self, parent, controller):
        self.controller=controller
        tk.Frame.__init__(self, parent)
        header = tk.Label(self, text="Cache Cafe", font= CacheCafeFont, bg = "#c9ab85")
        header.place(x = 285, y = 90)
        FaceCam = tk.Label(self, text="Beverage is Ready!", font = welcomeFont, bg = "#c9ab85")
        FaceCam.place(x = 250, y = 190)
        
        ### Once the camera is activated it will scan the user. If the users profile is found
        ### the UI will let the user know their face was found and will switch to the next window
        ### If the user is not found, the UI will ask the user to create a profile

        Home = tk.Button(self, text="Back to Home", font = buttonFont, bg = "#ebd5ae", width = 15, 
                            command=lambda: controller.show_frame(StartPage))
        Home.place(x = 295, y = 290)

        
 #-------------------------------------------------
        # Code for Virtual Keyboard
# Create rows and cloumns for each button in the keyboard
def enumerate_row_column(iterable, num_cols):
    for idx, item in enumerate(iterable):
        row = idx // num_cols
        col = idx % num_cols
        yield row,col,item

# Determine when the entry box has been clicked on. 
class NumpadEntry(Entry):
    def __init__(self,parent=None,**kw):
        Entry.__init__(self,parent,**kw)
        self.bind('<FocusIn>',self.numpadEntry)
        self.bind('<FocusOut>',self.numpadExit)
        self.edited = False
    def numpadEntry(self,event):
        if self.edited == False:
            self['bg']= '#ffffcc'
            self.edited = True
            new = numPad(self)
        #else:
            #self.edited = False
    def numpadExit(self,event):
        self['bg']= '#ffffff'

class numPad(simpledialog.Dialog):
    def __init__(self,master=None,textVariable=None):
        self.top = Toplevel(master=master)
        self.top.geometry('+%d+%d'%(10,300))
        self.top.protocol("WM_DELETE_WINDOW",self.ok)
        self.createWidgets()
        self.master = master
        
    # letters used for the buttons
    def createWidgets(self):
        btn_list = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p',
           'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l','   ',
           'z', 'x', 'c', 'v', 'b', 'n', 'm','Space','Delete', 'Done']
        
        # create and position all buttons with a for-loop
        btn = []
        # Use custom generator to give us row/column positions
        for r,c,label in enumerate_row_column(btn_list,10):
            # partial takes care of function and argument
            cmd = lambda x = label: self.click(x)
            # create the button
            cur = Button(self.top, text=label, width=6, height=2,bg = "#ebd5ae", command=cmd)
            # position the button
            cur.grid(row=r, column=c)                                              
            btn.append(cur)

    # Conditinal statements for specific button selections
    def click(self,label):
        if label == 'Delete':
            currentText = self.master.get()
            self.master.delete(0, END)
            self.master.insert(0, currentText[:-1])
        elif label == 'Space':
            self.master.insert(END, ' ')
        elif label == 'Done':
            #self.ok()
            self.top.destroy()
            self.top.master.focus()
            
        else:
            currentText = self.master.get()
            self.master.delete(0, END)
            self.master.insert(0, currentText+label)
 #-------------------------------------------------
      
class PageTwo(tk.Frame):
    ### First Page for Creating a Profile
    def __init__(self, parent, controller):
        self.controller=controller
        tk.Frame.__init__(self, parent)
        header = tk.Label(self, text="Cache Cafe", font= CacheCafeFont, bg = "#c9ab85")
        header.place(x = 285, y = 20)
        # Creates label for user entry
        Name = tk.Label(self, text="Enter your first name: ", font= buttonFont, bg = "#c9ab85")
        Name.place(x = 115, y = 150)
        global username
        global drinkSize

        #------------------------------------------
        # Entry call for virtual keyboard 
        username = StringVar()
        # username = user input
        NameEntry = NumpadEntry(self, textvariable = username)
        NameEntry.place(x = 120, y = 195)
        #------------------------------------------
        
        # Label for drop down menu
        ChooseSize = tk.Label(self, text="Select how many ounces of coffee: ", font= buttonFont, bg = "#c9ab85")
        ChooseSize.place(x = 450, y = 150)
        #Shows the users selection
        def show():
            label.config(text = drinkSize.get())

        # list of options available for the dropdown menu
        options = ["8", "12", "16"]
        # option 8 will be written in the text file as
        # 8oz -> 1, 12oz -> 2, 16oz -> 3
        
        # drinksize = user input
        drinkSize = StringVar()
        drinkSize.set( "Select an option" )
        # Create the dropdown Menu
        drop = OptionMenu(self, drinkSize, *options)
        drop.configure(font= buttonFont, bg = "#ebd5ae")
        drop.place(x = 475, y = 190)
        drop["menu"].configure(bg = "#ebd5ae")
        
        # Create continue button to move on to the next page of profile creation (PageTwo)
        Continue = tk.Button(self, text="Continue", font = buttonFont,
                            bg = "#ebd5ae", width = 15, command=lambda: [controller.show_frame(PageThree)])
        Continue.place(x = 297, y = 260)

        
class PageThree(tk.Frame):
    # Second Pgae of user profile creation
    def __init__(self, parent, controller):
        self.controller=controller
        tk.Frame.__init__(self, parent)
        header = tk.Label(self, text="Cache Cafe", font= CacheCafeFont, bg = "#c9ab85")
        header.place(x = 285, y = 90)
        # Users input for drink flavor and amount of teaspoons
        global drinkFlavor
        global teaspoonsNum
        #----------------------------------
        # Create & position label 
        ChooseDrink = tk.Label(self, text="Select your favorite drink: ", font= buttonFont, bg = "#c9ab85")
        ChooseDrink.place(x = 100, y = 220)
        # shows the users selected option of ceamer flavor and amount of creamer 
        def show():
            label.config(text = drinkFlavor.get())
            label2.config(text = teaspoonsNum.get())
        # Create a list of the flavor selection for the dropdown menu
        options = ["Vanilla", "Chocolate", "Hazelnut", "Sugar"]
        # drinkFlavor = user input
        drinkFlavor = StringVar()
        drinkFlavor.set( "Select an option" )
        # Configure & display dropdown menu
        drop = OptionMenu(self, drinkFlavor, *options)
        drop.configure(font= buttonFont, bg = "#ebd5ae")
        drop.place(x = 100, y = 260)
        drop["menu"].configure(bg = "#ebd5ae")
  
        #-----------------------------------
        # Create & position a label for the user to select the # of teaspoons
        ChooseTeaspoons = tk.Label(self, text="Select the amount of\n teaspoons of flavoring ",
                                   font= buttonFont, bg = "#c9ab85")
        ChooseTeaspoons.place(x = 450, y = 220)
        # Creates a list of the options for amount of teaspoons of flavoring
        amountOptions = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        # teaspoonsNum = user input
        teaspoonsNum = StringVar()
        teaspoonsNum.set( "Select an option" )
        # Configure & Display the dropdown menu for the teaspoon issues
        drop2 = OptionMenu(self, teaspoonsNum, *amountOptions)
        drop2.configure(font= buttonFont, bg = "#ebd5ae")
        drop2.place(x = 450, y = 290)
        drop2["menu"].configure(bg = "#ebd5ae")
        # Create and position "Done" Button which sends the usee to the next page when clicked
        Done = tk.Button(self, text="Save Info", font = buttonFont,
                           bg = "#ebd5ae", width = 15, command=lambda: [register_user(), controller.show_frame(PageSix)])
        Done.place(x = 295, y = 350)
 
# Register_User saves the users coffee preferences to a text file
# in the desire format
# There is a dispenser corresponding to each -> crm1 crm2 crm3 and suagr
def register_user():
    # Vanilla = Crm 1
    # Choclate = Crm 2
    # Hazelnut = Crm 3
    # Just Sugar = Sugar
    global crm1,crm2,crm3,sug,size
    # get the users inputted information
    username_info = username.get()
    flavor = drinkFlavor.get()
    teaspoons = teaspoonsNum.get()
    ounces = drinkSize.get()
    # if flavor = Vanilla  -> crm 1 will have the # of teaspoons and the other dispensers will dispense 0 teaspoons
    if flavor == "Vanilla":
        crm1 = teaspoons
        crm2 = '0'
        crm3 = '0'
        sugar = '0'
    # if flavor = Chocolate  -> crm 2 will have the # of teaspoons and the other dispensers will dispense 0 teaspoons
    elif flavor == "Chocolate":
        crm1 = '0'
        crm2 = teaspoons
        crm3 = '0'
        sugar = '0'
    # if flavor = Hazelnut  -> crm 3 will have the # of teaspoons and the other dispensers will dispense 0 teaspoons
    elif flavor == "Hazelnut":
        crm1 = '0'
        crm2 = '0'
        crm3 = teaspoons
        sugar = '0'
    # if flavor = Sugar  -> crm 4 will have the # of teaspoons and the other dispensers will dispense 0 teaspoons
    elif flavor == "Sugar":
        crm1 = '0'
        crm2 = '0'
        crm3 = '0'
        sugar = teaspoons
    # if the user does not select an option from the dropdown menu
    # The default value of flavor will be 0 which results in 0 teaspoons of
    # coffee creamer or sugar
    elif flavor == "Select an option":
        crm1 = '0'
        crm2 = '0'
        crm3 = '0'
        sugar = '0'
        
    # if the user selects 8oz, the number saved in the profile will be 1
    if ounces == "8":
        size = '1'
    # if the user selects 8oz, the number saved in the profile will be 2
    elif ounces == "12":
        size = '2'
    # if the user selects 8oz, the number saved in the profile will be 3
    elif ounces == "16":
        size = '3'
    # if the user does not select an option from the dropdown menu
    # The default value of size will be 1 (8oz)
    elif ounces == "Select an option":
        size = '1'
        
    # string of empty space
    space = "".join(' ' for i in range(20-len(username_info)))
    # Profile will contain the following items
    profile = crm1+crm2+crm3+sugar+size
    file = open("CoffeeProfiles.txt", "a")
    file.write(username_info+space+profile+'\n')
    file.close()

### This function allows the user to change their user profile preferences.
### The function will get the users input and save the preferences in the
### desired format [name crm1 crm2 crm3 sugar size]
### The name will remain the same but the users new prefernces will replace
### the previous preferences
### There is a dispenser corresponding to each -> crm1 crm2 crm3 and suagr
def edit_user(counter):
    # Get the users NEW preferences 
    flavor = newDrink.get()
    teaspoons = newAmount.get()
    ounces = newSize.get()
    # if flavor = Vanilla  -> crm 1 will have the # of teaspoons and the other dispensers will dispense 0 teaspoons
    if flavor == "Vanilla":
        crm1 = teaspoons
        crm2 = '0'
        crm3 = '0'
        sugar = '0'
    # if flavor = Chocolate  -> crm 2 will have the # of teaspoons and the other dispensers will dispense 0 teaspoons
    elif flavor == "Chocolate":
        crm1 = '0'
        crm2 = teaspoons
        crm3 = '0'
        sugar = '0'
    # if flavor = Hazelnut  -> crm 3 will have the # of teaspoons and the other dispensers will dispense 0 teaspoons
    elif flavor == "Hazelnut":
        crm1 = '0'
        crm2 = '0'
        crm3 = teaspoons
        sugar = '0'
    # if flavor = Sugar  -> crm 4 will have the # of teaspoons and the other dispensers will dispense 0 teaspoons
    elif flavor == "Sugar":
        crm1 = '0'
        crm2 = '0'
        crm3 = '0'
        sugar = teaspoons
    # if the user does not select an option from the dropdown menu
    # The default value of flavor will be 0 which results in 0 teaspoons of
    # coffee creamer or sugar
    elif flavor == "Select an option":
        crm1 = '0'
        crm2 = '0'
        crm3 = '0'
        sugar = '0'
        
    # if the user selects 8oz, the number saved in the profile will be 1
    if ounces == "8":
        size = '1'
    # if the user selects 8oz, the number saved in the profile will be 2
    elif ounces == "12":
        size = '2'
    # if the user selects 8oz, the number saved in the profile will be 3
    elif ounces == "16":
        size = '3'
    # if the user does not select an option from the dropdown menu
    # The default value of size will be 1 (8oz)
    elif ounces == "Select an option":
        size = '1'
        
    # save the format of profile preferences (to be saved in the text file) to variable menu
    menu = crm1+crm2+crm3+sugar+size
    #open file for reading and writing
    prf = open("CoffeeProfiles.txt","r+")
    #lines is a list of with all the lines
    lines = prf.readlines()
    #line for current profile copied to profileline
    profileline = lines[counter]
    #new profile name is unchanged characters, new menu, and new line
    newprofileline = profileline[0:20]+menu+"\n"
    lines[counter] = newprofileline
    prf.seek(0,0)
    prf.writelines(lines)
    prf.close()
    print("Your drink preferences have been updated.")


class PageFour(tk.Frame):
    ### Display current coffee preferences from previously saved profile
    ### Allow user to enter the new information to change their drink preferences
    def __init__(self, parent, controller):
        global Name1
        tk.Frame.__init__(self, parent)
        header = tk.Label(self, text="Cache Cafe", font= CacheCafeFont, bg = "#c9ab85")
        header.place(x = 285, y = 50)
        # Retrieve users profile information & use as strings to display in the GUI
        self.controller=controller
        self.Name1=tk.StringVar()
        self.Flav1=tk.StringVar()
        self.Size1=tk.StringVar()
        self.Amount1=tk.StringVar()
        self.Name1.set(self.controller.Name)
        self.Flav1.set(self.controller.Name)
        self.Amount1.set(self.controller.Name)
        self.Size1.set(self.controller.Name)
        
        def change_name():
            Name1.set(Name.get())
            time.sleep(.4)
            tk.Tk.update_idletasks(self)
            
        time.sleep(.4)
        tk.Tk.update_idletasks(self)
        # Create & display labels showing the users previous coffee preferences that
        # were stored in their profile
        of = tk.Label(self, text= "teaspoons" , font= prefferncesFont, bg = "#c9ab85")
        of.place(x = 295, y = 190)
        
        PrevPref = tk.Label(self, textvariable= self.Name1, font= prefferncesFont, bg = "#c9ab85")
        PrevPref.place(x = 60, y = 140)
        
        PrevFlav= tk.Label(self, textvariable= self.Flav1, font= prefferncesFont, bg = "#c9ab85")
        PrevFlav.place(x = 430, y = 190)
        
        PrevSize = tk.Label(self, textvariable= self.Size1, font= prefferncesFont, bg = "#c9ab85")
        PrevSize.place(x = 60, y = 190)
        
        PrevAmount = tk.Label(self, textvariable= self.Amount1, font= prefferncesFont, bg = "#c9ab85")
        PrevAmount.place(x = 275, y = 190)
        
        NewChoice = tk.Label(self, text="Select a New Drink: ", font= buttonFont, bg = "#c9ab85")
        NewChoice.place(x = 285, y = 250)
        
        NewChoice2 = tk.Label(self, text="Select a New Size: ", font= buttonFont, bg = "#c9ab85")
        NewChoice2.place(x = 60, y = 250)
        
        NewChoice3 = tk.Label(self, text="Select Flavoring Amount: ", font= buttonFont, bg = "#c9ab85")
        NewChoice3.place(x = 510, y = 250)
        
        global newDrink
        global newSize
        global newAmount
        #-----------------------------------
        def show():
            label.config(text = newDrink.get())
            label2.config(text = newSize.get())
            label3.config(text = newAmount.get())

        # Creates a dropdown list to show the flavored creamers
        # for the user to select ( Select a new flavor)
        options = ["Vanilla", "Chocolate", "Hazelnut", "Sugar"]
        # users new flavor input
        newDrink = StringVar()
        newDrink.set( "Select an option" )
        # Configure & Display Dropdown Menu
        drop = OptionMenu(self, newDrink, *options)
        drop.configure(font= buttonFont, bg = "#ebd5ae")
        drop.place(x = 285, y = 300)
        drop["menu"].configure(bg = "#ebd5ae")
        
        #-----------------------------------
        # Creates a dropdown list to show the options for flavor amount
        # measured in teaspoons
        # The user can select a new flavor amount
        amountOptions = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        # users input for new teaspoon amount
        newAmount = StringVar()
        newAmount.set( "Select an option" )
        # Configure & Display Dropdown Menu
        drop2 = OptionMenu(self, newAmount, *amountOptions)
        drop2.configure(font= buttonFont, bg = "#ebd5ae")
        drop2.place(x = 510, y = 300)
        drop2["menu"].configure(bg = "#ebd5ae")

        #-----------------------------------
        # Creates a dropdown list to show the options for coffee amount
        # measured in ounces
        # The user can select a beverage amount
        options = ["8", "12", "16"]
        # users input for new drink size
        newSize = StringVar()
        newSize.set( "Select an option" )
        # Configure & Display Dropdown Menu
        drop3 = OptionMenu(self, newSize, *options)
        drop3.configure(font= buttonFont, bg = "#ebd5ae")
        drop3.place(x = 60, y = 300)
        drop3["menu"].configure(bg = "#ebd5ae")

        # Create & Display Submit button
        # The submit button triggers the function that saves all of the users new input into their profile
        # THe submit button also changes the window to PageFour
        Submit = tk.Button(self, text="Submit", font = buttonFont,
                           bg = "#ebd5ae", width = 15, command=lambda:[edit_user(flag), controller.show_frame(PageFive)])
        Submit.place(x = 285, y = 380)
        


class PageFive(tk.Frame):
    ### Confirmation Page to inform the user their new coffee preferences were updates
    ### and saved to their profile.
    ### A button is added to allow the user to return back to the start page
    def __init__(self, parent, controller):
        self.controller=controller
        tk.Frame.__init__(self, parent)
        header = tk.Label(self, text="Cache Cafe", font= CacheCafeFont, bg = "#c9ab85")
        header.place(x = 285, y = 90)

        ProfileCreated = tk.Label(self, text="Your Profile has been Updated!", font= welcomeFont,
                                  bg = "#c9ab85")
        ProfileCreated.place(x = 165, y = 230)
        # Reset/Clear all user input widgets
        Home = tk.Button(self, text="Back to Home Page", font = buttonFont,
                           bg = "#ebd5ae", width = 15, command=lambda: [newDrink.set("Select an option"),
                                                                        newSize.set("Select an option"),newAmount.set("Select an option"),
                                                                        controller.show_frame(StartPage)])
        Home.place(x = 295, y = 350)

class PageSix(tk.Frame):
    ### Confirmation Page to inform the user their profile has been saved with their coffee preferences
    ### A button is added to allow the user to return back to the start page
    def __init__(self, parent, controller):
        self.controller=controller
        tk.Frame.__init__(self, parent)
        header = tk.Label(self, text="Cache Cafe", font= CacheCafeFont, bg = "#c9ab85")
        header.place(x = 285, y = 50)

        ProfileCreated = tk.Label(self, text="Your Profile has been Created!", font= welcomeFont,
                                  bg = "#c9ab85")
        ProfileCreated.place(x = 165, y = 230)

        Home = tk.Button(self, text="Back to Home Page", font = buttonFont,
                           bg = "#ebd5ae", width = 15, command=lambda: [username.set(""),drinkSize.set("Select an option"),
                                                                        teaspoonsNum.set("Select an option"),drinkFlavor.set("Select an option"),
                                                                        controller.show_frame(StartPage)])
        Home.place(x = 295, y = 350)


# The servos operate with a series of bursts.
# a burst is going to represent a unit
# the number of units we go through is gonna be used in for loops
def UART_Init(): #UART Initialization
    global ser
    ser = serial.Serial(
        port='/dev/ttyS0', #we are using ttyS0 serial port
        baudrate = 115200,   #baudrate 9600
        parity=serial.PARITY_NONE, #no parity bit
        stopbits=serial.STOPBITS_ONE, #one stop bit
        bytesize=serial.EIGHTBITS, #data size
        timeout=None
    )
    time.sleep(1)
    
def Servo_Init():#Servo Motor initialization
    # Set GPIO numbering mode
    global cream1,cream2,cream3,sugar
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(11,GPIO.OUT)
    cream1 = GPIO.PWM(11,50) # pin 11 for creamer 1 dispenser
    GPIO.setup(12,GPIO.OUT)
    cream2 = GPIO.PWM(12,50) # pin 12 for creamer 2 dispenser
    GPIO.setup(13,GPIO.OUT)
    cream3 = GPIO.PWM(13,50) # pin 13 for creamer 3 dispenser
    GPIO.setup(15,GPIO.OUT)
    sugar  = GPIO.PWM(15,50) # pin 15 for sugar dispenser
    GPIO.setup(31,GPIO.OUT)  # set up relay pins
    GPIO.setup(29,GPIO.OUT)
    cream1.start(2)          #start our pwm pins
    cream2.start(2)
    cream3.start(2)
    sugar.start(2)
    time.sleep(0.5)
    cream1.ChangeDutyCycle(0)
    cream2.ChangeDutyCycle(0)
    cream3.ChangeDutyCycle(0)
    sugar.ChangeDutyCycle(0)
    
def getprofileinfo(counter): #retrieve profile info
    global crm1,crm2,crm3,sug,size
    prf = open("CoffeeProfiles.txt","r") #open file for reading reading
    lines = prf.readlines()
    profileline = lines[counter]   #copy a specific profile line
    crm1 = int(profileline[20])    #retrieve profile info as integers
    crm2 = int(profileline[21])
    crm3 = int(profileline[22])
    sug  = int(profileline[23])
    size = int(profileline[24])
    return crm1,crm2,crm3,sug,size
    prf.close()
    
def getprofilename(counter): #retrieve profile name
    prf = open("CoffeeProfiles.txt","r") #open file for reading
    lines = prf.readlines()
    profileline = lines[counter]
    namesec = profileline[0:20]
    global name
    name = namesec.rstrip() #get name by taking the first 20 characters on line and stripping white space to the right
    prf.close()
    
def servo_motors(servo,units,sec):   #operate an individual motor
    for x in range(units):
        servo.ChangeDutyCycle(5) #open dispenser
        time.sleep(sec)
        servo.ChangeDutyCycle(2) #wait 'time' sec and close dispenser
        time.sleep(0.5)
        servo.ChangeDutyCycle(0) #no pulse in servo
        
def dispenser():                 #operate all our motors
    servo_motors(cream1,crm1,0.25)
    print ('We have dispensed',crm1,'tsps')
    servo_motors(cream2,crm2,0.25)
    print ('We have dispensed',crm2,'tsps')
    servo_motors(cream3,crm3,0.25)
    print ('We have dispensed',crm3,'tsps')
    servo_motors(sugar,sug,0.25)
    print ('We have dispensed',sug,'tsps')   
       if(size==1):
        time.sleep(1)
        GPIO.output(31,True)
        time.sleep(5)#50
        GPIO.output(29,True)
        time.sleep(5)#50
        GPIO.output(31,False)
        time.sleep(1)
        GPIO.output(29,False)
    elif(size==2):
        time.sleep(1)
        GPIO.output(31,True)
        time.sleep(5)#75
        GPIO.output(29,True)
        time.sleep(20)#75
        GPIO.output(31,False)
        time.sleep(1)
        GPIO.output(29,False)
    elif(size==3):
        time.sleep(1)
        GPIO.output(31,True)
        time.sleep(5)#150
        GPIO.output(29,True)
        time.sleep(5)#55
        GPIO.output(31,False)
        time.sleep(1)
        GPIO.output(29,False)
    
def UARTtransmit(val):
    print("We are sending a flag to the Jetson Nano.")
    num = int(val) #declare an int num with value from val
    sendval = bytes([num]) #convert into a byte
    ser.write(sendval) #write a byte to Nano
    print ("Flag sent")
    
def UARTreceive():
    print("We are waiting for facial recognition results...")
    value = ser.read() #read takes in a byte from Nano
    print(value)
    print('Profile identified')
    counter = int.from_bytes(value,'big') #assuming it's a byte, convert to an integer
    print(counter)
    return counter

def main():
    
    UART_Init()
    Servo_Init()
    GPIO.output(31,False)
    PageContainer()

main()
