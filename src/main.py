from scan import *
from passwordManager import *
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(QtWidgets.QWidget):
    # default constructor of GUI window
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Orion")
        MainWindow.resize(860, 591)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.createBackground()
        self.createButtons()
        self.setCheckMark()
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # creates label and updates it with background image
    def createBackground(self):
        self.background = QtWidgets.QLabel(self.centralwidget)
        self.background.setGeometry(QtCore.QRect(0, 0, 861, 591))
        self.background.setText("")
        self.background.setPixmap(QtGui.QPixmap("../assets/background/background4.0.png"))
        self.background.setObjectName("background")

    # generates core buttons of GUI
    def createButtons(self):
        self.createScanButton()
        self.createBackupButton()
        self.createPasswordButton()
        self.createAboutButton()

    def createScanButton(self):
        # resizes button
        self.scanButton = QtWidgets.QPushButton(self.centralwidget)
        self.scanButton.setGeometry(QtCore.QRect(40, 330, 181, 211))
        self.scanButton.setText("")

        # overlays button with scan png and resizes
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../assets/Icons/scan2.0.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.scanButton.setIcon(icon)
        self.scanButton.setIconSize(QtCore.QSize(210, 246))
        self.scanButton.setObjectName("scanButton")

        # links when button is clicked to passwordPopup function
        self.scanButton.clicked.connect(self.scanPopup)

    def scanPopup(self):
        # answer = QtWidgets.QInputDialog.getText(self, "Virus Found! ", 'Please type Y/N: ')
        self.checkMark.setPixmap(QtGui.QPixmap("../assets/Icons/xmark.png"))
        self.scanner = scanWindow()
        self.scanner.show()

    def createBackupButton(self):
        # resizes button
        self.backupButton = QtWidgets.QPushButton(self.centralwidget)
        self.backupButton.setGeometry(QtCore.QRect(240, 330, 181, 211))
        self.backupButton.setText("")

        # overlays button with backup png and resizes
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../assets/Icons/backup2.0.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.backupButton.setIcon(icon1)
        self.backupButton.setIconSize(QtCore.QSize(210, 246))

        self.backupButton.setObjectName("backupButton")

    def createPasswordButton(self):
        # resizes button
        self.passwordButton = QtWidgets.QPushButton(self.centralwidget)
        self.passwordButton.setGeometry(QtCore.QRect(440, 330, 181, 211))
        self.passwordButton.setText("")

        # overlays button with password png and resizes
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../assets/Icons/password2.0.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.passwordButton.setIcon(icon2)
        self.passwordButton.setIconSize(QtCore.QSize(210, 246))

        self.passwordButton.setObjectName("passwordButton")

        # links when button is clicked to passwordPopup function
        self.passwordButton.clicked.connect(self.passwordPopup)

    def passwordPopup(self):
        showPasswordGUI()

    def createAboutButton(self):
        self.aboutButton = QtWidgets.QPushButton(self.centralwidget)
        self.aboutButton.setGeometry(QtCore.QRect(640, 330, 181, 211))
        self.aboutButton.setText("")
        # overlays button with about png and resizes
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../assets/Icons/about2.0.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.aboutButton.setIcon(icon3)
        self.aboutButton.setIconSize(QtCore.QSize(210, 246))
        self.aboutButton.setObjectName("aboutButton")

    def setCheckMark(self):
        # resizes/changes name
        self.checkMark = QtWidgets.QLabel(self.centralwidget)
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

    # reupdates names of 
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Orion"))


# driver code
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
