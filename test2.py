#!/usr/bin/env python
#coding=utf-8

import xlrd
import re
import HTMLParser


def getValueContent(s):
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', s)
    dd= dd.replace('V&amp;','')
    return dd

workbook = xlrd.open_workbook('./excel/好奇心日报-3156条.xlsx')
worksheet = workbook.sheet_by_name(u'Worksheet')

num_rows = worksheet.nrows
for n in range(1,3156):
    row = worksheet.row_values(n)
    # print type(row[3])
    content_row = row[3]
    data = getValueContent(content_row)
    file_name = "./doc/"+str(n)+".txt"
    print file_name
    file_object = open(file_name , "w")
    print type(data)
    file_object.writelines(data.encode("utf-8"))
    file_object.close()
    print ('row%s is %s' %(n ,data))
