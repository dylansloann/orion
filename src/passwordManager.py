import tkinter as tk
import os

## TODO: CUSTIMIZE PASSWORD MANAGER

windowCurrentlyOpen = False

class PasswordManager():

    def __init__(self):
        global windowCurrentlyOpen
        if (windowCurrentlyOpen == True): return
        
        self.userPassword = ""
        self.passFileDump = []
        self.showPasswordGUI()

    def submitNewUserPassword(self):        
        self.newPass = newUserEntry.get()
        self.passFile.write(newPass + "\n")
        self.userPassword = newPass
        self.newUserWindow.destroy()
        self.introFunction()
            
    def introFunction(self):
        # Starts the intro screen asking the user for the password
        self.introWindow = tk.Tk()
        icon = tk.PhotoImage(master = self.introWindow, file = '../assets/Icons/lock2.0.png')
        self.introWindow.iconphoto(False, icon)
        self.introWindow.title("Password Manager")
        self.introWindow.geometry("400x200+750+350")
        self.introLabel = tk.Label(text="Enter your login: ", font = ('Verdana', 13))
        self.introEntry = tk.Entry(width=30, font = ('Verdana'))
        self.introButton = tk.Button(text="SUBMIT", width=20, height=3, bg="sea green", fg="white", font = ('Verdana', 11), command=lambda:self.introOnClick(self.introEntry.get(), self.introWindow))

        self.introLabel.pack(pady=10)
        self.introEntry.pack(pady=10)
        self.introButton.pack(pady=10) 
        
        self.introWindow.protocol("WM_DELETE_WINDOW", self.introWindowClosing)
        self.introWindow.mainloop()

    def introWindowClosing(self):
        global windowCurrentlyOpen
        windowCurrentlyOpen = False
        self.introWindow.destroy()
            
    def introOnClick(self, userEnteredPassword, inputWindow):
        if userEnteredPassword == self.userPassword:
            print("Access granted")
            inputWindow.destroy()
            self.passwordManagerViewer()
            
        else: print("Incorrect Password")
                
    def passwordManagerViewer(self):        
        self.passManWindow = tk.Tk()
        icon = tk.PhotoImage(master = self.passManWindow, file = '../assets/Icons/lock2.0.png')
        self.passManWindow.iconphoto(False, icon)
        self.passManWindow.title("Password Manager")
        self.passManWindow.geometry("860x590+521+199")
        self.label1 = tk.Text(borderwidth=5, relief="ridge", width=85, height=25, font = ('Verdana'))
        self.label1.pack(side="top")
        self.label1.insert(tk.END, "\t\tWebsite\t\t\tUsername\t\t\tPassword\n")
        
        # print(passFileDump)  
        
        # Need to update the text being displayed on screen
        for item in self.passFileDump:
            if item == self.userPassword: continue

            tempStr = item.split(" ")
            listItem = str("\t\t" + tempStr[0] + "\t\t\t" + tempStr[1] + "\t\t\t" + tempStr[2] + "\n")
            self.label1.insert(tk.END, listItem)
            
        self.newInfoButton = tk.Button(text="NEW PASSWORD", bg="sea green", fg="white", width=25, height=3, font = ('Verdana', 11), command=lambda:self.submitNewInfo(self.passManWindow))
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
        icon = tk.PhotoImage(master = self.newInfoWindow, file = '../assets/Icons/lock2.0.png')
        self.newInfoWindow.iconphoto(False, icon)
        self.newInfoWindow.title("Password Manager")
        self.newInfoWindow.geometry("400x320+750+300")
        self.lab1 = tk.Label(text="Enter the website name: ", font = ('Verdana'))
        self.ent1 = tk.Entry(width=30, font = ('Verdana'))
        self.lab2 = tk.Label(text="Enter the username for the website: ", font = ('Verdana'))
        self.ent2 = tk.Entry(width=30, font = ('Verdana'))
        self.lab3 = tk.Label(text="Enter the password for the website: ", font = ('Verdana'))
        self.ent3 = tk.Entry(width=30, font = ('Verdana'))
        self.submitNewInfoButton = tk.Button(text="SUBMIT", bg="sea green", fg="white", width=25, height=3, font = ('Verdana', 11), command=lambda:self.updatePassFile(self.newInfoWindow, self.ent1, self.ent2, self.ent3))
        
        self.lab1.pack(pady=10)
        self.ent1.pack()
        self.lab2.pack(pady=10)
        self.ent2.pack()
        self.lab3.pack(pady=10)
        self.ent3.pack()
        self.submitNewInfoButton.pack(pady=15)
        
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
                icon = tk.PhotoImage(master = self.newUserWindow, file = '../assets/Icons/lock2.0.png')
                self.newUserWindow.iconphoto(False, icon)
                self.newUserWindow.title("Password Manager")
                self.newUserWindow.geometry("400x200+750+350")
                self.newUserLabel = tk.Label(text="Enter a new login: ", font = ('Verdana', 13))
                self.newUserEntry = tk.Entry(width=30, font = ('Verdana'))
                self.newUserButton = tk.Button(text="SUBMIT", bg="sea green", fg="white", width=25, height=3, font = ('Verdana', 11), command = self.submitNewUserPassword)
                
                # Pack up all of the compnents of the window and show it
                self.newUserLabel.pack(pady=10)
                self.newUserEntry.pack(pady=10)
                self.newUserButton.pack(pady=10)
                
                self.newUserWindow.protocol("WM_DELETE_WINDOW", self.newUserWindowClosing)
                self.newUserWindow.mainloop()
            
            # Returning user
            else: # There is an existing password
                # Gets the line with the password
                print(self.passFileDump)
                self.userPassword = self.passFileDump[0]
                self.introFunction()

    def newUserwindowClosing(self):
        global windowCurrentlyOpen
        windowCurrentlyOpen = False
        self.newUserwindow.destroy()