from labradio.network import ipv4
from labradio.network import speedtest
from labradio.utils import conversion


class Network:

    def __init__(self):
        self.local_ip = ipv4.get_local_ip()

    def get_public_ip(self):
        self.public_ip = ipv4.get_public_ip()

        return self.public_ip

    def speedtest(self):
        results = speedtest.test()

        self.upload = results['upload']
        self.download = results['download']

    def get_upload(self, unit = 'Mb', string = 0):
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

    def get_download(self, unit = 'Mb', string = 0):
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