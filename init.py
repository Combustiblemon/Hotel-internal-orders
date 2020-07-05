"""Doc."""
from PyQt5 import QtWidgets
from UI import MainWindow
from openpyxl import Workbook, load_workbook 
import sys
import json
import io

# Save workbook
""" workbook = Workbook()
sheet = workbook.active

sheet["A1"] = "hello"
sheet["B1"] = "world!"

workbook.save(filename="./files/data/hello_world.xlsx") """

# load the excel file containing all the items
workbook = load_workbook(filename="./files/data/ProductList.xlsx")

# add all the individual sheets into one list
""" sheets = []
for sheet in workbook.worksheets:
    sheets.append(sheet) """
productList = {}
for sheet in workbook.sheetnames:
    productList[sheet] = []
    for row in workbook[sheet].iter_rows(values_only=True):
        productList[sheet].append(row)
# print(productList)
# print(workbook.sheetnames)
# with open('dictionary', 'w', encoding="utf8") as file:
#    json.dump(exDict, file, ensure_ascii=False)

# import the dictionary from the .json file
sectionDictionary = {}
with open('./files/data/dictionary.json', 'r', encoding="utf8") as file:
    sectionDictionary = json.load(file)

# print(sectionDictionary['Αποθήκη'])

# create sectionList from the dictionary
""" sectionList = []
for k in sectionDictionary.items():
    sectionList.append(k[0]) """
#print(sectionList)
#print(sectionDictionary['Κουζίνα'])
# sheets = workbook['ΣΥΝΟΛΟ']
# print(sheet['A1'].value)


# print(sheet.title)

# setup the application
app = QtWidgets.QApplication(sys.argv)
window = MainWindow(sectionDictionary, workbook)
window.show()
app.exec_() 