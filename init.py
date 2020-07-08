"""Doc."""
from PyQt5 import QtWidgets
from UI import LoadingWindow, MainWindow
from openpyxl import Workbook, load_workbook
from dotenv import load_dotenv
from pathlib import Path
import os
import sys
import json
import io


app = QtWidgets.QApplication(sys.argv)
loadingW = LoadingWindow()
loadingW.show()

# load .env file into memory
env_path = Path('./files/data/') / '.env'
load_dotenv(dotenv_path=env_path)

# load the excel file containing all the items
workbook = load_workbook(filename="./files/data/ProductList.xlsx")

# add all the individual sheets into one dictionary and link their data
productList = {}
for sheet in workbook.sheetnames:
    productList[sheet] = []
    for row in workbook[sheet].iter_rows(min_row=3, values_only=True):
        if(row[0] is None):
            continue
        productList[sheet].append(row)

# import the dictionary from the .json file
sectionDictionary = {}
with open('./files/data/dictionary.json', 'r', encoding="utf8") as file:
    sectionDictionary = json.load(file)

# setup the application
loadingW.close()
window = MainWindow(sectionDictionary, productList)
window.show()
app.exec_() 