from PyQt5 import QtWidgets
from input_controller import input_controller

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    the_mainwindow = input_controller()
    the_mainwindow.show()
    sys.exit(app.exec_())

