from PyQt5 import QtWidgets, uic
import sys

class PyQt(QtWidgets.QDialog):
    def __init__(self, layout):
        super(PyQt, self).__init__()
        uic.loadUi(layout, self)
        self.show()

class PyQtApp:
    def __init__(self, layout : str) -> None:
        self.app = QtWidgets.QApplication(sys.argv)
        self.Dialog = QtWidgets.QDialog()
        self.window = PyQt(layout)
    
    def execute(self) -> None:
        self.app.exec_()
    
    def getWindow(self) -> QtWidgets.QDialog:
        return self.window

    def getDialog(self) -> QtWidgets.QApplication:
        return self.Dialog

    def close(self) -> None:
        self.window.close()