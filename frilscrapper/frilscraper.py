from requests_html import HTMLSession
import sys
import urllib.request, urllib.error, urllib.parse
import webbrowser
from bs4 import BeautifulSoup
import pyautogui
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
import re
import enchant
import shutil
import pandas as pd
from statistics import mean
import os
from urllib.request import Request, urlopen
import urllib.parse
from collections import OrderedDict
import names
import random
import csv
from csv import writer
import datetime

thebrands=['Damir Doma']
owd=os.getcwd()
owd
def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)

def adjustbrandname(brands):
    editbrands=[]
    for brand in brands:
        editbrand=brand.replace(" ","+")
        editbrands.append(editbrand.lower())
    return editbrands

def getalllinks(brandname,thepage):
    url=frilurl+str(thepage)+"&query="+str(brandname)+"&sort=relevance"
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    values = {'name' : names.get_full_name(),
        'location' : 'Northampton',
        'language' : 'Python' }
    headers = { 'User-Agent' : user_agent }
    req = Request(url, headers=headers)
    the_page = urlopen(req).read()
    pageitemsoup = BeautifulSoup(the_page, 'lxml')
    linktags=pageitemsoup.find_all('a',{'class' : 'link_search_image'})
    for itematag in linktags:
        if brandname.replace("+"," ").lower() in str(itematag).lower():
            linklist.append(itematag['href'])
    return(linklist)

def getgetpagerange(brandname):
    checkpage=True
    thepage=1
    while checkpage:
        #changeurl scheme
        url=frilurl+str(thepage)+"&query="+str(brandname)+"&sort=relevance"
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
        values = {'name' : names.get_full_name(),
            'location' : 'Northampton',
            'language' : 'Python' }
        headers = { 'User-Agent' : user_agent }
        req = Request(url, headers=headers)
        the_page = urlopen(req).read()
        pageitemsoup = BeautifulSoup(the_page, 'lxml')
        pagesection=pageitemsoup.find_all('nav',{'class' : 'pagination'})[0]
        pagesectionspan=pagesection.find_all('span')
        if "page current" not in str(pagesectionspan[-1]):
            thepage+=1
        else:
            return thepage
            checkpage=False

for thebrand in adjustbrandname(thebrands):
    frilurl='https://fril.jp/s?except_for_no_brand=true&order=desc&page='
    linklist=[]
    os.chdir(owd)
    if not os.path.exists(thebrand):
        os.makedirs(thebrand)
    os.chdir(thebrand)
    if not os.path.exists(thebrand+"catalogue.csv"):
        append_list_as_row(thebrand+"catalogue.csv",["Brand", "ItemCode","URL","Price","ItemName","Availability","Time","Condition","Size"])
    for page in range(1,getgetpagerange(thebrand)+1):
        allthelinks=getalllinks(thebrand,page)
    owd=os.getcwd()
    owd
    for itemurl in allthelinks:
        spliturl=itemurl.split("/")
        itemcode=spliturl[-1]
        if not os.path.exists(itemcode):
            os.makedirs(itemcode)
            user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
            values = {'name' : names.get_full_name(),
                'location' : 'Northampton',
                'language' : 'Python' }
            headers = { 'User-Agent' : user_agent }
            item_req = Request(itemurl, headers=headers)
            item_page = urlopen(item_req).read()
            item_soup = BeautifulSoup(item_page, 'lxml')
            itemtitle=item_soup.find_all('h1',{'class' : 'item__name'})
            titleis=(itemtitle[0].contents[0].replace("\u3000"," "))
            theprice=item_soup.find_all('span',{'class' : 'item__value'})
            priceis=(theprice[0].contents[0])
            thetable=item_soup.find_all('table',{'class' : 'item__details'})[0]
            thedata=thetable.find_all('td')
            if len(thedata)>3:
                sizeis=(thedata[1].contents[0])
                conditionis=(thedata[3].contents[0])
            else:
                sizeis="N/A"
                conditionis="N/A"
            checksoldout=item_soup.find_all('span')
            thetimeis=datetime.datetime.now()
            if "SOLD OUT" in str(checksoldout):
                issold="SOLD"
            else:
                issold="AVAILABLE"
            allimages=item_soup.find_all('img',{'class' : 'sp-image'})
            imageurls=[]
            for image in allimages:
                imageurls.append(image['src'])
            for clothingimage in imageurls:
                splitimage=clothingimage.split('/')
                urllib.request.urlretrieve(str(clothingimage), str(splitimage[-1]))
                shutil.move(os.getcwd()+'/'+splitimage[-1], os.getcwd()+'/'+itemcode+'/'+splitimage[-1])
                #time.sleep(random.randint(0,2))
            append_list_as_row(thebrand+"catalogue.csv",[thebrand.replace("+"," ").upper(), itemcode,itemurl,priceis,titleis,issold,thetimeis,conditionis,sizeis])
            print(itemcode)
