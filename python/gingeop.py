## 파일명 : gingeop.py
## 용도 : 운영시 에러나 특별 음악 스트리밍에 사용
## 실행 시간 : 필요시 사용

import time
import datetime
import pymongo
from pymongo import MongoClient

today = '0000'
birthday = {
    '0421' : '송호용 선임',
    '0422' : '송준수 수석',
    '0427' : '김택규 수석, 김경민 선임',
    '0429' : '이윤수 선임',
    '0503' : '박재희 차장',
    '0506' : '최선용 부장',
    '0512' : '배정연 대리',
    '0513' : '맹다슬 사원',
    '0515' : '박영준 부장',
    '0525' : '선정완 선임',
    '0601' : '이동엽 수석',
    '0602' : '김진 대리',
    '0613' : '조용상 차장',
    '0619' : '이동진 수석',
    '0620' : '최석규 수석',
    '0623' : '임정희 차장',
    '0707' : '정호중 수석',
    '0710' : '황정교 부장',
    '0715' : '박동희 대리',
    '0721' : '윤성 수석',
    '0804' : '오상록 부장',
    '0809' : '이정민 선임',
    '0813' : '정보경 차장',
    '0819' : '이영미 수석',
    '0826' : '조준희 사원',
    '0828' : '김화종 수석',
    '0831' : '김나현 대리',
    '0901' : '김훈균 수석',
    '0908' : '박현준 과장',
    '0915' : '전진미 대리',
    '0917' : '이주현 수석',
    '0927' : '홍상돈 수석',
    '1022' : '윤경민 선임',
    '1109' : '한승희 과장',
    '1115' : '박양식 부장',
    '1119' : '김형기 부장',
    '1123' : '이대헌 부장',
    '1227' : '최구훈 대리, 안대석 수석',
    '1228' : '김봉수 차장',
}

weddinganniversary = {
    '0512' : '김화종 수석',
    '0901' : '김동구 수석, 이동진 수석',
    '0903' : '이영미 수석',
    '1011' : '정호중 수석',
    '1017' : '안대석 수석',
    '1023' : '최석규 수석',
    '1024' : '설성윤 수석',
    '1105' : '이주현 수석',
    '1122' : '김훈균 수석',
    '1123' : '이병식 수석',
    '1126' : '안상경 부장',
    '1206' : '김동우 수석',
    '1214' : '이임호 수석',
}

notice = {}

conn = MongoClient('127.0.0.1')

db = conn.admin
collect = db.songs

content = ""


if today in birthday :
    content = content + birthday[today] + "의 생일입니다 !^"
    print(birthday[today] + "의 생일입니다 !")

if today in weddinganniversary :
    content = content + weddinganniversary[today] + "의 결혼기념일입니다 !^"
    print(weddinganniversary[today] + "의 결혼기념일입니다 !")

if content != "" :
    content = content + '모두 축하해주세요 !'
    print('모두 축하해주세요 !')

if content == "" :
    if today in notice :
        content = notice[today]
    else :
        content = "출입 시 반드시 손 소독제로 손을 깨끗이 합시다"
        print('출입 시 반드시 손 소독제로 손을 깨끗이 합시다')

streamdata = db.streamings.find({})[0]
db.streamings.update_one(streamdata, { "$set": {"content" : content}} )