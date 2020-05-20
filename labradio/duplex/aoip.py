from openob.audio_interface import *
from openob.node import *
import traceback

from PyQt5.QtCore import *
import sys
import io

# AOIP THREAD WORKER

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

# LOGGING AOIP HANDLER

import logging


class AoipHandler(logging.StreamHandler):

    def __init__(self, output):
        super().__init__()
        self.output = output

    def emit(self, record):
        msg = self.format(record)
        self.output.append(msg)


from labradio.duplex.aoip_ui import Ui_Aoip
from labradio.audio.vumeter import VuMeter


# MAIN CLASS

class Aoip(Ui_Aoip):

    def __init__(self):
        # SETUP LINK CONFIG TODO: Rendre paramètrable
        self.link_name = 'duplex3'
        self.ip = '192.168.1.53'
        self.port = 3000
        self.bitrate = 256
        self.jitter = 0
        self.device = 'loopin'

    def setupUi(self, AoipUI):
        super().setupUi(AoipUI)

        # BIND INPUT METER
        newInputMeter = VuMeter()  # QWidget
        self.meters.replaceWidget(self.inputMeter, newInputMeter)

        newOutputMeter = VuMeter()
        self.meters.replaceWidget(self.outputMeter, newOutputMeter)

        # BIND BUTTON
        self.btnConnect.clicked.connect(self.connect_aoip)

        # CREATE THREADPOOL
        self.threadpool = QThreadPool()

    def connect_aoip(self):
        worker = Worker(self.aoip_start)
        worker.signals.finished.connect(self.test)
        self.threadpool.start(worker)

    def test(self):
        print('AOIP FINI')

    def aoip_start(self):

        # STREAM HANDLER TO OUTPUT TO TEXTBROWSER
        stream = AoipHandler(self.consoleOutput)

        link_config = LinkConfig(self.link_name + '-link', self.ip)
        link_config.logger.setLevel(logging.INFO)
        link_config.logger.addHandler(stream)
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

        audio_interface = AudioInterface(self.link_name + '-tx-node', 'loopin')
        audio_interface.logger.setLevel(logging.INFO)
        audio_interface.logger.addHandler(stream)
        audio_interface.set('mode', 'tx')
        audio_interface.set('type', 'alsa')
        audio_interface.set('samplerate', 48000)
        audio_interface.set('alsa_device', self.device)

        tx = RTPTransmitter(self.link_name + '-tx-node', link_config, audio_interface)
        tx.logger.setLevel(logging.INFO)
        tx.logger.addHandler(stream)

        node = Node(self.link_name + '-tx-node')
        node.logger.setLevel(logging.INFO)
        node.logger.addHandler(stream)
        node.run_link(link_config, audio_interface)


if __name__ == "__main__":
    import sys
    from PyQt5 import QtWidgets

    app = QtWidgets.QApplication(sys.argv)
    AoipUI = QtWidgets.QWidget()
    ui = Aoip()
    ui.setupUi(AoipUI)
    AoipUI.show()


    sys.exit(app.exec_())




