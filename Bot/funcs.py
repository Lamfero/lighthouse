from datetime import date
from random import randint
import sqlite3 as sql
import qrcode
import json
from PIL import Image, ImageGrab, ImageFont, ImageDraw
import datetime
import datetime as d
from dateutil.relativedelta import * 
import os
import re
from geopy import *
from aiogram.types.web_app_info import WebAppInfo
import requests
import math
from reply_markup import *

con = sql.connect('project.db', timeout=10)
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS `secret_keys` (`id` INTEGER, `secret_key` STRING)")
cur.execute("CREATE TABLE IF NOT EXISTS `profile` (`id` INTEGER, `name_surname` STRING)")
cur.execute("CREATE TABLE IF NOT EXISTS `events` (`eid` INTEGER, `id` INTEGER)")
cur.execute("CREATE TABLE IF NOT EXISTS `user_events` (`eid` INTEGER, `id` INTEGER, `title` STRING, `category` STRING)")
cur.execute("CREATE TABLE IF NOT EXISTS `payments_log` (`id` INTEGER, `sum` INTEGER, `action` STRING, `action_name` STRING)")
cur.execute("CREATE TABLE IF NOT EXISTS `tariff_booking`(`id` INTEGER, `name` STRING, `date` STRING)")
cur.execute("CREATE TABLE IF NOT EXISTS `tariff`(`name` STRING, `count` INTEGER, `description` STRING, `gives` STRING)")
result = cur.execute("SELECT * FROM `tariff`").fetchmany(3)
if len(result) == 0:
    cur.execute("INSERT INTO `tariff` VALUES('Стандарт', '100', 'Пусто', '')")
    cur.execute("INSERT INTO `tariff` VALUES('Расширенный', '100', 'Пусто', '')")
    cur.execute("INSERT INTO `tariff` VALUES('PRO', '100', 'Пусто', '')")
cur.execute("CREATE TABLE IF NOT EXISTS `first_touch`(`id` INTEGER, `create` STRING, `find` STRING, `my_work` STRING)")
cur.execute("CREATE TABLE IF NOT EXISTS `profile_moderation`(`id` INTEGER, `field` STRING, `data` STRING)")
cur.execute("CREATE TABLE IF NOT EXISTS `projects`(`project_id` INTEGER, `id` INTEGER, `need_categories` STRING, `city` STRING, `status` STRING)")
cur.execute("CREATE TABLE IF NOT EXISTS `find_projects`(`id` INTEGER, `project_type` STRING, `categories` STRING)")
cur.execute("CREATE TABLE IF NOT EXISTS `warns_project`(`id` INTEGER, `project_id`, `reason` STRING)")
con.commit()


def generate_secret_key(id):
    allowable_sumbles = ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "a", "s", "d", "f", "g", "h", "j", "k", "l", "z", "x", "c", "v", "b", "n", "m", ]
    len_key = 50
    result = ''
    i = 0
    while i <= len_key:
        i += 1
        result += str(allowable_sumbles[randint(0, len(allowable_sumbles))-1])
    cur.execute("UPDATE `secret_keys` SET `` = '{}' WHERE `id` = '{}'".format(result, id))
    con.commit()
    return result


def check_exist_user(id):
    return True
    

def add_user(id, username):
    allowable_sumbles = ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "a", "s", "d", "f", "g", "h", "j", "k", "l", "z", "x", "c", "v", "b", "n", "m", ]
    len_key = 50
    result = ''
    i = 0
    while i <= len_key:
        i += 1
        secret_key += str(allowable_sumbles[randint(0, len(allowable_sumbles))-1])
    date_ = f'{datetime.datetime.now().day}.{datetime.datetime.now().month}.{datetime.datetime.now().year}'
    cur.execute("INSERT INTO `tariff_booking` VALUES ('{}', 'Отсутствует', '')".format(id))
    cur.execute("INSERT INTO `first_touch` VALUES('{}', '-', '-', '-')".format(id))
    cur.execute("INSERT INTO `secret_keys` VALUES ('{}', '{}')".format(id, secret_key))
    generate_secret_key(id)
    con.commit()


def add_referal(id, ref_id):
    if os.path.exists(f"json/profile/{ref_id}.json"):
        with open(f"json/profile/{ref_id}.json", "r") as file:
            content = json.load(file)
            file.close()
        referals = content["referals"]
        referal = {
            "id": f"{id}",
            "verification": "none"
        }
        referals.append(referal)
        content["referals"] = referals
        with open(f"json/profile/{ref_id}.json", "w") as file:
            file.write(json.dumps(content))
            file.close()


def add_json_user(id, name_surname):
    structure ={
        "name_surname": f"{name_surname}",
        "date": f"{datetime.datetime.now()}",
        "date_birth": "",
        "city": "",
        "main_category_1": "",
        "main_category_2": "",
        "main_category_3": "",
        "description": "",
        "interests": "",
        "verification": "-",
        "stat": {
            "projects": {
                "rating": "0",
                "finished": "0",
                "waiting": "0",
            },
            "tasks": {
                "rating": "0",
                "finished": "0",
                "waiting": "0",
            },
            "questions": {
                "rating": "0",
                "finished": "0",
                "waiting": "0",
            },
            "rating": "0",
            "last_in_work": "Никогда",
        },
        
        "referals":[
        ]
    }
    
    with open(f"json/profile/{id}.json", "w") as file:
        file.write(json.dumps(structure))
        file.close()
    structure = {
        "notifications": [

        ]
    }
    with open(f"json/notification/{id}.json", "w") as file:
        file.write(json.dumps(structure))
        file.close()


def check_user_interests(id):
    with open(f"json/profile/{id}.json", "r") as file:
        content = json.load(file)
        file.close()
    return content["interests"]


def add_json_user_info(id, field, data):
    with open(f"json/profile/{id}.json", "r") as file:
        content = json.load(file)
        file.close()
    content[f"{field}"] = data
    with open(f"json/profile/{id}.json", "w") as file:
        file.write(json.dumps(content))
        file.close()


def add_json_user_stat_info(id, type_field, field, data):
    with open(f"json/profile/{id}.json", "r") as file:
        content = json.load(file)
        file.close()
    if type_field == 'projects':
        content["stat"]["projects"][f"{field}"] = data
    elif type_field == 'tasks':
        content["stat"]["tasks"][f"{field}"] = data
    elif type_field == 'questions':
        content["stat"]["questions"][f"{field}"] = data
    elif type_field == '':
        content["stat"][f"{field}"] = data
    
    with open(f"json/profile/{id}.json", "w") as file:
        file.write(json.dumps(content))
        file.close()


def get_json_user_field(id, field):
    with open(f"json/profile/{id}.json", "r") as file:
        content = json.load(file)
        file.close()
    return content[f"{field}"]


def check_interests_original(array, interest):
    for row in array:
        if row == interest:
            return False
    return True


def check_valid_date(date):
    split_date = date.rsplit('.')
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


def get_age_by_date(date_birth):
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
                                return age.years
                            except:
                                return 'Отсутствует'


def get_city_by_coods(coord):
    geolocator = Nominatim(user_agent="Yandex")
    location = geolocator.reverse(coord, exactly_one=True)
    address = location.raw['address']
    town = address.get('town', '')
    if town == '':
        town = address.get('city', '')
    return town


def get_registration_name_image(name):
    if len(re.split(' |-', name)) >= 2:
        if len(re.split(' |-', name)) >= 3:
            if len(re.split(' |-', name)) >= 4:
                if len(re.split(' |-', name)) >= 5:
                    splited_name = re.split(' |-', name)
                    name = f'{splited_name[0]} {splited_name[1]}\n{splited_name[2]} {splited_name[3]}\n{splited_name[4]}'
                else:
                    splited_name = re.split(' |-', name)
                    name = f'{splited_name[0]} {splited_name[1]}\n{splited_name[2]} {splited_name[3]}'
            else:
                splited_name = re.split(' |-', name)
                name = f'{splited_name[0]} {splited_name[1]}\n{splited_name[2]}'
    image = Image.open('images/registration/приятно_познакомиться.png')
    font_city = ImageFont.truetype("fonts/Inter-Medium.otf", 60)
    draw = ImageDraw.Draw(image)
    W, H = (image.size[0],image.size[1])
    w, h = draw.textsize(name,font=font_city) 
    draw.text(xy=((W-w)/2,250), text=name, align="center", font=font_city, fill=('#FFFFFF')) 
    path = f'photos/nontime/{randint(1111111111, 9999999999)}.png'
    image.save(path, 'PNG')
    return path


def get_registration_location_image(city):
    image = Image.open('images/registration/your_location.png')
    font_city = ImageFont.truetype("fonts/Inter-Medium.otf", 60)
    draw = ImageDraw.Draw(image)
    W, H = (image.size[0],image.size[1])
    w, h = draw.textsize(city,font=font_city)
    draw.text(xy=((W-w)/2,250), text=city, align="center", font=font_city, fill=('#FFFFFF')) 
    path = f'photos/nontime/{randint(1111111111, 9999999999)}.png'
    image.save(path, 'PNG')
    return path


def get_registration_main_catigories_image(id):
    category_1 = get_json_user_field(id, 'main_category_1')
    category_2 = get_json_user_field(id, 'main_category_2')
    category_3 = get_json_user_field(id, 'main_category_3')
    categories = f'{category_1}\n{category_2}\n{category_3}'
    image = Image.open('images/registration/your_categories.png')
    font_city = ImageFont.truetype("fonts/Inter-Medium.otf", 60)
    draw = ImageDraw.Draw(image)
    W, H = (image.size[0],image.size[1])
    w, h = draw.textsize(categories,font=font_city)
    draw.text(xy=((W-w)/2,170), text=categories, align="center", font=font_city, fill=('#FFFFFF')) 
    path = f'photos/nontime/{randint(1111111111, 9999999999)}.png'
    image.save(path, 'PNG')
    return path


def get_registration_main_catigories_final_image(id):
    category_1 = get_json_user_field(id, 'main_category_1')
    category_2 = get_json_user_field(id, 'main_category_2')
    category_3 = get_json_user_field(id, 'main_category_3')
    if category_3 == '':
        if category_2 == '':
            categories = f'{category_1}'
        else:
            f'{category_1},\n{category_2}'
    else:
        if category_2 == '':
            categories = f'{category_1},\n{category_3}'
        else:
            f'{category_1},\n{category_2},\n{category_3}'
    categories = f'{category_1}\n{category_2}\n{category_3}'
    image = Image.open('images/registration/your_categories_final.png')
    font_city = ImageFont.truetype("fonts/Inter-Medium.otf", 60)
    draw = ImageDraw.Draw(image)
    W, H = (image.size[0],image.size[1])
    w, h = draw.textsize(categories,font=font_city)
    draw.text(xy=((W-w)/2,200), text=categories, align="center", font=font_city, fill=('#FFFFFF')) 
    path = f'photos/nontime/{randint(1111111111, 9999999999)}.png'
    image.save(path, 'PNG')
    return path


def get_registration_interests_image(id):
    interests = get_json_user_field(id, 'interests')
    splited_interests = interests.rsplit("  ")
    if len(splited_interests) > 0:
        if len(splited_interests) > 1:
            if len(splited_interests) > 2:
                if len(splited_interests) > 3:
                    if len(splited_interests) > 4:
                        if len(splited_interests) > 5:
                            if len(splited_interests) > 6:
                                result = f'{splited_interests[0]}, {splited_interests[1]},\n{splited_interests[2]}, {splited_interests[3]},\n{splited_interests[4]}, {splited_interests[5]},\n{splited_interests[6]}'
                            else:
                                result = f'{splited_interests[0]}, {splited_interests[1]},\n{splited_interests[2]}, {splited_interests[3]},\n{splited_interests[4]}, {splited_interests[5]}'
                        else:
                            result = f'{splited_interests[0]}, {splited_interests[1]},\n{splited_interests[2]}, {splited_interests[3]},\n{splited_interests[4]}'
                    else:
                        result = f'{splited_interests[0]}, {splited_interests[1]},\n{splited_interests[2]}, {splited_interests[3]}'
                else:
                    result = f'{splited_interests[0]}, {splited_interests[1]},\n{splited_interests[2]}'
            else:
                result = f'{splited_interests[0]}, {splited_interests[1]}'
        else:
            result = f'{splited_interests[0]}'
    else:
        result = 'ERROR'
    categories = result
    image = Image.open('images/registration/your_interests.png')
    font_city = ImageFont.truetype("fonts/Inter-Medium.otf", 60)
    draw = ImageDraw.Draw(image)
    W, H = (image.size[0],image.size[1])
    w, h = draw.textsize(categories,font=font_city)
    draw.text(xy=((W-w)/2,170), text=categories, align="center", font=font_city, fill=('#FFFFFF')) 
    path = f'photos/nontime/{randint(1111111111, 9999999999)}.png'
    image.save(path, 'PNG')
    return path


def get_registration_interests_final_image(id):
    interests = get_json_user_field(id, 'interests')
    splited_interests = interests.rsplit("  ")
    if len(splited_interests) > 0:
        if len(splited_interests) > 1:
            if len(splited_interests) > 2:
                if len(splited_interests) > 3:
                    if len(splited_interests) > 4:
                        if len(splited_interests) > 5:
                            if len(splited_interests) > 6:
                                result = f'{splited_interests[0]}, {splited_interests[1]},\n{splited_interests[2]}, {splited_interests[3]},\n{splited_interests[4]}, {splited_interests[5]},\n{splited_interests[6]}'
                            else:
                                result = f'{splited_interests[0]}, {splited_interests[1]},\n{splited_interests[2]}, {splited_interests[3]},\n{splited_interests[4]}, {splited_interests[5]}'
                        else:
                            result = f'{splited_interests[0]}, {splited_interests[1]},\n{splited_interests[2]}, {splited_interests[3]},\n{splited_interests[4]}'
                    else:
                        result = f'{splited_interests[0]}, {splited_interests[1]},\n{splited_interests[2]}, {splited_interests[3]}'
                else:
                    result = f'{splited_interests[0]}, {splited_interests[1]},\n{splited_interests[2]}'
            else:
                result = f'{splited_interests[0]}, {splited_interests[1]}'
        else:
            result = f'{splited_interests[0]}'
    else:
        result = 'ERROR'
    categories = result
    image = Image.open('images/registration/your_interests_final.png')
    font_city = ImageFont.truetype("fonts/Inter-Medium.otf", 60)
    draw = ImageDraw.Draw(image)
    W, H = (image.size[0],image.size[1])
    w, h = draw.textsize(categories,font=font_city)
    draw.text(xy=((W-w)/2,170), text=categories, align="center", font=font_city, fill=('#FFFFFF')) 
    path = f'photos/nontime/{randint(1111111111, 9999999999)}.png'
    image.save(path, 'PNG')
    return path


def get_registration_avatar_image(id):
    img = Image.open(f'images/registration/user_photo.png', "r")

    def prepare_mask(size, antialias = 2):
        mask = Image.new('L', (size[0] * antialias, size[1] * antialias), color=0)
        ImageDraw.Draw(mask).ellipse((0, 0) + mask.size, fill=255)
        return mask.resize(size, Image.Resampling.LANCZOS)

    def crop(image, s):
        w, h = image.size
        k = w / s[0] - h / s[1]
        if k > 0: image = image.crop(((w - h) / 2, 0, (w + h) / 2, h))
        elif k < 0: image = image.crop((0, (h - w) / 2, w, (h + w) / 2))
        return image.resize(s, Image.Resampling.LANCZOS)

    size = (300, 300)
    image = Image.open(f'photos/profile/{id}.png', "r")
    image = crop(image, size)
    image.putalpha(prepare_mask(size, 4))
    user_photo = image
    img.paste(user_photo, (350, 170), mask=user_photo) 
    path = f'photos/nontime/{randint(1111111111, 9999999999)}.png'
    img.save(path, 'PNG')
    return path


def end_registration(id):
    with open(f"json/profile/{id}.json", "r") as file:
        content = json.load(file)
    name = content["name_surname"]
    cur.execute("UPDATE `users` SET `name` = '{}' WHERE `id` = '{}'".format(name, id))
    con.commit()


def check_accept_user(id):
    with open(f"json/profile/{id}.json", "r") as file:
        content = json.load(file)
    if content["verification"] == '-':
        return False
    elif content["verification"] == '+':
        return True


def get_all_users(select = 'menu'):
    result = cur.execute("SELECT * FROM `users`").fetchall()
    if len(result) > 0:
        if select == 'menu':
            users_menu = InlineKeyboardMarkup(row_width=1)
            for user in result:
                id = user[0]
                username = user[1]
                if str(username) == 'None':
                    username = 'Отсутствует'
                user_button = InlineKeyboardButton(text="@"+username, callback_data=f"see_user_info_{id}")
                users_menu.add(user_button)
            return users_menu
        elif select == 'text':
            i = 0
            for user in result:
                i += 1
            text = f'Пользователи:\nВсего пользователей:{i}'
            return text


def get_all_admins(select = 'menu'):
    result = cur.execute("SELECT * FROM `users`").fetchall()
    if len(result) > 0:
        if select == 'menu':
            users_menu = InlineKeyboardMarkup(row_width=1)
            for user in result:
                if int(user[6]) > 0:
                    id = user[0]
                    username = user[1]
                    if str(username) == 'None':
                        username = 'Отсутствует'
                    user_button = InlineKeyboardButton(text="@"+username, callback_data=f"see_user_info_{id}")
                    users_menu.add(user_button)
            return users_menu
        elif select == 'text':
            i = 0
            for user in result:
                if int(user[6]) > 0:
                    i += 1
            text = f'Администраторы:\nВсего администраторов:{i}'
            return text


def beautifull_date(date_):
    splited_date = date_.rsplit(".")
    if len(splited_date[0]) == 1:
        day = f"0{splited_date[0]}"
    else:
        day = f"{splited_date[0]}"
    if len(splited_date[1]) == 1:
        month = f"0{splited_date[1]}"
    else:
        month = f"{splited_date[1]}"
    return f"{day}.{month}.{splited_date[2]}"


def see_user_info_id(id):
    result = cur.execute("SELECT * FROM `users` WHERE `id` = '{}'".format(id)).fetchall()
    if len(result) > 0:
        result = result[0]
        id = result[0]
        username = result[1]
        balance = result[3]
        admin_level = result[5]
        level = result[5]
        result = cur.execute("SELECT * FROM `tariff_booking` WHERE `id` = '{}'".format(id)).fetchall()[0]
        tariff = result[1]
        date = result[2]
        with open(f'json/profile/{id}.json', 'r') as file:
            content = json.load(file)
            file.close()
        full_name = content["name_surname"]
        main_category_1 = content["main_category_1"]
        main_category_2 = content["main_category_2"]
        main_category_3 = content["main_category_3"]
        interests = content["interests"]
        description = content["description"]
        verification = content["verification"]
        if verification == "+":
            full_name = '✔️' + full_name
        if tariff == 'standart':
            tariff_name = 'Стандарт'
        elif tariff == 'extended':
            tariff_name = 'Расширенный'
        elif tariff == 'pro':
            tariff_name = 'PRO'
        else:
            tariff_name = 'Отсутствует'
        if tariff_name == 'Отсутствует':
            if level > 0:
                text = f"{full_name}\nКатегории профиля: {main_category_1} {main_category_2} {main_category_3}\nКатегории интересов: {interests}\nОписание: {description}\nВерификация: {verification}\nБаланс: {balance}₽\nТариф: {tariff_name} до {date}\nАдминистратор {level} уровня"
            else:
                text = f"{full_name}\nКатегории профиля: {main_category_1} {main_category_2} {main_category_3}\nКатегории интересов: {interests}\nОписание: {description}\nВерификация: {verification}\nБаланс: {balance}₽\nТариф: {tariff_name}"
        else:
            if level > 0:
                text = f"{full_name}\nКатегории профиля: {main_category_1} {main_category_2} {main_category_3}\nКатегории интересов: {interests}\nОписание: {description}\nВерификация: {verification}\nБаланс: {balance}₽\nТариф: {tariff_name} до {date}\nАдминистратор {level} уровня"
            else:
                text = f"{full_name}\nКатегории профиля: {main_category_1} {main_category_2} {main_category_3}\nКатегории интересов: {interests}\nОписание: {description}\nВерификация: {verification}\nБаланс: {balance}₽\nТариф: {tariff_name} до {date}"
        return text
    else:
        return '&&&^^^$$$'


def get_user_city(id):
    with open(f"json/profile/{id}.json", "r") as file:
        content = json.load(file)
        file.close()
    return content["city"]


def get_visa(id, username):
    with open(f"json/profile/{id}.json", 'r') as file:
        content = json.load(file)
    full_name = content["name_surname"]
    category_1 = content["main_category_1"]
    category_2 = content["main_category_2"]
    category_3 = content["main_category_3"]
    if len(category_2) == 0:
        if len(category_3) == 0:
            category = category_1.lower()
        else:
            category = category_1.lower()  + ', ' + category_2.lower()
    else:
        category = category_1.lower() + ', ' + category_2.lower() + ', ' + category_3.lower()
    username = '@' + str(username)
    if str(username) == '@None':
        username = ' '
    link = f'https://t.me/Koworking_lamfero_bot?start={id}'
    if check_type_visa(id) == 'partner':
        qr = qrcode.QRCode(border=0)
        qr.add_data(link)
        img_qr = qr.make_image(fill_color =(255,255,255), back_color= (32,31,36)).resize((800, 800))
        image = Image.open('images/VISA_PARTNER.png')
        font_fullname = ImageFont.truetype("fonts/Inter-Bold.otf", 150)
        font_username = ImageFont.truetype("fonts/Inter-Bold.otf", 100)
        font_category = ImageFont.truetype("fonts/Inter-Medium.otf", 85)
        draw = ImageDraw.Draw(image)
        draw.text((142,900), str(full_name), font=font_fullname, fill=('#FFFFFF'))#Имя Фамилия
        draw.text((142,1280), str(username), font=font_username, fill=('#ff9900'))#Юзернейм
        draw.text((142,1090), str(category), font=font_category, fill=('#FFFFFF'))#Категория
        image.paste(img_qr, (1300, 2950))
        #image.show()
        image.save(f'visa_partner/{id}.png', 'PNG')
    elif check_type_visa(id) == 'participant':
        qr = qrcode.QRCode(border=0)
        qr.add_data(link)
        img_qr = qr.make_image(fill_color =(255,255,255), back_color= (32,31,36)).resize((800, 800))
        image = Image.open('images/VISA.png')
        font_fullname = ImageFont.truetype("fonts/Inter-Bold.otf", 150)
        font_username = ImageFont.truetype("fonts/Inter-Bold.otf", 100)
        font_category = ImageFont.truetype("fonts/Inter-Medium.otf", 85)
        draw = ImageDraw.Draw(image)
        draw.text((142,900), str(full_name), font=font_fullname, fill=('#FFFFFF'))#Имя Фамилия
        draw.text((142,1280), str(username), font=font_username, fill=('#85b422'))#Юзернейм
        draw.text((142,1090), str(category), font=font_category, fill=('#FFFFFF'))#Категория
        image.paste(img_qr, (1300, 2950))
        #image.show()
        image.save(f'visa_participant/{id}.png', 'PNG')
    elif check_type_visa(id) == 'group':
        qr = qrcode.QRCode(border=0)
        qr.add_data(link)
        img_qr = qr.make_image(fill_color =(255,255,255), back_color= (32,31,36)).resize((800, 800))
        image = Image.open('images/VISA_GROUP.png')
        font_fullname = ImageFont.truetype("fonts/Inter-Bold.otf", 150)
        font_username = ImageFont.truetype("fonts/Inter-Bold.otf", 100)
        font_category = ImageFont.truetype("fonts/Inter-Medium.otf", 85)
        draw = ImageDraw.Draw(image)
        draw.text((142,900), str(full_name), font=font_fullname, fill=('#FFFFFF'))#Имя Фамилия
        draw.text((142,1280), str(username), font=font_username, fill=('#7ca1ff'))#Юзернейм
        draw.text((142,1090), str(category), font=font_category, fill=('#FFFFFF'))#Категория
        image.paste(img_qr, (1300, 2950))
        #image.show()
        image.save(f'visa_group/{id}.png', 'PNG')


def check_type_visa(id):
    result = cur.execute("SELECT `type` FROM `visa` WHERE `id` = '{}'".format(id)).fetchmany(1)
    if len(result) > 0:
        result = result[0]
        type_visa = result[0]
        return type_visa
    else:
        return 'not exist'


def get_user_select(id):
    result = cur.execute("SELECT `select` FROM `users` WHERE `id` = '{}'".format(id)).fetchmany(1)
    return result[0][0]


def delete_select(id):
    cur.execute("UPDATE `users` SET `select` = '' WHERE `id` = '{}'".format(id))
    con.commit()


def change_select(id, select='none'):
    cur.execute("UPDATE `users` SET `select` = '{}' WHERE `id` = '{}'".format(select, id))
    con.commit()


def change_choice_data(id, data='none'):
    cur.execute("UPDATE `users` SET `choice_data` = '{}' WHERE `id` = '{}'".format(data, id))
    con.commit()

def get_choice_data(id):
    result = cur.execute("SELECT `choice_data` FROM `users` WHERE `id` = '{}'".format(id)).fetchmany(1)
    return result[0][0]


def check_admin_level(id, level = 'none'):
    result = cur.execute("SELECT `admin` FROM `users` WHERE `id` = '{}'".format(id)).fetchmany(1)[0]
    if level == 'none':
        if len(result) == 0:
            return 0
        else:
            return result[0]
    else:
        if int(result[0]) >= int(level) :
            return True


def check_admin(id, level=1):
    result = cur.execute("SELECT `admin` FROM `users` WHERE `id` = '{}'".format(id)).fetchmany(1)[0][0]
    if result > level-1:
        return True
    else:
        return False


def check_category(category):
    categories = ["Художник", "СММ Специалист", "Фотограф", "Видеограф", "Оператор", "Музыкант", "Звукорежисер", "Певец", "Хореограф", "Танцовщик", "Скульптор", "Дизайнер интерьера",
    "Архитектор", "Гейм-дизайнер", "Графический дизайн", "Веб-дизайнер", "Дизайнер одежды", "Арт-директор", "Поэт", "Писатель", "Сценарист", "Режиссер", "Продюсер", "Лектор",
    "Лектор", "Коуч", "Коворкер", "Ведущий", "Блогер", "Актер", "Модель", "Бармен", "Гость", "Журналист"]
    category_exist = ''
    for category_ in categories:
        if str(category_) == str(category):
            category_exist = 'exits'
    if category_exist == 'exits':
        return True
    else:
        return False


def check_project_category(category):
    categories = ["Категория 1", "Категория 2", "Категория 3", "Категория 4"]
    category_exist = ''
    for category_ in categories:
        if str(category_) == str(category):
            category_exist = 'exits'
    if category_exist == 'exits':
        return True
    else:
        return False


def update_balance(id, sum):
    result = cur.execute("SELECT `balance` FROM `users` WHERE `id` = '{}'".format(id)).fetchmany(1)[0][0]
    balance = result + sum
    cur.execute("UPDATE `users` SET `balance` = '{}' WHERE `id` = '{}'".format(balance, id))
    con.commit()


def get_main_menu(id):
    level_admin = check_admin_level(id)
    if level_admin > 0:
        if level_admin == 1:
            return main_menu_apanel
        elif level_admin == 2:
            return main_menu_apanel
    else:
        return main_menu


def get_admin_panel(id):
    if check_admin(id, 1):
        return admin_panel_1_menu
    elif check_admin(id, 2):
        return admin_panel_2_menu


def get_balance(id):
    result = cur.execute("SELECT `balance` FROM `users` WHERE `id` = '{}'".format(id)).fetchmany(1)[0][0]
    return result


def add_action_at_payments_log(id, sum, action, action_name):
    cur.execute("INSERT INTO `payments_log` VALUES('{}', '{}', '{}', '{}')".format(id, sum, action, action_name))
    con.commit()


def get_payments_log_by_action(id, action):
    result = cur.execute("SELECT * FROM `payments_log` WHERE `id` = '{}' AND `action` = '{}'".format(id, action)).fetchmany(20)
    if len(result) > 0:
        text = ''
        for payment in result:
            if action == payment[2]:
                sum = payment[1]
                action_name= payment[3]
                text = text + f'\nСумма: {sum}₽, Операция: {action_name}'
        if len(text) > 0:
            return text
        else:
            return '\nПусто...'
    else:
        return '\nПусто...'


def get_my_events(id):
    result = cur.execute("SELECT * FROM `user_events` WHERE `id` = '{}'".format(id)).fetchmany(20)
    if len(result) > 0:
        menu = InlineKeyboardMarkup(row_width=1)
        for event in result:
            eid = event[0]
            title = event[2]
            button = InlineKeyboardButton(text=title, callback_data=f'see_event_info_by_participant_{eid}')
            menu.add(button)
        return menu
    else:
        menu = InlineKeyboardMarkup(row_width=1)
        button = InlineKeyboardButton(text='Нету', callback_data=f"none")
        menu.add(button)
        return menu


def check_referals(id, type_ref):
    text = ''
    with open(f"json/profile/{id}.json", "r") as file:
        content = json.load(file)
        file.close()
    referals = content["referals"]
    i = 0
    for referal in referals:
        verification = referal["verification"]
        if type_ref == 'appruf':
            if verification == 'accept':
                i += 1
                ref_id = referal["id"]
                result = cur.execute("SELECT `username` FROM `users` WHERE `id` = '{}'".format(ref_id)).fetchall()[0][0]
                text = text + f'@{result}\n'
        elif type_ref == 'in_hold':
            if verification == 'none':
                i += 1
                ref_id = referal["id"]
                result = cur.execute("SELECT `username` FROM `users` WHERE `id` = '{}'".format(ref_id)).fetchall()[0][0]
                text = text + f'@{result}\n'
    if i > 0:
        text = f'Количество ваших рефералов: {i}\n\n' + text
    else:
        text = 'У вас нету рефералов.'
    return text


def check_name_surname(string):
    alphabet = ["а","б","в","г","д","е","ё","ж","з","и","й","к","л","м","н","о", "п","р","с","т","у","ф","х","ц","ч","ш","щ","ъ","ы","ь","э","ю","я","q","w","e","r","t","y","u","i","o","p","a","s","d","f","g","h","j","k","l","z","x","c","v","b","n","m", " "]
    for one_char in string:
        if one_char == '-':
            continue
        else:
            if one_char.lower() in alphabet:
                continue
            else:
                return False
    return True


def get_tariff_info(tariff_name, type_of_delivery='for_menu'):
    result = cur.execute("SELECT * FROM `tariff` WHERE `name` = '{}'".format(tariff_name)).fetchmany(1)[0]
    if type_of_delivery == 'for_menu':
        tariff_info = f'🚀 Тариф {result[0]}\n\n{result[2]}\n\nЦена: {result[1]}₽'
        return tariff_info
    elif type_of_delivery == 'for_buy':
        return int(result[1])
    elif type_of_delivery == 'for_admin':
        return result


def check_exists_sum(id, sum):
    result = cur.execute("SELECT `balance` FROM `users` WHERE `id` = '{}'".format(id)).fetchmany(1)[0][0]
    if int(result) >= int(sum):
        return True
    else:
        return False


def update_tariff(id, tariff):
    result = cur.execute("SELECT * FROM `tariff_booking` WHERE `id` = '{}'".format(id)).fetchmany(1)[0]
    date_split = result[2].rsplit('-')
    today_date = date.today()
    if len(date_split) == 3:
        end_date = date(int(date_split[0]), int(date_split[1]), int(date_split[2]))
        if end_date > today_date:
            end_date_write = end_date + d.timedelta(days=30)
            tariff = result[1]
        else:
            end_date_write = today_date + d.timedelta(days=30)
    else:
        end_date_write = today_date + d.timedelta(days=30)
    cur.execute("UPDATE `tariff_booking` SET `name` = '{}' WHERE `id` = '{}'".format(tariff, id))
    cur.execute("UPDATE `tariff_booking` SET `date` = '{}' WHERE `id` = '{}'".format(end_date_write, id))
    con.commit()


def get_profile_menu(id):
    my_profile_menu = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    # my_visa = KeyboardButton('💳 Моя Виза')
    # my_tikets = KeyboardButton('🎟️ Мои билеты')
    notifications = KeyboardButton('📩 Уведомления')
    edit_profile = KeyboardButton('✏️ Редактировать')
    verification_profile = KeyboardButton('✔️ Верификация')
    my_profile_menu.add(notifications, edit_profile)
    with open(f'json/profile/{id}.json', 'r') as file:
        content = json.load(file)
        file.close()
    if content["verification"] == '-':
        my_profile_menu.add(verification_profile)
    my_profile_menu.add(back_button)
    return my_profile_menu


def set_moderation_for_profile(id, field, data=''):
    cur.execute("INSERT INTO `profile_moderation` VALUES('{}', '{}', '{}')".format(id, field, data))
    con.commit()


def check_exists_field_in_profile_moderatin(id, field):
    result = cur.execute("SELECT * FROM `profile_moderation` WHERE `id` = '{}' AND `field` = '{}'".format(id, field)).fetchmany(1)
    if len(result) > 0:
        return False
    else:
        return True


def create_project_sample(id, project_id):
    structure = {
        "project_id": f"{project_id}",
        "project_name": "",
        "project_description": "",
        "project_type": f"",
        "project_city": "none", # ЕСЛИ ОНЛАЙН ПРОЕКТ ТО НЕТУ
        "project_category": "",
        "project_subcategories": "",
        "project_need_categories": "",
        "project_price": "",
        "project_media": [

        ]
        
    }
    with open(f'json/creating_project/{id}.json', 'w') as file:
        file.write(json.dumps(structure))
        file.close()


def add_info_in_project_sample(id, field, data):
    with open(f"json/creating_project/{id}.json", "r") as file:
        structure = json.load(file)
        file.close()
    if field == 'project_need_categories':
        if structure["project_need_categories"] == '':
            structure["project_need_categories"] = data
        elif data == 'none':
            structure["project_need_categories"] = ''
        else:
            if len(data) > 0:
                structure["project_need_categories"] = structure["project_need_categories"] + '  ' + data
            else:
                structure["project_need_categories"] = ''
    elif field == 'project_subcategories':
        if structure["project_subcategories"] == '':
            structure["project_subcategories"] = data
        else:
            if len(data) > 0:
                structure["project_subcategories"] = structure["project_subcategories"] + '  ' + data
            else:
                structure["project_subcategories"] = ''
    else:
        structure[f"{field}"] = data
    with open(f'json/creating_project/{id}.json', 'w') as file:
        file.write(json.dumps(structure))
        file.close()


def check_count_categories_project(id, field):
    with open(f"json/creating_project/{id}.json", "r") as file:
        structure = json.load(file)
        file.close()
    data = structure[f"{field}"]
    if field == 'project_need_categories':
        if len(data.rsplit('  ')) < 6:
            return True
        else:
            return False
    elif field == 'project_subcategories':
        if len(data.rsplit('  ')) < 3:
            return True
        else:
            return False


def check_uniqueness_categories_project(id, field, data):
    with open(f"json/creating_project/{id}.json", "r") as file:
        structure = json.load(file)
        file.close()
    project_subcategories = structure["project_subcategories"]
    project_need_categories = structure["project_need_categories"]
    project_need_categories = project_need_categories.rsplit("+")
    if field == 'project_subcategories':
        if data in project_subcategories:
            return False
        else:
            return True
    elif field == 'project_need_categories':
        if data in project_need_categories:
            return False
        else:
            return True


def check_exists_field_of_project_sample(id, field): #ПРОВЕРКА СУЩЕСТВОВАНИЯ СОДЕРЖИМОГО ПОЛЯ В СОЗДАНИИ ШАБЛОНА ПРОЕКТА ДЛЯ ВОЗМОЖНОСТИ СКИПА УЖЕ ЗАПОЛНЕНЫХ
    with open(f"json/creating_project/{id}.json", "r") as file:
        structure = json.load(file)
    if len(structure[f"{field}"]) > 0:
        return True
    else:
        return False


def get_field_from_sample(id, field):
    with open(f"json/creating_project/{id}.json", "r") as file:
        structure = json.load(file)
        file.close()
    return structure[f"{field}"]


def add_media_in_project_sample(id, type_media, link=''):
    with open(f"json/creating_project/{id}.json", "r") as file:
        structure = json.load(file)
        file.close()
    len_array = len(structure["project_media"])
    if type_media == 'photo':
        if len_array <= 5:
            media_structure = {"type": f"{type_media}", "path": f"{id}_{len_array + 1}"}
            structure["project_media"].append(media_structure)
        else:
            structure["project_media"] = []
            media_structure = {"type": f"{type_media}", "path": f"{id}_1"}
            structure["project_media"].append(media_structure)
    elif type_media == 'video':
        if len_array <= 5:
            media_structure = {"type": f"{type_media}", "link": f"{link}"}
            structure["project_media"].append(media_structure)
        else:
            structure["project_media"] = []
            media_structure = {"type": f"{type_media}", "link": f"{link}"}
            structure["project_media"].append(media_structure)
        
        
    with open(f'json/creating_project/{id}.json', 'w') as file:
        file.write(json.dumps(structure))
        file.close()


def get_path_for_media_in_project_sample(id, project_type):
    with open(f"json/creating_project/{id}.json", "r") as file:
        structure = json.load(file)
        file.close()
    len_array = len(structure["project_media"])
    if project_type == 'photo':
        return f"photos/creating_project/{id}_{len_array}.png"


def check_full_project_sample(id):
    with open(f"json/creating_project/{id}.json", "r") as file:
        structure = json.load(file)
        file.close()
    if len(structure["project_price"]) > 0:
        if len(structure["project_name"]) > 0:
            if len(structure["project_description"]) > 0:
                if len(structure["project_category"]) > 0:
                    if len(structure["project_subcategories"]) > 0:
                        if len(structure["project_need_categories"]) > 0:
                            if len(structure["project_price"]) > 0:
                                return True
    return False


def send_project_sample(id):
    structure = {
        "projects": {

        }
    }
    if os.path.exists(f'json/projects/projects.json'):
        pass
    else:
        with open('json/projects/projects.json', 'w') as file:
            file.write(json.dumps(structure))
            file.close()
    with open(f"json/creating_project/{id}.json", 'r') as file:
        content = json.load(file)
        file.close()
    project_id = content["project_id"]
    project_type = content["project_type"]
    project_city = content["project_city"]
    project_category = content["project_category"]
    project_subcategories = content["project_subcategories"]
    project_need_categories = content["project_need_categories"]
    project_name = content["project_name"]
    project_description = content["project_description"]
    project_price = content["project_price"]
    project_media = content["project_media"]
    structure = {
        "project_name": f"{project_name}",
        "project_description": f"{project_description}",
        "project_type": f"{project_type}",
        "project_city": f"{project_city}", # ЕСЛИ ОНЛАЙН ПРОЕКТ ТО НЕТУ
        "project_category": f"{project_category}",
        "project_subcategories": f"{project_subcategories}",
        "project_need_categories": f"{project_need_categories}",
        "project_price": f"{project_price}",
        "project_media": f"{project_media}",
        "project_message_from_administration": "",
        "project_follows": [

        ],
    }
    with open(f"json/projects/projects.json", 'r') as file:
        content = json.load(file)
        file.close()
    content["projects"][f"project_{project_id}"] = structure
    with open('json/projects/projects.json', 'w') as file:
            file.write(json.dumps(content))
            file.close()
    cur.execute("INSERT INTO `projects` VALUES('{}', '{}', '{}', '{}', 'waiting')".format(project_id, id, project_need_categories, project_city))
    con.commit()


def add_info_in_find_project(id, field, data):
    if field == 'project_type':
        cur.execute("DELETE FROM `find_projects` WHERE `id` = '{}'".format(id))
        cur.execute("INSERT INTO `find_projects` VALUES('{}', '{}', '')".format(id, data))
    elif field == 'project_categories':
        cur.execute("UPDATE `find_projects` SET `categories` = '{}' WHERE `id` = '{}'".format(data, id))
    con.commit()

def get_user_categories(id):
    with open(f"json/profile/{id}.json", "r") as file:
        content = json.load(file)
        file.close()
    main_category_1 = content["main_category_1"]
    main_category_2 = content["main_category_2"]
    main_category_3 = content["main_category_3"]
    if main_category_2 == '':
        if main_category_3 == '':
            return main_category_1
        else:
            return main_category_1 + '  ' + main_category_3
    else:
        if main_category_3 == '':
            return main_category_1 + '  ' + main_category_2
        else:
            return main_category_1 + '  ' + main_category_2 + '  ' + main_category_3


def get_user_interests(id):
    with open(f"json/profile/{id}.json", "r") as file:
        content = json.load(file)
    return content["interests"]


def get_random_project_by_personal_settings(id):
    result = cur.execute("SELECT * FROM `projects` WHERE `status` = 'accept'").fetchall()
    user_categories = get_user_categories(id).rsplit("  ")
    right_projects = []
    for project in result:
        if project[3] == 'none':
            if get_field_projects_to_find(id, 'type_project') == 'online':
                need_categories = project[2].rsplit("  ")
                for need_category in need_categories:
                    if need_category in user_categories or need_category == 'Нету':
                        right_projects.append(project[0])
        else:
            if get_field_projects_to_find(id, 'type_project') == 'offline':
                if get_user_city(id) == project[3]:
                    need_categories = project[2].rsplit("  ")
                    for need_category in need_categories:
                        if need_category in user_categories or need_category == 'Нету':
                            right_projects.append(project[0])
    if len(right_projects) > 0:
        num_project = randint(1, len(right_projects))
        return right_projects[num_project-1]
    else:
        return 0


def get_random_project_by_not_personal_settings(id):
    result = cur.execute("SELECT * FROM `projects` WHERE `status` = 'accept'").fetchall()
    user_categories = get_user_categories(id).rsplit("  ")
    right_projects = []
    for project in result:
        if project[3] == 'none':
            if get_field_projects_to_find(id, 'type_project') == 'online':
                right_projects.append(project[0])
        else:
            if get_field_projects_to_find(id, 'type_project') == 'offline':
                if get_user_city(id) == project[3]:
                        right_projects.append(project[0])
    if len(right_projects) > 0:
        num_project = randint(1, len(right_projects))
        return right_projects[num_project-1]
    else:
        return 0


def get_profile_image(id):
    def prepare_mask(size, antialias = 2):
        mask = Image.new('L', (size[0] * antialias, size[1] * antialias), 0)
        ImageDraw.Draw(mask).ellipse((0, 0) + mask.size, fill=255)
        return mask.resize(size, Image.ANTIALIAS)

    def crop(im, s):
        w, h = im.size
        k = w / s[0] - h / s[1]
        if k > 0: im = im.crop(((w - h) / 2, 0, (w + h) / 2, h))
        elif k < 0: im = im.crop((0, (h - w) / 2, w, (h + w) / 2))
        return im.resize(s, Image.ANTIALIAS)

    size = (200, 200)
    im = Image.open(f'photos/profile/{id}.png')
    im = crop(im, size)
    im.putalpha(prepare_mask(size, 4))
    user_photo = im


def get_field_projects_to_find(id, field):
    result = cur.execute("SELECT * FROM `find_projects` WHERE `id` = '{}'".format(id)).fetchmany(1)
    if len(result[0]) > 0:
        result = result[0]
        if field == 'type_project':
            return result[1]
        elif field == 'categories':
            return result[2]


def get_project_about_sample(id):
    with open(f"json/creating_project/{id}.json", "r") as file:
        content = json.load(file)
    project = content
    media_text = ''
    if len(project["project_media"]) > 0:
        pass 
    else:
        media_text = 'Отсутствует'
    if project["project_type"] == 'offline':
        text = f'{project["project_name"]}\n\n{project["project_description"]}\n\n{project["project_city"]}\n\nКатегория проекта: {project["project_category"]}\n\nПодкатегории проекта: {project["project_subcategories"]}\n\nКатегории исполнителя: {project["project_need_categories"]}\n\nОплата: {project["project_price"]}\n\nМедиа: {media_text}'
    else:
        text = f'{project["project_name"]}\n\n{project["project_description"]}\n\nКатегория проекта: {project["project_category"]}\n\nПодкатегории проекта: {project["project_subcategories"]}\n\nКатегории исполнителя: {project["project_need_categories"]}\n\nОплата: {project["project_price"]}\n\nМедиа: {media_text}'
    return text


def get_photo_from_project_sample(id):
    with open(f"json/creating_project/{id}.json", "r") as file:
        content = json.load(file)
    project = content
    result = []
    if len(project["project_media"]) > 0:
        for media in project["project_media"]:
            if media["type"] == 'photo':
                result.append(media["path"])
        return result
    return 0                


def get_video_from_project_sample(id):
    with open(f"json/creating_project/{id}.json", "r") as file:
        content = json.load(file)
    project = content
    result = []
    if len(project["project_media"]) > 0:
        for media in project["project_media"]:
            if media["type"] == 'video':
                result.append(media["link"])
        menu = InlineKeyboardMarkup(row_width=1)
        for link in result:
            button = InlineKeyboardButton(text='Видео', web_app=WebAppInfo(url=link))
            menu.add(button)
        return menu
    return None


def get_project_as_text(project_id):
    with open(f"json/projects/projects.json", "r") as file:
        content = json.load(file)
    project = content["projects"][f"project_{project_id}"]
    media_text = ''
    if len(project["project_media"]) > 0:
        pass 
    else:
        media_text = 'Отсутствует'
    if project["project_type"] == 'offline':
        text = f'{project["project_name"]}\n\n{project["project_description"]}\n\n{project["project_city"]}\n\nКатегория проекта: {project["project_category"]}\n\nПодкатегории проекта: {project["project_subcategories"]}\n\nКатегории исполнителя: {project["project_need_categories"]}\n\nОплата: {project["project_price"]}\n\nМедиа: {media_text}'
    else:
        text = f'{project["project_name"]}\n\n{project["project_description"]}\n\nКатегория проекта: {project["project_category"]}\n\nПодкатегории проекта: {project["project_subcategories"]}\n\nКатегории исполнителя: {project["project_need_categories"]}\n\nОплата: {project["project_price"]}\n\nМедиа: {media_text}'
    return text


def get_photo_from_project(project_id):
    with open(f"json/projects/projects.json", "r") as file:
        content = json.load(file)
    project = content["projects"][f"project_{project_id}"]
    result = []
    if len(project["project_media"]) > 0:
        for media in project["project_media"]:
            if media["type"] == 'photo':
                result.append(media["path"])
        return result
    return 0


def get_video_from_project(project_id):
    with open(f"json/projects/projects.json", "r") as file:
        content = json.load(file)
    project = content["projects"][f"project_{project_id}"]
    result = []
    if len(project["project_media"]) > 0:
        for media in project["project_media"]:
            if media["type"] == 'video':
                result.append(media["link"])
        menu = InlineKeyboardMarkup(row_width=1)
        for link in result:
            button = InlineKeyboardButton(text='Видео', web_app=WebAppInfo(url=link))
            menu.add(button)
        return menu
    return None


def get_project_to_accept():
    result = cur.execute("SELECT `project_id` FROM `projects` WHERE `status` = 'waiting'").fetchmany(1)
    if len(result) > 0:
        result = result[0]
        if len(result) > 0:
            return get_project_as_text(result[0]), result[0], True
        else:
            return 0, 0, False
    else:
        return 0, 0, False


def delete_user(id):
    cur.execute("DELETE FROM `users` WHERE `id` = '{}'".format(id))
    con.commit()
    os.remove(f'json/profile/{id}.json')


def get_need_categories_for_project_samle(id):
    with open(f"json/creating_project/{id}.json", "r") as file:
        content = json.load(file)
    return content["project_need_categories"].rsplit("  ")


def send_notification(id, text):
    with open(f"json/notification/{id}.json", "r") as file:
        content = json.load(file)
    content["notifications"].append([text, f"{datetime.datetime.now().day}.{datetime.datetime.now().month}.{datetime.datetime.now().year}"])
    with open(f"json/notification/{id}.json", "w") as file:
        file.write(json.dumps(content))
    

def get_notifications(id):
    with open(f"json/notification/{id}.json", "r") as file:
        content = json.load(file)
    notifications = content["notifications"]
    result = ''
    if len(notifications) != 0:
        if notifications[0] != '':
            for notification in notifications:
                text = notification[0]
                date_notification = notification[1]
                result = result + f'{text}\n        {date_notification}\n\n'
            return result
        else:
            return 'У вас нет уведомлений'
    else:
        return 'У вас нет уведомлений'


def update_status_project(project_id, status, reason=''):
    cur.execute("UPDATE `projects` SET `status` = '{}' WHERE `project_id`".format(status))
    con.commit()
    result = cur.execute("SELECT `id` FROM `projects` WHERE `project_id` = '{}'".format(project_id)).fetchmany(1)
    id = result[0][0]
    if status == 'accept':
        send_notification(id, 'Ваш проект был одобрен администрацией')
    elif status == 'unaccept':
        send_notification(id, f'Ваш проект был отменен администрацией по причине {reason}')
        with open(f"json/projects/projects.json", 'r') as file:
            content = json.load(file)
            file.close()
        content["projects"][f"project_{project_id}"]["project_message_from_administration"] = reason
        with open('json/projects/projects.json', 'w') as file:
                file.write(json.dumps(content))
                file.close()


def follow_project(id, project_id):
    with open("json/projects/projects.json", "r") as file:
        content = json.load(file)
    owner_id = cur.execute("SELECT `id` FROM `projects` WHERE `project_id` = '{}'".format(project_id)).fetchmany(1)[0][0]
    content["projects"][f"project_{project_id}"]["project_follows"].append({"id": f"{id}", "status": "waiting"})
    with open(f"json/projects/projects.json", "w") as file:
        file.write(json.dumps(content))
    send_notification(owner_id, f'У вашего проекта новый отклик. Всего {len(content["projects"][f"project_{project_id}"]["project_follows"])} откликов')


def warn_project(id, project_id, reason):
    result = cur.execute("SELECT * FROM `warns_project` WHERE `id` = '{}' AND `project_id` = '{}'".format(id, project_id)).fetchmany(1)
    if len(result) == 0:
        cur.execute("INSERT INTO `warns_project` VALUES('{}', '{}', '{}')".format(id, project_id, reason))
        con.commit()
        return 'Ваша жалоба отправленна администрации.'
    else:
        return 'Вы уже отправляли жалобу на этот проект'


def create_question_sample(id, question_id):
    structure = {
        "question_id": f"{question_id}",
        "question_text": "",
        "question_category_1": "",
        "question_category_2": "",
        "photo_1": "-",
        "photo_2": "-",
        "photo_3": "-",
        "video_1": "-",
        "question_deadline": "",
    }
    with open(f"json/creating_question/{id}.json", "w") as file:
        file.write(json.dumps(structure))


def add_info_in_creating_question(id, field, data):
    with open(f"json/creating_question/{id}.json", "r") as file:
        structure = json.load(file)
    structure[f"{field}"] = data
    with open(f"json/creating_question/{id}.json", "w") as file:
        file.write(json.dumps(structure))


def get_field_from_question_sample(id, field):
    with open(f"json/creating_question/{id}.json", "r") as file:
        structure = json.load(file)
    return structure[f"{field}"]


def get_profile(id, username):
    profile_image = Image.open("images/profile/profile.png")
    date_ = get_json_user_field(id, "date_birth")
    split_date = date_.rsplit(".")
    today = date.today()
    dob = date(int(split_date[2]), int(split_date[1]), int(split_date[0])) 
    age = relativedelta(today, dob).years
    name_surname = get_json_user_field(id, "name_surname") + ', ' + str(age)
    city = get_json_user_field(id, "city")
    stat = get_json_user_field(id, "stat")
    last_in_work = stat["last_in_work"]
    rating = stat["rating"]
    font_name_surname = ImageFont.truetype("fonts/Inter-SemiBold.otf", 35)
    font_city = ImageFont.truetype("fonts/Inter-Regular.otf", 30)
    font_categories = ImageFont.truetype("fonts/Inter-Regular.otf", 20)
    font_rating = ImageFont.truetype("fonts/Inter-Regular.otf", 26)
    font_dates = ImageFont.truetype("fonts/Inter-Regular.otf", 18)
    draw = ImageDraw.Draw(profile_image)
    def make_border(profile_image, coords_to_draw, border_width):
        draw = ImageDraw.Draw(profile_image)
        coords = coords_to_draw
        i = 0
        while i <= border_width:
            coords += 1
            i += 1
            draw.ellipse((coords - 15, 460, coords + 15, 490), fill=("#D8D5E1"))
        return profile_image
    width_main_image = (profile_image.size[0])

    """
    
    Аватар
    
    """
    W, H = (profile_image.size[0],profile_image.size[1])
    def prepare_mask(size, antialias = 2):
        mask = Image.new('L', (size[0] * antialias, size[1] * antialias), color=0)
        ImageDraw.Draw(mask).ellipse((0, 0) + mask.size, fill=255)
        return mask.resize(size, Image.Resampling.LANCZOS)

    def crop(image, s):
        w, h = image.size
        k = w / s[0] - h / s[1]
        if k > 0: image = image.crop(((w - h) / 2, 0, (w + h) / 2, h))
        elif k < 0: image = image.crop((0, (h - w) / 2, w, (h + w) / 2))
        return image.resize(s, Image.Resampling.LANCZOS)
    w, h = 200, 200
    size = (w, h)
    image = Image.open(f'photos/profile/{id}.png', "r")
    image = crop(image, size)
    image.putalpha(prepare_mask(size, 4))
    user_photo = image
    profile_image.paste(user_photo, (int((W - w)/2), 24), mask=user_photo) 
    
    """

    Имя Фамилия

    """
    
    W, H = (profile_image.size[0]+80,profile_image.size[1])
    w, h = draw.textsize(name_surname,font=font_name_surname)
    draw.text(xy=((W - w)/2,270), text=name_surname, align="center", font=font_name_surname, fill=('#FFFFFF')) 
    if check_accept_user(id):
        accept_unaccept_user_image = Image.open("images/profile/accept_user.png")
    else:
        accept_unaccept_user_image = Image.open("images/profile/unaccept_user.png")
    accept_unaccept_user_image = accept_unaccept_user_image.resize(size=(35, 35))
    width_for_name_surname_logo = int((W/2 - w/2 )-55)
    profile_image.paste(accept_unaccept_user_image, (width_for_name_surname_logo, 273), mask=accept_unaccept_user_image)
    """

    Город

    """
    W, H = (profile_image.size[0]+80,profile_image.size[1])
    w, h = draw.textsize(city,font=font_city)
    draw.text(xy=((W - w)/2,330), text=city, align="center", font=font_city, fill=('#D8D5E1')) 
    
    city_image = Image.open("images/profile/location.png")
    city_image = city_image.resize(size=(30, 30))
    width_for_city_logo = int((W/2 - w/2 )-50)
    profile_image.paste(city_image, (width_for_city_logo, 332), mask=city_image)
    # profile_image.show()
    """
    
    Категории

    """
    W, H = (profile_image.size[0],profile_image.size[1])
    
    
    categories = get_user_categories(id).rsplit("  ")
    if len(categories) == 1:
        w, h = draw.textsize(categories[0],font=font_categories)
        profile_image = make_border(profile_image, (W - w)/2, draw.textsize(categories[0],font=font_categories)[0])
        draw.text(xy=((W - w)/2,463), text=categories[0], align="center", font=font_categories, fill=('#252429')) 
    elif len(categories) == 2:
        width_to_margin_categories = draw.textsize(categories[0],font=font_categories)[0] + draw.textsize(categories[1],font=font_categories)[0] - 90

        x_to_draw = (W - width_to_margin_categories)/2 - draw.textsize(categories[0],font=font_categories)[0]/2 - 22.5
        profile_image = make_border(profile_image, x_to_draw, draw.textsize(categories[0],font=font_categories)[0])
        draw.text(xy=(x_to_draw,463), text=categories[0], font=font_categories, fill=('#252429'))

        x_to_draw = (W - width_to_margin_categories)/2 + draw.textsize(categories[0],font=font_categories)[0]/2 + 22.5
        profile_image = make_border(profile_image, x_to_draw, draw.textsize(categories[1],font=font_categories)[0])
        draw.text(xy=(x_to_draw, 463), text=categories[1], font=font_categories, fill=('#252429'))

    elif len(categories) == 3:
        width_to_margin_categories = draw.textsize(categories[0],font=font_categories)[0] + draw.textsize(categories[1],font=font_categories)[0] + draw.textsize(categories[2],font=font_categories)[0] - 30

        x_to_draw = (W - width_to_margin_categories)/2 - 60
        profile_image = make_border(profile_image, x_to_draw, draw.textsize(categories[0],font=font_categories)[0])
        draw.text(xy=(x_to_draw,463), text=categories[0], align="center", font=font_categories, fill=('#252429'))
        
        x_to_draw = (W - width_to_margin_categories)/2 + draw.textsize(categories[0],font=font_categories)[0] - 15
        profile_image = make_border(profile_image, x_to_draw  , draw.textsize(categories[1],font=font_categories)[0])
        draw.text(xy=(x_to_draw,463), text=categories[1], align="center", font=font_categories, fill=('#252429'))

        x_to_draw = (W - width_to_margin_categories)/2 + draw.textsize(categories[0],font=font_categories)[0] + draw.textsize(categories[1],font=font_categories)[0] + 30
        profile_image = make_border(profile_image, x_to_draw, draw.textsize(categories[2],font=font_categories)[0])
        draw.text(xy=(x_to_draw, 463), text=categories[2], align="center", font=font_categories, fill=('#252429'))

    """
    
    Summary Rating
    
    """

    w = int(math.ceil(draw.textsize(rating, font=font_rating)[0])) + 35
    rate_image = Image.open("images/profile/star.png")
    star_width = int((W - w)/2)
    width = (star_width, 560)
    profile_image.paste(im=rate_image, box=width, mask=rate_image)
    draw.text(xy=((W - w)/2 + 35, 558), text=rating, font=font_rating)

    """

    Last Online и Last in Work

    """

    last_online = get_last_online(id)
    draw.text(xy=(110, 730), text = last_online, font=font_dates, fill=("#252429"))

    draw.text(xy=(630, 730), text = last_in_work, font=font_dates, fill=("#252429"))

    path = f'photos/nontime/{randint(1111111111, 9999999999)}.png'
    profile_image.save(path, "PNG")


def get_last_online(id):
    result = cur.execute("SELECT `last_online` FROM `users` WHERE `id` = '{}'".format(id)).fetchmany(1)[0][0]
    return beautifull_date(result)


def update_last_online(id):
    date_ = f'{datetime.datetime.now().day}.{datetime.datetime.now().month}.{datetime.datetime.now().year}'
    cur.execute("UPDATE `users` SET `last_online` = '{}' WHERE `id` = '{}'".format(date_, id))
    con.commit()


def get_profile(id):
    profile_image = Image.open("images/profile/profile.png")
    date_ = get_json_user_field(id, "date_birth")
    split_date = date_.rsplit(".")
    today = date.today()
    dob = date(int(split_date[2]), int(split_date[1]), int(split_date[0])) 
    age = relativedelta(today, dob).years
    name_surname = get_json_user_field(id, "name_surname") + ', ' + str(age)
    city = get_json_user_field(id, "city")
    stat = get_json_user_field(id, "stat")
    last_in_work = stat["last_in_work"]
    rating = stat["rating"]
    font_name_surname = ImageFont.truetype("fonts/Inter-SemiBold.otf", 35)
    font_city = ImageFont.truetype("fonts/Inter-Regular.otf", 30)
    font_categories = ImageFont.truetype("fonts/Inter-Regular.otf", 20)
    font_rating = ImageFont.truetype("fonts/Inter-Regular.otf", 26)
    font_dates = ImageFont.truetype("fonts/Inter-Regular.otf", 18)
    draw = ImageDraw.Draw(profile_image)
    def make_border(profile_image, coords_to_draw, border_width):
        draw = ImageDraw.Draw(profile_image)
        coords = coords_to_draw
        i = 0
        while i <= border_width:
            coords += 1
            i += 1
            draw.ellipse((coords - 15, 460, coords + 15, 490), fill=("#D8D5E1"))
        return profile_image
    width_main_image = (profile_image.size[0])

    """
    
    Аватар
    
    """
    W, H = (profile_image.size[0],profile_image.size[1])
    def prepare_mask(size, antialias = 2):
        mask = Image.new('L', (size[0] * antialias, size[1] * antialias), color=0)
        ImageDraw.Draw(mask).ellipse((0, 0) + mask.size, fill=255)
        return mask.resize(size, Image.Resampling.LANCZOS)

    def crop(image, s):
        w, h = image.size
        k = w / s[0] - h / s[1]
        if k > 0: image = image.crop(((w - h) / 2, 0, (w + h) / 2, h))
        elif k < 0: image = image.crop((0, (h - w) / 2, w, (h + w) / 2))
        return image.resize(s, Image.Resampling.LANCZOS)
    w, h = 200, 200
    size = (w, h)
    image = Image.open(f'photos/profile/{id}.png', "r")
    image = crop(image, size)
    image.putalpha(prepare_mask(size, 4))
    user_photo = image
    profile_image.paste(user_photo, (int((W - w)/2), 24), mask=user_photo) 
    
    """

    Имя Фамилия

    """
    
    W, H = (profile_image.size[0]+80,profile_image.size[1])
    w, h = draw.textsize(name_surname,font=font_name_surname)
    draw.text(xy=((W - w)/2,270), text=name_surname, align="center", font=font_name_surname, fill=('#FFFFFF')) 
    if check_accept_user(id):
        accept_unaccept_user_image = Image.open("images/profile/accept_user.png")
    else:
        accept_unaccept_user_image = Image.open("images/profile/unaccept_user.png")
    accept_unaccept_user_image = accept_unaccept_user_image.resize(size=(35, 35))
    width_for_name_surname_logo = int((W/2 - w/2 )-55)
    profile_image.paste(accept_unaccept_user_image, (width_for_name_surname_logo, 273), mask=accept_unaccept_user_image)
    """

    Город

    """
    W, H = (profile_image.size[0]+80,profile_image.size[1])
    w, h = draw.textsize(city,font=font_city)
    draw.text(xy=((W - w)/2,330), text=city, align="center", font=font_city, fill=('#D8D5E1')) 
    
    city_image = Image.open("images/profile/location.png")
    city_image = city_image.resize(size=(30, 30))
    width_for_city_logo = int((W/2 - w/2 )-50)
    profile_image.paste(city_image, (width_for_city_logo, 332), mask=city_image)
    # profile_image.show()
    """
    
    Категории

    """
    W, H = (profile_image.size[0],profile_image.size[1])
    
    
    categories = get_user_categories(id).rsplit("  ")
    if len(categories) == 1:
        w, h = draw.textsize(categories[0],font=font_categories)
        profile_image = make_border(profile_image, (W - w)/2, draw.textsize(categories[0],font=font_categories)[0])
        draw.text(xy=((W - w)/2,463), text=categories[0], align="center", font=font_categories, fill=('#252429')) 
    elif len(categories) == 2:
        width_to_margin_categories = draw.textsize(categories[0],font=font_categories)[0] + draw.textsize(categories[1],font=font_categories)[0] - 90

        x_to_draw = (W - width_to_margin_categories)/2 - draw.textsize(categories[0],font=font_categories)[0]/2 - 22.5
        profile_image = make_border(profile_image, x_to_draw, draw.textsize(categories[0],font=font_categories)[0])
        draw.text(xy=(x_to_draw,463), text=categories[0], font=font_categories, fill=('#252429'))

        x_to_draw = (W - width_to_margin_categories)/2 + draw.textsize(categories[0],font=font_categories)[0]/2 + 22.5
        profile_image = make_border(profile_image, x_to_draw, draw.textsize(categories[1],font=font_categories)[0])
        draw.text(xy=(x_to_draw, 463), text=categories[1], font=font_categories, fill=('#252429'))

    elif len(categories) == 3:
        width_to_margin_categories = draw.textsize(categories[0],font=font_categories)[0] + draw.textsize(categories[1],font=font_categories)[0] + draw.textsize(categories[2],font=font_categories)[0] - 30

        x_to_draw = (W - width_to_margin_categories)/2 - 60
        profile_image = make_border(profile_image, x_to_draw, draw.textsize(categories[0],font=font_categories)[0])
        draw.text(xy=(x_to_draw,463), text=categories[0], align="center", font=font_categories, fill=('#252429'))
        
        x_to_draw = (W - width_to_margin_categories)/2 + draw.textsize(categories[0],font=font_categories)[0] - 15
        profile_image = make_border(profile_image, x_to_draw  , draw.textsize(categories[1],font=font_categories)[0])
        draw.text(xy=(x_to_draw,463), text=categories[1], align="center", font=font_categories, fill=('#252429'))

        x_to_draw = (W - width_to_margin_categories)/2 + draw.textsize(categories[0],font=font_categories)[0] + draw.textsize(categories[1],font=font_categories)[0] + 30
        profile_image = make_border(profile_image, x_to_draw, draw.textsize(categories[2],font=font_categories)[0])
        draw.text(xy=(x_to_draw, 463), text=categories[2], align="center", font=font_categories, fill=('#252429'))

    """
    
    Summary Rating
    
    """

    w = int(math.ceil(draw.textsize(rating, font=font_rating)[0])) + 35
    rate_image = Image.open("images/profile/star.png")
    star_width = int((W - w)/2)
    width = (star_width, 560)
    profile_image.paste(im=rate_image, box=width, mask=rate_image)
    draw.text(xy=((W - w)/2 + 35, 558), text=rating, font=font_rating)

    """

    Last Online и Last in Work

    """

    last_online = get_last_online(id)
    draw.text(xy=(110, 730), text = last_online, font=font_dates, fill=("#252429"))

    draw.text(xy=(630, 730), text = last_in_work, font=font_dates, fill=("#252429"))

    path = f'photos/nontime/{randint(1111111111, 9999999999)}.png'
    profile_image.save(path, "PNG")
    return path


def check_first_touch(id, field):
    result = cur.execute("SELECT `{}` FROM `first_touch` WHERE `id` = '{}'".format(field, id)).fetchmany(1)
    if result[0][0] == '-':
        return True
    else:
        return False


def add_first_touch(id, field):
    cur.execute("UPDATE `first_touch` SET `{}` = '+' WHERE `id` = '{}'".format(field, id))
    con.commit()


def get_random_user_id():
    result = cur.execute("SELECT `id`, `select` FROM `users`").fetchall()
    i = 0
    while i == 0:
        num_user = randint(0, len(result)-1)
        if 'registration' in result[num_user][1]:
            pass
        else:
            user_id = result[num_user]
            i = 1
    return user_id[0]


def find_user_by_name(name, row):
    result = cur.execute("SELECT `name`, `id`, `select` FROM `users`").fetchall()
    i = 0
    for user in result:
        if 'registration' in user[2]:
            pass
        else:
            if name.lower() in user[0].lower():
                i += 1
                if i > row:
                    return user[1], i
    return 0, 0


def set_verification(id):
    with open(f"json/profile/{id}.json", "r") as file:
        content = json.load(file)
    content["verification"] = '+'
    with open(f"json/profile/{id}.json", "w") as file:
        file.write(json.dumps(content))


def check_verification(id):
    with open(f"json/profile/{id}.json", "r") as file:
        content = json.load(file)
    if content["verification"] == '+':
        return True
    else:
        return False
