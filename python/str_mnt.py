from selenium import webdriver
import time
import pymongo
from pymongo import MongoClient
import json
from bs4 import BeautifulSoup
import random
import datetime

today = datetime.datetime.today().strftime("%m%d")
holiday = tuple()
holiday = (
    '0101','0124','0127',
    '0415','0430','0505',
    '0930','1001','1002',
    '1009','1225'
    )

if today in holiday :
    print('today is holiday')
    sys.exit()
elif time.localtime().tm_wday==5 :
    print('today is holiday')
    sys.exit()
elif time.localtime().tm_wday==6 :
    print('today is holiday')
    sys.exit()

cnt=2

download_start = time.time()

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

driver.implicitly_wait(3)
driver.get('https://www.genie.co.kr/chart/top200')

#로그인 화면 이동
driver.find_element_by_xpath("//*[@id=\"gnb\"]/div/div/button").click()
driver.find_element_by_xpath("//*[@id=\"gnb\"]/div/div/div/ul/li[1]/a").click()

#로그인
driver.switch_to.window(driver.window_handles[1])
driver.find_element_by_xpath("//*[@id=\"id_email_2\"]").send_keys(kakao_id)
driver.find_element_by_xpath("//*[@id=\"id_password_3\"]").send_keys(kakao_pw)
driver.find_element_by_xpath("//*[@id=\"login-form\"]/fieldset/div[8]/button[1]").click()

time.sleep(5)

driver.switch_to.window(driver.window_handles[0])

#노래 담기
#모두 담기#driver.find_element_by_xpath("//*[@id=\"body-content\"]/div[6]/div/div[1]/input").click()
#if not a:
#  print("List is empty")
all_duration = 0
duration = []

for i in range(cnt) : 
    try : 
        driver.switch_to.window(driver.window_handles[0])
        song.append(songs[i])
        serch_content = songs[i]["title"] + " " + songs[i]["singer"]
        driver.find_element_by_xpath("//*[@id=\"sc-fd\"]").clear()
        driver.find_element_by_xpath("//*[@id=\"sc-fd\"]").send_keys(serch_content)
        driver.find_element_by_xpath("//*[@id=\"frmGNB\"]/fieldset/input[3]").click()
        driver.find_element_by_xpath("//*[@id=\"body-content\"]/div/div[2]/div/table/tbody/tr[1]/td[6]/a").click()
        random_str_yn = False
    except IndexError :
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
            "title" : title,
            "singer": singer,
            "image" : image,
            "task"  : task,
            "name"  : name
        }
        driver.find_element_by_xpath("//*[@id=\"body-content\"]/div[6]/div/table/tbody/tr["+ str(rdm) +"]/td[6]/a").click()
        song.append(song1)
    finally :
        driver.implicitly_wait(5)
        driver.switch_to.window(driver.window_handles[1])
        if umsoge : 
            driver.find_element_by_xpath("//*[@id=\"fp-audio\"]/div/div[1]/div[3]/div[2]/a").send_keys('\n') #음소거
            umsoge = False
        try :
            driver.find_element_by_xpath("//*[@id=\"login-another\"]/div[2]/a[1]").click()
            time.sleep(3)
        except :
            print()
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        dr = soup.select('#fp-audio > div > div.fp-ui > div.fp-controls > span.fp-duration')[0].text.strip().split(':')
        print(int(dr[0]) * 60 + int(dr[1]))
        duration.append(int(dr[0]) * 60 + int(dr[1]))
        all_duration = all_duration + int(dr[0]) * 60 + int(dr[1])

#노래 재생
driver.switch_to.window(driver.window_handles[1])
driver.implicitly_wait(3)
try :
    driver.find_element_by_xpath("//*[@id=\"login-another\"]/div[2]/a[1]").click()
except :
    print('next')
driver.find_element_by_xpath("//*[@id=\"fp-audio\"]/div/div[1]/div[3]/button[1]").click()
#if random_str_yn : 
#    driver.find_element_by_xpath("//*[@id=\"fp-audio\"]/div/div[1]/div[3]/button[2]").click()
driver.find_element_by_xpath("//*[@id=\"fp-audio\"]/div/div[1]/div[3]/button[4]").click()

driver.find_element_by_xpath("//*[@id=\"fp-audio\"]/div/div[1]/div[3]/a").click() #일시정지
time.sleep(1)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
text = soup.select('#fp-audio > div > div.fp-ui > div.fp-controls > a')[0].text.strip()

text = '일지정지'
while(text != '재생') :
    driver.find_element_by_xpath("//*[@id=\"fp-audio\"]/div/div[1]/div[3]/a").click() #일시정지
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.select('#fp-audio > div > div.fp-ui > div.fp-controls > a')[0].text.strip())
    text = soup.select('#fp-audio > div > div.fp-ui > div.fp-controls > a')[0].text.strip()

download_duration = int(time.time() - download_start)
#시간 정지
print('download_daration : ' + str(download_duration))
print('all_duration : ' + str(all_duration))

driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/div[2]/div/div[1]/div[3]/div[2]/div/em[6]").click() #음소거
driver.find_element_by_xpath("//*[@id=\"fp-audio\"]/div/div[1]/div[3]/a").click() #재생
for i in range(cnt) :
    streamdata = db.streamings.find({})[0]
    db.streamings.update_one(streamdata, { "$set": {"str":True, "song": song[i]}} )
    time.sleep(duration[i] + 1)
    try : collect.update_one(song[i], { "$set": {"streamingYN":True, "up_date":datetime.datetime.now().strftime('%Y-%m-%d')}} )
    except Exception as ex :
        print('에러가 발생 했습니다', ex)

streamdata = db.streamings.find({})[0]
db.streamings.update_one(streamdata, { "$set": {"str":False, "song": {}}})


#while(1) :
    #streamdata = db.streamings.find({})[0]
    #streamdata = db.streamings.find({})[0]
    #db.streamings.update_one(streamdata, { "$set": {"str":True, "song": song[i]}} )
#    time.sleep(4)
#driver.find_element_by_xpath("//*[@id=\"fp-audio\"]/div/div[1]/div[3]/a").click()

#for i in range(6, 0, -1) : 
#    driver.find_element_by_xpath("//*[@id=\"fp-audio\"]/div/div[1]/div[3]/div[2]/div/em[" + str(i) +"]").click()
#    time.sleep(1)
#
driver.quit()