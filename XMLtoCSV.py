# Librerías
import pandas as pd
import numpy as np
import os
from pdfminer.high_level import extract_text
from re import search
import re


def toCSV(path):
    os.chdir(path)
    files = os.listdir(path)
    valFiles = set()#Archivos validados con extensión válida
    for file in files:
        if file.endswith(".xml") or file.endswith(".pdf"):
            valFiles.add(file.split(".")[0])
    def finder2(word,lista,spaces):
        i = lista.index(word)
        return lista[i+spaces]
    def finder(word,string,escape="\""):
        it = [m.start() for m in re.finditer(word, string)]
        out = []
        for i in it:
            indice = 0
            temp = []
            start = i
            # Búsqueda exhaustiva de la existencia de palabras
            if start == -1:
                print("Error Fatal")
                return None
            start += len(word)+1
            while string[start] != escape:
                temp.append(string[start])
                start+=1
            temp = "".join(temp)
            out.append(temp)
            indice +=1
        out = np.array(out).T
        return out
    # Se ha creado la lista de archivos validada
    it = 0
    arr = []
    for file in valFiles:
        print(file)
        # Procesado de archivos XML
        if os.path.exists(file+".xml"):
            xmlFile = open(file+".xml","r")
            s = xmlFile.read()
            # Variables que tienen que ser almacenadas
            fecha = 0
            serie = 0
            tc = 0
            # occbi y referencia no se encuentran en XML
            occbi = 0
            ref = 0
            folio = 0
            tequila = 0
            tipo = 0
            concepto = 0
            totCargos = 0
            subtot = 0
            
            # Exploración del archivo por string para llenar variables
            s.find("Fecha=")
            
            fecha = finder("Fecha=",s,"T")
            serie = finder("Serie=",s)
            tc = finder("TipoCambio=",s)
            # occbi y referencia no se encuentran en XML
            occbi = 0
            ref = 0
            folio = finder("Folio=",s)
            tequila = 0
            tipo = 0
            concepto = finder("Descripcion=",s,".")
            cases = finder("Cantidad=",s)
            bot = 0
            lit = 0
            subtot = finder("SubTotal=",s)
            desc = 0
            abo = 0
            putas = ["0"]*(len(concepto)-1)
            putas.append(subtot[-1])
            subtot = putas
            totCargos = putas

            
            # Corrección de palabra añejo
            print(concepto)
            for i in range(len(concepto)):
                corr = search(" A.*EJO",concepto[i])
                if corr:
                   new = concepto[i][:corr.span()[0]] + " AÑEJO" + concepto[i][corr.span()[1]:]
                   concepto[i] = new
            # Corrección quotes
            for j in range(2):
                for i in range(len(concepto)):
                    corr = search("&quot;",concepto[i])
                    if corr:
                       new = concepto[i][:corr.span()[0]] + "\"" + concepto[i][corr.span()[1]:]
                       concepto[i] = new
            
            
            
            
            # Procesado de PDF
            pdfFile = extract_text(file+".pdf")
            # Exploración del archivo por string para llenar variables
            ref =  finder("ORDE",pdfFile,"P")
            occbi = ref
            print(concepto)
            # Iterando conceptos dentro de una factura
            for i in range(len(concepto)):        
                arr.append([fecha[0],serie[0],tc[0],occbi[0],ref[0],folio[0],tequila,tipo,concepto[i],
                                      cases[i],bot,lit,subtot[i],desc,abo,totCargos[i]])
        else: #sólo se procesa PDF

            print("Procesando sólo PDF")
            s = extract_text(file+".pdf")
            fecha = re.findall(r'creada.([0-2][0-9]|3[0-1])/([0-2][0-9]|3[0-1])/(\d{4})',s,flags=re.I|re.M|re.X)
            fecha = "/".join(list(fecha[0]))
            s = re.split("\n",s)
            s.remove('')
            serie = "P"
            tc = finder2("TC ",s,4)
            occbi = [x for x in s if "CBI" in x]
            if occbi:
                occbi = "OC"+occbi[0]
            else:
                occbi = 0
            ref = occbi
            def folio(lista):
                filter_object = filter(lambda a: "INVOICE" in a, lista)
                invoice = re.findall(r'\d+',list(filter_object)[0])
                return int(invoice[0])
            folio = folio(s)
            tequila = 0
            tipo = 0
            concepto = [s[s.index("Cantidad")+1] +" "+ s[s.index("Descripcion")+1]]
            bot = 0
            lit = 0
            desc = 0
            abo = 0
            cases = 0
            tot = [x for x in s if "." in x]
            tot = tot[-1]
            subtot = tot

            arr.append([fecha, serie, tc, occbi, ref, folio, tequila, tipo, concepto[0],
                    cases, bot, lit, subtot, desc, abo, tot])

    arr = np.array(arr)
    target = pd.DataFrame(data = arr,columns = ["Fecha","Serie","TC"," OC. CBI ","Referencia","Folio",
                                     "Tequila","Tipo","Concepto","Cases","Botellas","Litros",
                                     "Subtotal","Descuentos","Abonos","Total Cargos"])
    target.sort_values(by=["Folio"],inplace=True)
    target.to_csv("resultado.csv",index=False,encoding="iso-8859-1")
    print(path)
    


def askDir():
    import tkinter as tk
    from tkinter import filedialog
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askdirectory()
    return path
    
# debugger 
#toCSV(r"D:\\VENVXMLCSV\\SeriePprueba\\")





    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    