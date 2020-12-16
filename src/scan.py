from PyQt5 import QtCore, QtGui, QtWidgets
from rules import *
import sys, os, time


class scanWindow(QtWidgets.QWidget): 
	def __init__(self, parent):
		self.parent = parent 
		super().__init__()  
		self.initUI() 
   
	def initUI(self):
		self.pbar = QtWidgets.QProgressBar(self) 
		self.pbar.setGeometry(30, 40, 200, 25) 
		self.startButton = QtWidgets.QPushButton('Start', self) 
		self.startButton.move(40, 80) 
		self.startButton.clicked.connect(self.startScan) 
		self.setGeometry(820, 400, 280, 170) 
		self.setWindowTitle("Scanner") 
		self.show() 
  
	def startScan(self):
		# uses global rules
		global rules

		# finding home path
		home = os.path.expanduser("~")
		dirs = os.listdir(home)
		count = 0

		file_count = sum(len(files) for _, _, files in os.walk(r'C:\Users\dylan\Desktop'))
		counter = file_count / 100
		

		# iterates through each directory
		for root, dirs, files in os.walk(r'C:\Users\dylan\Desktop'):
			# iterates through each file
			for file in files:
				# handles if certain files cause program to crash
				try:
					# attaches root of path for checking against YARA rules
					conjoinedPath = os.path.join(root, file)
					checkForMatch = rules.match(conjoinedPath, timeout = 10)
					print(conjoinedPath)
				except:
					count += counter
					self.pbar.setValue(count)
					continue

				# if file did contain virus, prompt for deletion
				if (checkForMatch != []):
					self.parent.changeToUnprotected()
					answer = QtWidgets.QInputDialog.getText(self, "Virus Found! ", conjoinedPath + '   Please type Y/N: ')
					if (answer[0] == 'Y'):
						# removes path from directory
						os.remove(conjoinedPath)
					self.parent.changeToProtected()
				
			count += 0.1
			self.pbar.setValue(count)

			## ADD SPECIFIED DIRECTORY OPTION
			# time.sleep(0.05)
			# self.pbar.setValue(count)