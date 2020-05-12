from openob.audio_interface import *
from openob.node import *
import traceback

from PyQt5.QtCore import *
import sys


class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    info = pyqtSignal(tuple)


class Worker(QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs

        self.kwargs['info_callback'] = self.signals.info

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done


from labradio.duplex.aoip_ui import Ui_Aoip
from labradio.audio.vumeter import VuMeter
import logging


class Aoip(Ui_Aoip):

    def __init__(self):
        # SETUP LINK CONFIG TODO: Rendre paramètrable
        self.link_name = 'duplex3'
        self.ip = '192.168.129.72'
        self.port = 3000
        self.bitrate = 256
        self.jitter = 0
        self.device = 'default'

    def setupUi(self, AoipUI):
        super().setupUi(AoipUI)

        # BIND INPUT METER
        newInputMeter = VuMeter()  # QWidget
        self.meters.replaceWidget(self.inputMeter, newInputMeter)

        # BIND BUTTON
        self.btnConnect.clicked.connect(self.connect_aoip)

        # CREATE THREADPOOL
        self.threadpool = QThreadPool()

    def connect_aoip(self):
        worker = Worker(self.aoip_start)
        self.threadpool.start(worker)

    def aoip_start(self, info_callback):
        link_config = LinkConfig(self.link_name + '-link', self.ip)
        # link_config.logger.setLevel(logging.INFO)
        link_config.set('name', self.link_name + '-link')
        link_config.set('port', self.port)
        link_config.set('jitter_buffer', self.jitter)
        link_config.set('encoding', 'opus')
        link_config.set('bitrate', self.bitrate)
        link_config.set("multicast", False)
        link_config.set("input_samplerate", 48000)
        link_config.set("receiver_host", self.ip)
        link_config.set("opus_framesize", 20)
        link_config.set("opus_complexity", 9)
        link_config.set("opus_fec", True)
        link_config.set("opus_loss_expectation", 0)
        link_config.set("opus_dtx", False)

        audio_interface = AudioInterface(self.link_name + '-tx-node', 'LabRadio')
        # audio_interface.logger.setLevel(logging.INFO)
        audio_interface.set('mode', 'tx')
        audio_interface.set('type', 'alsa')
        audio_interface.set('samplerate', 48000)
        audio_interface.set('alsa_device', self.device)

        tx = RTPTransmitter('duplex1-tx-node', link_config, audio_interface)
        # tx.logger.setLevel(logging.INFO)
        tx.run()
        tx.loop()


if __name__ == "__main__":
    import sys
    from PyQt5 import QtWidgets

    app = QtWidgets.QApplication(sys.argv)
    AoipUI = QtWidgets.QWidget()
    ui = Aoip()
    ui.setupUi(AoipUI)
    AoipUI.show()
    sys.exit(app.exec_())




