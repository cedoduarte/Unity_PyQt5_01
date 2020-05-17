# This Python file uses the following encoding: utf-8
from PyQt5.QtCore import *
from PyQt5.QtNetwork import *

class Server(QTcpServer):
    socket = None
    dataReceived = pyqtSignal(str)
    newClientConnected = pyqtSignal()
    clientDisconnected = pyqtSignal()
    messageSent = pyqtSignal(str)

    def __init__(self, parent=None):
        QTcpServer.__init__(self, parent)

    def incomingConnection(self, handle):
        if self.socket == None:
            self.socket = QTcpSocket(self)
            self.socket.setSocketDescriptor(handle)
            self.socket.readyRead.connect(self.onClientReadyRead)
            self.socket.disconnected.connect(self.onClientDisconnected)
            self.newClientConnected.emit()

    def onClientReadyRead(self):
        data = self.socket.readAll()
        data = str(data, "utf-8")
        self.dataReceived.emit(data)

    def onClientDisconnected(self):
        self.socket = None
        self.clientDisconnected.emit()

    def sendMessage(self, message):
        self.socket.write(message.encode("utf-8"))
        self.messageSent.emit(message)
