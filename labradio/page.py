from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QWidget


class Page(QWidget):

    showed = pyqtSignal('PyQt_PyObject')

    def __init__(self, name, UI_Obj):
        super().__init__()

        # DISPLAY NAME
        self.name = name

        # WIDGET INIT
        # self.widget = QtWidgets.QWidget()
        self.ui = UI_Obj
        self.ui.setupUi(self)
        self.setAccessibleName(name)

        # OPTIONAL PROPERTIES
        self.stack = None
        self.parentPage = None

    # ADD WIDGET TO A STACKED WIDGET
    def addToStack(self, stack):
        stack.addWidget(self)
        self.stack = stack
        return self

    # GET ID FROM CURRENT STACKED WIDGET
    def getStackId(self):
        return self.stack.indexOf(self.widget)

    # SET PARENT PAGE
    def setParent(self, page):
        self.parentPage = page
        return self

    # ADD PAGE TO AUTOMATIC MENU
    def addToMenu(self, menu):
        menu.ui.addItem(self)
        self.setParent(menu)
        return self

    # SWITCH STACKED WIDGET TO THIS PAGE
    def show(self):
        self.stack.setCurrentWidget(self)
        self.showed.emit(self)

