#!/usr/bin/python3
# VU meter written in Python (www.python.org) by Tim Howlett 1st April 2013,
# Does not work with Python 2.7.3 or 2.7.4 Does work with 3.2.3
# Requires the Pygame module (www.pygame.org)and the Pyaudio module (http://people.csail.mit.edu/hubert/pyaudio/)

import sys, pygame, pyaudio, wave, audioop, math
from pygame.locals import *


class VuMeter(object):
    def __init__(self, width=130, height=500):
        self.width = width
        self.height = height

        self.init_view()
        self.init_audio()

    def init_view(self):
        self.bg_color = (0, 0, 0)
        self.peakL = 0
        self.peakR = 0

        pygame.init()
        pygame.mixer.quit()

        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('VU Meter')  # A SUPPRIMER ?

        self.fontSmall = pygame.font.Font('freesansbold.ttf', round(0.1 * self.width))

        self.calculate_sizes()

    def calculate_sizes(self):
        W = self.width
        H = self.height

        self.side_margin = round(W * 0.07)
        self.exp_height = round(H - (H*0.05))
        self.rect_height_margin = round(self.exp_height / 40)
        self.rect_height = self.rect_height_margin - 1
        self.rect_width = round(0.23 * W)

        self.start_meter_L = self.side_margin
        self.end_meter_L = self.start_meter_L + self.rect_width

        self.middle_width = round(0.38 * W)
        self.start_middle = self.end_meter_L
        self.start_line_L = self.start_middle
        self.end_line_L = self.start_line_L + self.rect_height
        self.start_text = self.end_line_L + round(0.5 * self.side_margin)
        self.start_line_R = self.end_line_L + round(0.6 * self.middle_width)
        self.end_line_R = self.start_line_R + self.rect_height

        self.ecart = round(self.exp_height / 40)

        self.start_meter_R = self.end_line_R
        self.end_meter_R = self.start_meter_R + self.rect_height

        self.exp_height_peak = self.exp_height + 10


    def init_audio(self):
        self.pa = pyaudio.PyAudio()

        self.pa_infos = self.pa.get_default_input_device_info()
        self.samplerate = int(self.pa_infos['defaultSampleRate'])

        print(self.pa_infos)  # DEBUG

        self.pa_stream = self.pa.open(format=pyaudio.paInt16,
                                      channels=2,
                                      rate=self.samplerate,
                                      input=True,
                                      frames_per_buffer=1024)

    def draw(self, levelL, levelR):
        self.display.fill(self.bg_color)

        # Write the scale and draw in the lines
        for dB in range(0, 60, 4):
            number = str(dB)
            text = self.fontSmall.render("-" + number, 1, (255, 255, 255))
            textpos = text.get_rect()
            self.display.blit(text, (self.start_text, (self.rect_height_margin * dB)))
            pygame.draw.line(self.display, (255, 255, 255), (self.start_line_L, 5 + (self.rect_height_margin * dB)), (self.end_line_L, 5 + (self.rect_height_margin * dB)), 1)
            pygame.draw.line(self.display, (255, 255, 255), (self.start_line_R, 5 + (self.rect_height_margin * dB)), (self.end_line_R, 5 + (self.rect_height_margin * dB)), 1)

        # Draw the boxes
        for i in range(0, levelL):
            if i < 20:
                pygame.draw.rect(self.display, (0, 192, 0), (self.start_meter_L, (self.exp_height - i * self.ecart), self.rect_width, self.rect_height))
            elif i >= 20 and i < 30:
                pygame.draw.rect(self.display, (255, 255, 0), (self.start_meter_L, (self.exp_height - i * self.ecart), self.rect_width, self.rect_height))
            else:
                pygame.draw.rect(self.display, (255, 0, 0), (self.start_meter_L, (self.exp_height - i * self.ecart), self.rect_width, self.rect_height))
        for i in range(0, levelR):
            if i < 20:
                pygame.draw.rect(self.display, (0, 192, 0), (self.start_meter_R, (self.exp_height - i * self.ecart), self.rect_width, self.rect_height))
            elif i >= 20 and i < 30:
                pygame.draw.rect(self.display, (255, 255, 0), (self.start_meter_R, (self.exp_height - i * self.ecart), self.rect_width, self.rect_height))
            else:
                pygame.draw.rect(self.display, (255, 0, 0), (self.start_meter_R, (self.exp_height - i * self.ecart), self.rect_width, self.rect_height))
        # Draw the peak bars
        pygame.draw.rect(self.display, (255, 255, 255), (self.start_meter_L, (self.exp_height_peak - int(self.peakL) * self.ecart), self.rect_width, 2))
        pygame.draw.rect(self.display, (255, 255, 255), (self.start_meter_R, (self.exp_height_peak - int(self.peakR) * self.ecart), self.rect_width, 2))

    def loop(self):
        while True:
            data = self.pa_stream.read(1024, exception_on_overflow=False)

            ldata = audioop.tomono(data, 2, 1, 0)
            amplitudel = ((audioop.max(ldata, 2)) / 32767)
            LevelL = (int(41 + (20 * (math.log10(amplitudel + (1e-40))))))
            rdata = audioop.tomono(data, 2, 0, 1)
            amplituder = ((audioop.max(rdata, 2)) / 32767)
            LevelR = (int(41 + (20 * (math.log10(amplituder + (1e-40))))))

            if LevelL > self.peakL:
                self.peakL = LevelL
            elif self.peakL > 0:
                self.peakL = self.peakL - 0.2
            if LevelR > self.peakR:
                self.peakR = LevelR
            elif self.peakR > 0:
                self.peakR = self.peakR - 0.2

            self.draw(LevelL, LevelR)

            pygame.display.update()

if __name__ == "__main__":

    import pyaudio

    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print
            "Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name')

    vumeter = VuMeter(width=180, height=600)

    vumeter.loop()



