from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QAction, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.uic import uiparser

uiparser.WidgetStack.topIsLayoutWidget = lambda self: False

class AddItemWindow(QtWidgets.QDialog):
    def __init__(self, productsList):
        super(AddItemWindow, self).__init__()
        # Load the main UI file
        uic.loadUi('./files/UI/createOrder.ui', self)
        # self.ConnectLogicToObjects()
        self.addButton = self.findChild(QtWidgets.QPushButton, 'addItem')
        self.addButton.clicked.connect(self.AddButtonPressed)
        
        self.productList = self.findChild(QtWidgets.QTableWidget, 'productList')
        self.SetTableStyle()
        for i in range(len(productsList)):
            print(productsList[i][1])
            self.AddItemToView(productsList[i][0], productsList[i][1])
    
    def SetTableStyle(self):
        header = self.productList.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        
    def AddButtonPressed(self):
        currentItem = []
        currentItem.append(self.productList.item(self.productList.currentItem().row(), 0).text())
        currentItem.append(self.productList.item(self.productList.currentItem().row(), 1).text())
        print(currentItem.text())
        # self.close()
    
    def AddItemToView(self, unit='', name=''):
        '''Adds an item to the list.
 
        :param amount: The amount of the item
        :type amount: float
        :param unit: The unit of the item
        :type unit: string
        :param name: The name of the item
        :type name: string
        '''
        rowPosition = self.productList.rowCount()
        self.productList.insertRow(rowPosition)
        self.productList.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(f'{unit}'))
        self.productList.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(name))