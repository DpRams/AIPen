# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 11:32:12 2020

@author: exzob
"""

from openpyxl import Workbook
import numpy as np

wb = Workbook()

ws = wb.create_sheet("che")
label = [[0],
         [1],
         [2],
         [3]
         ]
feature = 
#这个地方之所以 变成numpy格式是因为在很多时候我们都是在numpy格式下计算的，模拟一下预处理
label = np.array(label)
feature = np.array(feature)

label_input = []
for l in range(len(label)):
    label_input.append(label[l][0])



ws.append(label_input)
for f in range(len(feature[0])):

    ws.append(feature[:, f].tolist())


wb.save("chehongshu.xlsx")
