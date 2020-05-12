from openob.audio_interface import *
from openob.node import *
from labradio.duplex.aoip_ui import Ui_Aoip
from labradio.audio.vumeter import VuMeter
import logging


class Aoip(Ui_Aoip):

    def setupUi(self, AoipUI):
        super().setupUi(AoipUI)

        newInputMeter = VuMeter()  # QWidget
        self.meters.replaceWidget(self.inputMeter, newInputMeter)


if __name__ == "__main__":
    import sys
    from PyQt5 import QtWidgets

    app = QtWidgets.QApplication(sys.argv)
    AoipUI = QtWidgets.QWidget()
    ui = Aoip()
    ui.setupUi(AoipUI)
    AoipUI.show()
    sys.exit(app.exec_())


# link_config = LinkConfig('duplex1-link', '192.168.1.53')
# link_config.logger.setLevel(logging.INFO)
# link_config.set('name', 'duplex1-link')
# link_config.set('port', 3000)
# # link_config.set('jitter_buffer', 2000)
# link_config.set('encoding', 'opus')
# link_config.set('bitrate', 256)
# link_config.set("multicast", False)
# link_config.set("input_samplerate", 48000)
# link_config.set("receiver_host", '192.168.1.53')
# link_config.set("opus_framesize", 20)
# link_config.set("opus_complexity", 9)
# link_config.set("opus_fec", True)
# link_config.set("opus_loss_expectation", 0)
# link_config.set("opus_dtx", False)
#
#
#
# audio_interface = AudioInterface('duplex1-tx-node', 'LabRadio')
# audio_interface.logger.setLevel(logging.INFO)
# audio_interface.set('mode', 'tx')
# audio_interface.set('type', 'alsa')
# audio_interface.set('samplerate', 48000)
# audio_interface.set('alsa_device', 'loopin')
#
# # audio_interface.set('jack_auto', True)
# # audio_interface.set('jack_name', 'LabRadio-openob')
# # audio_interface.set('jack_port_pattern', 'capture')
#
#
# tx = RTPTransmitter('duplex1-tx-node', link_config, audio_interface)
# tx.logger.setLevel(logging.INFO)
# tx.run()
# tx.loop()

