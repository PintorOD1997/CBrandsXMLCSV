import os
from re import A
import pandas as pd
path = os.chdir("SerieAprueba")
files = os.listdir(path)
valFiles = set()#Archivos validados con extensión válida
for file in files:
    if file.endswith(".xml"):
        valFiles.add(file.split(".")[0])
# Find with a ReGex what comes after the word "Descuento" and before the next space
def findDiscount(string):
    import re
    try:
        a = re.search('Descuento="(.*?)"', string).group(1)
    except:
        print("Fail")
        a = "Fail"
    print(a)
    return a

invoiceName = []
disc = []
df = pd.DataFrame(columns=["Invoice","Descuento"])
for file in valFiles:
    xmlFile = open(file+".xml","r")
    s = xmlFile.read()
    invoiceName.append(file)
    disc.append(findDiscount(s))

df["Invoice"] = invoiceName
df["Descuento"] = disc

# Save the dataframe to a csv file
df.to_csv("Descuentos.csv",index=False)


