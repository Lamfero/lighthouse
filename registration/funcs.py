import re
from main.models import Users
import sqlite3 as sql
from geopy import *
import os
from pathlib import Path
from dateutil.relativedelta import * 
from datetime import date
from . import towns_list
import json


con = sql.connect("./db.sqlite3", check_same_thread=False)
cur = con.cursor()

def check_exist_user(telegram_id, secret_key):
    
    if Users.objects.filter(telegram_id = telegram_id).exists():
        return True
    else:
        error =  add_user(telegram_id=telegram_id, secret_key=secret_key)
        return error


def add_user(telegram_id, secret_key):
    result = cur.execute("SELECT `secret_key` FROM `secret_keys` WHERE `id` = '{}' AND `secret_key` = '{}'".format(str(telegram_id), str(secret_key))).fetchmany(1)
    if len(result) == 1:
        user = Users(telegram_id=telegram_id, secret_key = result[0][0], select="registration")
        user.save()
        return False
    else:
        return None #Юзер отсутствует в бд ТГ БОТА или неверный secret_key в БД БОТА. Невозможно получить secret key


def check_secret_key(id, secret_key):
    result = cur.execute("SELECT * FROM `secret_keys` WHERE `id` = '{}' AND `secret_key` = '{}'".format(id, secret_key)).fetchmany(1)
    if len(result) == 1:
        return True
    else:
        return False


def check_valid_name_surname(name_surname):
    if len(str(name_surname)) <= 30:
        if len(re.split(' |-', name_surname)) <= 5 and len(re.split(' |-', name_surname)) >= 2:
            alphabet = ["а","б","в","г","д","е","ё","ж","з","и","й","к","л","м","н","о", "п","р","с","т","у","ф","х","ц","ч","ш","щ","ъ","ы","ь","э","ю","я","q","w","e","r","t","y","u","i","o","p","a","s","d","f","g","h","j","k","l","z","x","c","v","b","n","m", " "]
            for one_char in name_surname:
                if one_char == '-':
                    continue
                else:
                    if one_char.lower() in alphabet:
                        continue
                    else:
                        return False
            return True
        else:
            return False
    else:
        return False


def check_valid_date(_date):
    split_date = _date.rsplit('.')
    if split_date[0].isdigit() and split_date[1].isdigit() and split_date[2].isdigit():
        if len(split_date[0]) == 2:
            if int(split_date[0]) <= 31:
                if len(split_date[1]) == 2:
                    if int(split_date[1]) < 13:
                        if len(split_date[2]) == 4:
                            return True
    return False


def check_age_by_date(date_birth):
    split_date = date_birth.rsplit('.')
    if split_date[0].isdigit() and split_date[1].isdigit() and split_date[2].isdigit():
        if len(split_date[0]) == 2:
            if int(split_date[0]) < 32:
                if len(split_date[1]) == 2:
                    if int(split_date[1]) < 13:
                        if len(split_date[2]) == 4:
                            try:
                                today = date.today()
                                dob = date(int(split_date[2]), int(split_date[1]), int(split_date[0])) 
                                age = relativedelta(today, dob)
                                #relativedelta(years=+33, months=+11, days=+16)
                                if int(age.years) >= 16 and int(age.years) <= 90:
                                    return True
                            except:
                                return False
    return False


# def get_city_by_coords(lat, lon):
#     geolocator = Nominatim(user_agent="Yandex")
#     location = geolocator.reverse(str(f'{lat}, {lon}'), exactly_one=True)
#     if location != None:
#         address = location.raw['address']
#     else:
#         return ''
#     town = address.get('town', '')
#     if town == '':
#         town = address.get('city', '')
#     return town


def check_valid_city(city):
    if city in towns_list.towns:
        return True
    else:
        return False    


def check_valid_category(category):
    categories = ["Категория 1", "Категория 2"]
    if category in categories:
        return True
    else:
        return False


def check_valid_subcategories(user_subcategories):
    subcategories = ["Подкатегория 1", "Подкатегория 2", "Подкатегория 3", "Подкатегория 4", "Подкатегория 5", "Подкатегория 6", "Подкатегория 7", "Подкатегория 8", "Подкатегория 9", "Подкатегория 10", "Подкатегория 11", "Подкатегория 12"]
    for user_subcategory in user_subcategories:
        if user_subcategory in subcategories:
            pass
        else:
            return False
    return True


def check_valid_interests(user_interests):
    interests = ["Интерес 1", "Интерес 2", "Интерес 3", "Интерес 4", "Интерес 5", "Интерес 6", "Интерес 7", "Интерес 8", "Интерес 9", "Интерес 10", "Интерес 11", "Интерес 12"]
    for user_interes in user_interests:
        if user_interes in interests:
            pass
        else:
            return False
    return True


def get_userinfo_for_fields(db):
    class userinfo():
        if db.name_surname != None:
            name_surname = db.name_surname
        
        if db.description != None:
            description = db.description

        img = db.img
        
        if db.portfolio != None:
            portfolio = eval(db.portfolio)
            if 'instagram' in portfolio:
                instagram = portfolio["instagram"]
            else:
                instagram = ''
            if 'behance' in portfolio:
                behance = portfolio["behance"]
            else:
                behance = ''
            if 'dribbble' in portfolio:
                dribbble = portfolio["dribbble"]
            else:
                dribbble = ''
            if 'vk' in portfolio:
                vk = portfolio["vk"]
            else:
                vk = ''
        else:
            instagram = ''
            behance = ''
            dribbble = ''
            vk = ''
        
        
    return userinfo


def get_userinfo_for_registration(db):
    class userinfo():
        if db.name_surname != None:
            if len(db.name_surname) > 10:
                name_surname = f'{db.name_surname[:10]}...'
            else:
                name_surname = db.name_surname
        
        if db.city != None:
            if len(db.city) > 10:
                city = f'{db.city[:10]}...'
            else:
                city = db.city
        
        if db.subcategories != None:
            if len(db.subcategories) > 10:
                subcategories = f'{db.subcategories[:10]}...'
            else:
                subcategories = db.subcategories
        
        if db.interests != None:
            if len(db.interests) > 10:
                interests = f'{db.interests[:10]}...'
            else:
                interests = db.interests
        
        if db.description != None:
            if len(db.description) > 10:
                description = f'{str(db.description)[:10]}...'
            else:
                description = db.description
        
        if db.date_birth != None:
            date_birth = db.date_birth
        
        category = db.category
        img = db.img
        
        
    return userinfo


def delete_last_userphoto_from_disk(db):
    if db.img != '':
        path = f"{Path(__name__).resolve().parent}{db.img.url}".replace("\\", "/")
        os.remove(path)


def get_links_error(form):
    if form.data.get("instagram") != '':
        if 'instagram.com/' in form.data.get("instagram"):
            pass
        else:
            return 'Введите верную ссылку на Instagram'
    if form.data.get("behance") != '':
        if 'behance.net/' in form.data.get("behance"):
            pass
        else:
            return 'Введите верную ссылку на Behance'
    if form.data.get("dribbble") != '':
        if 'dribbble.com/' in form.data.get("dribbble"):
            pass
        else:
            return 'Введите верную ссылку на Dribbble'
    if form.data.get("vk") != '':
        if 'vk.com/' in form.data.get("vk"):
            pass
        else:
            return 'Введите верную ссылку на Vk'
    return None


def get_dict_portfolio(form):
    result = '{'
    if form.data.get("instagram") != '':
        result += f'"instagram": "{form.data.get("instagram")}",'
    if form.data.get("behance") != '':
        result += f'"behance": "{form.data.get("behance")}",'
    if form.data.get("dribbble") != '':
        result += f'"dribbble": "{form.data.get("dribbble")}",'
    if form.data.get("vk") != '':
        result += f'"vk": "{form.data.get("vk")}",'
    return str(result) + '}'


def check_full_registration_form(db):
    if db.name_surname == None:
        return "Заполните поле Имя Фамилия"
    if db.date_birth == None:
        return "Заполните поле Дата рождения"
    if db.city == None:
        return "Заполните поле Город"
    if db.category == None:
        return "Заполните поле Категория деятельности"
    if db.subcategories == None:
        return "Заполните поле Подкатегории"
    if db.interests == None:
        return "Заполните поле Интересы"
    if db.description == None:
        return "Заполните поле О себе"
    if db.img == '':
        return "Заполните поле Фото"
    return None