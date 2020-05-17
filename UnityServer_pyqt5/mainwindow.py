# This Python file uses the following encoding: utf-8
from PyQt5.QtNetwork import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic

from server import Server

class MainWindow(QMainWindow):
    server = None
    validator = None
    serverRunning = False

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        uic.loadUi("mainwindow.ui", self)
        self.server = self.makeServer()
        self.validator = self.makeValidator()
        self.send_pushButton.setDisabled(True)
        self.start_pushButton.clicked.connect(self.onStartClicked)
        self.send_pushButton.clicked.connect(self.onSendClicked)

    def closeEvent(self, e):
        self.sendMessage("_to_unity_abort_");
        QMainWindow.closeEvent(e)

    def makeValidator(self):
        validator = QDoubleValidator(self)
        validator.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))

        self.xpos_lineEdit.setValidator(validator)
        self.ypos_lineEdit.setValidator(validator)
        self.zpos_lineEdit.setValidator(validator)

        self.xrot_lineEdit.setValidator(validator)
        self.yrot_lineEdit.setValidator(validator)
        self.zrot_lineEdit.setValidator(validator)

        self.xscale_lineEdit.setValidator(validator)
        self.yscale_lineEdit.setValidator(validator)
        self.zscale_lineEdit.setValidator(validator)

        return validator

    def onSendClicked(self):
        xpos = self.xpos_lineEdit.text()
        ypos = self.ypos_lineEdit.text()
        zpos = self.zpos_lineEdit.text()

        xrot = self.xrot_lineEdit.text()
        yrot = self.yrot_lineEdit.text()
        zrot = self.zrot_lineEdit.text()

        xscale = self.xscale_lineEdit.text()
        yscale = self.yscale_lineEdit.text()
        zscale = self.zscale_lineEdit.text()

        data = "_to_unity_parameters_(xpos={0};ypos={1};zpos={2};xrot={3};yrot={4};zrot={5};xscale={6};yscale={7};zscale={8})"
        data = data.format(xpos, ypos, zpos, xrot, yrot, zrot, xscale, yscale, zscale)
        self.server.sendMessage(data)

    def onStartClicked(self):
        if self.serverRunning:
            return
        port = self.port_lineEdit.text()
        port = int(port)
        if self.server.listen(QHostAddress.Any, port):
            self.serverRunning = True
            self.plainTextEdit.appendPlainText("Listening...")
        else:
            self.plainTextEdit.appendPlainText("Not listening")

    def onNewClientConnected(self):
        self.plainTextEdit.appendPlainText("New client connected...")

    def onClientDisconnected(self):
        self.plainTextEdit.appendPlainText("Client disconnected")

    def onDataReceived(self, data):
        self.plainTextEdit.appendPlainText("From client: " + data)

        if "_to_pyqt_parameters_(" in data:
            txt = data.replace("_to_pyqt_parameters_(", "")
            txt = txt.replace(")", "")
            params = txt.split(";")

            xpos = params[0]
            ypos = params[1]
            zpos = params[2]

            xrot = params[3]
            yrot = params[4]
            zrot = params[5]

            xscale = params[6]
            yscale = params[7]
            zscale = params[8]

            xpos = xpos[xpos.find("=")+1:]
            ypos = ypos[ypos.find("=")+1:]
            zpos = zpos[zpos.find("=")+1:]

            xrot = xrot[xrot.find("=")+1:]
            yrot = yrot[yrot.find("=")+1:]
            zrot = zrot[zrot.find("=")+1:]

            xscale = xscale[xscale.find("=")+1:]
            yscale = yscale[yscale.find("=")+1:]
            zscale = zscale[zscale.find("=")+1:]

            xpos = xpos.replace(",", ".")
            ypos = ypos.replace(",", ".")
            zpos = zpos.replace(",", ".")

            xrot = xrot.replace(",", ".")
            yrot = yrot.replace(",", ".")
            zrot = zrot.replace(",", ".")

            xscale = xscale.replace(",", ".")
            yscale = yscale.replace(",", ".")
            zscale = zscale.replace(",", ".")

            self.xpos_lineEdit.setText(xpos)
            self.ypos_lineEdit.setText(ypos)
            self.zpos_lineEdit.setText(zpos)

            self.xrot_lineEdit.setText(xrot)
            self.yrot_lineEdit.setText(yrot)
            self.zrot_lineEdit.setText(zrot)

            self.xscale_lineEdit.setText(xscale)
            self.yscale_lineEdit.setText(yscale)
            self.zscale_lineEdit.setText(zscale)

            self.send_pushButton.setEnabled(True)

    def onMessageSent(self, data):
        self.plainTextEdit.appendPlainText("Message sent: " + data)

    def makeServer(self):
        server = Server(self)
        server.newClientConnected.connect(self.onNewClientConnected)
        server.clientDisconnected.connect(self.onClientDisconnected)
        server.dataReceived.connect(self.onDataReceived)
        server.messageSent.connect(self.onMessageSent)
        return server
