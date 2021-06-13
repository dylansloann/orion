from PyQt5 import QtCore, QtGui, QtWidgets


class AboutWindow(QtWidgets.QWidget): 

	def __init__(self):
		# initializes AboutWindow
		super().__init__()
		self.setupUI()

	def setupUI(self):
		self.setFixedSize(560, 300) 
		self.setWindowTitle("About")
		self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
		self.setWindowIcon(QtGui.QIcon('../assets/Icons/about.png'))
		self.createBackground()
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
		self.background.setPixmap(QtGui.QPixmap("../assets/background/aboutbackground.png"))
		self.background.setObjectName("background")
