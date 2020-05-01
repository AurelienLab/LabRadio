from PyQt5.QtCore import QThreadPool

from labradio.network import ipv4
from labradio.network import test
from labradio.network.network_ui import Ui_Network
from labradio.utils import conversion
from labradio.utils.worker import Worker


class Network(Ui_Network):

    def __init__(self):
        self.local_ip = ipv4.get_local_ip()
        self.threadpool = QThreadPool()

    def setupUi(self, NetworkUI):
        super().setupUi(NetworkUI)  # On met en place l'UI à partir de la classe mère

        # Ajout des events
        self.getIpButton.clicked.connect(self.ui_show_ip)
        self.speedTestButton.clicked.connect(self.ui_show_speedtest)

    # FONCTIONS UI
    def ui_show_ip(self):
        self.publicIp.setText(self.get_public_ip())
        self.localIp.setText(self.local_ip)

    def ui_show_speedtest(self):
        self.ui_start_speed_test()

        worker = Worker(self.speedtest)
        worker.signals.finished.connect(self.ui_end_speed_test)

        self.threadpool.start(worker)

    def ui_start_speed_test(self):
        self.speedTestButton.setDisabled(True)
        self.speedTestButton.setText("Tests en cours...")

    def ui_end_speed_test(self):
        self.uploadLabel.setText(self.get_upload(string=1) + " Mb/s")
        self.downloadLabel.setText(self.get_download(string=1) + " Mb/s")
        self.speedTestButton.setDisabled(False)
        self.speedTestButton.setText("Redémarrer le test")

    # FONCTIONS CORE
    def get_public_ip(self):
        self.public_ip = ipv4.get_public_ip()
        return self.public_ip

    def speedtest(self, progress_callback=None):
        results = test.speed()

        self.upload = results['upload']
        self.download = results['download']

    def get_upload(self, unit='Mb', string=0):
        if unit == 'Mb':
            if string:
                return conversion.bit_to_mb_str(self.upload)
            else:
                return conversion.bit_to_mb(self.upload)
        else:
            if string:
                return str(round(self.upload, 2))
            else:
                return round(self.upload, 2)

    def get_download(self, unit='Mb', string=0):
        if unit == 'Mb':
            if string:
                return conversion.bit_to_mb_str(self.download)
            else:
                return conversion.bit_to_mb(self.download)
        else:
            if string:
                return str(round(self.download, 2))
            else:
                return round(self.download, 2)


if __name__ == "__main__":
    import sys
    from PyQt5 import QtWidgets

    app = QtWidgets.QApplication(sys.argv)
    NetworkUI = QtWidgets.QWidget()
    ui = Network()
    ui.setupUi(NetworkUI)
    NetworkUI.show()
    sys.exit(app.exec_())
