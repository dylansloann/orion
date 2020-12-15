import rules.py
import passwordManager.py
from PyQt5 import QtCore, QtGui, QtWidgets
import sys, os

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(860, 591)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.background = QtWidgets.QLabel(self.centralwidget)
        self.background.setGeometry(QtCore.QRect(0, 0, 861, 591))
        self.background.setText("")
        self.background.setPixmap(QtGui.QPixmap("Orion/assets/background/background2.0.png"))
        self.background.setObjectName("background")
        self.scanButton = QtWidgets.QPushButton(self.centralwidget)
        self.scanButton.setEnabled(True)
        self.scanButton.setGeometry(QtCore.QRect(40, 330, 181, 211))
        self.scanButton.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.scanButton.setAutoFillBackground(False)
        self.scanButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Orion/assets/Icons/scan2.0.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.scanButton.setIcon(icon)
        self.scanButton.setIconSize(QtCore.QSize(210, 246))
        self.scanButton.setObjectName("scanButton")
        self.backupButtom = QtWidgets.QPushButton(self.centralwidget)
        self.backupButtom.setGeometry(QtCore.QRect(240, 330, 181, 211))
        self.backupButtom.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Orion/assets/Icons/backup2.0.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.backupButtom.setIcon(icon1)
        self.backupButtom.setIconSize(QtCore.QSize(210, 246))
        self.backupButtom.setObjectName("backupButtom")
        self.passwordButton = QtWidgets.QPushButton(self.centralwidget)
        self.passwordButton.setGeometry(QtCore.QRect(440, 330, 181, 211))
        self.passwordButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("Orion/assets/Icons/password2.0.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.passwordButton.setIcon(icon2)
        self.passwordButton.setIconSize(QtCore.QSize(210, 246))
        self.passwordButton.setObjectName("passwordButton")
        self.aboutButton = QtWidgets.QPushButton(self.centralwidget)
        self.aboutButton.setGeometry(QtCore.QRect(640, 330, 181, 211))
        self.aboutButton.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("Orion/assets/Icons/about2.0.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.aboutButton.setIcon(icon3)
        self.aboutButton.setIconSize(QtCore.QSize(210, 246))
        self.aboutButton.setObjectName("aboutButton")
        self.checkMark = QtWidgets.QLabel(self.centralwidget)
        self.checkMark.setEnabled(True)
        self.checkMark.setGeometry(QtCore.QRect(640, 180, 51, 51))
        self.checkMark.setText("")
        self.checkMark.setPixmap(QtGui.QPixmap("Orion/assets/Icons/checkmark.png"))
        self.checkMark.setObjectName("checkMark")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

# driver code
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
