"""Doc."""
from PyQt5 import QtWidgets
from UI import Ui
import sys

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
