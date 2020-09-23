##http://ncov.mohw.go.kr/

import requests
from bs4 import BeautifulSoup
import os
import time
import glob
import datetime
import subprocess
import pymongo
from pymongo import MongoClient
import pytube
import sys

program_start = time.time()
conn = MongoClient('127.0.0.1')

db = conn.admin
   
streamdata = db.streamings.find({})[0]

req = requests.get('http://ncov.mohw.go.kr/')
html = req.text
soup = BeautifulSoup(html, 'html.parser')

date = soup.select('body > div > div.mainlive_container > div.container > div > div.liveboard_layout > div.liveNumOuter > h2 > a > span.livedate')[0].text
domestic = soup.select('body > div > div.mainlive_container > div.container > div > div.liveboard_layout > div.liveNumOuter > div.liveNum_today_new > div > ul > li:nth-child(1) > span.data')[0].text
overseas = soup.select('body > div > div.mainlive_container > div.container > div > div.liveboard_layout > div.liveNumOuter > div.liveNum_today_new > div > ul > li:nth-child(2) > span.data')[0].text
status = req.status_code
is_ok = req.ok

print("날짜기준 : " + date)
print("국내유입 : " + domestic)
print("해외유입 : " + overseas)
print(date + " " + "국내발생:"+domestic + " 해외유입:"+overseas)

ment=date + " " + "국내발생:"+domestic + " 해외유입:"+overseas
db.streamings.update_one(streamdata, { "$set": {"corona": ment}})