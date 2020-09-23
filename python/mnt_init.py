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
db.streamings.update_one(streamdata, { "$set": {"str":False, "song": {}}})