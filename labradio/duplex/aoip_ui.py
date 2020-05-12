# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'duplex/aoip.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Aoip(object):
    def setupUi(self, Aoip):
        Aoip.setObjectName("Aoip")
        Aoip.resize(854, 581)
        self.gridLayout_3 = QtWidgets.QGridLayout(Aoip)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.btnConnect = QtWidgets.QPushButton(Aoip)
        self.btnConnect.setMinimumSize(QtCore.QSize(2, 40))
        self.btnConnect.setMaximumSize(QtCore.QSize(100, 16777215))
        self.btnConnect.setIconSize(QtCore.QSize(16, 16))
        self.btnConnect.setObjectName("btnConnect")
        self.gridLayout_3.addWidget(self.btnConnect, 0, 1, 1, 1)
        self.meters = QtWidgets.QGridLayout()
        self.meters.setObjectName("meters")
        self.label_2 = QtWidgets.QLabel(Aoip)
        self.label_2.setObjectName("label_2")
        self.meters.addWidget(self.label_2, 1, 1, 1, 1)
        self.outputMeter = QtWidgets.QWidget(Aoip)
        self.outputMeter.setObjectName("outputMeter")
        self.meters.addWidget(self.outputMeter, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(Aoip)
        self.label.setObjectName("label")
        self.meters.addWidget(self.label, 1, 0, 1, 1)
        self.inputMeter = QtWidgets.QWidget(Aoip)
        self.inputMeter.setMinimumSize(QtCore.QSize(87, 356))
        self.inputMeter.setStyleSheet("")
        self.inputMeter.setObjectName("inputMeter")
        self.meters.addWidget(self.inputMeter, 0, 0, 1, 1)
        self.meters.setColumnStretch(0, 1)
        self.meters.setColumnStretch(1, 1)
        self.meters.setRowStretch(0, 9)
        self.meters.setRowStretch(1, 1)
        self.gridLayout_3.addLayout(self.meters, 1, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(Aoip)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.consoleOutput = QtWidgets.QTextBrowser(self.groupBox)
        self.consoleOutput.setObjectName("consoleOutput")
        self.gridLayout_2.addWidget(self.consoleOutput, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox, 1, 1, 1, 1)
        self.gridLayout_3.setColumnStretch(0, 3)
        self.gridLayout_3.setColumnStretch(1, 10)

        self.retranslateUi(Aoip)
        QtCore.QMetaObject.connectSlotsByName(Aoip)

    def retranslateUi(self, Aoip):
        _translate = QtCore.QCoreApplication.translate
        Aoip.setWindowTitle(_translate("Aoip", "Form"))
        self.btnConnect.setText(_translate("Aoip", "CONNECT"))
        self.label_2.setText(_translate("Aoip", "Output Studio"))
        self.label.setText(_translate("Aoip", "Input Local"))
        self.groupBox.setTitle(_translate("Aoip", "Sortie"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Aoip = QtWidgets.QWidget()
    ui = Ui_Aoip()
    ui.setupUi(Aoip)
    Aoip.show()
    sys.exit(app.exec_())
