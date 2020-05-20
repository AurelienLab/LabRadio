import traceback

from PyQt5.QtCore import *
import sys

class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    data = pyqtSignal(tuple)


class Worker(QRunnable):

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs

        self.kwargs['data_callback'] = self.signals.data

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


import pyaudio, audioop, math

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPainter, QPen, QBrush, QPalette, QFont
from PyQt5.QtCore import Qt, QThreadPool
from PyQt5.QtWidgets import QApplication, QWidget



class VuMeter(QWidget):

    def __init__(self, width=130, height=500):
        super().__init__()
        self.width = width
        self.height = height

        self.LevelL = 0
        self.LevelR = 0
        self.peakL = 0
        self.peakR = 0

        # self.init_view()
        self.init_audio()

        self.started = False

        self.threadpool = QThreadPool()


    def showEvent(self, event):
        super().showEvent(event)

        # self.adjustSize()
        self.width = self.frameGeometry().width()
        self.height = self.frameGeometry().height()

        self.init_view()

        worker = Worker(self.loop)
        worker.signals.data.connect(self.draw)
        self.threadpool.start(worker)

    def resizeEvent(self, QResizeEvent):
        super().resizeEvent(QResizeEvent)

        self.width = self.frameGeometry().width()
        self.height = self.frameGeometry().height()

        self.calculate_sizes()

    def init_view(self):
        self.setGeometry(0, 0, self.width, self.height)
        self.bg_color = (0, 0, 0)
        self.peakL = 0
        self.peakR = 0

        self.calculate_sizes()
        # self.fontSmall = pygame.font.Font('freesansbold.ttf', round(0.1 * self.width))
        # self.setStyleSheet("background-color: rgb(0, 0, 0);")

        pal = self.palette()
        pal.setColor(QPalette.Background, Qt.black)
        self.setAutoFillBackground(True)
        self.setPalette(pal)

    def init_audio(self):
        self.pa = pyaudio.PyAudio()

        self.pa_infos = self.pa.get_default_input_device_info()
        self.samplerate = int(self.pa_infos['defaultSampleRate'])
        print(self.pa_infos)

        self.pa_stream = self.pa.open(output_device_index=2,
                                      format=pyaudio.paInt16,
                                      channels=2,
                                      rate=self.samplerate,
                                      input=True,
                                      frames_per_buffer=1024)

    def calculate_sizes(self):
        W = self.width
        H = self.height

        self.side_margin = W * 0.04
        exp_width = self.width - (2 * self.side_margin)
        self.exp_height = H - (H*0.05)
        self.rect_height_margin = self.exp_height / 40
        self.rect_height = self.rect_height_margin - 1
        self.rect_width = 0.21 * W

        self.start_meter_L = self.side_margin
        self.end_meter_L = self.start_meter_L + self.rect_width

        self.middle_width = 0.42 * W
        self.start_middle = self.end_meter_L
        self.start_line_L = self.start_middle
        self.end_line_L = self.start_line_L + 0.3 * self.middle_width
        self.start_text = self.end_line_L + 0.10 * self.middle_width
        self.start_line_R = self.end_line_L + 0.6 * self.middle_width
        self.end_line_R = self.start_line_R + 0.3 * self.middle_width

        self.ecart = self.exp_height / 40

        self.start_meter_R = self.end_line_R
        self.end_meter_R = self.start_meter_R + self.rect_width

        self.exp_height_peak = self.exp_height + 10

    def loop(self, data_callback):
        while True:
            data = self.pa_stream.read(1024, exception_on_overflow=False)

            ldata = audioop.tomono(data, 2, 1, 0)
            amplitudel = ((audioop.max(ldata, 2)) / 32767)
            self.LevelL = (int(41 + (20 * (math.log10(amplitudel + (1e-40))))))
            rdata = audioop.tomono(data, 2, 0, 1)
            amplituder = ((audioop.max(rdata, 2)) / 32767)
            self.LevelR = (int(41 + (20 * (math.log10(amplituder + (1e-40))))))

            if self.LevelL > self.peakL:
                self.peakL = self.LevelL
            elif self.peakL > 0:
                self.peakL = self.peakL - 0.2
            if self.LevelR > self.peakR:
                self.peakR = self.LevelR
            elif self.peakR > 0:
                self.peakR = self.peakR - 0.2

            dataTuple = (self.LevelL, self.LevelR, self.peakL, self.peakR)

            data_callback.emit(dataTuple)

    def draw(self, data):
        self.LevelL = data[0]
        self.LevelR = data[1]
        self.peakL = data[2]
        self.peakR = data[3]

        self.repaint()

    def paintEvent(self, event):
        painter = QPainter(self)

        # DRAW THE MIDDLE SCALE
        painter.setPen(QPen(Qt.white, 1, Qt.SolidLine))
        painter.setFont(QFont("Helvetica", round(0.08 * self.width)))
        for dB in range(0, 60, 4):
            number = str(dB)
            current_height = self.rect_height_margin * dB + 10
            painter.drawText(self.start_text, current_height + 5, '-'+number)
            painter.drawLine(self.start_line_L, current_height, self.end_line_L, current_height)
            painter.drawLine(self.start_line_R, current_height, self.end_line_R, current_height)

        painter.setPen(QPen(Qt.black, 0, Qt.SolidLine))
        for i in range(0, self.LevelL):
            current_height = self.exp_height - i * self.ecart
            if i < 20:
                painter.setBrush(QBrush(Qt.green, Qt.SolidPattern))
            elif 20 <= i < 30:
                painter.setBrush(QBrush(Qt.yellow, Qt.SolidPattern))
            else:
                painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))

            painter.drawRect(self.start_meter_L, current_height, self.rect_width, self.rect_height)

        for i in range(0, self.LevelR):
            current_height = self.exp_height - i * self.ecart
            if i < 20:
                painter.setBrush(QBrush(Qt.green, Qt.SolidPattern))
            elif 20 <= i < 30:
                painter.setBrush(QBrush(Qt.yellow, Qt.SolidPattern))
            else:
                painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))

            painter.drawRect(self.start_meter_R, current_height, self.rect_width, self.rect_height)

        painter.setPen(QPen(Qt.white, 2, Qt.SolidLine))
        painter.drawLine(self.start_meter_L,
                         (self.exp_height_peak - int(self.peakL) * self.ecart),
                         self.end_meter_L,
                         (self.exp_height_peak - int(self.peakL) * self.ecart))
        painter.drawLine(self.start_meter_R,
                         (self.exp_height_peak - int(self.peakR) * self.ecart),
                         self.end_meter_R,
                         (self.exp_height_peak - int(self.peakR) * self.ecart))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    vumeter = VuMeter(width=150, height=300)

    vumeter.show()
    sys.exit(app.exec())



