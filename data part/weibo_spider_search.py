import time
import datetime
import re            
import os    
import sys  
import codecs  
import shutil
import urllib 
from selenium import webdriver        
from selenium.webdriver.common.keys import Keys        
import selenium.webdriver.support.ui as ui        
from selenium.webdriver.common.action_chains import ActionChains
import xlwt
from bs4 import BeautifulSoup

global frist_click
frist_click = 0 
driver = webdriver.Chrome(r'D:\\VSCode\\chromedriver_win32\\chromedriver.exe')

def login_manually(login_url, cookies_file, driver1=None):
    if driver1 is None:
        driver.get(login_url)
    time.sleep(40) 
    cookies = driver.get_cookies()
    print(cookies)
def GetSearchContent(key):

    print ('搜索热点主题：', key)

    item_inp = driver.find_element_by_xpath("//*[@id='pl_homepage_search']/div/div[2]/div/input")
    item_inp.send_keys(key)
    item_inp.send_keys(Keys.RETURN)    

    current_url = driver.current_url
    print(current_url)
    current_url = current_url.split('&')[0] 

    global start_stamp
    global page

    start_date = datetime.datetime(2020,2,18,0)
    end_date = datetime.datetime(2020,2,22,0)
    delta_date = datetime.timedelta(days=1)

    start_stamp = start_date
    end_stamp = start_date + delta_date

    global outfile
    global sheet

    outfile = xlwt.Workbook(encoding = 'utf-8')

    while end_stamp <= end_date:

        page = 1

        sheet = outfile.add_sheet(str(start_stamp.strftime("%Y-%m-%d-%H")))
        initXLS()

        url = current_url + '&typeall=1&suball=1&timescope=custom:' + str(start_stamp.strftime("%Y-%m-%d-%H")) + ':' + str(end_stamp.strftime("%Y-%m-%d-%H")) + '&Refer=g'
        driver.get(url)
        
        handlePage() 

        start_stamp = end_stamp
        end_stamp = end_stamp + delta_date


def handlePage():
    while True:
        time.sleep(2)
        if  True:
            print ("getContent")
            getContent()
            if True:
                print(getnextpage() == "下一页")
                print(getformerpage() == '')
                if getnextpage() == "下一页" and getformerpage() == '': 
                    print(getnextpage())
                    next_page_btn = driver.find_element_by_xpath("//*[@id='pl_feedlist_index']/div[3]/div/a")
                    next_page_btn.click()
                    print('go to next page1')
                elif getnextpage() == '下一页' and getformerpage() =='上一页':
                    print(getnextpage())
                    next_page_btn = driver.find_element_by_xpath("//*[@id='pl_feedlist_index']/div[3]/div/a[2]")
                    next_page_btn.click()
                    print('go to next page2')
                elif getnextpage() == '' and getformerpage() == '上一页':
                     print('last page')
                     break
                else:
                    print('就一页')
                    break
            else:
                print ("no Next")
                break
        else:
            print ("no Content")
            break

def checkContent():
    try:
        driver.find_element_by_xpath("//div[@class='pl_noresult']")
        flag = False
    except:
        flag = True
    return flag


def getformerpage():
    bsobj = BeautifulSoup(driver.page_source,features="lxml")
    try:
        formerpage = str(bsobj.find('a',{'class':'prev'}).text)
    except:
        formerpage = ''
    return formerpage

def getnextpage():
    bsobj = BeautifulSoup(driver.page_source,features="lxml")
    try:
        nextpage = str(bsobj.find('a',{'class':'next'}).text)
    except:
        nextpage = ''
    return nextpage

def checkNext():
    try:
        driver.find_element_by_xpath("//*[@id='pl_feedlist_index']/div[3]/div/a")
    except:
        pass
    
    if checkifthelastpage(): 
            print('donot have next')
            return False
    else:
            print('have next')
            return True

def initXLS():
    name = ['博主昵称', '博主主页', '微博内容', '发布时间','转发','赞']
    
    global row
    global outfile
    global sheet

    row  = 0
    for i in range(len(name)):
        sheet.write(row, i, name[i])
    row = row + 1
    outfile.save("./crawl_output_YS.xls")

def writeXLS(dic):
    global row
    global outfile
    global sheet

    for k in dic:
        for i in range(len(dic[k])):
            sheet.write(row, i, dic[k][i])
        row = row + 1
    outfile.save("./crawl_output_YS.xls")

def getContent():
    nodes = driver.find_elements_by_xpath("//div[@class='card-wrap']")
    dic = {}
    global page
    print (str(start_stamp.strftime("%Y-%m-%d-%H")))
    print ('页数:', page)
    page = page + 1

    for i in range(len(nodes)):
        dic[i] = []
        
        try:
            BZNC = nodes[i].find_element_by_xpath(".//div[@class='content']/p[@class='txt']").get_attribute('nick-name')
            print ('博主昵称:', BZNC)
        except:
            pass
        dic[i].append(BZNC)

        try:
            BZZY = nodes[i].find_element_by_xpath(".//div[@class='content']/p[@class='from']/a").get_attribute("href")
            print ('博主主页:', BZZY)
        except:
            pass  
        dic[i].append(BZZY)

       
        try:
            WBNR = nodes[i].find_element_by_xpath(".//div[@class='content']/p[@class='txt']").text
            print ('微博内容:', WBNR)
        except:
            pass 
        dic[i].append(WBNR)

        try:
            FBSJ = nodes[i].find_element_by_xpath(".//div[@class='content']/p[@class='from']/a").text
            print ('发布时间:', FBSJ)
        except:
            pass
        dic[i].append(FBSJ)

        try:
            DIANZAN = nodes[i].find_element_by_xpath(".//div[@class='card-act']/ul/li[4]/a").text
            print("点赞数",DIANZAN)
        except:
            pass
        dic[i].append(DIANZAN)

        try:
            ZHUANFA = nodes[i].find_element_by_xpath(".//div[@class='card-act']/ul/li[2]/a").text
            try:
                ZHUANFA = ZHUANFA.replace('转发','')
                print("转发数",ZHUANFA)
            except:
                pass
        except:
            pass
        dic[i].append(ZHUANFA)
                
        print ('\n')

    #写入Excel
    writeXLS(dic)

if __name__ == '__main__':
    login_manually("http://s.weibo.com/","Weibo.cookies",None)
    key = '冠状病毒'
    GetSearchContent(key)
