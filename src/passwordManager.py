import tkinter as tk
import os

# Tkinter check for if it is already opened as it it not seperated by thread
windowCurrentlyOpen = False

class PasswordManagerWindow():

    def __init__(self):
        global windowCurrentlyOpen
        if (windowCurrentlyOpen == True): return
        
        self.userPassword = ""
        self.passFileDump = []
        self.showPasswordGUI()
            
    def introFunction(self):
        # Starts the intro screen asking the user for the password
        self.introWindow = tk.Tk()
        self.introWindow.resizable(0,0)
        icon = tk.PhotoImage(master = self.introWindow, file = '../assets/Icons/lock3.0.png')
        self.introWindow.iconphoto(False, icon)
        backgroundImage = tk.PhotoImage(master = self.introWindow, file = '../assets/background/passbackground.png')
        backgroundLoad = tk.Label(self.introWindow, image=backgroundImage)
        backgroundLoad.place(x=0, y=0, relwidth=1, relheight=1)
        self.introWindow.title("Password Manager")
        self.introWindow.geometry("400x200+750+375")
        self.introEntry = tk.Entry(width=30, font = ('Verdana'))
        self.introButton = tk.Button(text="Submit", width=20, height=3, bg="Steelblue4", fg="white", font = ('Verdana', 11), command=lambda:self.introOnClick(self.introEntry.get(), self.introWindow))
        self.introEntry.place(x = 45, y = 55)
        self.introButton.place(x = 100, y = 90) 
        
        self.introWindow.protocol("WM_DELETE_WINDOW", self.introWindowClosing)
        self.introWindow.mainloop()

    def introWindowClosing(self):
        global windowCurrentlyOpen
        windowCurrentlyOpen = False
        self.introWindow.destroy()
            
    def introOnClick(self, userEnteredPassword, inputWindow):
        if userEnteredPassword == self.userPassword:
            inputWindow.destroy()
            self.passwordManagerViewer()
                
    def passwordManagerViewer(self):        
        self.passManWindow = tk.Tk()
        self.passManWindow.resizable(0,0)
        icon = tk.PhotoImage(master = self.passManWindow, file = '../assets/Icons/lock2.0.png')
        self.passManWindow.iconphoto(False, icon)
        backgroundImage = tk.PhotoImage(master = self.passManWindow, file = '../assets/background/newpassbackground.png')
        backgroundLoad = tk.Label(self.passManWindow, image=backgroundImage)
        backgroundLoad.place(x=0, y=0, relwidth=1, relheight=1)
        self.passManWindow.title("Password Manager")
        self.passManWindow.geometry("860x590+521+199")
        self.infoLabel = tk.Text(borderwidth=5, relief="ridge", width=85, height=25, font = ('Verdana'))
        self.infoLabel.pack(side="top")
        self.infoLabel.insert(tk.END, "\t\tWebsite\t\t\tUsername\t\t\tPassword\n")  
        
        # Need to update the text being displayed on screen
        for item in self.passFileDump:
            if item == self.userPassword: continue

            tempStr = item.split(" ")
            listItem = str("\t\t" + tempStr[0] + "\t\t\t" + tempStr[1] + "\t\t\t" + tempStr[2] + "\n")
            self.infoLabel.insert(tk.END, listItem)
            
        self.newInfoButton = tk.Button(text="New Password", bg="Steelblue4", fg="white", width=25, height=3, font = ('Verdana', 11), command=lambda:self.submitNewInfo(self.passManWindow))
        self.newInfoButton.pack(pady=10)
        
        self.passManWindow.protocol("WM_DELETE_WINDOW", self.passManWindowClosing)
        self.passManWindow.mainloop()

    def passManWindowClosing(self):
        global windowCurrentlyOpen
        windowCurrentlyOpen = False
        self.passManWindow.destroy()

    def submitNewInfo(self, passManWindow):
        self.passManWindow.destroy()
        
        # Setup a new window to gather the new password information
        self.newInfoWindow = tk.Tk()
        self.newInfoWindow.resizable(0,0)
        icon = tk.PhotoImage(master = self.newInfoWindow, file = '../assets/Icons/lock2.0.png')
        self.newInfoWindow.iconphoto(False, icon)
        backgroundImage = tk.PhotoImage(master = self.newInfoWindow, file = '../assets/background/newinfobackground.png')
        backgroundLoad = tk.Label(self.newInfoWindow, image=backgroundImage)
        backgroundLoad.place(x=0, y=0, relwidth=1, relheight=1)
        self.newInfoWindow.title("Password Manager")
        self.newInfoWindow.geometry("400x320+750+300")
        self.ent1 = tk.Entry(width=30, font = ('Verdana'))
        self.ent2 = tk.Entry(width=30, font = ('Verdana'))
        self.ent3 = tk.Entry(width=30, font = ('Verdana'))
        self.submitNewInfoButton = tk.Button(text="Submit", bg="Steelblue4", fg="white", width=25, height=3, font = ('Verdana', 11), command=lambda:self.updatePassFile(self.newInfoWindow, self.ent1, self.ent2, self.ent3))
        
        self.ent1.pack(pady=30)
        self.ent2.pack(pady=10)
        self.ent3.pack(pady=30)
        self.submitNewInfoButton.pack()
        
        self.newInfoWindow.protocol("WM_DELETE_WINDOW", self.newInfoWindowClosing)
        self.newInfoWindow.mainloop()
        
        # Destroy the window on button click and run passwordManagerView() with the updated info

    def newInfoWindowClosing(self):
        global windowCurrentlyOpen
        windowCurrentlyOpen = False
        self.newInfoWindow.destroy()
        self.passwordManagerViewer()

    # Write the new information to the file
    def updatePassFile(self, newInfoWindow, in1, in2, in3):
            newStr = str(in1.get()) + " " + str(in2.get()) + " " + str(in3.get())
            if (newStr != "  "):
                self.passFile.write(newStr + "\n")
                self.passFileDump.append(newStr)

            self.newInfoWindow.destroy()
            self.passwordManagerViewer()

    def showPasswordGUI(self):
        global windowCurrentlyOpen
        windowCurrentlyOpen = True
        self.pf = open("passwordList.txt", "a+")
        self.pf.close()
        with open("passwordList.txt", "r+") as self.passFile:
            self.passFileDump = self.passFile.readlines()
            for i in range(len(self.passFileDump)):
                self.passFileDump[i] = self.passFileDump[i].strip("\n")
            
            # Lets the new user set their password
            if self.passFileDump == []: # The password file is completely empty
                
                # Pop up a window prompting the user to input their new password
                # Possible double check on password (for correct syntax)
                self.newUserWindow = tk.Tk()
                self.newUserWindow.resizable(0,0)
                icon = tk.PhotoImage(master = self.newUserWindow, file = '../assets/Icons/lock3.0.png')
                self.newUserWindow.iconphoto(False, icon)
                backgroundImage = tk.PhotoImage(master = self.newUserWindow, file = '../assets/background/newuserbackground.png')
                backgroundLoad = tk.Label(self.newUserWindow, image=backgroundImage)
                backgroundLoad.place(x=0, y=0, relwidth=1, relheight=1)
                self.newUserWindow.title("Password Manager")
                self.newUserWindow.geometry("400x200+750+375")
                self.newUserEntry = tk.Entry(width=30, font = ('Verdana'))
                self.newUserButton = tk.Button(text="Submit", width=20, height=3, bg="Steelblue4", fg="white", font = ('Verdana', 11), command=lambda:self.submitNewUserPassword(self.newUserEntry.get(), self.passFile))
                
                # places all of the compnents of the window and show it
                self.newUserEntry.place(x = 45, y = 55)
                self.newUserButton.place(x = 100, y = 90)
                
                self.newUserWindow.protocol("WM_DELETE_WINDOW", self.newUserWindowClosing)
                self.newUserWindow.mainloop()
            
            # Returning user
            else: # There is an existing password
                # Gets the line with the password
                self.userPassword = self.passFileDump[0]
                self.introFunction()

    def submitNewUserPassword(self, newUserEntry, passFile):        
        self.newPass = newUserEntry
        passFile.write(self.newPass + "\n")
        self.userPassword = self.newPass
        self.newUserWindow.destroy()
        self.introFunction()

    def newUserWindowClosing(self):
        global windowCurrentlyOpen
        windowCurrentlyOpen = False
        self.newUserWindow.destroy()