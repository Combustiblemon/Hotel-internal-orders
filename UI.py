
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QDialog, QMessageBox, QMainWindow, QWidget, QPushButton, QAction, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.uic import uiparser
from shutil import copyfile

uiparser.WidgetStack.topIsLayoutWidget = lambda self: False


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, sectionDictionary, productList):
        super(MainWindow, self).__init__()
        # Load the main UI file
        uic.loadUi('./files/UI/mainWindow.ui', self)
        self.sectionDictionary = sectionDictionary
        self.productList = productList
        sectionList = []
        for k in sectionDictionary.items():
            sectionList.append(k[0])
        self.ConnectLogicToObjects(sectionList)
        self.show()

    # Adding pointers to all the objects of the UI
    def ConnectLogicToObjects(self, sectionList):
        self.orderView = self.findChild(QtWidgets.QTableWidget, 'orderView')
        self.SetTableStyle()
        # self.AddItemToView('15', 'kg', 'Πόλπα ντομάτα')

        self.addItemButton = self.findChild(QtWidgets.QPushButton, 'addItem')
        self.addItemButton.clicked.connect(self.AddItemPressed)

        self.createOrderButton = self.findChild(QtWidgets.QPushButton, 'createOrder')
        self.createOrderButton.clicked.connect(self.CreateOrderPressed)
        
        self.deleteItemButton = self.findChild(QtWidgets.QPushButton, 'deleteItem')
        self.deleteItemButton.clicked.connect(self.DeleteItemPressed)
        
        self.dateLabel = self.findChild(QtWidgets.QLabel, 'dateLabel')
        self.fromLabel = self.findChild(QtWidgets.QLabel, 'fromLabel')
        self.toLabel = self.findChild(QtWidgets.QLabel, 'toLabel')
        
        self.fromSelectorBox = self.findChild(QtWidgets.QComboBox, 'fromSelector')
        self.fromSelectorBox.clear()
        self.fromSelectorBox.addItems(sectionList)
        # self.text = str(self.fromSelectorBox.currentText())
        # print(self.text)
        self.toSelectorBox = self.findChild(QtWidgets.QComboBox, 'toSelector')
        self.toSelectorBox.clear()
        self.toSelectorBox.addItems(sectionList)
        
        self.dateEdit = self.findChild(QtWidgets.QDateEdit, 'dateEdit')
        self.SetDateStyle()
        
        self.menuBar = self.findChild(QtWidgets.QMenuBar, 'menubar')
        self.menu = self.findChild(QtWidgets.QMenu, 'menu')
        self.adminMenu = self.findChild(QtWidgets.QMenu, 'administrator')
        self.changeProducts = self.findChild(QtWidgets.QAction, 'changeProducts')
        self.menuExitOption = self.findChild(QtWidgets.QAction, 'exit')
        self.adminPasswordChange = self.findChild(QtWidgets.QAction, 'adminPasswordChange')
        self.SetUpMenuBar()
        
    def SetTableStyle(self):
        header = self.orderView.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        
    def SetDateStyle(self):
        self.dateEdit.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dateEdit.setMaximumDate(QtCore.QDate(7999, 12, 28))
        # print(self.dateEdit.date().toString('dd/MM/yyyy'))

    def AddItemPressed(self):
        selectedSectionFrom = str(self.fromSelectorBox.currentText())
        dialog = AddItemWindow(self.productList[self.sectionDictionary[selectedSectionFrom]])
        item = dialog.getResults()
        if(len(item) > 0):
            self.AddItemToView(item[0], item[1], item[2])

    def CreateOrderPressed(self):
        data = self.getTableData()
        
    def ChangeProductList(self):
        self.insertProductList()
        
    def DeleteItemPressed(self):
        rowPosition = self.orderView.rowCount()
        self.orderView.removeRow(rowPosition - 1)
        
    def exitCall(self):
        self.close()
        
    def SetUpMenuBar(self):
        # setup menu exit button       
        self.menuExitOption.setShortcut('Ctrl+Q')
        self.menuExitOption.setStatusTip('Έξοδος προγράμματος')
        self.menuExitOption.triggered.connect(self.exitCall)
        
        # setup change products option
        self.changeProducts.setShortcut('Ctrl+E')
        self.changeProducts.setStatusTip('Αλλαγή λίστας προϊόντων')
        self.changeProducts.triggered.connect(self.ChangeProductList)
        
        # setup change password option
        self.adminPasswordChange.setStatusTip('Αλλαγή κωδικού διαχειρηστή')
        self.adminPasswordChange.triggered.connect(self.ChangeAdminPassword)    
        
    def ChangeAdminPassword(self):
        print('Password Changed')

    def AddItemToView(self, amount='0', unit='', name=''):
        '''Adds an item to the list.
 
        :param amount: The amount of the item
        :type amount: float
        :param unit: The unit of the item
        :type unit: string
        :param name: The name of the item
        :type name: string
        '''
        rowPosition = self.orderView.rowCount()
        self.orderView.insertRow(rowPosition)
        self.orderView.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(f'{amount} {unit}'))
        self.orderView.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(name))
    
    def getTableData(self):
        model = self.orderView.model()
        data = []
        for row in range(model.rowCount()):
            data.append([])
            for column in range(model.columnCount()):
                index = model.index(row, column)
                # We suppose data are strings
                data[row].append(str(model.data(index)))
        return data
        
    def saveFileDialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Αποθήκευση παραγγελίας", "", "Excel Files (*.xlsx);;All Files (*)", options=options)
        if fileName:
            print(fileName)
            """ dest = './files/data/'
            copyfile(fileName, dest) """
            
    def insertProductList(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Άνοιγμα λίστας", "", "Excel Files (*.xlsx);;All Files (*)", options=options)
        if fileName:
            dest = './files/data/ProductList.xlsx'
            copyfile(fileName, dest)
    
    def closeEvent(self, event):
        close = QMessageBox()
        close.setWindowTitle('Exit')
        close.setText("Are you sure you want to exit?")
        close.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        close = close.exec()

        if close == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
            

class AddItemWindow(QtWidgets.QDialog):
    def __init__(self, productsList):
        super(AddItemWindow, self).__init__()
        # Load the main UI file
        uic.loadUi('./files/UI/createOrder.ui', self)
        self.ConnectLogicToObjects(productsList)   
    
    def ConnectLogicToObjects(self, productsList):
        self.addButton = self.findChild(QtWidgets.QPushButton, 'addItem')
        self.addButton.clicked.connect(self.AddButtonPressed)
        
        self.productList = self.findChild(QtWidgets.QTableWidget, 'productList')
        self.SetTableStyle()
        for i in range(len(productsList)):
            #print(productsList[i][1])
            self.AddItemToView(productsList[i][0], productsList[i][1])
            
    def SetTableStyle(self):
        header = self.productList.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        
    def AddButtonPressed(self):
        self.currentItem = []
        if self.productList.currentItem():
            inputBox = ItemNumberInput()
            amount = inputBox.getResults()
            self.currentItem.append(amount) 
            self.currentItem.append(self.productList.item(self.productList.currentItem().row(), 0).text())
            self.currentItem.append(self.productList.item(self.productList.currentItem().row(), 1).text())   
            self.close()
    
    def getResults(self):
        if self.exec_() == QDialog.Accepted:
            return self.currentItem
        else:
            return None
    
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

class ItemNumberInput(QtWidgets.QDialog):
    def __init__(self):
        super(ItemNumberInput, self).__init__()
        # Load the main UI file
        uic.loadUi('./files/UI/itemNumberInput.ui', self)
        self.ConnectLogicToObjects()
        
    def ConnectLogicToObjects(self):
        self.itemLabel = self.findChild(QtWidgets.QLabel, 'itemLabel')
        self.itemInput = self.findChild(QtWidgets.QLineEdit, 'itemInput')
        self.buttonBox = self.findChild(QtWidgets.QDialogButtonBox, 'buttonBox')
        
    def getResults(self):
        if self.exec_() == QDialog.Accepted:
            return self.itemInput.text()
        else:
            return None
             
    def accepted(self):
        return super().accepted()(self)
    
class LoadingWindow(QtWidgets.QDialog):
    def __init__(self):
        super(LoadingWindow, self).__init__()
        # Load the main UI file
        uic.loadUi('./files/UI/LoadingWindow.ui', self)