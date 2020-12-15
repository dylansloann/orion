import tkinter as tk
import os
#import matplotlib as mp
#import matplotlib.pyplot as plot

# User password
userPassword = ""

# Cross-function boolean trackers
isWrong = False
isRight = False
endProgram = False

# Attempt counter
attemptCtr = 0

# Becomes true if the user inputs the correct password
isCorrect = False

# Establishing a few global variables to use as the information passes between functions
tempVar1 = ""
tempvar2 = ""
tempVar3 = ""

# Global variable to store all of the file's information and keeps it properly updated
passFileDump = []

def submitNewUserPassword():
        global userPassword
        
        newPass = newUserEntry.get()
        passFile.write(newPass + "\n")
        userPassword = newPass
        newUserWindow.destroy()
        introFunction()
        
def introFunction():
        # Declaration that we're using global variables
        global userPassword
        
        # Starts the intro screen asking the user for the password
        introWindow = tk.Tk()
        introWindow.geometry("1280x840")
        introLabel = tk.Label(text="Enter your password: ")
        introEntry = tk.Entry(width=50)
        introButton = tk.Button(text="Submit", width=25, height=5, bg="green", fg="orange", command=lambda:introOnClick(introEntry.get(), introWindow, introLabel, introEntry, introButton))
        
        introLabel.pack()
        introEntry.pack()
        introButton.pack()
        
        introWindow.mainloop()
        
def introOnClick(userEnteredPassword, inputWindow, inputLabel, inputEntry, inputButton):
        global attemptCtr
        
        if userEnteredPassword == userPassword:
            print("Access granted")
            inputWindow.destroy()
            passwordManagerViewer()
            
        else: # Wrong password
            attemptCtr += 1
            print("Incorrect! You have " + str(10-attemptCtr) + " attempts left :/")
            if attemptCtr == 10:
                passFile.close()
                os.remove("passwordList.txt")
                inputWindow.destroy()
            else:
                inputEntry.delete(0, tk.END)
                
def passwordManagerViewer():
    global passFileDump
    global userPassword
    
    passManWindow = tk.Tk()
    passManWindow.geometry("1280x840")
    label1 = tk.Text(borderwidth=3, relief="ridge", width=160, height=45)
    label1.pack(side="top")
    label1.insert(tk.END, "\t\t\tWebsite\t\t\t\t\t\tUsername\t\t\t\t\t\tPassword\n")
    
    print(passFileDump)
    
    #scroll = tk.Scrollbar(label1)
    #scroll.pack(side="right", fill="y", expand=False)    
    
    # Need to update the text being displayed on screen
    for item in passFileDump:
        if item == userPassword:
            continue
        tempStr = item.split(" ")
        listItem = str("\t\t" + tempStr[0] + "\t\t\t\t\t\t" + tempStr[1] + "\t\t\t\t\t\t" + tempStr[2] + "\n")
        label1.insert(tk.END, listItem)
        
    newInfoButton = tk.Button(text="New Password", width=25, height=5, command=lambda:submitNewInfo(passManWindow))
    newInfoButton.pack()
    
    #scroll.config(yscrollcommand=scroll.set)
    passManWindow.mainloop()

def submitNewInfo(passManWindow):
    passManWindow.destroy()
    
    # Setup a new window to gather the information
    newInfoWindow = tk.Tk()
    newInfoWindow.geometry("1280x840")
    lab1 = tk.Label(text="Enter the website name: ")
    ent1 = tk.Entry(width=50)
    lab2 = tk.Label(text="Enter the username for the website: ")
    ent2 = tk.Entry(width=50)
    lab3 = tk.Label(text="Enter the password for the website: ")
    ent3 = tk.Entry(width=50)
    submitNewInfoButton = tk.Button(text="submit", width=25, height=5, command=lambda:updatePassFile(newInfoWindow, ent1, ent2, ent3))
    
    lab1.pack()
    ent1.pack()
    lab2.pack()
    ent2.pack()
    lab3.pack()
    ent3.pack()
    submitNewInfoButton.pack()
    
    newInfoWindow.mainloop()
    
    # Destroy the window on buttonclick and run passwordManagerView() with the updated info

# Write the new information to the file
def updatePassFile(newInfoWindow, in1, in2, in3):
        newStr = str(in1.get()) + " " + str(in2.get()) + " " + str(in3.get())
        passFile.write(newStr + "\n")
        passFileDump.append(newStr)
        
        newInfoWindow.destroy()
        
        passwordManagerViewer()

# Main function
pf = open("passwordList.txt", "a+")
pf.close()
with open("passwordList.txt", "r+") as passFile:
    passFileDump = passFile.readlines()
    for i in range(len(passFileDump)):
        passFileDump[i] = passFileDump[i].strip("\n")
    
    # Lets the new user set their password
    if passFileDump == []: # The password file is completely empty
        
        # Pop up a window prompting the user to input their new password
        # Possible double check on password (for correct syntax)
        newUserWindow = tk.Tk()
        newUserWindow.geometry("1280x840")
        newUserLabel = tk.Label(text="Enter a new password: ")
        newUserEntry = tk.Entry(width=50)
        newUserButton = tk.Button(text="Submit", width=25, height=5, command = submitNewUserPassword)
        
        # Pack up all of the compnents of the window and show it
        newUserLabel.pack()
        newUserEntry.pack()
        newUserButton.pack()
        
        newUserWindow.mainloop()
    
    # Returning user
    else: # There is an existing password
        # Gets the line with the password
        print(passFileDump)
        userPassword = passFileDump[0]
        
        introFunction()
        