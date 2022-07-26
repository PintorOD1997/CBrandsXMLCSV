from tkinter import filedialog as fd
from tkinter import *
from openpyxl import Workbook
import pandas as pd

win = Tk()
win.withdraw()
filename = fd.askopenfilename()

# Abriendo archivo
data = pd.read_excel(filename)


