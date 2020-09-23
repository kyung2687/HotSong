import os
import time
import glob
import datetime
import subprocess

import pymongo
from pymongo import MongoClient
import pytube
import sys

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

##########
streamingcnt = 7
##########

program_start = time.time()
conn = MongoClient('127.0.0.1')

db = conn.admin
collect = db.songs
song_dir = "C:/Users/admin/Desktop/mp3tmp"

songs = collect.find({"streamingYN":False})
song_duration = 0 #int(song1["duration"]) + int(song2["duration"])
song = []

err_arr = []
for index in range(0, streamingcnt):
    song.append(songs[index])

download_start = time.time()
for i, s in enumerate(song):
    song_duration = song_duration + int(s["duration"]) 
download_duration = int(time.time() - download_start)

for s in err_arr :
    song.remove(s)
print("Download_duration : " + str(download_duration))
print("Song     duration : " + str(song_duration))


_files = sorted(glob.glob(song_dir+'/*.mp3'))

remove_files = glob.glob(song_dir+'/*')

def streaming() :
    for i, s in enumerate(_files) :
        streamdata = db.streamings.find({})[0]
        db.streamings.update_one(streamdata, { "$set": {"str":True, "song": song[i]}} )
        os.system('\"' + _files[i] + '\"')
        print(song[i]["title"])
        time.sleep(int(song[i]["duration"]))
        collect.update_one(song[i], { "$set": {"streamingYN":True, "up_date":datetime.datetime.now().strftime('%Y-%m-%d')}} )
    
    streamdata = db.streamings.find({})[0]
    db.streamings.update_one(streamdata, { "$set": {"str":False, "song": {}}})

streaming()

program_duration = int(time.time() - program_start)

print("Program Duration : " + str(program_duration))