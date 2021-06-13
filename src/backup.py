from PyQt5 import QtCore, QtGui, QtWidgets
import sys, shutil


class BackupWindow(QtWidgets.QWidget): 

	def __init__(self):
		# initializes BackupWindow
		super().__init__()
		self.setupUI()

		# initializes mutex and condition for pausing threads
		self.sourceDirectory = ''
		self.destinationDirectory = ''
		self.backing = ScanningThread(self.sourceDirectory, self.destinationDirectory)
   
	def setupUI(self):
		#sets geometry/title and creates all buttons
		self.setFixedSize(560, 300)
		self.setWindowTitle("Backup Files")
		self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
		self.setWindowIcon(QtGui.QIcon('../assets/Icons/backup.png'))
		self.createBackground()
		self.createButtons()
		self.center()
		self.show()

	def center(self):
		qtRectangle = self.frameGeometry()
		centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
		qtRectangle.moveCenter(centerPoint)
		self.move(qtRectangle.topLeft())

	def createBackground(self):
		self.background = QtWidgets.QLabel(self)
		self.background.move(0, 0)
		self.background.setText("")
		self.background.setPixmap(QtGui.QPixmap("../assets/background/backupbackground.png"))
		self.background.setObjectName("background")

	def createButtons(self):
		self.createSourceButton()
		self.createDestinationButton()

	def createSourceButton(self):
		self.sourceButton = QtWidgets.QPushButton('', self) 
		self.sourceButton.setGeometry(80, 90, 180, 120)
		fullScanIcon = QtGui.QIcon()
		fullScanIcon.addPixmap(QtGui.QPixmap("../assets/Icons/src.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.sourceButton.setIcon(fullScanIcon)
		self.sourceButton.setIconSize(QtCore.QSize(150, 85))
		self.sourceButton.clicked.connect(self.chooseSource)

	def chooseSource(self):
		if (self.backing.isRunning()):
			self.backupInProgressMessage()
			return
		self.sourceDirectory = QtWidgets.QFileDialog.getExistingDirectory()

	def createDestinationButton(self):
		self.destinationButton = QtWidgets.QPushButton('', self)
		self.destinationButton.setGeometry(290, 90, 180, 120)
		pickFolderIcon = QtGui.QIcon()
		pickFolderIcon.addPixmap(QtGui.QPixmap("../assets/Icons/dest.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
		self.destinationButton.setIcon(pickFolderIcon)
		self.destinationButton.setIconSize(QtCore.QSize(150, 85))
		self.destinationButton.clicked.connect(self.chooseDestination)

	def chooseDestination(self):
		if (self.backing.isRunning()):
			self.backupInProgressMessage()
			return
		
		self.destinationDirectory = QtWidgets.QFileDialog.getExistingDirectory()
		
		# if backup was not selected or cancel was hit
		if (self.destinationDirectory == ''): return

		# if no source was selected
		if (self.sourceDirectory == ''):
			self.noSourceMessage()
			return

		self.startBackup()

	def noSourceMessage(self):
		scanBox = QtWidgets.QMessageBox(parent=self)
		scanBox.setIcon(QtWidgets.QMessageBox.Warning)
		scanBox.setWindowTitle("Alert!")
		scanBox.setText("No source and/or destination has been selected.")
		scanBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
		scanBox.exec()

	def backupInProgressMessage(self):
		scanBox = QtWidgets.QMessageBox(parent=self)
		scanBox.setIcon(QtWidgets.QMessageBox.Warning)
		scanBox.setWindowTitle("Alert!")
		scanBox.setText("Backup already in progress.")
		scanBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
		scanBox.exec()

	def startBackup(self):
		# reupdates backing thread with new passed in directory
		self.backing = ScanningThread(self.sourceDirectory, self.destinationDirectory)
		self.backing.start()

		# connects emits of ScanningThread
		self.backing.queueNewPathMessage.connect(self.promptNewPathMessage)
		self.backing.errorMessage.connect(self.promptErrorMessage)

	def promptNewPathMessage(self, path):
		completionBox = QtWidgets.QMessageBox(parent=self)
		completionBox.setIcon(QtWidgets.QMessageBox.Information)
		completionBox.setWindowTitle("Alert!")
		completionBox.setText("New backup path: " + path)
		completionBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
		completionBox.exec()

	def promptErrorMessage(self):
		completionBox = QtWidgets.QMessageBox(parent=self)
		completionBox.setIcon(QtWidgets.QMessageBox.Critical)
		completionBox.setWindowTitle("Alert!")
		completionBox.setText("An error has occurred, please retry.")
		completionBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
		completionBox.exec()


class ScanningThread(QtCore.QThread):
	# setup of signal to emit to BackupWindow
	queueCompletionMessage = QtCore.pyqtSignal()
	queueNewPathMessage = QtCore.pyqtSignal(str)
	errorMessage = QtCore.pyqtSignal()

	def __init__(self, src, dest):
		QtCore.QThread.__init__(self)
		self.src = src
		self.dest = dest
		self.dest = dest + "/New Backup"

	def run(self):
		# iterates through each directory
		try:
			destination = shutil.copytree(self.src, self.dest)
			self.queueNewPathMessage.emit(destination)
		except:
			self.errorMessage.emit()
			return