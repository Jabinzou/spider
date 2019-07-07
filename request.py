# -*- coding: utf-8 -*-

import sys
import requests
import linecache
from bs4 import BeautifulSoup
from xlwt import *
import xlwt
from tqdm import tqdm
import time
import random
from multiprocessing import Process,Pool,Manager
import os

reload(sys)
sys.setdefaultencoding('utf-8')
# 获取文件制定行数，是第一次读取后面直接从缓存中拿
def get_line(filePath, line):
  data = linecache.getline(filePath, line)
  line_date = data.split(',')
  return line_date

def request_line(startInfo = ['','','', ''], endInfo = ['','','', ''], composeData = []):
  param = {
    '_fm.es._0.s': startInfo[0],
    '_fm.es._0.se': startInfo[1],
    '_fm.es._0.sen': startInfo[2],
    '_fm.es._0.r': endInfo[0],
    '_fm.es._0.re': endInfo[1],
    '_fm.es._0.rec': endInfo[2]
  }
  try:
    list = get_ip_list()
    proxy = get_random_ip(list)
    r = requests.get('https://56.1688.com/order/price/estimate_price.htm?notFirst=true&_fm.es._0.o=&_fm.es._0.c=&_fm.es._0.co=&_fm.es._0.sp=&_fm.es._0.i=&_fm.es._0.is=&_fm.es._0.isf=&_fm.es._0.isp=&_fm.es._0.iscn=&_fm.es._0.isn=&_fm.es._0.isc=&_fm.es._0.isa=&_fm.es._0.ro=&_fm.es._0.w=&_fm.es._0.we=&_fm.es._0.v=&_fm.es._0.vo=&_fm.es._0.tra=&_fm.es._0.tran=&_fm.es._0.isfr=&_fm.es._0.a=&_fm.es._0.d=&_fm.es._0.d=&_fm.es._0.d=&_fm.es._0.d=&r=1560672972573&sizePerPage=&pageIndex=1&weight=&expressRouteSortType=&_fm.es._0.sentc=',proxies=proxy ,params=param)
    soup = BeautifulSoup(r.text, 'lxml')
    tags = soup.select('#orderbyBar span[style="font-weight:bold;color:#FF7300"]')
    composeData.append([startInfo[3].replace('\n', ''), endInfo[3].replace('\n', ''),tags[0].get_text(), tags[1].get_text()])
  except Exception as e:
    # print(e, r.text)
    print('\n'+startInfo[3]+'-'+endInfo[3]+'\n')

def get_ip_list():
    temp_ip_list=[]
    with open('iplist.txt', 'r') as f:
      while True:
        ip=f.readline().replace('\n','')
        temp_ip_list.append('http://'+ip)
        if not ip:
            break
    return temp_ip_list
     
def get_random_ip(list):        
    proxy_ip=random.choice(list)
    proxies={
        'http':proxy_ip
    }
    return proxies

def pollData():
  queryInfo = []
  for line in range(start, end+1):
    resData = get_line('/Users/lavi/Documents/cplus/city_province.txt', line)
    for inLine in range(start, end+1):
      toData = get_line('/Users/lavi/Documents/cplus/city_province.txt', inLine)
      queryInfo.append([[resData[0], resData[2],'', resData[1]+resData[3]], [toData[0], toData[2],'', toData[1]+toData[3]]])
  return queryInfo

def init():
  global start
  global end
  global pbar
  start = input('请输入开始行数:')
  end = input('请输入结束行数:')
  pbar = tqdm(total=((end-start+1) * (end-start+1)))

def saveFile():
  file = Workbook(encoding = 'utf-8')
  table = file.add_sheet('广东省物流数据')
  table.col(0).width = 256 * 24
  table.col(1).width = 256 * 24
  font = xlwt.Font()  # Create Font
  style = xlwt.XFStyle()  # Create Style
  font.height = 20 * 14  # 字体大小
  style.font = font
  try: 
    for i,p in enumerate(composeData):
      for j,q in enumerate(p):
        # print i,j,q
        table.write(i,j,q,style)
    file.save('nation.xlsx')
  except Exception as e:
    f = open("nation.txt",'w')
    for da in composeData:
      print da
      f.write(','.join(da))
      f.write('\n')

def updatePb(res):
  pbar.update(1)

def main():
  init()
  global composeData
  compose = pollData()
  manager = Manager()
  composeData = manager.list([['起始位置','终点位置', '公司数量', '线路数量']])
  pool = Pool(4)
  print '\nParent process %s'%os.getpid()
  for i in compose:
    pool.apply_async(request_line, args=(i[0],i[1],composeData),callback=updatePb)
  pool.close()
  pool.join()
  pbar.close()
  print '\ndone'
  saveFile()

if __name__=='__main__':
  main()