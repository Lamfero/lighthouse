from main.models import Users, Orders, BankDetalis, Service, DiplomsSertificats, ProfileViews, UserSettings
import os
from pathlib import Path
from geopy import *
import json
from . import towns_list

doman_name = '127.0.0.1:8000'

def check_exist_user(telegram_id, secret_key):
    
    if Users.objects.filter(telegram_id = telegram_id, secret_key=secret_key).exists():
        db = Users.objects.get(telegram_id=telegram_id)
        if db.select != 'registration':
            return True
    return False


def check_exist_user_for_view(telegram_id):
    
    if Users.objects.filter(telegram_id = telegram_id).exists():
        db = Users.objects.get(telegram_id=telegram_id)
        if db.select != 'registration':
            return True
    return False


def get_user_rating(telegram_id):
    db = Users.objects.get(telegram_id=telegram_id)
    if Orders.objects.filter(employee = db).exists():
        orders = Orders.objects.filter(employee = db)
        positive_1 = 0
        negative_1 = 0
        for order in orders:
            if order.feedback_to_employee != None:
                if order.feedback_to_employee == 'positive':
                    positive_1 += 1
                elif order.feedback_to_employee == 'negative':
                    negative_1 += 1
                summary_rating_1 = positive_1 + negative_1
    if Orders.objects.filter(employee = db).exists():
        orders = Orders.objects.filter(employee = db)
        positive_2 = 0
        negative_2 = 0
        for order in orders:
            if order.feedback_to_employer != None:
                if order.feedback_to_employer == 'positive':
                    positive_2 += 1
                elif order.feedback_to_employer == 'negative':
                    negative_1 += 1
                summary_rating_2 = positive_2 + negative_2
        if positive_1 != 0 or positive_2 != 0:
            return round((positive_1 + positive_2)/(summary_rating_1 + summary_rating_2)*5, 2)
        elif negative_1 != 0 or negative_2 != 0:
            return 0
        else:
            return 5
    return 5


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
    portfolio = eval(db.portfolio)
    class userinfo():
        if db.name_surname != None:
            name_surname = db.name_surname
        
        if db.description != None:
            description = db.description

        img = db.img
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
        
        
    return userinfo


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


def get_enabled_card(telegram_id):
    db = Users.objects.get(telegram_id=telegram_id)
    if BankDetalis.objects.filter(user = db).exists():
        cards = BankDetalis.objects.filter(user = db)
        for card in cards:
                return card
    else:
        return None


def get_user_cards(telegram_id):
    db = Users.objects.get(telegram_id=telegram_id)
    if BankDetalis.objects.filter(user = db).exists():
        cards = BankDetalis.objects.filter(user = db)
        cards_array = []
        for card in cards:
            cards_array.append(f"{card.card_number[:4]} **** **** ****")
        return cards_array
    else:
        return None


def get_service_count(telegram_id):
    db = Users.objects.get(telegram_id=telegram_id)
    if Service.objects.filter(user = db).exists():
        service = Service.objects.filter(user = db)
        return len(service)
    else:
        return 0


def get_positive_and_negative_feedbacks(telegram_id):
    db = Users.objects.get(telegram_id=telegram_id)
    positive_1 = 0
    negative_1 = 0
    positive_2 = 0
    negative_2 = 0
    if Orders.objects.filter(employee = db).exists():
        orders = Orders.objects.filter(employee = db)
        for order in orders:
            if order.feedback_to_employee != None:
                if order.feedback_to_employee == 'positive':
                    positive_1 += 1
                elif order.feedback_to_employee == 'negative':
                    negative_1 += 1
    if Orders.objects.filter(employer = db).exists():
        orders = Orders.objects.filter(employer = db)
        for order in orders:
            if order.feedback_to_employer != None:
                if order.feedback_to_employer == 'positive':
                    positive_2 += 1
                elif order.feedback_to_employer == 'negative':
                    negative_1 += 1
    positive = positive_1 + positive_2
    negative = negative_1 + negative_2
    return positive, negative


def get_count_repeated_orders(telegram_id):
    db = Users.objects.get(telegram_id=telegram_id)
    if Orders.objects.filter(employee = db).exists():
        orders = Orders.objects.filter(employee = db)
        repeated_epmloyers = {}
        for order in orders:
            if str(order.employer.id) in repeated_epmloyers:
                repeated_epmloyers[f"{order.employer.id}"] = repeated_epmloyers[f"{order.employer.id}"] + 1
            else:
                repeated_epmloyers[f"{order.employer.id}"] = 1
        
        result = 0
        for repeated_epmloyer in repeated_epmloyers:
            if int(repeated_epmloyers[f"{repeated_epmloyer}"]) > 1:
                result += int(repeated_epmloyers[f"{repeated_epmloyer}"])
        return result
    else:
        return 0


def get_count_in_work_orders(telegram_id):
    db = Users.objects.get(telegram_id=telegram_id)
    if Orders.objects.filter(employee = db).exists():
        orders = Orders.objects.filter(employee = db)
        count_done_orders = 0
        for order in orders:
            if order.status == 'in work':
                count_done_orders += 1
        return count_done_orders 
    else:
        return 0


def get_count_done_orders(telegram_id):
    db = Users.objects.get(telegram_id=telegram_id)
    if Orders.objects.filter(employee = db).exists():
        orders = Orders.objects.filter(employee = db)
        count_done_orders = 0
        for order in orders:
            if order.status == 'done':
                count_done_orders += 1
        return count_done_orders 
    else:
        return 0


def get_count_canceled_orders(telegram_id):
    db = Users.objects.get(telegram_id=telegram_id)
    if Orders.objects.filter(employee = db).exists():
        orders = Orders.objects.filter(employee = db)
        count_done_orders = 0
        for order in orders:
            if order.status == 'cancel':
                count_done_orders += 1
        return count_done_orders 
    else:
        return 0


def get_diploms_and_sertificats_files(telegram_id):
    db = Users.objects.get(telegram_id=telegram_id)
    if DiplomsSertificats.objects.filter(user = db).exists():
        data = DiplomsSertificats.objects.filter(user = db)
        return data
    else:
        return None


def delete_service_photo(service_db):
    if service_db.image != '':
        path = f"{Path(__name__).resolve().parent}{service_db.image.url}".replace("\\", "/")
        os.remove(path)


def delete_diplom_photo(diplom_db):
    if diplom_db.img != '':
        path = f"{Path(__name__).resolve().parent}{diplom_db.img.url}".replace("\\", "/")
        os.remove(path)


def get_feedbacks_list(telegram_id):
    db = Users.objects.get(telegram_id=telegram_id)
    feedbacks = {}
    if Orders.objects.filter(employee = db).exists():
        orders = Orders.objects.filter(employee = db)
        for order in orders:
            if order.feedback_to_employee != None:
                feedbacks[f"{order.id}"] = [f"{order.employer.img.url}", f"{order.employer.telegram_id}", f"{order.employer.name_surname}", f"{order.feedback_to_employee}"]
    if Orders.objects.filter(employer = db).exists():
        orders = Orders.objects.filter(employer = db)
        
        for order in orders:
            if order.feedback_to_employer != None:
                feedbacks[f"{order.id}"] = [f"{order.employee.img.url}", f"{order.employee.telegram_id}", f"{order.employee.name_surname}", f"{order.feedback_to_employer}"]
    if feedbacks != {}:
        return feedbacks
        
    else:
        return None


def get_orders_complited_on_time(telegram_id):
    db = Users.objects.get(telegram_id=telegram_id)
    if Orders.objects.filter(employee = db).exists():
        orders = Orders.objects.filter(employee = db)
        completed_on_time_orders = 0
        for order in orders:
            if order.completed_on_time == 'True' and order.status == 'done':
                completed_on_time_orders += 1
        return completed_on_time_orders
    else:
        return 0


def get_info_about_user_service(telegram_id):
    db = Users.objects.get(telegram_id=telegram_id)
    if Service.objects.filter(user = db).exists():
        service = Service.objects.filter(user = db)
        return service

    else:
        return None


def set_view_by_user(telegram_id, view_telegram_id):
    db = Users.objects.get(telegram_id=telegram_id)
    db_profile = Users.objects.get(telegram_id=view_telegram_id)
    if ProfileViews.objects.filter(user_who_view = db, user_profile=db_profile).exists():
        pass
    else:
        view_db = ProfileViews(user_who_view = db, user_profile=db_profile)
        view_db.save()


def get_views_count(telegram_id):
    db = Users.objects.get(telegram_id=telegram_id)
    if ProfileViews.objects.filter(user_profile=db).exists():
        return len(ProfileViews.objects.filter(user_profile=db))
    else:
        return 0


def get_user_portfolio(telegram_id):
    db = Users.objects.get(telegram_id=telegram_id)
    portfolio = eval(db.portfolio)
    return portfolio


def get_user_settings_save_cards(telegram_id):
    db = Users.objects.get(telegram_id=telegram_id)
    usersettings_db = UserSettings.objects.get(user = db)
    return usersettings_db.save_cards


def update_user_settings_save_cards(telegram_id, data):
    db = Users.objects.get(telegram_id=telegram_id)
    usersettings_db = UserSettings.objects.get(user = db)
    usersettings_db.save_cards = data
    usersettings_db.save()


def get_userinfo_by_telegram_id_by_owner(telegram_id): #ЗАРЕГАННЫЙ ПРОФИЛЬ ПРОСМОТР СО СТОРОНЫ ВЛАДЕЛЬЦА (ВСЯ ЛИЧНАЯ ИНФОРМАЦИЯ)
    db = Users.objects.get(telegram_id=telegram_id)
    feedbacks = get_positive_and_negative_feedbacks(telegram_id)
    class userinfo():
        telegram_id = db.telegram_id
        share_url = f"{doman_name}/profile/{telegram_id}"
        name_surname = db.name_surname
        category = db.category
        rating = get_user_rating(telegram_id)
        status = db.status
        verification = db.verification
        if get_enabled_card(telegram_id) != None:
            card_number = f"{get_enabled_card(telegram_id).card_number[:4]} **** **** ****"
        else:
            card_number = ''
        if len(db.city) > 10:
            city = f'{db.city[:10]}...'
        else:
            city = db.city
        
        category = db.category

        if len(db.subcategories) > 10:
            subcategories = f'{db.subcategories[:10]}...'
        else:
            subcategories = db.subcategories
        
        if len(db.interests) > 10:
            interests = f'{db.interests[:10]}...'
        else:
            interests = db.interests
        
        if len(db.description) > 20:
            description = f'{str(db.description)[:20]}...'
        else:
            description = db.description
        
        service_count = get_service_count(telegram_id)

        positive_feedbacks = feedbacks[0]
        negative_feedbacks = feedbacks[1]

        orders_in_work = get_count_in_work_orders(telegram_id)
        orders_done = get_count_done_orders(telegram_id)
        repeated_orders = get_count_repeated_orders(telegram_id)
        completed_on_time_orders = get_orders_complited_on_time(telegram_id)
        orders_cancel = get_count_canceled_orders(telegram_id)
        profile_views = get_views_count(telegram_id=telegram_id)

        img = db.img
    return userinfo


def get_userinfo_by_telegram_id_from_outside(telegram_id): # ПРОСМОТР ПРОФИЛЯ СО СТОРОНЫ (ОГРАНИЦЕННАЯ ИНФОРМАЦИЯ)
    db = Users.objects.get(telegram_id=telegram_id)
    feedbacks = get_positive_and_negative_feedbacks(telegram_id)
    class userinfo():
        telegram_id = db.telegram_id
        share_url = f"{doman_name}/profile/{telegram_id}"
        name_surname = db.name_surname
        category = db.category
        rating = get_user_rating(telegram_id)
        status = db.status
        verification = db.verification
        
        description = db.description
        
        service_count = get_service_count(telegram_id)

        positive_feedbacks = feedbacks[0]
        negative_feedbacks = feedbacks[1]

        orders_done = get_count_done_orders(telegram_id)
        repeated_orders = get_count_repeated_orders(telegram_id)
        completed_on_time_orders = get_orders_complited_on_time(telegram_id)
        orders_cancel = get_count_canceled_orders(telegram_id)

        img = db.img

    return userinfo