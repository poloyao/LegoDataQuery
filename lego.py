import requests
import re
from bs4 import BeautifulSoup
import csv
import time
import xlsxwriter
import urllib3
import sqlite3Help

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

def get_one_page(url):
    try:
        response = requests.get(url,headers = headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(content):
    try:
        soup = BeautifulSoup(content,'html.parser')
        items = soup.find('div',class_=re.compile('detail_main')).find('div',class_=re.compile('main'))
        for div in items.find('ul').find_all('li'):
            ImgPath = div.find('div',class_=re.compile('img')).find('a')['href']
            pic = requests.get(ImgPath, timeout=10)
            yield {
                'Quantity':int(div.find('div',class_=re.compile('qty')).text.replace('x','')),
                'ImgPath': ImgPath,
                'Img':pic.content,
                #div.find('div',class_=re.compile('img')).find('a')['href'],
                'Part':div.find_all('div',class_=re.compile('code'))[0].text,
                'Design':div.find_all('div',class_=re.compile('code'))[1].text,

            }
        if div['Quantity', 'Img', 'Part', 'Design'] == None:
                return None
    except Exception:
        return None


def main():
    db_name = "legodb.db"
    dbtable = '''create table Part (ImgPath text,Img blob,Part text,Design text)'''
    sqlite3Help.CreateDB(db_name,dbtable)
    dbtable = '''create table Model (ModelID text,Design text)'''
    sqlite3Help.CreateDB(db_name,dbtable)
    dbtable = '''create table PM (ModelID text,PartID text,Design text,Quantity int)'''
    sqlite3Help.CreateDB(db_name,dbtable)
    #legoID = input("请输入编号")
    for legoID in range(42055,42056):
        url = 'http://www.town0.com/inventories/{}.html'.format(legoID)
        content = get_one_page(url)
        print('抓取{}完毕'.format(legoID))
        print('准备插入{}数据'.format(legoID))
        modelItems = sqlite3Help.selectDB(db_name,"select * from Model where ModelID == '{}'".format(legoID))
        if len(modelItems) > 0:
            print("{}已存在将取消插入".format(legoID))
            continue
        else:
            modelsql = ''' insert into Model
                    (ModelID)
                    values
                    ({})'''.format(legoID)    
            sqlite3Help.insterDB(db_name,modelsql)
        partlsql = ''' insert into Part
                (ImgPath,Img,Part,Design)
                values
                (:ImgPath,:Img,:Part,:Design)'''
        pmlsql = ''' insert into PM
                (ModelID,PartID,Design,Quantity)
                values
                ({},:Part,:Design,:Quantity)'''.format(legoID)
        for item in parse_one_page(content):
            print(item['Part'])
            partItem = sqlite3Help.selectDB(db_name,"select Part from Part where Part == {} and Design == {}".format(item['Part'],item['Design']))
            if len(partItem) == 0:
                sqlite3Help.insterDB_item(db_name,partlsql,item)
            sqlite3Help.insterDB_item(db_name,pmlsql,item)


        



    # legoID = input("请输入编号")
    # url = 'http://www.town0.com/inventories/{}.html'.format(legoID)
    # content = get_one_page(url)
    # print('抓取{}完毕'.format(legoID))
    # with open('LegoData.csv', 'a', newline='') as f:
    #     fieldnames = ['Quantity', 'ImgPath', 'Part', 'Design']
    #     writer = csv.DictWriter(f, fieldnames=fieldnames)
    #     writer.writeheader()
    #     for item in parse_one_page(content):
    #         writer.writerow(item)
    #         print(item)

#https://www.lego.com/service/bricks/5/2/302326

if __name__=='__main__':
    main()
