from scan import *
from passwordManager import *
from backup import *
from about import *


class MainGUI(QtWidgets.QWidget):
    
    def __init__(self):
        # initializes mainWindow
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("Orion")
        self.resize(860, 591)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
        self.setWindowTitle("Orion")
        self.setWindowIcon(QtGui.QIcon('../assets/Icons/orionIcon.png'))
        self.createBackground()
        self.createButtons()
        self.setCheckMark()
        self.show()

    def createBackground(self):
        self.background = QtWidgets.QLabel(self)
        self.background.setGeometry(QtCore.QRect(0, 0, 861, 591))
        self.background.setText("")
        self.background.setPixmap(QtGui.QPixmap("../assets/background/background3.0.png"))
        self.background.setObjectName("background")

    def createButtons(self):
        self.createScanButton()
        self.createBackupButton()
        self.createPasswordButton()
        self.createAboutButton()

    def createScanButton(self):
        # resizes button
        self.scanButton = QtWidgets.QPushButton(self)
        self.scanButton.setGeometry(QtCore.QRect(40, 330, 181, 211))
        self.scanButton.setText("")

        # overlays button with scan png and resizes
        scanIcon = QtGui.QIcon()
        scanIcon.addPixmap(QtGui.QPixmap("../assets/Icons/scan2.0.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.scanButton.setIcon(scanIcon)
        self.scanButton.setIconSize(QtCore.QSize(210, 246))
        self.scanButton.setObjectName("scanButton")

        # links when button is clicked to passwordPopup method
        self.scanButton.clicked.connect(self.scanPopup)

    def scanPopup(self):
        self.scannerInitiate = ScanWindow(parent=self)

    def createBackupButton(self):
        # resizes button
        self.backupButton = QtWidgets.QPushButton(self)
        self.backupButton.setGeometry(QtCore.QRect(240, 330, 181, 211))
        self.backupButton.setText("")

        # overlays button with backup png and resizes
        backupIcon = QtGui.QIcon()
        backupIcon.addPixmap(QtGui.QPixmap("../assets/Icons/backup2.0.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.backupButton.setIcon(backupIcon)
        self.backupButton.setIconSize(QtCore.QSize(210, 246))
        self.backupButton.setObjectName("backupButton")

        # links when button is clicked to backupPopup method
        self.backupButton.clicked.connect(self.backupPopup)

    def backupPopup(self):
        self.backupInitiate = BackupWindow()

    def createPasswordButton(self):
        # resizes button
        self.passwordButton = QtWidgets.QPushButton(self)
        self.passwordButton.setGeometry(QtCore.QRect(440, 330, 181, 211))
        self.passwordButton.setText("")

        # overlays button with password png and resizes
        passwordIcon = QtGui.QIcon()
        passwordIcon.addPixmap(QtGui.QPixmap("../assets/Icons/password2.0.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.passwordButton.setIcon(passwordIcon)
        self.passwordButton.setIconSize(QtCore.QSize(210, 246))
        self.passwordButton.setObjectName("passwordButton")

        # links when button is clicked to passwordPopup method
        self.passwordButton.clicked.connect(self.passwordPopup)

    def passwordPopup(self):
        self.passwordInitiate = PasswordManagerWindow()

    def createAboutButton(self):
        self.aboutButton = QtWidgets.QPushButton(self)
        self.aboutButton.setGeometry(QtCore.QRect(640, 330, 181, 211))
        self.aboutButton.setText("")
        
        # overlays button with about png and resizes
        aboutIcon = QtGui.QIcon()
        aboutIcon.addPixmap(QtGui.QPixmap("../assets/Icons/about2.0.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.aboutButton.setIcon(aboutIcon)
        self.aboutButton.setIconSize(QtCore.QSize(210, 246))
        self.aboutButton.setObjectName("aboutButton")

        # links when button is clicked to aboutPopup method
        self.aboutButton.clicked.connect(self.aboutPopup)

    def aboutPopup(self):
        self.aboutInitiate = AboutWindow()

    def setCheckMark(self):
        # resizes/changes name
        self.checkMark = QtWidgets.QLabel(self)
        self.checkMark.setGeometry(QtCore.QRect(640, 180, 51, 51))
        self.checkMark.setText("")
        
        # overlays button with checkmark png and resizes
        self.checkMark.setPixmap(QtGui.QPixmap("../assets/Icons/checkmark.png"))
        self.checkMark.setObjectName("checkMark")

    # used for scanner window to be able to change protection status
    def changeToUnprotected(self):
        self.checkMark.setPixmap(QtGui.QPixmap("../assets/Icons/xmark.png"))

    def changeToProtected(self):
        self.checkMark.setPixmap(QtGui.QPixmap("../assets/Icons/checkmark.png"))
