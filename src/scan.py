from PyQt5 import QtCore, QtGui, QtWidgets
from rules import *
import sys, os, time


## FIX STILL SCANNING ON CLOSING SCAN WINDOW!
## ADD SPECIFIED DIRECTORY OPTION
## ADD SCAN COMPLETE MESSAGE BOX
## CHANGE SCAN ICON COLOR

class ScanWindow(QtWidgets.QWidget): 
	def __init__(self, parent):
		# connects parent window (GUI) for altering
		self.parent = parent

		# initializes ScanWindow
		super().__init__()
		self.initUI()

		# initializes mutex and condition for pausing threads
		self.mutex = QtCore.QMutex()
		self.condition = QtCore.QWaitCondition()
   
	def initUI(self):
		#sets geometry/title and creates all buttons
		self.setGeometry(700, 350, 550, 300) 
		self.setWindowTitle("File Scanner")
		self.setWindowIcon(QtGui.QIcon('../assets/Icons/scanIcon2.0.png'))
		self.createProgressBar()
		self.createStartButton()
		self.createStopButton()
		self.show()

	def createProgressBar(self):
		self.pbar = QtWidgets.QProgressBar(self) 
		self.pbar.setGeometry(145, 40, 300, 25) 

	def createStartButton(self):
		self.startButton = QtWidgets.QPushButton('Start', self) 
		self.startButton.move(40, 80) 
		self.startButton.clicked.connect(self.startScan)
  
	def startScan(self):
		# connects to thread (ScanningThread) and passes in mutex and condition to have option to pause thread
		self.scanning = ScanningThread(self.mutex, self.condition)
		self.scanning.start()

		# connects emits of ScanningThread
		self.scanning.updateMarkThread.connect(self.updateMarkMain)
		self.scanning.addToProgress.connect(self.updateProgressBar)
		self.scanning.queueDeletionMessage.connect(self.promptDeletionMessage)

	def updateMarkMain(self, val):
		if (val == 1): self.parent.changeToUnprotected()
		else: self.parent.changeToProtected()

	def updateProgressBar(self, val):
		self.pbar.setValue(val)

	def promptDeletionMessage(self, path):
		# prompts input box for user
		deletionBox = QtWidgets.QMessageBox(parent=self)
		deletionBox.setIcon(QtWidgets.QMessageBox.Critical)
		deletionBox.setWindowTitle("Potential Virus Found!")
		deletionBox.setText("Path: " + path)
		deletionBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
		
		# resets OK button to "Delete"
		OKButton = deletionBox.button(QtWidgets.QMessageBox.Ok)
		OKButton.setText("Delete")
		returnValue = deletionBox.exec()

		if (returnValue == QtWidgets.QMessageBox.Ok):
			print("VIRUS DELETED")
			# os.remove(path)  (KEEP COMMENTED JUST INCASE)
		
		# unpauses thread
		self.condition.wakeAll()

	def createStopButton(self):
		self.stopButton = QtWidgets.QPushButton('Stop', self) 
		self.stopButton.move(150, 80) 
		self.stopButton.clicked.connect(self.stopScan)

	def stopScan(self):
		self.scanning.stop()





class ScanningThread(QtCore.QThread):
	updateMarkThread = QtCore.pyqtSignal(int)
	addToProgress = QtCore.pyqtSignal(int)
	queueDeletionMessage = QtCore.pyqtSignal(str)

	def __init__(self, mutex, condition):
		QtCore.QThread.__init__(self)
		self.mutex = mutex
		self.condition = condition


	def run(self):
		global rules

		self.stopped = False

		# finding home path
		home = os.path.expanduser("~")
		dirs = os.listdir(home)
		count = 0

		# obtains total count for increament progress bar
		fileCount = sum(len(files) for _, _, files in os.walk(r'C:\Users\dylan\Desktop'))
		counter = fileCount / 100
		

		# iterates through each directory/obtains root
		for root, dirs, files in os.walk(r'C:\Users\dylan\Desktop'):
			for file in files:
				# handles if stop button is clicked
				if (self.stopped == True): return

				# handles if certain files cause program to crash/run excessive amount
				try:
					# attaches root of path for checking against YARA rules
					conjoinedPath = os.path.join(root, file)
					checkForMatch = rules.match(conjoinedPath, timeout = 15)
					print(conjoinedPath)

				except:
					# count += 0.1
					# self.addToProgress.emit(count)
					continue

				# if file did contain virus, prompt for deletion
				if (checkForMatch != []):
					# changes mark to unprotected on main GUI
					self.updateMarkThread.emit(1)
					self.queueDeletionMessage.emit(conjoinedPath)
					
					# pauses thread until condition is unlocked in ScanWindow.promptDeletionMessage
					self.mutex.lock()
					try:
						self.condition.wait(self.mutex)
					finally:
						self.mutex.unlock()

					# changes mark back to rotected on main GUI
					self.updateMarkThread.emit(0)
			
			# time.sleep(0.25)
			# count += 0.1
			# self.addToProgress.emit(count)

	def stop(self):
		self.stopped = True
		print("SCAN STOPPED")