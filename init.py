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

workbook = load_workbook(filename="./files/data/ProductList.xlsx")
# print(workbook.sheetnames)
sheets = []
for sheet in workbook.worksheets:
    sheets.append(sheet)
# print(workbook)

# with open('dictionary', 'w', encoding="utf8") as file:
#    json.dump(exDict, file, ensure_ascii=False)
sectionDictionary = {}
with open('dictionary', 'r', encoding="utf8") as file:
    sectionDictionary = json.load(file)
#print(dictTest)

sectionList = []
for k in sectionDictionary.items():
    sectionList.append(k[0])
#print(sectionList)
#print(sectionDictionary['Κουζίνα'])
# sheets = workbook['ΣΥΝΟΛΟ']
# print(sheet['A1'].value)


# print(sheet.title)

app = QtWidgets.QApplication(sys.argv)
window = MainWindow(sectionDictionary)
window.show()
app.exec_()