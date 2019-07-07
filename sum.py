# -*- coding: utf-8 -*-
# coding=utf-8

import sys
import requests
import linecache
from xlwt import *
import xlwt
import time
reload(sys)
sys.setdefaultencoding('utf-8')

def main():
  boomark = [['A县区','B县区', '联系强度']]
  file = Workbook(encoding = 'utf-8')
  table = file.add_sheet('联系强度')
  table.col(0).width = 256 * 24
  table.col(1).width = 256 * 24
  font = xlwt.Font()  # Create Font
  style = xlwt.XFStyle()  # Create Style
  font.height = 20 * 14  # 字体大小
  style.font = font
  map = {}
  data = linecache.getlines('/Users/lavi/Documents/cplus/621-relation.txt')
  for line in range(len(data)):
    mapData = data[line].split(',')
    keyNormal = mapData[0]+'_'+mapData[1]
    keyReverse = mapData[1]+'_'+mapData[0]
    if map.has_key(keyNormal):
      continue
    elif map.has_key(keyReverse):
      continue
    else:
      map[keyNormal] = int(mapData[2])
      dataGroup = keyNormal.split('_')
      boomark.append([dataGroup[0],dataGroup[1],map[keyNormal]])
  for i,p in enumerate(boomark):
    for j,q in enumerate(p):
        # print i,j,q
        table.write(i,j,q,style)
  file.save('relations.xlsx')
  #print len(data)

if __name__=='__main__':
  main()