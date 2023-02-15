from PyQt5 import QtWidgets
from input_controller import InputController

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    the_mainwindow = InputController()
    the_mainwindow.show()
    sys.exit(app.exec_())

