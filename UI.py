
from PyQt5 import QtWidgets, uic
from PyQt5.uic import uiparser

uiparser.WidgetStack.topIsLayoutWidget = lambda self: False


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        # Load the main UI file
        uic.loadUi('testUI.ui', self)
        self.ConnectLogicToObjects()
        self.show()

    # Adding pointers to all the objects of the UI
    def ConnectLogicToObjects(self):
        self.orderView = self.findChild(QtWidgets.QTableWidget, 'orderView')
        self.AddItemToView()

        self.addItemButton = self.findChild(QtWidgets.QPushButton, 'addItem')
        self.addItemButton.clicked.connect(self.AddItemPressed)

        self.createOrderButton = self.findChild(QtWidgets.QPushButton, 'createOrder')
        self.createOrderButton.clicked.connect(self.CreateOrderPressed)

    def AddItemPressed(self):
        print('ping!')

    def CreateOrderPressed(self):
        print('ping!')

    def AddItemToView(self):
        rowPosition = self.orderView.rowCount()
        self.orderView.insertRow(rowPosition)
        self.orderView.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem('text 1'))
        self.orderView.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem('text 2'))
