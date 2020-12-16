import tkinter as tk
import os

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
    introWindow.title("Password Manager")
    introWindow.geometry("400x200+750+350")
    introLabel = tk.Label(text="Enter your login: ", font = ('Verdana', 13))
    introEntry = tk.Entry(width=30, font = ('Verdana'))
    introButton = tk.Button(text="SUBMIT", width=20, height=3, bg="midnight blue", fg="white", font = ('Verdana', 11), command=lambda:introOnClick(introEntry.get(), introWindow, introLabel, introEntry, introButton))

    introLabel.pack(pady=10)
    introEntry.pack(pady=10)
    introButton.pack(pady=10) 
    
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
    passManWindow.title("Password Manager")
    passManWindow.geometry("920x650+500+180")
    label1 = tk.Text(borderwidth=5, relief="ridge", width=100, height=30, font = ('Verdana'))
    label1.pack(side="top")
    label1.insert(tk.END, "\t\tWebsite\t\t\tUsername\t\t\tPassword\n")
    
    # print(passFileDump)  
    
    # Need to update the text being displayed on screen
    for item in passFileDump:
        if item == userPassword:
            continue
        tempStr = item.split(" ")
        listItem = str("\t\t" + tempStr[0] + "\t\t\t" + tempStr[1] + "\t\t\t" + tempStr[2] + "\n")
        label1.insert(tk.END, listItem)
        
    newInfoButton = tk.Button(text="NEW PASSWORD", bg="midnight blue", fg="white", width=25, height=3, font = ('Verdana', 11), command=lambda:submitNewInfo(passManWindow))
    newInfoButton.pack(pady=10)
    
    #scroll.config(yscrollcommand=scroll.set)
    passManWindow.mainloop()

def submitNewInfo(passManWindow):
    passManWindow.destroy()
    
    # Setup a new window to gather the information
    newInfoWindow = tk.Tk()
    newInfoWindow.title("Password Manager")
    newInfoWindow.geometry("400x320+750+250")
    lab1 = tk.Label(text="Enter the website name: ", font = ('Verdana'))
    ent1 = tk.Entry(width=30, font = ('Verdana'))
    lab2 = tk.Label(text="Enter the username for the website: ", font = ('Verdana'))
    ent2 = tk.Entry(width=30, font = ('Verdana'))
    lab3 = tk.Label(text="Enter the password for the website: ", font = ('Verdana'))
    ent3 = tk.Entry(width=30, font = ('Verdana'))
    submitNewInfoButton = tk.Button(text="SUBMIT", bg="midnight blue", fg="white", width=25, height=3, font = ('Verdana', 11), command=lambda:updatePassFile(newInfoWindow, ent1, ent2, ent3))
    
    lab1.pack(pady=10)
    ent1.pack()
    lab2.pack(pady=10)
    ent2.pack()
    lab3.pack(pady=10)
    ent3.pack()
    submitNewInfoButton.pack(pady=15)
    
    newInfoWindow.mainloop()
    
    # Destroy the window on buttonclick and run passwordManagerView() with the updated info

# Write the new information to the file
def updatePassFile(newInfoWindow, in1, in2, in3):
        newStr = str(in1.get()) + " " + str(in2.get()) + " " + str(in3.get())
        passFile.write(newStr + "\n")
        passFileDump.append(newStr)
        
        newInfoWindow.destroy()
        
        passwordManagerViewer()

def showPasswordGUI():
    """updating global variables for use in other functions (SPOOKY)
        also becuase originally this was the main and now this "function" 
        is being called in another file making these pre-globalized variables local"""
    global passFile
    global newUserEntry
    global newUserLabel
    global newUserWindow
    global passFileDump
    global userPassword

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
            newUserWindow.title("Password Manager")
            newUserWindow.geometry("400x200+750+350")
            newUserLabel = tk.Label(text="Enter a new login: ")
            newUserEntry = tk.Entry(width=50)
            newUserButton = tk.Button(text="SUBMIT", bg="midnight blue", fg="white", width=25, height=3, font = ('Verdana', 11), command = submitNewUserPassword)
            
            # Pack up all of the compnents of the window and show it
            newUserLabel.pack(pady=10)
            newUserEntry.pack(pady=10)
            newUserButton.pack(pady=10)
            
            newUserWindow.mainloop()
        
        # Returning user
        else: # There is an existing password
            # Gets the line with the password
            print(passFileDump)
            userPassword = passFileDump[0]
            
            introFunction()
        