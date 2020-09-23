## 파일명 : musicplusyyyy.py
## 용도 : 음악 채우기용 배치파일 (실시간 TOP200)
## 실행 시간 : 현재 사용 안함

from selenium import webdriver
import time
import pymongo
from pymongo import MongoClient
import json
from bs4 import BeautifulSoup
import random
import datetime

kakao_id = "rudals2392@gmail.com"
kakao_pw = "dbwls2705"
driver = webdriver.Chrome('C:/Users/admin/Desktop/HotSong/chromedriver')
conn = MongoClient('127.0.0.1')
db = conn.admin
collect = db.songs
songs = collect.find({"streamingYN":False})
song = []
random_str_yn = True
umsoge = True
year = random.randint(2000, 2020)
print('random year is ' + str(year))

driver.implicitly_wait(3)
driver.get('https://www.genie.co.kr/chart/top200')
driver.switch_to.window(driver.window_handles[0])

if(year == 2020) :
    for i in range(14 - songs.count()) : 
        rdm = random.randint(1, 49)
        driver.get('https://www.genie.co.kr/chart/top200?ditc=D&ymd=20200706&hh=15&rtm=Y&pg=' + str(random.randint(1,4)))
        driver.implicitly_wait(3)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.select('#body-content > div.newest-list > div > table > tbody > tr:nth-child('+ str(rdm) +') > td.info > a.title.ellipsis')[0].text.strip()
        singer = soup.select('#body-content > div.newest-list > div > table > tbody > tr:nth-child('+ str(rdm) +') > td.info > a.artist.ellipsis')[0].text.strip()
        image = soup.select('#body-content > div.newest-list > div > table > tbody > tr:nth-child('+ str(rdm) +') > td:nth-child(3) > a > img')[0].get('src').strip()
        task = "지니뮤직 TOP200"
        name = ""
        song1 = { 
            "streamingYN":False, 
            "up_date":datetime.datetime.now().strftime('%Y-%m-%d'),
            "title" : title,
            "singer": singer,
            "image" : image,
            "task"  : task,
            "name"  : name,
            "url"   : "",
            "duration" : "0"
        }
        db.songs.insert_one(song1)
else :
    for i in range(14 - songs.count()) : 
        rdm = random.randint(1, 49)
        driver.get('https://www.genie.co.kr/chart/musicHistory?year='+ str(year) +'&category=0&pg=' + str(random.randint(1,2)))
        driver.implicitly_wait(3)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        target = soup.select('#body-content > div.songlist-box > div.music-list-wrap > table > tbody > tr:nth-child('+ str(rdm) +') > td.info > a.title.ellipsis')[0].text.split("TITLE")
        title = target[len(target) - 1].strip()
        singer = soup.select('#body-content > div.songlist-box > div.music-list-wrap > table > tbody > tr:nth-child('+ str(rdm) +') > td.info > a.artist.ellipsis')[0].text.strip()
        image = soup.select('#body-content > div.songlist-box > div.music-list-wrap > table > tbody > tr:nth-child('+ str(rdm) +') > td:nth-child(3) > a > img')[0].get('src').strip()
        task = "지니뮤직 " + str(year) + " TOP100"
        name = ""
        song1 = { 
            "streamingYN":False, 
            "up_date":datetime.datetime.now().strftime('%Y-%m-%d'),
            "title" : title,
            "singer": singer,
            "image" : image,
            "task"  : task,
            "name"  : name,
            "url"   : "",
            "duration" : "0"
        }
        db.songs.insert_one(song1)


driver.quit()