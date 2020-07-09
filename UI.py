
from PyQt5 import Qt, QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QLabel, QDialog, QMessageBox, QMainWindow, QWidget, QPushButton, QAction, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.uic import uiparser
from shutil import copyfile
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Side, Border
from openpyxl.styles import Fill, fills, PatternFill
from openpyxl.styles.colors import Color
from openpyxl.cell import Cell
from copy import copy
import os

uiparser.WidgetStack.topIsLayoutWidget = lambda self: False

borderStyle = Border(left=Side(border_style='medium', color='FF000000'),
                     right=Side(border_style='medium', color='FF000000'),
                     top=Side(border_style='medium', color='FF000000'),
                     bottom=Side(border_style='medium', color='FF000000'),
                     diagonal=Side(border_style=None, color='FF000000'),
                     diagonal_direction=0,
                     outline=Side(border_style=None, color='FF000000'),
                     vertical=Side(border_style=None, color='FF000000'),
                     horizontal=Side(border_style=None, color='FF000000')
                     )      

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, sectionDictionary, productDictionary):
        super(MainWindow, self).__init__()
        # Load the main UI file
        uic.loadUi('./files/UI/mainWindow.ui', self)
        self.sectionDictionary = sectionDictionary
        self.productDictionary = productDictionary
        self.sectionList = []
        self.text = ''
        self.items = []
        self.index = 0
        for k in sectionDictionary.items():
            self.sectionList.append(k[0])
        self.ConnectLogicToObjects()
        self.show()

    # Adding pointers to all the objects of the UI
    def ConnectLogicToObjects(self):
        self.orderView = self.findChild(QtWidgets.QTableWidget, 'orderView')
        self.SetTableStyle()
        # self.AddItemToView('15', 'kg', 'Πόλπα ντομάτα')

        self.addItemButton = self.findChild(QtWidgets.QPushButton, 'addItem')
        self.addItemButton.clicked.connect(self.AddItemPressed)

        self.createOrderButton = self.findChild(QtWidgets.QPushButton, 'createOrder')
        self.createOrderButton.clicked.connect(self.CreateOrderPressed)
        
        self.deleteItemButton = self.findChild(QtWidgets.QPushButton, 'deleteItem')
        self.deleteItemButton.clicked.connect(self.DeleteItemPressed)
        
        self.searchButton = self.findChild(QtWidgets.QPushButton, 'searchButton')
        self.searchButton.clicked.connect(self.searchTable) 
        
        self.clearButton = self.findChild(QtWidgets.QPushButton, 'clearButton')
        self.clearButton.clicked.connect(self.clearButtonPressed)
        
        self.dateLabel = self.findChild(QtWidgets.QLabel, 'dateLabel')
        self.fromLabel = self.findChild(QtWidgets.QLabel, 'fromLabel')
        self.toLabel = self.findChild(QtWidgets.QLabel, 'toLabel')
        
        self.fromSelectorBox = self.findChild(QtWidgets.QComboBox, 'fromSelector')
        self.fromSelectorBox.clear()
        self.fromSelectorBox.addItems(self.sectionList)
        
        self.toSelectorBox = self.findChild(QtWidgets.QComboBox, 'toSelector')
        self.toSelectorBox.clear()
        self.toSelectorBox.addItems(self.sectionList)
        
        self.searchInput = self.findChild(QtWidgets.QLineEdit, 'searchInput')
        
        self.dateEdit = self.findChild(QtWidgets.QDateEdit, 'dateEdit')
        self.SetDateStyle()
        
        self.menuBar = self.findChild(QtWidgets.QMenuBar, 'menubar')
        self.menu = self.findChild(QtWidgets.QMenu, 'menu')
        self.adminMenu = self.findChild(QtWidgets.QMenu, 'administrator')
        self.adminTools = self.findChild(QtWidgets.QAction, 'adminTools')
        self.menuExitOption = self.findChild(QtWidgets.QAction, 'exit')
        self.openOrder = self.findChild(QtWidgets.QAction, 'openOrder')
        self.SetUpMenuBar()
        
    def SetUpMenuBar(self):
        # setup menu exit button       
        self.menuExitOption.setShortcut('Ctrl+Q')
        self.menuExitOption.setStatusTip('Έξοδος προγράμματος')
        self.menuExitOption.triggered.connect(self.exitCall)
        
        # setup admin tools option
        self.adminTools.setShortcut('Ctrl+E')
        self.adminTools.setStatusTip('Εργαλεία Διαχειριστή')
        self.adminTools.triggered.connect(self.adminToolsPressed)
        
        # setup open order option
        self.openOrder.setShortcut('Ctrl+R')
        self.openOrder.setStatusTip('Αλλαγή Υπάρχουσας παραγγελίας')
        self.openOrder.triggered.connect(self.openOrderFile)
        
    def SetTableStyle(self):
        header = self.orderView.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        
    def SetDateStyle(self):
        self.dateEdit.setDateTime(QtCore.QDateTime.currentDateTime())
        self.dateEdit.setMaximumDate(QtCore.QDate(7999, 12, 28))
        
    def clearButtonPressed(self):
        self.orderView.setRowCount(0)

    def AddItemPressed(self):
        selectedSectionTo = str(self.toSelectorBox.currentText())
        dialog = AddItemWindow(self.productDictionary[self.sectionDictionary[selectedSectionTo]], selectedSectionTo)
        item = dialog.getResults()
        dialog.close()
        if(item is None):
            return
        if(len(item) > 0):
            self.AddItemToView(item[0], item[1], item[2])

    def CreateOrderPressed(self):
        filepath = self.saveFileDialog()
        if filepath is None:
            return
        data = self.getTableData()
        try:
            wb = load_workbook(filename="./files/data/Template.xlsx")
        except Exception as e:
            QMessageBox.information(self, 'Σφάλμα!', f'Το αρχείο "{e.filename}" δεν υπάρχει.\nΚλείστε το αρχείο και ξαναπροσπαθήστε.\n\n{e}')
        ws = wb.worksheets[0]
        
        ws['B2'] = self.fromSelectorBox.currentText()
        ws['D2'] = self.toSelectorBox.currentText()
        ws['E3'] = self.dateEdit.date().toString('dd/MM/yyyy')
        for index, row in enumerate(data):
            ws[f'A{index + 5}'] = row[0]
            ws[f'B{index + 5}'] = row[1]
            ws[f'A{index + 5}']._style = copy(ws['B3']._style)
            ws[f'B{index + 5}']._style = copy(ws['B3']._style)
            ws[f'C{index + 5}']._style = copy(ws['B3']._style)
            ws[f'D{index + 5}']._style = copy(ws['B3']._style)
            ws[f'E{index + 5}']._style = copy(ws['B3']._style)
        
        try:    
            wb.save(filepath)
        except Exception as e:
            QMessageBox.information(self, 'Σφάλμα!', f'Το αρχείο "{e.filename}" ειναι ήδη ανοιχτό.\nΚλείστε το αρχείο και ξαναπροσπαθήστε.\n\n{e}')
    
    def adminToolsPressed(self):
        password = PasswordInputWindow().getData()
        if password == os.getenv('ADMIN_PASSWORD'):
            window = adminTools(self.sectionList, self.sectionDictionary)
            window.exec_()
        else:
            QMessageBox.information(self, 'Προσοχή', 'Εσφαλμένος κωδικός')  
            
    def DeleteItemPressed(self):
        rowPosition = self.orderView.rowCount()
        self.orderView.removeRow(rowPosition - 1)
        
    def exitCall(self):
        self.close()  
        
    def openOrderFile(self):
        filepath = self.openFileDialog()
        wb = load_workbook(filename=filepath)
        ws = wb.worksheets[0]
        if wb is None:
            return
        self.orderView.setRowCount(0)
        for row in ws.iter_rows(min_row=5, values_only=True):
            if(row[0] is None):
                continue
            self.AddItemToView(amount=row[0], name=row[1])
        self.productList.sortItems(1, order=QtCore.Qt.AscendingOrder)

    def AddItemToView(self, amount='0', unit='', name=''):
        '''Adds an item to the list.
 
        :param amount: The amount of the item
        :type amount: float
        :param unit: The unit of the item
        :type unit: string
        :param name: The name of the item
        :type name: string
        '''
        totalUnits = f'{amount} {unit}'
        rowPosition = self.orderView.rowCount()
        self.orderView.insertRow(rowPosition)
        self.orderView.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(totalUnits.strip()))
        self.orderView.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(name.strip()))
        
    def searchTable(self):
        # self.find(self.searchInput.text().strip().upper())
        if (self.text != self.searchInput.text().strip().upper()):
            self.text = self.searchInput.text().strip().upper()
            self.items = self.orderView.findItems(self.text, QtCore.Qt.MatchContains)
            self.index = 0
        else:
            if(self.index < len(self.items) - 1):
                self.index += 1
            else:
                self.index = 0
        if self.items:
            self.orderView.selectRow(self.items[self.index].row())
        else:
            if(self.text != ''):
                QMessageBox.information(self, 'Αναζήτηση', f'Δεν βρέθηκε το προϊόν με το ονομα "{self.searchInput.text().strip()}"')
    
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
        
    def saveFileDialog(self, filetypes="Excel Files (*.xlsx);;All Files (*)"):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self, "Αποθήκευση παραγγελίας", "", filetypes, options=options)
        if fileName:
            return fileName
            
    def openFileDialog(self, filetypes="Excel Files (*.xlsx);;All Files (*)"):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Άνοιγμα λίστας", "", "Excel Files (*.xlsx);;All Files (*)", options=options)
        if fileName:
            return fileName
    
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
    def __init__(self, productDictionary, currentSection):
        super(AddItemWindow, self).__init__()
        # Load the main UI file
        uic.loadUi('./files/UI/createOrder.ui', self)
        self.text = ''
        self.items = []
        self.index = 0
        self.ConnectLogicToObjects(productDictionary, currentSection)   
    
    def ConnectLogicToObjects(self, productDictionary, currentSection):
        self.addButton = self.findChild(QtWidgets.QPushButton, 'addItem')
        self.addButton.clicked.connect(self.AddButtonPressed)
        
        self.searchButton = self.findChild(QtWidgets.QPushButton, 'searchButton')
        self.searchButton.clicked.connect(self.searchTable) 
        
        self.manualAddItemButton = self.findChild(QtWidgets.QPushButton, 'manualAddItem')
        self.manualAddItemButton.clicked.connect(self.manualAddItemPressed) 
        
        self.currentSectionLabel = self.findChild(QtWidgets.QLabel, 'currentSectionLabel')
        self.currentSectionLabel.setText(currentSection)
        
        self.searchInput = self.findChild(QtWidgets.QLineEdit, 'searchInput')
        
        self.productList = self.findChild(QtWidgets.QTableWidget, 'productList')
        self.SetTableStyle()
        
        for i in range(len(productDictionary)):
            self.AddItemToView(productDictionary[i][2], productDictionary[i][1])
        self.productList.sortItems(1, order=QtCore.Qt.AscendingOrder)
            
    def SetTableStyle(self):
        header = self.productList.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        
    def searchTable(self):
        # self.find(self.searchInput.text().strip().upper())
        if (self.text != self.searchInput.text().strip().upper()):
            self.text = self.searchInput.text().strip().upper()
            self.items = self.productList.findItems(self.text, QtCore.Qt.MatchContains)
            self.index = 0
        else:
            if(self.index < len(self.items) - 1):
                self.index += 1
            else:
                self.index = 0
        if self.items:
            self.productList.selectRow(self.items[self.index].row())
        else:
            if(self.text != ''):
                QMessageBox.information(self, 'Αναζήτηση', f'Δεν βρέθηκε το προϊόν με το ονομα "{self.searchInput.text().strip()}"')        
                
    def manualAddItemPressed(self):
        self.currentItem = []
        inputBox = addExtraItem()
        amount = inputBox.getResults()
        inputBox.close()
        if (amount is None):
            self.close()
        else:
            self.currentItem.append(amount[0]) 
            self.currentItem.append(amount[1])
            self.currentItem.append(amount[2])
            
    def AddButtonPressed(self):
        self.currentItem = []
        if self.productList.currentItem():
            inputBox = ItemNumberInput()
            amount = inputBox.getResults()
            inputBox.close()
            if (amount is None):
                self.close()
            else:
                self.currentItem.append(amount) 
                self.currentItem.append(self.productList.item(self.productList.currentItem().row(), 0).text())
                self.currentItem.append(self.productList.item(self.productList.currentItem().row(), 1).text())
                
    def getResults(self):
        if self.exec_() == QDialog.Accepted:
            item = self.currentItem
            return item
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
    
class addExtraItem(QtWidgets.QDialog):
    def __init__(self):
        super(addExtraItem, self).__init__()
        # Load the main UI file
        uic.loadUi('./files/UI/addExtraItem.ui', self)
        self.ConnectLogicToObjects()
        
    def ConnectLogicToObjects(self):
        self.nameInputBox = self.findChild(QtWidgets.QLineEdit, 'nameInputBox')
        self.amountInputBox = self.findChild(QtWidgets.QLineEdit, 'amountInputBox')
        self.unitInputBox = self.findChild(QtWidgets.QLineEdit, 'unitInputBox')
        
        self.amountLabel = self.findChild(QtWidgets.QLabel, 'amountLabel')
        self.nameLabel = self.findChild(QtWidgets.QLabel, 'nameLabel')
        self.unitInputLabel = self.findChild(QtWidgets.QLabel, 'unitInputLabel')
        
    def getResults(self):
        if self.exec_() == QDialog.Accepted:
            item = ['0', '0', 'Empty']
            item[0] = self.amountInputBox.text().strip().upper()
            item[1] = self.unitInputBox.text().strip().upper()
            item[2] = self.nameInputBox.text().strip().upper()
            return item
        else:
            return None
        
class adminTools(QtWidgets.QDialog):
    def __init__(self, sectionList, sectionDictionary):
        super(adminTools, self).__init__()
        # Load the main UI file
        uic.loadUi('./files/UI/adminTools.ui', self)
        self.sectionList = sectionList
        self.sectionDictionary = sectionDictionary
        self.ConnectLogicToObjects()
        
    def ConnectLogicToObjects(self):
        self.changeProductList = self.findChild(QtWidgets.QPushButton, 'changeProductList')
        self.changeProductList.clicked.connect(self.changeProductListClicked)
    
        self.addSingleItem = self.findChild(QtWidgets.QPushButton, 'addSingleItem')
        self.addSingleItem.clicked.connect(self.addSingleItemClicked)
        
        self.adminPasswordChange = self.findChild(QtWidgets.QPushButton, 'adminPasswordChange')
        self.adminPasswordChange.clicked.connect(self.adminPasswordChangeClicked)
        
    def changeProductListClicked(self):
        filepath = self.openFileDialog()
        if(filepath):
            dest = './files/data/ProductList.xlsx'
            try:    
                copyfile(filepath, dest)
            except Exception as e:
                QMessageBox.information(self, 'Σφάλμα!', f'Το αρχείο "{e.filename}" ειναι ήδη ανοιχτό.\nΚλείστε το αρχείο και ξαναπροσπαθήστε.\n\n{e}')
                
    def addSingleItemClicked(self):
        dialog = addExtraItemToData(self.sectionList, self.sectionDictionary)
        item = dialog.getData()
        if item:
            try:
                wb = load_workbook(filename="./files/data/ProductList.xlsx")
            except Exception as e:
                QMessageBox.information(self, 'Σφάλμα!', f'Το αρχείο "{e.filename}" ειναι ήδη ανοιχτό.\nΕπικοινωνήστε με τον διαχειρηστή του συστήματος σας.\n\n{e}')
            
            # add item to total view
            ws = wb.worksheets[0]
            ws.append([item[0], item[1], item[2]])
            
            # add the item to the section worksheet
            if (self.sectionDictionary[item[3]] != wb.sheetnames[0]):
                ws = wb[self.sectionDictionary[item[3]]]
                ws.append([item[0], item[1], item[2]])
            
            try:
                wb.save('./files/data/ProductList.xlsx')
            except Exception as e:
                QMessageBox.information(self, 'Σφάλμα!', f'Το αρχείο "{e.filename}" δεν μπορούσε να αποθηκευτεί.\nΕπικοινωνήστε με τον διαχειρηστή του συστήματος σας.\n\n{e}')               
    
    def adminPasswordChangeClicked(self):
        dialog = PasswordInputWindow('Εισαγωγή νέου κωδικού Διαχειριστή:')
        password = dialog.getData()
        if password:
            os.environ["ADMIN_PASSWORD"] = password
            try:
                with open('./files/data/data.dat', 'w') as file:
                    file.write(password)
                QMessageBox.information(self, '', 'Ο κωδικός αλλαξε επιτυχώς.')
            except Exception as e:
                QMessageBox.information(self, 'Σφάλμα!', f'Ο κωδικός δεν μπόρεσε να αλλαχθεί. Προσπαθήστε ξανά.\n\n {e}')
        elif password == 'PASSWORD REJECTED':
            return
        else:
            QMessageBox.information(self, 'Σφάλμα!', 'Ο κωδικός δεν μπόρεσε να αλλαχθεί. Προσπαθήστε ξανά.')
    
    def openFileDialog(self, filetypes="Excel Files (*.xlsx);;All Files (*)"):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Άνοιγμα λίστας", "", "Excel Files (*.xlsx);;All Files (*)", options=options)
        if fileName:
            return fileName
            
        
class addExtraItemToData(QtWidgets.QDialog):
    def __init__(self, sectionList, sectionDictionary):
        super(addExtraItemToData, self).__init__()
        # Load the main UI file
        uic.loadUi('./files/UI/addExtraItemToData.ui', self)
        self.sectionDictionary = sectionDictionary
        self.sectionList = sectionList
        self.ConnectLogicToObjects()
        
    def ConnectLogicToObjects(self):
        self.nameInputBox = self.findChild(QtWidgets.QLineEdit, 'nameInputBox')
        self.codeInputBox = self.findChild(QtWidgets.QLineEdit, 'codeInputBox')
        self.unitInputBox = self.findChild(QtWidgets.QLineEdit, 'unitInputBox')
        
        self.codeLabel = self.findChild(QtWidgets.QLabel, 'codeLabel')
        self.nameLabel = self.findChild(QtWidgets.QLabel, 'nameLabel')
        self.unitInputLabel = self.findChild(QtWidgets.QLabel, 'unitInputLabel')
        self.sectionLabel = self.findChild(QtWidgets.QLabel, 'sectionLabel')
        
        self.sectionSelector = self.findChild(QtWidgets.QComboBox, 'sectionSelector')
        self.sectionSelector.clear()
        self.sectionSelector.addItems(self.sectionList)
        
    def getData(self):
        '''Returns the new item in an array
        
        [0] the code of the item as input by the user
        
        [1] the name of the item as input by the user
        
        [2] the unit of the item as input by the user
        
        [3] the section of the item as input by the user
        '''
        if self.exec_() == QDialog.Accepted:
            item = []
            item.append(self.codeInputBox.text().strip())
            item.append(self.nameInputBox.text().strip())
            item.append(self.unitInputBox.text().strip())
            item.append(self.sectionSelector.currentText())
            return(item)
        else:
            return None
        
class PasswordInputWindow(QtWidgets.QDialog):
    def __init__(self, text='Κωδικός Διαχειριστή:'):
        super(PasswordInputWindow, self).__init__()
        # Load the main UI file
        uic.loadUi('./files/UI/passwordInput.ui', self)
        self.ConnectLogicToObjects(text)
    
    def ConnectLogicToObjects(self, text):
        self.label = self.findChild(QtWidgets.QLabel, 'label')
        self.label.setText(text)
        self.passwordInput = self.findChild(QtWidgets.QLineEdit, 'passwordInput')
        
    def getData(self):
        if self.exec_() == QDialog.Accepted:
            return self.passwordInput.text()
        elif self.exec_() == QDialog.Rejected:
            return 'PASSWORD REJECTED'
        else:
            return None
    
    def closeEvent(self, event):
        self.close()
    
        
class LoadingWindow(QtWidgets.QDialog):
    def __init__(self):
        super(LoadingWindow, self).__init__()
        # Load the main UI file
        uic.loadUi('./files/UI/LoadingWindow.ui', self)