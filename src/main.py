from GUI import *

# driver code
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MainGUI()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())