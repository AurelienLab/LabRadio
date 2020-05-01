from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QVBoxLayout, QGridLayout

from labradio.utils.menu.menu_ui import Ui_Menu


class Menu(Ui_Menu):

    def __init__(self):
        self.items = list()

    def setupUi(self, Menu):
        super().setupUi(Menu)

    def addItem(self, Page):
        self.items.append(Page)

    # MENU RENDERING FN
    def renderItems(self):
        nb_items = len(self.items)
        # IF LESS THAN 3 ITEMS, STACK BUTTONS VERTICALLY
        if nb_items <= 3:
            layout = QVBoxLayout()
            for i in self.items:
                btn = self.createButton(i)
                layout.addWidget(btn)
        # IF MORE THAN 3 ITEMS, 4 ROWS / 2 COLS GRID
        else:
            positions = [(y, x) for y in range(4) for x in range(2)]
            layout = QGridLayout()

            for position, i in zip(positions, self.items):
                if i is None:
                    break
                btn = self.createButton(i)
                layout.addWidget(btn, *position)

        self.gridLayout_2.addLayout(layout, 0, 0)

    # CLICKABLE BTN GENERATOR
    def createButton(self, item):

        # FONT
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)

        # GEOMETRY + ASPECT
        btn = QtWidgets.QPushButton()
        btn.setMinimumSize(QtCore.QSize(200, 60))
        btn.setMaximumSize(QtCore.QSize(16777215, 800))
        btn.setStyleSheet("QPushButton { color: rgb(255, 255, 255);\n"
                          "border: 3px, solid,  rgb(223, 223, 223);\n"
                          "background-color: rgb(0, 57, 84); }\n"
                          "QPushButton:pressed { background-color: rgb(0, 139, 204); }")
        btn.setFlat(False)
        btn.setFont(font)
        btn.setText(item.name)

        # HANDLER
        btn.clicked.connect(lambda: item.show())

        return btn
