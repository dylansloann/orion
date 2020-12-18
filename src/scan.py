from PyQt5 import QtCore, QtGui, QtWidgets
from rules import *
import sys, os, time

## TODO: FIX ICONS

class ScanWindow(QtWidgets.QWidget): 

	def __init__(self, parent):
		self.parent = parent	# connects parent window (GUI) for altering

		# initializes ScanWindow
		super().__init__()
		self.initUI()

		# initializes mutex and condition for pausing threads
		self.mutex = QtCore.QMutex()
		self.condition = QtCore.QWaitCondition()
		self.userDirectory = os.path.expanduser("~")
		self.resumeBool = False
		self.scanning = ScanningThread(self.mutex, self.condition, self.userDirectory)
   
	def initUI(self):
		#sets geometry/title and creates all buttons
		self.setGeometry(680, 350, 560, 300) 
		self.setWindowTitle("File Scanner")
		self.setWindowIcon(QtGui.QIcon('../assets/Icons/scanIcon2.0.png'))
		self.createBackground()
		self.createProgressBar()
		self.createButtons()
		self.show()

	def createBackground(self):
		self.background = QtWidgets.QLabel(self)
		self.background.move(0, 0)
		self.background.setText("")
		self.background.setPixmap(QtGui.QPixmap("../assets/background/test2.png"))
		self.background.setObjectName("background")

	def createButtons(self):
		self.createUserScanButton()
		self.createSpecifiedScanButton()
		self.createStopButton()
		self.createResumebutton()
		self.createCancelbutton()

	def createProgressBar(self):
		self.pbar = QtWidgets.QProgressBar(self) 
		self.pbar.setGeometry(150, 70, 300, 25) 

	def createUserScanButton(self):
		self.userScanButton = QtWidgets.QPushButton('User Directory Scan', self) 
		self.userScanButton.setGeometry(55, 150, 150, 50)
		self.userScanButton.clicked.connect(self.userScan)

	def userScan(self):
		if (self.scanning.isRunning()):
			self.scanInProgressMessage()
			return
		self.resumeBool = False
		self.userDirectory = os.path.expanduser("~")	# reupdates user directory to home path
		self.startScan()

	def createSpecifiedScanButton(self):
		self.specifiedScanButton = QtWidgets.QPushButton('Specified Directory Scan', self) 
		self.specifiedScanButton.setGeometry(355, 150, 150, 50)
		self.specifiedScanButton.clicked.connect(self.specifiedScan)

	def specifiedScan(self):
		if (self.scanning.isRunning()):
			self.scanInProgressMessage()
			return
		self.resumeBool = False
		self.userDirectory = QtWidgets.QFileDialog.getExistingDirectory()
		if (self.userDirectory == ''):	# if cancel is hit or no directory selected
			return
		self.startScan()

	def scanInProgressMessage(self):
		scanBox = QtWidgets.QMessageBox(parent=self)
		scanBox.setIcon(QtWidgets.QMessageBox.Warning)
		scanBox.setWindowTitle("Alert!")
		scanBox.setText("Scan already in progress.")
		scanBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
		scanBox.exec()

	def startScan(self):
		# reupdates scanning thread with new passed in directory
		self.scanning = ScanningThread(self.mutex, self.condition, self.userDirectory)
		self.scanning.start()

		# connects emits of ScanningThread
		self.scanning.updateMarkThread.connect(self.updateMarkMain)
		self.scanning.addToProgress.connect(self.updateProgressBar)
		self.scanning.queueDeletionMessage.connect(self.promptDeletionMessage)
		self.scanning.queueCompletionMessage.connect(self.promptCompletionMessage)
		self.scanning.queueStopScan.connect(self.stopScan)

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
		
		OKButton = deletionBox.button(QtWidgets.QMessageBox.Ok) 	# resets OK button to "Delete"
		OKButton.setText("Delete")
		returnValue = deletionBox.exec()	# obtains which button clicked

		if (returnValue == QtWidgets.QMessageBox.Ok):
			print("VIRUS DELETED")
			# os.remove(path)  (KEEP COMMENTED JUST INCASE)
		
		self.condition.wakeAll()	# unpauses thread

	def promptCompletionMessage(self):
		completionBox = QtWidgets.QMessageBox(parent=self)
		completionBox.setIcon(QtWidgets.QMessageBox.Information)
		completionBox.setWindowTitle("Alert!")
		completionBox.setText("Scan has completed!")
		completionBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
		completionBox.exec()

	def createStopButton(self):
		self.stopButton = QtWidgets.QPushButton('Stop', self) 
		self.stopButton.setGeometry(230, 120, 100, 35) 
		self.stopButton.clicked.connect(self.stopScan)

	def stopScan(self):
		if (self.resumeBool == False):
			self.scanning.stop()
		else:
			self.scanning.resume()
			self.condition.wakeAll()
			self.resumeBool = False

	def createResumebutton(self):
		self.resumeButton = QtWidgets.QPushButton('Resume', self) 
		self.resumeButton.setGeometry(230, 170, 100, 35)
		self.resumeButton.clicked.connect(self.resumeScan)

	def resumeScan(self):
		self.resumeBool = True
		self.stopScan()

	def createCancelbutton(self):
		self.cancelButton = QtWidgets.QPushButton('Cancel', self) 
		self.cancelButton.setGeometry(230, 220, 100, 35)
		self.cancelButton.clicked.connect(self.cancelScan)

	def cancelScan(self):
		self.scanning.cancel()
		self.pbar.setValue(0)

	def closeEvent(self, event=None):
		self.scanning.cancel()





class ScanningThread(QtCore.QThread):
	# setup of signal to emit to ScanWindow
	updateMarkThread = QtCore.pyqtSignal(int)
	addToProgress = QtCore.pyqtSignal(int)
	queueDeletionMessage = QtCore.pyqtSignal(str)
	queueCompletionMessage = QtCore.pyqtSignal()
	queueStopScan = QtCore.pyqtSignal()

	def __init__(self, mutex, condition, directory):
		QtCore.QThread.__init__(self)
		self.mutex = mutex
		self.condition = condition
		self.directory = directory

	def run(self):
		self.stopped = False
		self.cancelled = False

		# setup of total file count/obtaining file count incremation for progress bar
		self.addToProgress.emit(0)
		totalFileCount = sum(len(files) for _, _, files in os.walk(self.directory))
		fileIncrement = 100 * (1/totalFileCount)
		progressBarCounter = 0
		print(progressBarCounter)

		# iterates through each directory
		for root, dirs, files in os.walk(self.directory):
			for file in files:
				if (self.cancelled == True): return    # handles if cancel button is clicked

				# handles stopping of current scan
				if (self.stopped == True): 
					self.queueStopScan.emit()
					self.mutex.lock()
					try:
						self.condition.wait(self.mutex)
					finally:
						self.mutex.unlock()

				try:
					# attaches root of path for checking against YARA rules
					conjoinedPath = os.path.join(root, file)
					
					checkForMatch = rules.match(conjoinedPath, timeout = 10)
					print(conjoinedPath)
					progressBarCounter += fileIncrement

					# skips files with .yar or .yara extension, len runs O(1)
					if (file[len(file) - 3: len(file)] == ("yar" or "ara")): raise Exception()

				# handles if certain files cause program to crash/run excessive amount
				except:
					continue

				# if file did contain virus, prompt for deletion
				if (checkForMatch != []):
					self.updateMarkThread.emit(1)	# changes mark to unprotected on main GUI
					self.queueDeletionMessage.emit(conjoinedPath)
					
					# pauses thread until condition is unlocked in ScanWindow.promptDeletionMessage
					self.mutex.lock()
					try:
						self.condition.wait(self.mutex)
					finally:
						self.mutex.unlock()

					self.updateMarkThread.emit(0)	# changes mark back to protected on main GUI
			
			# updates progress every new directory checked
			self.addToProgress.emit(progressBarCounter)

		# adds remainder of progress if nessaccary
		if (progressBarCounter != 100):
			self.addToProgress.emit(100)

		# prompts completion message
		self.queueCompletionMessage.emit()

	def stop(self):
		self.stopped = True
		print("SCAN STOPPED")

	def resume(self):
		self.stopped = False
		print("SCAN RESUMED")

	def cancel(self):
		self.cancelled = True
		print("SCAN CANCELLED")
		