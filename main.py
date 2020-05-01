from PyQt5.QtCore import Qt

from labradio.network.network import Network
from labradio.page import Page
from labradio.utils.menu.menu import Menu
from main_ui import Ui_MainWindow


class Main(Ui_MainWindow):

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.stackedWidget.currentChanged.connect(self.updateTopBar)

        self.quitButton.clicked.connect(app.quit)
        self.fullscreenButton.clicked.connect(lambda: self.fullScreen(MainWindow))

        # MAIN MENU INIT
        menu = Page('Accueil', Menu())
        menu.addToStack(self.stackedWidget)

        # ASSIGN HOME BUTTON TO MAIN MENU PAGE
        self.homeButton.clicked.connect(lambda: menu.show())

        # NETWORK MENU
        menu_network = Page('Reseau', Menu())

        page_network_test = Page('Tests', Network())
        page_network_test.addToStack(self.stackedWidget).addToMenu(menu_network)

        menu_network.ui.renderItems()

        # DUPLEX MENU
        menu_duplex = Page('Duplex', Menu())

        # MONITORING MENU
        menu_monitoring = Page('Monitoring', Menu())

        # ADD PAGES TO MAIN MENU
        menu_network.addToStack(self.stackedWidget).addToMenu(menu)
        menu_duplex.addToStack(self.stackedWidget).addToMenu(menu)
        menu_monitoring.addToStack(self.stackedWidget).addToMenu(menu)

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

    def updateTopBar(self):
        # TITLE UPDATE
        self.pageTitle.setText(self.stackedWidget.currentWidget().accessibleName())

        # PREVIOUS BTN MANAGEMENT
        parentPage = self.stackedWidget.currentWidget().parentPage

        if parentPage is None:
            self.previousButton.setDisabled(True)
            self.previousButton.hide()
        else:
            self.previousButton.setDisabled(False)
            self.previousButton.show()
            self.previousButton.clicked.connect(lambda: parentPage.show())

    def on_Page_showed(self, Page):
        print('Changement de page')


if __name__ == "__main__":
    import sys
    from PyQt5 import QtWidgets

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Main()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
