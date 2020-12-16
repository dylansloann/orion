from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
import rules
import sys, os, time

class scanWindow(QWidget): 
	def __init__(self): 
		super().__init__()  
		self.initUI() 
   
	def initUI(self):  
		self.pbar = QProgressBar(self) 
		self.pbar.setGeometry(30, 40, 200, 25) 
		self.startButton = QPushButton('Start', self) 
		self.startButton.move(40, 80) 
		self.startButton.clicked.connect(self.startScan) 
		self.setGeometry(820, 400, 280, 170) 
		self.setWindowTitle("Scanner") 
		self.show() 
  
	def startScan(self):
		# finding home path
		home = os.path.expanduser("~")
		dirs = os.listdir(home)
		count = 0

		# iterates through each directory
		for root, dirs, files in os.walk(home):
			# iterates through each file
			for file in files:
				try:
					# attaches root of path for checking against YARA rules
					conjoinedPath = os.path.join(root, file)
					absolutePath = os.path.abspath(conjoinedPath)

					# if file did contain virus, prompt for deletion
					if (rules.match(absolutePath) != []):
						#infectedFiles.append(absolutePath)
						answer = QtWidgets.QInputDialog.getText(self, "Virus Found! " + absolutePath, "Please type Y/N: ")
						if (answer[0] == 'Y'):
							# removes file from directory
							os.remove(absolutePath)

				# handles if certain files cause program to crash
				except:
					continue
			# count += 1

			## ADD SPECIFIED DIRECTORY OPTION

			# time.sleep(0.05)
			self.pbar.setValue(count)








# for i in range(101):
# time.sleep(0.05)
# self.pbar.setValue(i)