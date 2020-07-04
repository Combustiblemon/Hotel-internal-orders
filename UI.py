
from PyQt5 import QtWidgets, uic
from PyQt5.uic import uiparser

uiparser.WidgetStack.topIsLayoutWidget = lambda self: False


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('testUI.ui', self)
        self.show()
