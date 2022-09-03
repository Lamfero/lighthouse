import re
from main.models import Users
import sqlite3 as sql
from geopy import *
import os
from pathlib import Path
from dateutil.relativedelta import * 
from datetime import date

con = sql.connect("./db.sqlite3", check_same_thread=False)
cur = con.cursor()

def check_exist_user(telegram_id, secret_key):
    
    if Users.objects.filter(telegram_id = telegram_id, secret_key = secret_key).exists():
        return True
    else:
        return False
