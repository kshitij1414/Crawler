# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 19:04:48 2019

@author: Kshitij
"""

#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import *
from selenium.common.exceptions import JavascriptException
import time
from datetime import date
import datetime
import json
import requests

def scraper(url,Dep_date,Dest):
    proxy = Proxy()
    PROXY=  'zproxy.lum-superproxy.io:22225'
    proxy.http_proxy = PROXY
    proxy.ftp_proxy = PROXY
    proxy.sslProxy = PROXY
    proxy.proxy_type = ProxyType.MANUAL
    
    proxy.socksUsername = 'lum-customer-hl_66084dfd-zone-static'
    proxy.socksPassword = "dkacqfyc6h9l"
    
    capabilities = webdriver.DesiredCapabilities.CHROME

    proxy.add_to_capabilities(capabilities)

    browser = webdriver.Chrome(desired_capabilities=capabilities)
    
    browser.get(url)
    time.sleep(10)
    i=0
    date1_arr=[]
    duration_arr= []
    date2_arr=[]
    cost_arr=[]
    flight_arr= []
    failure_arr=[]
    
    try:
        while(i<10):
            stri = str(i)
            date1 = browser.execute_script('x=document.querySelector("#app").shadowRoot.querySelector("#flights-search").shadowRoot.querySelector("#flightResultList").shadowRoot.querySelector("#listview").querySelectorAll(".group");return x['+stri+'].querySelector("flight-card").shadowRoot.querySelector(".time").children[0].children[0].innerText;')
            date1_arr.append(date1)
            duration = browser.execute_script('x=document.querySelector("#app").shadowRoot.querySelector("#flights-search").shadowRoot.querySelector("#flightResultList").shadowRoot.querySelector("#listview").querySelectorAll(".group");return x['+stri+'].querySelector("flight-card").shadowRoot.querySelector(".time").children[1].children[0].innerText;')
            duration_arr.append(duration)
            date2= browser.execute_script('x=document.querySelector("#app").shadowRoot.querySelector("#flights-search").shadowRoot.querySelector("#flightResultList").shadowRoot.querySelector("#listview").querySelectorAll(".group");return x['+stri+'].querySelector("flight-card").shadowRoot.querySelector(".time").children[2].children[0].innerText;')
            date2_arr.append(date2)
            cost= browser.execute_script('x=document.querySelector("#app").shadowRoot.querySelector("#flights-search").shadowRoot.querySelector("#flightResultList").shadowRoot.querySelector("#listview").querySelectorAll(".group");return x['+stri+'].querySelector("flight-card").shadowRoot.querySelector(".card-price").querySelector("wego-price").shadowRoot.querySelector(".price-text").children[3].innerText;')
            cost_1= cost.replace(",", "")
            cost_arr.append(cost_1)
            flight = browser.execute_script('x=document.querySelector("#app").shadowRoot.querySelector("#flights-search").shadowRoot.querySelector("#flightResultList").shadowRoot.querySelector("#listview").querySelectorAll(".group");return x['+stri+'].querySelector("flight-card").shadowRoot.querySelector(".airline").children[1].children[0].innerText;')
            flight_arr.append(flight)
            i=i+1
    except JavascriptException as exception:
        pass
    #Creating JSON data
    json_arr=[flight_arr,date1_arr,date2_arr,cost_arr]
    if len(json_arr)==0 :
      failure_arr.append(Dep_date)
    print(failure_arr)
    data= json.dumps(json_arr)
    payload = {'json_payload': data}
    print(payload)
    res = requests.post('https://elastic:med3THJy1h2GQZgcAFramGi4@7ec87bd5cc074b749e6cd57e5970e48b.us-east-1.aws.found.io:9243/my_index/my_doc ',json=payload)
    print (res.text)
    print(res.status_code)
    #print(json_arr)
    browser.quit()
    

def invoke() :
  loop=[3,7,9,21]
  k=0
  Origin='BAH'
  #Destination=['CAI','DXB','IST','BKK','AMM']
  Destination='DXB'
  failure_arr=[]
  for l in loop:
    #while(k<5):
        Str= date.today()+datetime.timedelta(days=l)
        Dep_date = str(Str)
        Dest= Destination
        url= 'https://www.wego.co.in/flights/searches/c'+Origin+'-c'+Destination+'-'+Dep_date+'/economy/1a:0c:0i?sort=price&order=asc'
        scraper(url,Dep_date,Dest)
        
  if (len(failure_arr)!=0):
      while(k<=len(failure_arr)-1):
        url= 'https://www.wego.co.in/flights/searches/c'+Origin+'-c'+Destination+'-'+failure_arr[k]+'/economy/1a:0c:0i?sort=price&order=asc'    
        Dep_date2= failure_arr[k]
        scraper(url,Dep_date2,Dest)
        k+=1

invoke()



