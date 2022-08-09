from cmath import nan
import numpy as np
import pandas as pd

from tabula import read_pdf

def extract_useful_rows_indexes(table):
    rows_index = [index for index, value in enumerate(table.values) if str(value) != 'nan'] 
    return rows_index


if __name__ == '__main__':
    raw_table = read_pdf(r"D:\\VENVXMLCSV\\ocPrueba\\oc CBI0746 UNGERER & CO.pdf", pages='all')[0][2:]
    rows_index = extract_useful_rows_indexes(raw_table.iloc[0])

    clean_table = pd.DataFrame()
    table = []
    for index, row in raw_table.iterrows():
        row_values = [value for index, value in enumerate(row.values) if index in rows_index]
        if "Terms:" in row_values:
            print('chingaste a tu madre pendejo')
            break
        else: 
            table.append(row_values)
        print(row_values)