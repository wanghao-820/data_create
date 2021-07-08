# -*- coding: utf-8 -*-



import openpyxl
#打开文件，获取文件的workbook
file =u"D:\pythonspace\orderexcel\内部报班1000.xlsx"   #文件路径

wb = openpyxl.load_workbook(file)
sheetname =wb['Sheet1']
print(sheetname)
