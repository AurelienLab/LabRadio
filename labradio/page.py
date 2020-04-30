from PyQt5 import QtWidgets


class Page:

    def __init__(self, name, UI_Obj):
        # DISPLAY NAME
        self.name = name

        # WIDGET INIT
        self.widget = QtWidgets.QWidget()
        self.ui = UI_Obj
        self.ui.setupUi(self.widget)

        # OPTIONAL PROPERTIES
        self.stack = None
        self.parent = None

    # ADD WIDGET TO A STACKED WIDGET
    def addToStack(self, stack):
        stack.addWidget(self.widget)
        self.stack = stack
        return self

    # GET ID FROM CURRENT STACKED WIDGET
    def getStackId(self):
        return self.stack.indexOf(self.widget)

    # SET PARENT PAGE
    def setParent(self, page):
        self.parent = page
        return self

    # ADD PAGE TO AUTOMATIC MENU
    def addToMenu(self, menu):
        menu.ui.addItem(self)
        return self

    # SWITCH STACKED WIDGET TO THIS PAGE
    def show(self):
        print('test')
        self.stack.setCurrentWidget(self.widget)
