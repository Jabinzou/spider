
# -*- coding: utf-8 -*-

import sys
from bs4 import BeautifulSoup
import requests
reload(sys)
sys.setdefaultencoding('utf-8')
url='http://www.xicidaili.com/nn/'
headers={
  'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',        
}
ip_list=[]
for a in range(0, 20):
  ip_data=requests.get(url+bytes(a), headers=headers)
  soup=BeautifulSoup(ip_data.text,'html.parser')
  ips=soup.select('tr')
  for i in range(1,len(ips)):
    ip_info=ips[i]
    tds=ip_info.select('td')
    quality = ip_info.select('.country .bar div')
    # 过滤高可用的ip
    if (int((quality[0]['style'].split(':')[1]).encode("utf-8").replace('%', '')) >= 90
      and int((quality[1]['style'].split(':')[1]).encode("utf-8").replace('%', '')) >= 90):
      ip_list.append(tds[1].text+':'+tds[2].text)
f = open("iplist.txt",'w')
for ip in ip_list:
    f.write(ip)
    f.write('\n')