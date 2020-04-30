from labradio.network.network import Network
from labradio.page import Page
from labradio.utils.menu.menu import Menu
from main_ui import Ui_MainWindow
from labradio.utils.menu.menu import Menu
from PyQt5.QtCore import Qt

class Main(Ui_MainWindow):

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)

        self.quitButton.clicked.connect(app.quit)
        self.fullscreenButton.clicked.connect(lambda: self.fullScreen(MainWindow))

        # MAIN MENU INIT
        menu = Page('Menu', Menu())
        menu.addToStack(self.stackedWidget)

        # ASSIGN HOME BUTTON TO MAIN MENU PAGE
        self.homeButton.clicked.connect(lambda: menu.show)

        # NETWORK MENU
        menu_network = Page('Reseau', Menu())
        page_network_test = Page('Tests', Network())
        page_network_test.addToStack(self.stackedWidget).addToMenu(menu_network)
        menu_network.ui.renderItems()

        # ADD PAGES TO MENU
        menu_network.addToStack(self.stackedWidget).addToMenu(menu)

        # MENU RENDER
        menu.ui.renderItems()

    # UI FUNCTIONS
    def fullScreen(self, MainWindow):

        # GET CURRENT STATE
        state = MainWindow.windowState()

        if state == Qt.WindowFullScreen:
            MainWindow.showNormal()
        elif state == Qt.WindowNoState:
            MainWindow.showFullScreen()


if __name__ == "__main__":
    import sys
    from PyQt5 import QtWidgets

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Main()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())