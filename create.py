import json
import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

with open('data.json') as project_file:    
    data = json.load(project_file)  

df = pd.json_normalize(data, record_path='included')

df1 = df.head(1)

df2 = df1[['attributes.name', 'attributes.address', 'attributes.phone']]
df2.set_axis(['MÜŞTERİ ADI', 'ADRESİ', 'TELEFON'], axis=1, inplace=True)

df3 = df[(df['type'] == 'products')]

df4 = df3[['attributes.code', 'attributes.name']]
df4.set_axis(['ÜRÜN KODU', 'ÜRÜN ADI'], axis=1, inplace=True)
df4.reset_index(inplace=True)

df5 = df[(df['type'] == 'sales_invoice_details')]

df6 = df5[['attributes.quantity']]
df6.set_axis(['ADET'], axis=1, inplace=True)
df6.reset_index(inplace=True)

df_out = pd.concat([df2, df4, df6], axis=1)
df_out.drop(df_out.columns[[3,6]], axis=1, inplace=True)

import numpy as np

df_out['LİTRE'] = np.where(df_out['ÜRÜN ADI'].str.contains('4L', regex= True), 4, 12)

df_out['ADET'] = df_out['ADET'].astype(float)

df_out['ADET/KOLİ'] = df_out['ADET'] / df_out['LİTRE']

df_out['ADET/KOLİ'] = df_out['ADET/KOLİ'].astype(int)

df_out['KG_c'] = np.where(df_out['LİTRE'] == 4, 15, 10)

df_out['KG'] = df_out['ADET/KOLİ'] * df_out['KG_c']

df_final = df_out.drop(['KG_c', 'LİTRE'], axis=1)

df_final = df_final[['MÜŞTERİ ADI', 'ADRESİ', 'TELEFON', 'ÜRÜN KODU', 'ÜRÜN ADI', 'ADET/KOLİ', 'ADET', 'KG']]

import datetime

filename = "DİNÇER SİPARİŞ " + datetime.datetime.now().strftime("%d.%m.%Y_%H.%M")

writer = pd.ExcelWriter(f"{filename}.xlsx") 
df_final.to_excel(writer, sheet_name='siparis', index=False)

# Auto-adjust columns' width
for column in df_final:
    column_width = max(df_final[column].astype(str).map(len).max(), len(column))
    col_idx = df_final.columns.get_loc(column)
    writer.sheets['siparis'].set_column(col_idx, col_idx, (column_width*1.1))

writer.save()