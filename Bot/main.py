import sqlite3 as sql
import os
import time as t
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentType
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, message, BotCommandScopeChat, AllowedUpdates
from aiogram.utils import executor
from aiogram.types.web_app_info import WebAppInfo
from aiogram.dispatcher.filters.filters import FilterRecord
from asyncio import *

 

from reply_markup import *
from pyqiwip2p import QiwiP2P
from config import *
from funcs import *
from random import randint
import requests




token = token
PAYMENT_TOKEN = PAYMENT_TOKEN_TEST
bot = Bot(token=token)
dp = Dispatcher(bot)
# p2p = QiwiP2P(auth_key=PAYMENT_QIWI_TOKEN)
#1230154081
con = con = sql.connect('project.db', timeout=10)
cur = con.cursor()


@dp.message_handler(commands=['a'])
async def a(message: types.Message):
    id = message.from_user.id
    await bot.get_updates(allowed_updates=AllowedUpdates.MESSAGE + AllowedUpdates.EDITED_MESSAGE)
    await bot.delete_message(id, message.message_id)
    if id in [5236738540, 1230154081, 423479827]:
        cur.execute("UPDATE `users` SET `admin` = '2' WHERE `id` = '{}'".format(id))
        con.commit()
        await bot.send_message(message.from_user.id, "Статус Главный Администратор выдан выдан.", reply_markup=get_main_menu(id))


@dp.message_handler(commands=['project'])
async def project(message: types.Message):
    if message.chat.type == 'private':
        id = message.from_user.id
        menu = InlineKeyboardMarkup()
        site = InlineKeyboardButton(text="Сайтик", web_app=WebAppInfo(url="https://xn--80aue1f.online/creating_project?telegram_id=111111&secret_key=111111"))
        menu.add(site)
        await bot.send_message(id, "Тест", reply_markup=menu)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.chat.type == 'private':
        id = message.from_user.id
        username = message.from_user.username
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        subtext = message.text[7:]
        if check_exist_user(id):
            update_last_online(id)
            user_select = get_user_select(id)
            if subtext == '':
                if 'registration' in user_select:
                    await bot.delete_my_commands(BotCommandScopeChat(chat_id=id))
                    change_select(id, 'registration (start)')
                    menu = InlineKeyboardMarkup()
                    site = InlineKeyboardButton(text="Сайтик", web_app=WebAppInfo(url="https://xn--80aue1f.online/registration?telegram_id=111111&secret_key=111111"))
                    menu.add(site)
                    await bot.send_message(id, "Тест", reply_markup=menu)
                    await bot.send_message(message.from_user.id, f'Привет! В нашем боте Вы сможете создать, разместить в общем каталоге и прямо здесь же начать продавать билеты через интегрированную систему. Подробнее о работе бота Вы можете прочитать в разделах "FAQ" и "О нас".', reply_markup=menu)
                else:
                    await bot.set_my_commands([
                        types.BotCommand("profile", "Профиль"),
                        types.BotCommand("purse", "Кошелек"),
                        types.BotCommand("tariff", "Тарифы"),
                        types.BotCommand("ref_program", "Реф. прогр."),
                        ], BotCommandScopeChat(chat_id=id))
                    level_admin = check_admin_level(id)
                    if level_admin > 0:
                        
                        if level_admin == 1:
                            level_name = 'Администратор'
                            await bot.send_message(message.from_user.id, f'Привет {level_name}! В нашем боте Вы сможете создать, разместить в общем каталоге и прямо здесь же начать продавать билеты через интегрированную систему. Подробнее о работе бота Вы можете прочитать в разделах "FAQ" и "О нас".', reply_markup=get_main_menu(id))
                        elif level_admin == 2:
                            level_name = 'Главный Администратор'
                            await bot.send_message(message.from_user.id, f'Привет {level_name}! В нашем боте Вы сможете создать, разместить в общем каталоге и прямо здесь же начать продавать билеты через интегрированную систему. Подробнее о работе бота Вы можете прочитать в разделах "FAQ" и "О нас".', reply_markup=get_main_menu(id))
                    else:
                        await bot.send_message(message.from_user.id, 'Привет! В нашем боте Вы сможете создать, разместить в общем каталоге и прямо здесь же начать продавать билеты через интегрированную систему. Подробнее о работе бота Вы можете прочитать в разделах "FAQ" и "О нас".', reply_markup=get_main_menu(id))
            else:
                id_to_action = subtext
                if user_select == '':
                    pass
        else:
            await bot.delete_my_commands(BotCommandScopeChat(chat_id=id))
            add_user(id, username)
            secret_key = generate_secret_key(id)
            print(f'+ юзер {first_name}')
            if len(subtext) > 0:
                add_referal(id, subtext)
                
            change_select(id, 'registration (start)')
            await bot.send_message(message.from_user.id, f'МаякБот – это\n— Проекты\n— Задачи\n— Вопросы\nНаходи полезные знакомства, участвуй в творческих проектах или создавай их сам, решай разовые задачи бок о бок со специалистами!', reply_markup=start_menu)


@dp.message_handler(commands='profile')
async def profile(message: types.Message):
    if message.chat.type == 'private':
        id = message.from_user.id
        if check_exist_user(id):
            update_last_online(id)
            user_select = get_user_select(id)
            await bot.delete_message(id, message.message_id)
            if 'registration' in user_select:
                await bot.send_message(id, "Пройдите регистрацию")
            else:
                change_select(id, 'profile_menu')
                text = see_user_info_id(id)
                if len(text) > 0:
                    path = get_profile(id)
                    with open(path, "rb") as file:
                        await bot.send_photo(id, file, reply_markup=get_profile_menu(id))
                    os.remove(path)
                else:
                    await bot.send_message(id, 'Пользователь отсутствует.')
        else:
            await bot.send_message(id, "Введите /start")


@dp.message_handler(commands='purse')
async def purse(message: types.Message):
    if message.chat.type == 'private':
        id = message.from_user.id
        if check_exist_user(id):
            update_last_online(id)
            user_select = get_user_select(id)
            await bot.delete_message(id, message.message_id)
            if 'registration' in user_select:
                await bot.send_message(id, "Пройдите регистрацию")
            else:
                delete_select(id)
                await bot.send_message(id, '👛 Кошелек:', reply_markup=purse_menu)
        else:
            await bot.send_message(id, "Введите /start")


@dp.message_handler(commands='tariff')
async def tariff(message: types.Message):
    if message.chat.type == 'private':
        id = message.from_user.id
        if check_exist_user(id):
            update_last_online(id)
            user_select = get_user_select(id)
            await bot.delete_message(id, message.message_id)
            if 'registration' in user_select:
                await bot.send_message(id, "Пройдите регистрацию")
            else:
                delete_select(id)
                result = cur.execute("SELECT * FROM `tariff`").fetchall()
                tariff_menu = ReplyKeyboardMarkup(row_width=3)
                for tariff in result:
                    name = tariff[0]
                    tariff_button = KeyboardButton(text=f'🚀 Тариф {name}')
                    tariff_menu.add(tariff_button)
                tariff_menu.add(back_button)
                await bot.send_message(id, 'Тарифы:', reply_markup=tariff_menu)
        else:
            await bot.send_message(id, "Введите /start")


@dp.message_handler(commands='ref_program')
async def ref_program(message: types.Message):
    if message.chat.type == 'private':
        id = message.from_user.id
        if check_exist_user(id):
            update_last_online(id)
            user_select = get_user_select(id)
            await bot.delete_message(id, message.message_id)
            if 'registration' in user_select:
                await bot.send_message(id, "Пройдите регистрацию")
            else:
                await bot.send_message(id, "👨‍👦‍👦 Реф. прогр.", reply_markup=ref_menu)
                change_select(id, 'ref_menu')
        else:
            await bot.send_message(id, "Введите /start")


@dp.message_handler(commands='faq')
async def FAQ(message: types.Message):
    if message.chat.type == 'private':
        id = message.from_user.id
        if check_exist_user(id):
            update_last_online(id)
            user_select = get_user_select(id)
            await bot.delete_message(id, message.message_id)
            if 'registration' in user_select:
                await bot.send_message(id, "Пройдите регистрацию")
            else:
                delete_select(id)
                text = '🧐 FAQ\n\nЧастые вопросы:\nКонтакты:\n\nРазработчик:'
                await bot.send_message(id, text, reply_markup=back_to_main_menu)
        else:
            await bot.send_message(id, "Введите /start")


@dp.message_handler(commands='delete_me')
async def delete_me(message: types.Message):
    if message.chat.type == 'private':
        id = message.from_user.id
        if check_exist_user(id):
            delete_user(id)
            await bot.send_message(id, 'Успешно')


@dp.callback_query_handler(text_contains='see_user_info_')
async def see_user_info(callback: types.CallbackQuery):
    if message.chat.type == 'private':
        id = callback.from_user.id
        uid = callback.data[14:]
        if check_admin_level(id, 2):
            update_last_online(id)
            text = see_user_info_id(uid)
            if len(text) > 0:
                await bot.send_message(id, f'{text}')
            else:
                await bot.send_message(id, 'Пользователь отсутствует')


@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message: types. Message):
    id = message.from_user.id
    if 'buy_' in message.successful_payment.invoice_payload:
        sum = int(message.successful_payment.invoice_payload[4:])
        await bot.send_message(id, f"Баланс пополнен на {sum}₽")
        update_balance(id, sum)
        add_action_at_payments_log(id, sum, "replenish", 'Пополнение баланса.')



    """"
    
    <!DOCTYPE html>
    <html>
    <body>

    <iframe width="420" height="345" src="https://www.youtube.com/embed/tgbNymZ7vqY">
    </iframe>

    </body>
    </html>


    """


@dp.message_handler(content_types=['photo'])
async def photo(message: types.Message):
    if message.chat.type == 'private':
        id = message.from_user.id
        if check_exist_user(id):
            update_last_online(id)
            user_select = get_user_select(id)
            # if 'registration' in user_select:
            #     if user_select == 'registration (enter photo)':
            #         await message.photo[-1].download(destination_file= f"photos/profile/{id}.png")
            #         change_select(id, 'registration')
            #         path = get_registration_avatar_image(id)
            #         with open(path, "rb") as file:
            #             await bot.send_photo(message.from_user.id, file)
            #         os.remove(path)
            #         answer = f'Профиль:\n\n{get_json_user_field(id, "name_surname")}\nВозраст:{get_age_by_date(get_json_user_field(id, "date_birth"))}\nГород:{get_json_user_field(id, "city")}\nОсновные категории:{get_json_user_field(id, "main_category_1")} {get_json_user_field(id, "main_category_2")} {get_json_user_field(id, "main_category_3")}\nОписание:{get_json_user_field(id, "description")}\nИнтересы:{get_json_user_field(id, "interests")}'
            #         await bot.send_message(id, f"Так выглядит Ваша анкета.\n\n{answer}\n\n Желаете что-то изменить?", reply_markup=edit_profile_menu)
            if user_select == 'edit_item_profile_menu_photo':
                delete_select(id)
                if check_verification(id):
                    if os.path.exists(f"photos/for_profile_moderation/{id}.png"):
                        await bot.send_message(id, 'У вас уже есть заявка на смену аватара.')
                    else:
                        set_moderation_for_profile(id, 'photo')
                        await message.photo[-1].download(destination_file= f"photos/for_profile_moderation/{id}.png")
                        await bot.send_message(id, 'Вы успешно добавили заявку на смену аватара.', reply_markup=get_main_menu(id))
                else:
                    await message.photo[-1].download(destination_file= f"photos/profile/{id}.png")
                    await bot.send_message(id, 'Вы успешно сменили аватар.', reply_markup=get_main_menu(id))
            elif user_select == 'create_project_media':
                add_media_in_project_sample(id, 'photo')
                path = get_path_for_media_in_project_sample(id, 'photo')
                await message.photo[-1].download(destination_file = path)
                with open(f"json/creating_project/{id}.json", "r") as file:
                    structure = json.load(file)
                    file.close()
                len_array = len(structure["project_media"])
                if len_array == 5:
                    change_select(id, "create_project_final_step")
                    await bot.send_message(id, get_project_about_sample(id), reply_markup=ending_creating_project_menu)
                    photos = get_photo_from_project_sample(id)
                    if photos != 0:
                        for photo in photos:
                            with open(f"photos/creating_project/{photo}.png", "rb") as file:
                                await bot.send_photo(id, file)
                    video_menu = get_video_from_project_sample(id)
                    if video_menu != None:
                        await bot.send_message(id, "Видео:", reply_markup=video_menu)
                else:
                    await bot.send_message(id, f"Отправте еще фото/видео")
                    
            elif user_select == 'create_question_add_photo_file_1' or user_select == 'create_question_add_photo_file_2' or user_select == 'create_question_add_photo_file_3':
                if user_select == 'create_question_add_photo_file_1':
                    change_select(id, 'create_question_add_photo_file_2')
                    add_info_in_creating_question(id, 'photo_1', '+')
                    await message.photo[-1].download(destination_file= f"photos/creating_question/{id}_1.png")
                elif user_select == 'create_question_add_photo_file_2':
                    change_select(id, 'create_question_add_photo_file_3')
                    add_info_in_creating_question(id, 'photo_2', '+')
                    await message.photo[-1].download(destination_file= f"photos/creating_question/{id}_2.png")
                elif user_select == 'create_question_add_photo_file_3':
                    change_select(id, 'create_question_add_video_file')
                    add_info_in_creating_question(id, 'photo_3', '+')
                    await message.photo[-1].download(destination_file= f"photos/creating_question/{id}_3.png")
        else:
            await bot.send_message(id, "Введите /start")


@dp.message_handler(content_types='location')
async def location(message: types.Message):
    if message.chat.type == 'private':
        id = message.from_user.id
        if check_exist_user(id):
            update_last_online(id)
            user_select = get_user_select(id)
            coord = message.location
            if user_select == 'registration (enter city)':
                coord = str(coord["latitude"]) + ', ' + str(coord["longitude"])
                city = get_city_by_coods(coord)
                add_json_user_info(id, 'city', city)
                change_select(id, 'registration (enter main_category_1)')
                path = get_registration_location_image(city)
                with open(path, "rb") as file:
                    await bot.send_photo(id, file, reply_markup=select_category_for_profile)
                with open("images/registration/enter_main_categories.png", "rb") as file:
                    await bot.send_photo(id, file, reply_markup=select_category_for_profile)
                os.remove(path)
            elif user_select == 'create_project_geo':
                coord = str(coord["latitude"]) + ', ' + str(coord["longitude"])
                city = get_city_by_coods(coord)
                change_select(id, 'create_project_category')
                add_info_in_project_sample(id, 'project_city', city)
                await bot.send_message(id, f"Вы выбрали город {city}.\nВыберите категорию проекта", reply_markup=select_category_for_project)
        else:
            await bot.send_message(id, "Введите /start")


@dp.message_handler(content_types=['text'])
async def text(message: types.Message):
    if message.chat.type == 'private':
        id = message.from_user.id
        username = message.from_user.username
        msg = str(message.text)
        if check_exist_user(id):
            user_select = get_user_select(id)
            print(f'Уникальный индетификатор: {id} Время: {datetime.datetime.today().time().hour}:{datetime.datetime.today().time().minute} Шаг: {user_select}')
            update_last_online(id) 
            
            print(f'Уникальный индетификатор: {id} Время: {datetime.datetime.today().time().hour}:{datetime.datetime.today().time().minute} Шаг: {user_select}')
            if 'registration' in user_select:
                await bot.send_message(id, "Пройдите регистрацию", reply_markup=registration_site_menu)
            #     if msg == 'Начать':
            #         if user_select == 'registration (start)':
            #             change_select(id, 'registration (i_read)')
            #             with open("images/registration/terms_of_use.png", "rb") as file:
            #                 photo = file
            #                 await bot.send_photo(id, photo, reply_markup=i_read_menu)
            #             await bot.send_message(id, "1)\n2)\n3)")
            #     elif msg == 'Понятно':
            #         if user_select == 'registration (start input)':
            #             change_select(id, 'registration (enter name_surname)')
            #             with open("images/registration/name_surname.png", "rb") as file:
            #                 await bot.send_photo(id, file, reply_markup=remove_reply_keyboard)
            #     elif msg == 'Назад':
            #         await bot.delete_message(id, message.message_id)
            #         if user_select == 'registration (enter city)':
            #             change_select(id, 'registration (enter date_birth)')
            #             with open("images/registration/date_birth.png", "rb") as file:
            #                 await bot.send_photo(id, file, reply_markup=registration_menu)
                                
            #         elif user_select == 'registration (enter main_category_1)':
            #             change_select(id, 'registration (enter city)')
            #             with open("images/registration/your_city.png", "rb") as file:
            #                 await bot.send_photo(id, file, reply_markup=registration_menu)
                        
            #         elif user_select == 'registration (enter main_category_2)':
            #             change_select(id, 'registration (enter main_category_1)')
            #             add_json_user_info(id, 'main_category_1', '')
            #             add_json_user_info(id, 'main_category_2', '')
            #             add_json_user_info(id, 'main_category_3', '')
            #             with open("images/registration/enter_main_categories.png", "rb") as file:
            #                 await bot.send_photo(id, file, reply_markup=select_category_for_profile)
            #         elif user_select == 'registration (enter main_category_3)':
            #             change_select(id, 'registration (enter main_category_2)')
            #             add_json_user_info(id, 'main_category_3', '')
            #             add_json_user_info(id, 'main_category_2', '')
            #             path = get_registration_main_catigories_image(id)
            #             with open(path, "rb") as file:
            #                 await bot.send_photo(id, file, reply_markup=select_category_for_profile)
            #             os.remove(path)

            #         elif user_select == 'registration (enter photo)':
            #             change_select(id, 'registration (enter description)')
            #             with open("images/registration/your_description.png", "rb") as file:
            #                 await bot.send_photo(id, file, reply_markup=registration_menu)
            #         elif user_select == 'registration (enter interest)':
            #             change_select(id, 'registration (enter main_category_3)')
            #             add_json_user_info(id, 'main_category_3', '')
            #             path = get_registration_main_catigories_image(id)
            #             with open(path, "rb") as file:
            #                 await bot.send_photo(id, file, reply_markup=select_category_for_profile)
            #             os.remove(path)
            #         elif user_select == 'registration (enter description)':
            #             change_select(id, 'registration (enter interest)')
            #             add_json_user_info(id, 'interests', '')
            #             with open('images/registration/enter_interests.png', "rb") as file:
            #                 await bot.send_photo(id, file, reply_markup=select_category_for_profile)
            #         elif user_select == 'registration (enter date_birth)':
            #             change_select(id, 'registration (enter name_surname)')
            #             await bot.send_message(id, "Введите Имя и Фамилию.", reply_markup=remove_reply_keyboard)
                
            #     elif msg == 'Далее':
            #         await bot.delete_message(id, message.message_id)
            #         if user_select == 'registration (enter main_category_1)':
            #             with open("images/registration/enter_main_categories.png", "rb") as file:
            #                 await bot.send_photo(id, file, reply_markup=select_category_for_profile)
            #         elif user_select == 'registration (enter main_category_2)':
            #             add_json_user_info(id, 'main_category_2', '')
            #             change_select(id, 'registration (enter interest)')
            #             with open("images/registration/enter_interests.png", "rb") as file:
            #                 await bot.send_photo(id, file, reply_markup=select_category_for_profile)
            #         elif user_select == 'registration (enter main_category_3)':
            #             change_select(id, 'registration (enter interest)')
            #             with open("images/registration/enter_interests.png", "rb") as file:
            #                 await bot.send_photo(id, file, reply_markup=select_category_for_profile)
            #         elif user_select == 'registration (enter interest)':
                        
            #             interests = check_user_interests(id)
            #             array = interests.rsplit("  ")
            #             if len(array)-1 > 0:
            #                 change_select(id, 'registration (enter description)')
            #                 with open("images/registration/your_description.png", "rb") as file:
            #                     await bot.send_photo(id, file, reply_markup=registration_menu)
            #             else:
            #                 await bot.send_message(id, 'Выберите от одной категории интересов.')
            #         else:
            #             await bot.send_message(id, "Этот пункт пропустить нельзя.")
            #     elif user_select == 'registration (i_read)':
            #         if msg == 'Согласен с условиями':
            #             change_select(id, 'registration (start input)')
            #             with open("images/registration/start_input.png", "rb") as file:
            #                 await bot.send_photo(id, file, reply_markup=understand_menu)
                        
            #     elif user_select == 'registration (enter main_category_1)' or user_select == 'registration (enter main_category_2)' or user_select == 'registration (enter main_category_3)' or user_select == 'registration (enter interest)':
            #         if check_category(msg):
            #             category = msg
            #             await bot.delete_message(id, message.message_id)
            #             if user_select == 'registration (enter main_category_1)':
            #                 change_select(id, 'registration (enter main_category_2)')
            #                 add_json_user_info(id, 'main_category_1', category)
            #                 path = get_registration_main_catigories_image(id)
            #                 with open(path, "rb") as file:
            #                     await bot.send_photo(id, file, reply_markup=select_category_for_profile)
            #                 os.remove(path)
            #             elif user_select == 'registration (enter main_category_2)':
            #                 if get_json_user_field(id, 'main_category_1') == msg:
            #                     await bot.send_message(id, 'Эту категорию вы уже выбирали для данного пункта')
            #                 else:
            #                     change_select(id, 'registration (enter main_category_3)')
            #                     add_json_user_info(id, 'main_category_2', category)
            #                     path = get_registration_main_catigories_image(id)
            #                     with open(path, "rb") as file:
            #                         await bot.send_photo(id, file, reply_markup=select_category_for_profile)
            #                     os.remove(path)
            #             elif user_select == 'registration (enter main_category_3)':
            #                 if get_json_user_field(id, 'main_category_1') == msg or get_json_user_field(id, 'main_category_2') == msg:
            #                     await bot.send_message(id, 'Эту категорию вы уже выбирали для данного пункта')
            #                 else:
            #                     add_json_user_info(id, 'main_category_3', category)
            #                     change_select(id, 'registration (enter interest)')
            #                     path = get_registration_main_catigories_final_image(id)
            #                     with open(path, "rb") as file:
            #                         await bot.send_photo(id, file, reply_markup=select_category_for_profile)
            #                     with open("images/registration/enter_interests.png", "rb") as file:
            #                         await bot.send_photo(id, file, reply_markup=select_category_for_profile)
            #                     os.remove(path)
            #             elif user_select == 'registration (enter interest)':
            #                 interests = check_user_interests(id)
            #                 array = interests.rsplit("  ")
            #                 if len(array) <= 7:
            #                     if check_interests_original(array, category):
            #                         if len(array) == 6:
            #                             if interests == '':
            #                                 interests = category
            #                             else:
            #                                 interests = interests + '  ' + category
            #                             add_json_user_info(id, 'interests', interests)
                                        
            #                             change_select(id, 'registration (enter description)')

            #                             path = get_registration_interests_final_image(id)
            #                             with open(path, "rb") as file:
            #                                 await bot.send_photo(id, file, reply_markup=select_category_for_profile)
            #                             os.remove(path)

            #                             with open("images/registration/your_description.png", "rb") as file:
            #                                 await bot.send_photo(id, file, reply_markup=registration_menu)
            #                         else:
            #                             if interests == '':
            #                                 interests = category
            #                             else:
            #                                 interests = interests + '  ' + category
            #                             add_json_user_info(id, 'interests', interests)
            #                             path = get_registration_interests_image(id)
            #                             with open(path, "rb") as file:
            #                                 await bot.send_photo(id, file, reply_markup=select_category_for_profile)
            #                             os.remove(path)
            #                     else:
            #                         await bot.send_message(id, 'Вы уже выбирали данную категорию.')
            #     elif user_select == 'registration':
            #         if msg == 'Создать заново':
            #             change_select(id, 'registration (i_read)')
            #             with open("images/registration/terms_of_use.png", "rb") as file:
            #                 photo = file
            #                 await bot.send_photo(id, photo, reply_markup=i_read_menu)
            #             await bot.send_message(id, "1)\n2)\n3)")
            #         elif msg == 'Поменять описание':
            #             user_select = get_user_select(id)
            #             change_select(id, 'registration (edit description)')
            #             await bot.send_message(id, f"Расскажите немного о себе:\nКакой у Вас опыт? Что хотите найти? Какие можете подметить в себе полезные качества?", reply_markup=registration_menu)
            #         elif msg == 'Подтвердить':
            #             await bot.set_my_commands([
            #             types.BotCommand("profile", "Профиль"),
            #             types.BotCommand("purse", "Кошелек"),
            #             types.BotCommand("tariff", "Тарифы"),
            #             types.BotCommand("ref_program", "Реф. прогр."),
            #             types.BotCommand("faq", "FAQ"),
            #             ], BotCommandScopeChat(chat_id=id))
            #             user_select = get_user_select(id)
            #             change_select(id, '')
            #             end_registration(id)
            #             await bot.send_message(id, 'Отлично! Статус Вашего аккаунта – базовый.Для того, чтобы получить статус "Верифицирован", пройдите в раздел "Профиль" через левое Меню. Это поможет Вам получать больше откликов и поспособствует комфортному взаимодействию внутри сервиса.Нажмите на пункты меню, чтобы получить краткую информацию по всему функционалу сервиса. Если у Вас будут вопросы или Вы забудете, где расположены определенные функции, перейдите в раздел FAQ в Левом Меню.', reply_markup=get_main_menu(id))
            #         else:
            #             await bot.send_message(id, 'Выберите нужный пункт на клавиатуре.')
            #     else:
            #         if user_select == 'registration (enter name_surname)':
            #             if len(msg) < 35:
            #                 n_words = len(re.split(' |-', msg))
            #                 if n_words > 1 and n_words <= 5:
            #                     if check_name_surname(msg):
            #                         name_surname = msg
            #                         add_json_user(id, name_surname)
            #                         change_select(id, 'registration (enter date_birth)')
            #                         path = get_registration_name_image(name_surname)
            #                         with open(path, "rb") as file:
            #                             await bot.send_photo(id, file, reply_markup=next_and_back_menu)
            #                         os.remove(path)
            #                         with open("images/registration/date_birth.png", "rb") as file:
            #                             await bot.send_photo(id, file, reply_markup=registration_menu)
            #                     else:
            #                         await bot.send_message(id, "Введите верное Имя и Фамилию.")
            #                 else:
            #                     await bot.send_message(id, 'Введите верное Имя и Фамилию. До 35 символов. Разрешено использовать "-"')
            #         elif user_select == 'registration (enter date_birth)':
            #             if len(msg) == 10:
            #                 date = msg
            #                 splited_date = date.rsplit(".")
            #                 if msg == '00.00.0000' or splited_date[0] == '00' or splited_date[1] == '00' or splited_date[2] == '0000':
            #                     await bot.send_message(id, '☦   ☦   ☦   ☦')
            #                 else:
            #                     if check_valid_date(date):
            #                         add_json_user_info(id, 'date_birth', date)
            #                         if check_age_by_date(date):
            #                             with open("images/registration/your_city.png", "rb") as file:
            #                                 await bot.send_photo(id, file, reply_markup=registration_menu)
            #                             change_select(id, 'registration (enter city)')
            #                         else:
            #                             await bot.send_message(id, f'Ваш возраст не соответствует необходимому.')
            #                     else:
            #                         await bot.send_message(id, 'Что-то пошло не так. Укажите правильную дату: день, месяц, год в формате ДД.ММ.ГГГГ')
            #             else:
            #                 await bot.send_message(id, 'Что-то пошло не так. Укажите правильную дату: день, месяц, год в формате ДД.ММ.ГГГГ')
            #         elif user_select == 'registration (enter description)':
            #             if len(msg) < 300:
            #                 add_json_user_info(id, 'description', msg)
            #                 change_select(id, 'registration (enter photo)')
            #                 await bot.send_message(id, f'Отправьте фото профиля.', reply_markup=registration_menu)
            #             else:
            #                 await bot.send_message(id, 'Что-то пошло не так. Лимит описания профиля: 300 символов.')
            #         elif user_select == 'registration (edit description)':
            #             if len(msg) < 300:
            #                 add_json_user_info(id, 'description', msg)
            #                 change_select(id, 'registration')
            #                 path = get_registration_avatar_image(id)
            #                 with open(path, "rb") as file:
            #                     await bot.send_photo(message.from_user.id, file)
            #                 os.remove(path)
            #                 answer = f'Профиль:\n\n{get_json_user_field(id, "name_surname")}\nВозраст:{get_age_by_date(get_json_user_field(id, "date_birth"))}\nГород:{get_json_user_field(id, "city")}\nОсновные категории:{get_json_user_field(id, "main_category_1")} {get_json_user_field(id, "main_category_2")} {get_json_user_field(id, "main_category_3")}\nОписание:{get_json_user_field(id, "description")}\nИнтересы:{get_json_user_field(id, "interests")}'
            #                 await bot.send_message(id, f"Так выглядит Ваша анкета.\n\n{answer}\n\n Желаете что-то изменить?", reply_markup=edit_profile_menu)
            #             else:
            #                 await bot.send_message(id, 'Что-то пошло не так. Лимит описания профиля: 300 символов.')
            else:
                if msg == '👨‍💼 Админ панель':
                    await bot.delete_message(id, message.message_id)
                    level = check_admin_level(id)
                    print(level)
                    if level == 1:
                        change_select(id, "admin_panel")
                        await bot.send_message(message.from_user.id, 'Панель Администратора.', reply_markup=admin_panel_1_menu)
                    elif level == 2:
                        change_select(id, "admin_panel")
                        await bot.send_message(message.from_user.id, 'Панель Главного Администратора.', reply_markup=admin_panel_2_menu)
                elif msg == 'Вернуться в главное меню':
                    change_select(id, 'main_menu')
                    await bot.send_message(id , 'Главное меню:', reply_markup=get_main_menu(id))
                elif msg == 'Назад':
                    if 'balance_menu_' in user_select:
                        delete_select(id)
                        await bot.delete_message(id, message.message_id)
                        await bot.send_message(id, '👛 Кошелек:', reply_markup=purse_menu)
                    elif user_select == 'balance_menu_payments_log_replenish':
                        delete_select(id)
                        await bot.delete_message(id, message.message_id)
                        await bot.send_message(id, 'Движение средств:\nВыберите пункт.', reply_markup=purse_log_menu)
                    elif user_select == 'ref_menu' or user_select == 'profile_menu':
                        delete_select(id)
                        await bot.delete_message(id, message.message_id)
                        await bot.send_message(id, 'Главное меню:', reply_markup=get_main_menu(id))
                    elif user_select == 'ref_menu_link':
                        change_select(id, 'ref_menu')
                        await bot.delete_message(id, message.message_id)
                        await bot.send_message(id, '👨‍👦‍👦 Реф. прогр.', reply_markup=ref_menu)
                    elif user_select == 'ref_menu_appruf':
                        change_select(id, 'ref_menu')
                        await bot.delete_message(id, message.message_id)
                        await bot.send_message(id, '👨‍👦‍👦 Реф. прогр.', reply_markup=ref_menu)
                    elif user_select == 'ref_menu_in_hold':
                        change_select(id, 'ref_menu')
                        await bot.delete_message(id, message.message_id)
                        await bot.send_message(id, '👨‍👦‍👦 Реф. прогр.', reply_markup=ref_menu)
                    elif user_select == 'ref-menu_terms':
                        change_select(id, 'ref_menu')
                        await bot.delete_message(id, message.message_id)
                        await bot.send_message(id, '👨‍👦‍👦 Реф. прогр.', reply_markup=ref_menu)
                    elif user_select == 'watching_tariff':
                        delete_select(id)
                        result = cur.execute("SELECT * FROM `tariff`").fetchall()
                        tariff_menu = ReplyKeyboardMarkup(row_width=3)
                        for tariff in result:
                            name = tariff[0]
                            tariff_button = KeyboardButton(text=f'🚀 Тариф {name}')
                            tariff_menu.add(tariff_button)
                        tariff_menu.add(back_button)
                        await bot.send_message(id, 'Тарифы:', reply_markup=tariff_menu)
                    elif user_select == 'edit_profile_menu' or user_select == 'notifications_profile_menu' or user_select == 'verification_profile_menu':
                        change_select(id, 'profile_menu')
                        text = see_user_info_id(id)
                        if len(text) > 0:
                            path = get_profile(id)
                            with open(path, "rb") as file:
                                await bot.send_photo(id, file, reply_markup=get_profile_menu(id))
                            os.remove(path)
                        else:
                            await bot.send_message(id, 'Пользователь отсутствует.')
                    elif 'edit_item_profile_menu_' in user_select:
                        change_select(id, 'edit_profile_menu')
                        await bot.send_message(id, 'Выберите пункт для редактирования.', reply_markup=edit_profile_item_menu)
                    elif user_select == 'edit_item_profile_menu_category_profile':
                        delete_select(id)
                        await bot.send_message(id, 'Главное меню:', reply_markup=get_main_menu(id))
                    elif user_select == 'edit_item_profile_menu_category_profile_2':
                        change_select(id, 'edit_item_profile_menu_category_profile')
                        await bot.send_message(id, 'Выберите новые категории профиля.', reply_markup=select_category_for_profile)
                    elif user_select == 'edit_item_profile_menu_category_profile_3':
                        change_select(id, 'edit_item_profile_menu_category_profile')
                        await bot.send_message(id, 'Выберите новые категории профиля.', reply_markup=select_category_for_profile)
                    
                    elif 'create_project_' in user_select:                                                          #НАЗАД В СОЗДАНИИ ПРОЕКТА
                        if user_select == 'create_project_name':
                            change_select(id, "create")
                            await bot.send_message(id, 'Что необходимо создать?', reply_markup=create_menu)
                        
                        elif user_select == 'create_project_description':
                            change_select(id, "create_project_name")
                            await bot.send_message(id, "Введите название проекта", reply_markup=next_and_back_and_back_to_main_menu_menu)
                        
                        elif user_select == 'create_project_type':
                            change_select(id, "create_project_description")
                            await bot.send_message(id, "Введите описание проекта", reply_markup=next_and_back_and_back_to_main_menu_menu)
                        
                        elif user_select == 'create_project_category' or user_select == "create_project_geo":
                            change_select(id, "create_project_type")
                            await bot.send_message(id, "Выберите тип проекта", reply_markup=create_project_type_menu)

                        elif user_select == 'create_project_subcategories': 
                            change_select(id, "create_project_category")
                            await bot.send_message(id, "Выберите категорию проекта", reply_markup=select_category_for_project)
                        
                        elif user_select == 'create_project_need_categories':
                            with open(f"json/creating_project/{id}.json", "r") as file:
                                content = json.load(file)
                            content["project_subcategories"] = ''
                            with open(f"json/creating_project/{id}.json", "w") as file:
                                file.write(json.dumps(content))
                            change_select(id, "create_project_subcategories")
                            await bot.send_message(id, "Выберите подкатегории проекта", reply_markup=select_category_for_project)
                                
                        elif user_select == 'create_project_price' or user_select == 'create_project_price_fixed' or user_select == 'create_project_price_intermediate':
                            with open(f"json/creating_project/{id}.json", "r") as file:
                                content = json.load(file)
                            content["project_need_categories"] = ''
                            with open(f"json/creating_project/{id}.json", "w") as file:
                                file.write(json.dumps(content))
                            change_select(id, "create_project_need_categories")
                            await bot.send_message(id, "Выберите категории исполнителя", reply_markup=select_type_for_need_categories_of_project)

                        elif user_select == 'create_project_media':
                            change_select(id, "create_project_price")
                            await bot.send_message(id, "Выберите вознаграждение", reply_markup=select_type_of_payment_for_project)
                        
                        elif user_select == 'create_project_final_step':
                            change_select(id, "create_project_media")
                            await bot.send_message(id, "Отправте до 5 фото/видео\nВидео необходимо отправить в виде ссылки на видеохостинг YouTube.com", reply_markup=next_and_back_and_back_to_main_menu_menu)

                    elif 'warn_project_' in user_select:
                        project_id = user_select[13:]
                        change_select(id, f'action_with_project_{project_id}')
                        await bot.send_message(id, get_project_as_text(project_id), reply_markup=project_menu_in_find)
                    

                    elif 'create_question_' in user_select:
                        if user_select == 'create_question_text':
                            change_select(id, 'create_question_category_1')
                        elif user_select == 'create_question_add_photo_file_1' or user_select == 'create_question_add_photo_file_2' or user_select == 'create_question_add_photo_file_3':
                            change_select(id, 'create_question_text')
                            if os.path.exists(f"photos/creating_question/{id}_1"):
                                os.remove(f"photos/creating_question/{id}_1")
                            add_info_in_creating_question(id, 'photo_1', '-')
                            if os.path.exists(f"photos/creating_question/{id}_2"):
                                os.remove(f"photos/creating_question/{id}_2")
                            add_info_in_creating_question(id, 'photo_2', '-')
                            if os.path.exists(f"photos/creating_question/{id}_3"):
                                os.remove(f"photos/creating_question/{id}_3")
                            await bot.send_message(id, "Введите вопрос.", reply_markup=next_and_back_menu)
                        
                    else:
                        delete_select(id)
                        await bot.delete_message(id, message.message_id)
                        await bot.send_message(id, 'Главное меню:', reply_markup=get_main_menu(id))
                elif msg == 'Далее':
                    await bot.delete_message(id, message.message_id)
                    if user_select == 'edit_item_profile_menu_category_profile_2':
                        add_json_user_info(id, 'main_category_2', '')
                        add_json_user_info(id, 'main_category_3', '')
                        change_select(id, '')
                        await bot.send_message(id, f'Главное меню:', reply_markup=get_main_menu(id))
                    elif user_select == 'edit_item_profile_menu_category_profile_3':
                        add_json_user_info(id, 'main_category_3', '')
                        change_select(id, '')
                        await bot.send_message(id, f'Главное меню:', reply_markup=get_main_menu(id))
                    elif user_select == 'find_user_in_general_catalog':
                        random_id = get_random_user_id()
                        path = get_profile(random_id)
                        with open(path, "rb") as file:
                            await bot.send_photo(id, file, reply_markup=see_finding_user_profile)
                        os.remove(path)
                    elif 'find_user_by_name_' in user_select:
                        row = int(user_select[18:])
                        if len(msg) >= 3 <= 35:
                            name = get_choice_data(id)
                            n_words = len(re.split(' |-', name))
                            if n_words > 1 and n_words <= 5:
                                name = msg
                                result = find_user_by_name(name, row)
                                if result[0] != 0:
                                    change_select(id, f"find_user_by_name_{result[1]}")
                                    path = get_profile(result[0])
                                    with open(path, "rb") as file:
                                        await bot.send_photo(id, file, reply_markup=next_and_back_to_main_menu_menu)
                                    os.remove(path)
                                else:
                                    await bot.send_message(id, "Пользователей по таким фильтрам больше нет.", reply_markup=back_to_main_menu)
                            else:
                                await bot.send_message(id, "Введите корректные Имя Фамилию")
                        else:
                            await bot.send_message(id, "Введите корректные Имя Фамилию")
                    elif 'create_project_' in user_select:                                                          #ДАЛЕЕ В СОЗДАНИИ ПРОЕКТА
                        if user_select == 'create_project_name':
                            if check_exists_field_of_project_sample(id, "project_name"):
                                change_select(id, "create_project_description")
                                await bot.send_message(id, "Введите описание проекта", reply_markup=next_and_back_and_back_to_main_menu_menu)
                            else:
                                await bot.send_message(id, "Вы еще не заполняли данный пункт\n\nВведите название проекта", reply_markup=next_and_back_and_back_to_main_menu_menu)
                        
                        elif user_select == 'create_project_description':
                            if check_exists_field_of_project_sample(id, "project_description"):
                                change_select(id, "create_project_type")
                                await bot.send_message(id, 'Выберите тип проекта', reply_markup=create_project_type_menu)
                            else:
                                await bot.send_message(id, "Вы еще не заполняли данный пункт\n\nВведите описание проекта", reply_markup=next_and_back_and_back_to_main_menu_menu)
                        
                        elif user_select == 'create_project_type':
                            if check_exists_field_of_project_sample(id, "project_type"):
                                change_select(id, "create_project_category")
                                await bot.send_message(id, "Выберите категорию проекта", reply_makup=select_category_for_project)
                            else:
                                await bot.send_message(id, "Вы еще не заполняли данный пункт\n\nВыберите тип проекта", reply_markup=create_project_type_menu)


                        elif user_select == 'create_project_subcategories': 
                            with open(f"json/creating_project/{id}.json", "r") as file:
                                content = json.load(file)
                            if len(content["project_subcategories"].rsplit("  ")) > 0:
                                with open(f"json/creating_project/{id}.json", "r") as file:
                                    content = json.load(file)
                                content["project_need_categories"] = ''
                                with open(f"json/creating_project/{id}.json", "w") as file:
                                    file.write(json.dumps(content))
                                change_select(id, "create_project_need_categories")
                                await bot.send_message(id, "Выберите категории исполнителя", reply_markup=select_type_for_need_categories_of_project)
                            else:
                                await bot.send_message(id, "Необходимо выбрать от одной подкатегории проекта", reply_markup=select_category_for_project)
                        
                        elif user_select == 'create_project_need_categories':
                            with open(f"json/creating_project/{id}.json", "r") as file:
                                content = json.load(file)
                            if len(content["project_need_categories"].rsplit("  ")) > 0:
                                change_select(id, "create_project_price")
                                await bot.send_message(id, "Выберите вознаграждение", reply_markup=select_type_of_payment_for_project)
                            else:
                                await bot.send_message(id, "Необходимо выбрать от одной категории исполнителя", reply_markup=select_type_for_need_categories_of_project)
                                
                        elif user_select == 'create_project_price' or user_select == 'create_project_price_fixed' or user_select == 'create_project_price_intermediate':
                            if check_exists_field_of_project_sample(id, "project_price"):
                                change_select(id, "create_project_media")
                                await bot.send_message(id, "Отправте до 5 фото/видео\nВидео необходимо отправить в виде ссылки на видеохостинг YouTube.com", reply_markup=next_and_back_and_back_to_main_menu_menu)
                            else:
                                await bot.send_message(id, "Вы еще не заполняли данный пункт\n\nВыберите вознаграждение", reply_markup=select_type_of_payment_for_project)

                        elif user_select == 'create_project_media':
                            change_select(id, "create_project_final_step")
                            await bot.send_message(id, get_project_about_sample(id), reply_markup=ending_creating_project_menu)
                            photos = get_photo_from_project_sample(id)
                            if photos != 0:
                                for photo in photos:
                                    with open(f"photos/creating_project/{photo}.png", "rb") as file:
                                        await bot.send_photo(id, file)
                            video_menu = get_video_from_project_sample(id)
                            if video_menu != None:
                                await bot.send_message(id, "Видео:", reply_markup=video_menu)

                elif msg == 'Понятно':
                    if user_select == 'find':
                        await bot.send_message(id, 'Что необходимо найти?', reply_markup=find_menu)
                    elif user_select == 'create':
                        await bot.send_message(id, 'Что необходимо создать?', reply_markup=create_menu)

                elif user_select == 'edit_item_profile_menu_description':
                    if check_verification(id):
                        if check_exists_field_in_profile_moderatin(id, 'description'):
                            if len(msg) < 300:
                                delete_select(id)
                                set_moderation_for_profile(id, 'description', data=msg)
                                await bot.send_message(id, 'Ваше описание отправлено на модерацию.', reply_markup=get_main_menu(id))
                            else:
                                await bot.send_message(id, '!!! До 300 символов !!!')
                        else:
                            await bot.send_message(id, 'У вас уже есть заявка на изменение описания.')
                    else:
                        delete_select(id)
                        add_json_user_info(id, "description", msg)
                        await bot.send_message(id, 'Ваше описание успешно обновленно', reply_markup=get_main_menu(id))
                elif 'edit_item_profile_menu_category_' in user_select:
                    await bot.delete_message(id, message.message_id)
                    if check_category(msg):
                        category = msg
                        if user_select == 'edit_item_profile_menu_category_profile':
                            add_json_user_info(id, 'main_category_1', category)
                            change_select(id, 'edit_item_profile_menu_category_profile_2')
                            await bot.send_message(id, f'Категория {category} успешно добавлена. Выберите еще одну категорию или нажмите далее.',reply_markup=select_category_for_profile)
                        elif user_select == 'edit_item_profile_menu_category_profile_2':
                            add_json_user_info(id, 'main_category_2', category)
                            change_select(id, 'edit_item_profile_menu_category_profile_3')
                            await bot.send_message(id, f'Категория {category} успешно добавлена. Выберите еще одну или нажмите Далее',)
                        elif 'edit_item_profile_menu_category_profile_3' in user_select:
                            add_json_user_info(id, 'main_category_3', category)
                            change_select(id, '')
                            await bot.send_message(id, f'Категория {category} успешно добавлена.', reply_markup=get_main_menu(id))
                # elif msg == '💳 Моя Виза':
                #     await bot.delete_message(id, message.message_id)
                #     if check_type_visa(id) == 'participant':
                #         visa = open(f'visa_participant/{id}.png', 'rb')
                #         await bot.send_photo(id, visa, 'Ваша виза.')
                #     elif check_type_visa(id) == 'partner':
                #         visa = open(f'visa_partner/{id}.png', 'rb')
                #         await bot.send_photo(id, visa, 'Ваша виза.')
                #     elif check_type_visa(id) == 'group':
                #         visa = open(f'visa_group/{id}.png', 'rb')
                #         await bot.send_photo(id, visa, 'Ваша виза.')
                elif msg == 'Ссылка':
                    if user_select == 'ref_menu':
                        change_select(id, 'ref_menu_link')
                        me = await bot.me
                        link = f'https://t.me/{me.username}?start={id}'
                        await bot.send_message(id, f"Ваша реф. ссылка: {link}", reply_markup=back_menu)
                elif msg == 'Аппрувнуто':
                    if user_select == 'ref_menu':
                        change_select(id, 'ref_menu_appruf')
                        text = check_referals(id, 'appruf')
                        text = 'Аппрувнуто:\n\n' + text
                        await bot.send_message(id, text, reply_markup=back_menu)
                elif msg == 'В холде':
                    if user_select == 'ref_menu':
                        change_select(id, 'ref_menu_in_hold')
                        text = check_referals(id, 'in_hold')
                        text = 'В холде:\n\n' + text
                        await bot.send_message(id, text, reply_markup=back_menu)
                elif msg == 'Условия и правила реф. программы':
                    if user_select == 'ref_menu':
                        change_select(id, 'ref_menu_terms')
                        await bot.send_message(id, "Условия и правила реф. программы:\n- Пользователь должен пройти верификацию.\n\nПри выполнении условий начисляются средства на баланс\n\nВ холде отображает пользователей, не прошедших верификацию.", reply_markup=back_menu)
                
                
                elif '🚀 Тариф' in msg:
                    change_select(id, 'watching_tariff')
                    await bot.delete_message(id, message.message_id)
                    tariff_name = msg[8:]
                    buy_tariff_menu = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
                    if tariff_name == 'Стандарт':
                        tariff_info = get_tariff_info(tariff_name)
                        change_select(id, 'buy_tariff_standart')
                        buy_button = KeyboardButton(text='🚀 Купить')
                        buy_tariff_menu.add(buy_button)
                        await bot.send_message(id, tariff_info, reply_markup=buy_tariff_menu)
                    elif tariff_name == 'Расширенный':
                        tariff_info = get_tariff_info(tariff_name, back_button)
                        change_select(id, 'buy_tariff_extended')
                        buy_button = KeyboardButton(text='🚀 Купить')
                        buy_tariff_menu.add(buy_button, back_button)
                        await bot.send_message(id, tariff_info, reply_markup=buy_tariff_menu)
                    elif tariff_name == 'PRO':
                        tariff_info = get_tariff_info(tariff_name)
                        change_select(id, 'buy_tariff_pro')
                        buy_button = KeyboardButton(text='🚀 Купить')
                        buy_tariff_menu.add(buy_button, back_button)
                        await bot.send_message(id, tariff_info, reply_markup=buy_tariff_menu)
                elif msg == '🚀 Купить':
                    if 'buy_tariff_' in user_select:
                        tariff = user_select[11:]
                        price = 0
                        if tariff == 'standart':
                            tariff_name = 'Стандарт'
                            price = get_tariff_info(tariff_name, 'for_buy')
                        elif tariff == 'extended':
                            tariff_name = 'Расширенный'
                            price = get_tariff_info(tariff_name, 'for_buy')
                        elif tariff == 'pro':
                            tariff_name = 'PRO'
                            price = get_tariff_info(tariff_name, 'for_buy')
                        if len(tariff_name) > 0:
                            if check_exists_sum(id, price):
                                update_balance(id, -price)
                                add_action_at_payments_log(id, price, "spending", f'Покупка тарифа {tariff_name}.')
                                update_tariff(id, tariff)
                                await bot.send_message(id, f'Вы приобрели тариф {tariff_name} на 30 дней.')
                            else:
                                await bot.send_message(id, 'Недостаточно средств на балансе.')

                elif msg == 'Создать':
                    change_select(id, 'create')
                    await bot.delete_message(id, message.message_id)
                    if check_first_touch(id, 'create'):
                        add_first_touch(id, "create")
                        await bot.send_message(id, "Создать\n\nВ данном разделе Вы можете создать запрос любой сложности.\n\nВопрос – создать вопрос, который можно решить в диалоге.\n\nЗадача – создать запрос, подразумевающий разовую работу от одного человека.\n\nПроект – опубликовать запрос на сбор коллектива для проектной деятельности.", reply_markup=understand_menu)
                    else:
                        await bot.send_message(id, 'Что необходимо создать?', reply_markup=create_menu)
                
                elif msg == 'Найти':
                    change_select(id, 'find')
                    await bot.delete_message(id, message.message_id)
                    if check_first_touch(id, 'find'):
                        add_first_touch(id, "find")
                        await bot.send_message(id, "Найти\n\nВ данном разделе расположен каталог запросов и пользователей\n\nКастомизируйте поиск запросов при помощи фильтров и выбирайте то, что подходит Вам больше всего\n\nИ подбирайте людей для Ваших собственных запросов", reply_markup=understand_menu)
                    else:
                        await bot.send_message(id, 'Что необходимо найти?', reply_markup=find_menu)
            
                elif user_select == 'create':
                    if msg == '📁 Проект':
                        project_id = randint(1111111111, 9999999999)
                        create_project_sample(id, project_id)
                        change_select(id, 'create_project_name')
                        await bot.delete_message(id, message.message_id)
                        await bot.send_message(id, 'Введите название проекта', reply_markup=next_and_back_to_main_menu_menu)
                    elif msg == '📘 Задача':
                        change_select(id, 'create_task_menu')
                        await bot.delete_message(id, message.message_id)
                        await bot.send_message(id, 'В разработке. Можете воспользоваться другими функциями проекта.')
                    elif msg == '❓ Вопрос':
                        question_id = randint(1111111, 9999999)
                        change_select(id, 'create_question_category_1')
                        create_question_sample(id, question_id)
                        await bot.delete_message(id, message.message_id)
                        await bot.send_message(id, 'Выберите категории вопроса(до 2-ух)', reply_markup=select_category_for_profile)
                        
                
                elif user_select == 'find':
                    if msg == '📁 Проект':
                        change_select(id, 'find_project_menu')
                        await bot.delete_message(id, message.message_id)
                        await bot.send_message(id, 'Укажите тип проекта', reply_markup=create_project_type_menu)
                    elif msg == '📘 Задача':
                        change_select(id, 'find_task_menu')
                        await bot.delete_message(id, message.message_id)
                        await bot.send_message(id, 'В разработке. Можете воспользоваться другими функциями проекта.')
                    elif msg == '❓ Вопрос':
                        change_select(id, 'find_question_menu')
                        await bot.delete_message(id, message.message_id)
                        await bot.send_message(id, 'В разработке. Можете воспользоваться другими функциями проекта.')
                    elif msg == 'Каталог пользователей':
                        change_select(id, 'find_user_menu')
                        await bot.delete_message(id, message.message_id)
                        await bot.send_message(id, 'Выберите тип поиска', reply_markup=find_user_type_menu)
                
                elif user_select == 'find_project_menu':
                    if msg == 'Онлайн':
                        change_select(id , 'find_project_categories')
                        add_info_in_find_project(id, 'project_type', 'online')
                        await bot.send_message(id, 'Выберите по каким категориям искать проект', reply_markup=find_project_categories_menu)
                    elif msg == 'Оффлайн':
                        change_select(id , 'find_project_categories')
                        add_info_in_find_project(id, 'project_type', 'offline')
                        await bot.send_message(id, 'Выберите по каким категориям искать проект', reply_markup=find_project_categories_menu)
                    else:
                        await bot.send_message(id, 'Выберите тип проекта', reply_markup=find_project_menu)

                elif user_select == 'find_project_categories':
                    if msg == 'Мои категории':
                        change_select(id, 'find_project_final')
                        add_info_in_find_project(id, 'project_categories', 'my')
                        await bot.send_message(id, 'Начать поиск?', reply_markup=start_finding_menu)
                    elif msg == 'Все категории':
                        add_info_in_find_project(id, 'project_categories', 'all')
                        change_select(id, 'find_project_final')
                        await bot.send_message(id, 'Начать поиск ?', reply_markup=start_finding_menu)

                elif user_select == 'find_project_final':
                    if msg == 'Начать поиск':
                        await bot.delete_message(id, message.message_id)
                        if get_field_projects_to_find(id, 'categories') == 'my':
                            project_id =  get_random_project_by_personal_settings(id)
                            change_select(id, f'action_with_project_{project_id}')
                            if project_id == 0:
                                await bot.send_message(id, 'По вашим фильтрам нету проектов', reply_markup=back_to_main_menu)
                            else:
                                await bot.send_message(id, get_project_as_text(project_id), reply_markup=project_menu_in_find)
                        elif get_field_projects_to_find(id, 'categories') == 'all':
                            project_id = get_random_project_by_not_personal_settings(id)
                            change_select(id, f'action_with_project_{project_id}')
                            await bot.send_message(id, get_project_as_text(project_id), reply_markup=project_menu_in_find)
                        else:
                            await bot.send_message(id, 'DB ERROR', reply_markup=back_to_main_menu)
                
                elif 'action_with_project_' in user_select:
                    project_id = user_select[20:]
                    if msg == 'Откликнуться':
                        await bot.delete_message(id, message.message_id)
                        follow_project(id, project_id)
                        await bot.send_message(id, 'Вы успешно откликнулись на проект.')
                    elif msg == 'Пожаловаться':
                        change_select(id, f'warn_project_{project_id}')
                        await bot.delete_message(id, message.message_id)
                        await bot.send_message(id, 'В чем заключается нарушение?', reply_markup=warn_project_menu)
                    elif msg == 'Следующий':
                        await bot.delete_message(id, message.message_id)
                        if get_field_projects_to_find('1230154081', 'categories') == 'my':
                            project_id =  get_random_project_by_personal_settings(id)
                            change_select(id, f'action_with_project_{project_id}')
                            if project_id == 0:
                                await bot.send_message(id, 'По вашим фильтрам нету проектов', reply_markup=back_to_main_menu)
                            else:
                                await bot.send_message(id, get_project_as_text(project_id), reply_markup=project_menu_in_find)
                        elif get_field_projects_to_find('1230154081', 'categories') == 'all':
                            project_id = get_random_project_by_not_personal_settings(id)
                            change_select(id, f'action_with_project_{project_id}')
                            await bot.send_message(id, get_project_as_text(project_id), reply_markup=project_menu_in_find)
                        else:
                            await bot.send_message(id, 'DB ERROR', reply_markup=back_to_main_menu)

                elif 'warn_project_' in user_select:
                    project_id = user_select[13:]
                    await bot.send_message(id, warn_project(id, project_id, msg), reply_markup=warn_project_menu)

                elif 'find_user_' in user_select:
                    if user_select == 'find_user_menu':
                        if msg == 'Найти по имени':
                            change_select(id, 'find_user_by_name')
                            await bot.send_message(id, "Введите имя пользователя для поиска", reply_markup=back_to_main_menu)
                        elif msg == 'Общий каталог':
                            change_select(id, "find_user_in_general_catalog")
                            random_id = get_random_user_id()
                            path = get_profile(random_id)
                            with open(path, "rb") as file:
                                await bot.send_photo(id, file, reply_markup=see_finding_user_profile)
                            os.remove(path)
                        else:
                            await bot.send_message(id, "Выберите один из указанных пунктов на клавиатуре", reply_markup=find_user_type_menu)
                    elif user_select == 'find_user_by_name':
                        if len(msg) >= 3 <= 35:
                            n_words = len(re.split(' |-', msg))
                            if n_words > 1 and n_words <= 5:
                                name = msg
                                change_choice_data(id, name)
                                result = find_user_by_name(name, 0)
                                if result[0] != 0:
                                    change_select(id, f"find_user_by_name_{result[1]}")
                                    path = get_profile(result[0])
                                    with open(path, "rb") as file:
                                        await bot.send_photo(id, file, reply_markup=next_and_back_to_main_menu_menu)
                                    os.remove(path)
                                else:
                                    await bot.send_message(id, "По такому имени пользователей ничего не найдено.", reply_markup=back_to_main_menu)
                            else:
                                await bot.send_message(id, "Введите корректные Имя Фамилию")
                        else:
                            await bot.send_message(id, "Введите корректные Имя Фамилию")
                    
                elif 'create_project_' in user_select: #СОЗДАНИЕ ПРОЕКТА
                    if user_select == 'create_project_name':
                        if len(msg) < 50:
                            if len(msg.rsplit("    ")) == 1 and msg.rsplit("    ")[0] == msg:
                                if check_full_project_sample(id):
                                    add_info_in_project_sample(id, "project_name", msg)
                                    change_select(id, "create_project_final_step")
                                    await bot.send_message(id, get_project_about_sample(id), reply_markup=ending_creating_project_menu)
                                    videos = get_photo_from_project_sample(id)
                                    photos = get_photo_from_project_sample(id)
                                    if photos != 0:
                                        for photo in photos:
                                            with open(f"photos/creating_project/{photo}.png", "rb") as file:
                                                await bot.send_photo(id, file)
                                    video_menu = get_video_from_project_sample(id)
                                    if video_menu != None:
                                        await bot.send_message(id, "Видео:", reply_markup=video_menu)

                                else:
                                    change_select(id, 'create_project_description')
                                    add_info_in_project_sample(id, "project_name", msg)
                                    await bot.send_message(id, 'Введите описание проекта', reply_markup=next_and_back_and_back_to_main_menu_menu)
                            else:
                                await bot.send_message(id, "❗❗❗Красные строки использовать запрещено❗❗❗", reply_markup=next_and_back_to_main_menu_menu)
                        else:
                            await bot.send_message(id, "❗❗❗Лимит до 50 символов❗❗❗", reply_markup=next_and_back_to_main_menu_menu)
                    
                    elif user_select == 'create_project_description':
                        if len(msg) < 400:
                            if len(msg.rsplit("    ")) == 1 and msg.rsplit("    ")[0] == msg:
                                if check_full_project_sample(id):
                                    add_info_in_project_sample(id, "project_description", msg)
                                    change_select(id, "create_project_final_step")
                                    await bot.send_message(id, get_project_about_sample(id), reply_markup=ending_creating_project_menu)
                                    photos = get_photo_from_project_sample(id)
                                    if photos != 0:
                                        for photo in photos:
                                            with open(f"photos/creating_project/{photo}.png", "rb") as file:
                                                await bot.send_photo(id, file)
                                    video_menu = get_video_from_project_sample(id)
                                    if video_menu != None:
                                        await bot.send_message(id, "Видео:", reply_markup=video_menu)
                                    
                                else:
                                    change_select(id, 'create_project_type')
                                    add_info_in_project_sample(id, "project_description", msg)
                                    await bot.send_message(id, 'Выберите тип проекта', reply_markup=create_project_type_menu)
                            else:
                                await bot.send_message(id, "❗❗❗Красные строки использовать запрещено❗❗❗", reply_markup=next_and_back_and_back_to_main_menu_menu)
                        else:
                            await bot.send_message(id, "❗❗❗Лимит до 400 символов❗❗❗", reply_markup=next_and_back_and_back_to_main_menu_menu)
                    
                    elif user_select == 'create_project_type':
                        if msg == 'Онлайн':
                            change_select(id, "create_project_category")
                            add_info_in_project_sample(id, "project_type", msg)
                            add_info_in_project_sample(id, "project_city", "none")
                            await bot.send_message(id, "Выберите категорию вашего проекта", reply_markup=select_category_for_project)
                        elif msg == 'Оффлайн':
                            change_select(id, "create_project_geo")
                            add_info_in_project_sample(id, "project_type", msg)
                            await bot.send_message(id, 'Отправте геопозицию вашего проекта', reply_markup=next_and_back_and_back_to_main_menu_menu)
                        else:
                            await bot.send_message(id, "❗❗❗ Выберите один из пунктов ❗❗❗", reply_markup=next_and_back_and_back_to_main_menu_menu)
                    
                    elif user_select == 'create_project_category':
                        if check_project_category(msg):
                            with open(f"json/creating_project/{id}.json", "r") as file:
                                content = json.load(file)
                            content["project_subcategories"] = ''
                            with open(f"json/creating_project/{id}.json", "w") as file:
                                file.write(json.dumps(content))
                            change_select(id, "create_project_subcategories")
                            add_info_in_project_sample(id, "project_category", msg)
                            await bot.send_message(id, "Выберите до 4 подкатегорий для проекта", reply_markup=select_category_for_project)
                        else:
                            await bot.send_message(id, "Выберите из категорий на клавиатуре", reply_markup=select_category_for_project)
                    
                    elif user_select == 'create_project_subcategories':
                        if check_project_category(msg):
                            if check_uniqueness_categories_project(id, "project_subcategories", msg):
                                if check_count_categories_project(id, 'project_subcategories'):
                                    add_info_in_project_sample(id, "project_subcategories", msg)
                                    await bot.send_message(id, f"Вы выбрали {msg}. Выберите еще подкатегорию", reply_markup=select_category_for_project)
                                else:
                                    with open(f"json/creating_project/{id}.json", "r") as file:
                                        content = json.load(file)
                                    content["project_need_categories"] = ''
                                    with open(f"json/creating_project/{id}.json", "w") as file:
                                        file.write(json.dumps(content))
                                    add_info_in_project_sample(id, "project_subcategories", msg)
                                    change_select(id, "create_project_need_categories")
                                    await bot.send_message(id, "Выберите категории исполнителя", reply_markup=select_type_for_need_categories_of_project)
                            else:
                                await bot.send_message(id, "Вы уже выбирали эту категорию")
                        else:
                            await bot.send_message(id, "Выберите из категорий на клавиатуре", reply_markup=select_category_for_project)

                    elif user_select == 'create_project_need_categories':
                        if msg == 'Выбрать интересы':
                            await bot.send_message(id, "Выберите категории исполнителя", reply_markup=select_category_for_profile)
                        elif msg == 'Без выбора':
                            if check_full_project_sample(id):
                                    add_info_in_project_sample(id, "project_need_categories", msg)
                                    change_select(id, "create_project_final_step")
                                    await bot.send_message(id, get_project_about_sample(id), reply_markup=ending_creating_project_menu)
                                    photos = get_photo_from_project_sample(id)
                                    if photos != 0:
                                        for photo in photos:
                                            with open(f"photos/creating_project/{photo}.png", "rb") as file:
                                                await bot.send_photo(id, file)
                                    video_menu = get_video_from_project_sample(id)
                                    if video_menu != None:
                                        await bot.send_message(id, "Видео:", reply_markup=video_menu)       
                            else:
                                change_select(id, "create_project_price")
                                add_info_in_project_sample(id, "project_need_categories", 'Нету')
                                await bot.send_message(id, "Выберите вознаграждение", reply_markup=select_type_of_payment_for_project)
                        elif msg == 'Мои интересы':
                            if check_full_project_sample(id):
                                add_info_in_project_sample(id, "project_need_categories", msg)
                                change_select(id, "create_project_final_step")
                                await bot.send_message(id, get_project_about_sample(id), reply_markup=ending_creating_project_menu)
                                photos = get_photo_from_project_sample(id)
                                if videos != 0:
                                    for photo in photos:
                                        with open(f"photos/creating_project/{photo}.png", "rb") as file:
                                            await bot.send_photo(id, file)
                                video_menu = get_video_from_project_sample(id)
                                if video_menu != None:
                                    await bot.send_message(id, "Видео:", reply_markup=video_menu)
                                
                            else:
                                change_select(id, "create_project_price")
                                add_info_in_project_sample(id, "project_need_categories", get_user_interests(id))
                                await bot.send_message(id, "Выберите вознаграждение", reply_markup=select_type_of_payment_for_project)
                        elif check_category(msg):
                            if check_uniqueness_categories_project(id, "project_need_categories", msg):
                                if check_count_categories_project(id, 'project_need_categories'):
                                    add_info_in_project_sample(id, "project_need_categories", msg)
                                    await bot.send_message(id, f"Вы выбрали {msg}. Выберите еще категорию исполнителя", reply_markup=select_category_for_profile)
                                else:
                                    if check_full_project_sample(id):
                                        add_info_in_project_sample(id, "project_need_categories", msg)
                                        change_select(id, "create_project_final_step")
                                        await bot.send_message(id, get_project_about_sample(id), reply_markup=ending_creating_project_menu)
                                        photos = get_photo_from_project_sample(id)
                                        if photos != 0:
                                            for photo in photos:
                                                with open(f"photos/creating_project/{photo}.png", "rb") as file:
                                                    await bot.send_photo(id, file)
                                        video_menu = get_video_from_project_sample(id)
                                        if video_menu != None:
                                            await bot.send_message(id, "Видео:", reply_markup=video_menu)
                                    else:
                                        add_info_in_project_sample(id, "project_need_categories", msg)
                                        change_select(id, "create_project_price")
                                        await bot.send_message(id, "Выберите вознаграждение", reply_markup=select_type_of_payment_for_project)
                            else:
                                await bot.send_message(id, "Вы уже выбирали эту категорию")
                        else:
                                await bot.send_message(id, "Выберите пункты на клавиатуре", reply_markup=select_category_for_profile)
                    
                    elif user_select == 'create_project_price':
                        if msg == 'Фикс цена без искажения':
                            change_select(id, "create_project_price_fixed")
                            await bot.send_message(id, "Введите фиксированное вознаграждение за проект с указанием валюты\Формат: СУММА $ или СУММА ₽", reply_markup=next_and_back_and_back_to_main_menu_menu)
                        elif msg == 'Размытый ценник':
                            change_select(id, "create_project_price_intermediate")
                            await bot.send_message(id, "Введите вознаграждение за проект с указанием валюты\Формат: СУММА $ - СУММА $ или СУММА ₽ - СУММА ₽", reply_markup=next_and_back_and_back_to_main_menu_menu)
                        elif msg == 'Безвозмездное оказание услуги':
                            add_info_in_project_sample(id, "project_price", msg)
                            with open(f"json/creating_project/{id}.json") as file:
                                content = json.load(file)
                            if len(content["project_media"]) == 5:
                                change_select(id, "create_project_final_step")
                                await bot.send_message(id, get_project_about_sample(id), reply_markup=ending_creating_project_menu)
                                photos = get_photo_from_project_sample(id)
                                if videos != 0:
                                    for photo in photos:
                                        with open(f"photos/creating_project/{photo}.png", "rb") as file:
                                            await bot.send_photo(id, file)
                                video_menu = get_video_from_project_sample(id)
                                if video_menu != None:
                                    await bot.send_message(id, "Видео:", reply_markup=video_menu)
                            else:
                                change_select(id, "create_project_media")
                                await bot.send_message(id, "Отправте до 5 фото/видео\nВидео необходимо отправить в виде ссылки на видеохостинг YouTube.com", reply_markup=next_and_back_and_back_to_main_menu_menu)
                    
                    elif user_select == 'create_project_price_fixed':
                        if len(msg) < 12:
                            add_info_in_project_sample(id, "project_price", msg)
                            with open(f"json/creating_project/{id}.json") as file:
                                content = json.load(file)
                            if len(content["project_media"]) == 5:
                                change_select(id, "create_project_final_step")
                                await bot.send_message(id, get_project_about_sample(id), reply_markup=ending_creating_project_menu)
                                photos = get_photo_from_project_sample(id)
                                if videos != 0:
                                    for photo in photos:
                                        with open(f"photos/creating_project/{photo}.png", "rb") as file:
                                            await bot.send_photo(id, file)
                                video_menu = get_video_from_project_sample(id)
                                if video_menu != None:
                                    await bot.send_message(id, "Видео:", reply_markup=video_menu)
                            else:
                                change_select(id, "create_project_media")
                                await bot.send_message(id, "Отправте до 5 фото/видео\nВидео необходимо отправить в виде ссылки на видеохостинг YouTube.com", reply_markup=next_and_back_and_back_to_main_menu_menu)
                        else:
                            await bot.send_message(id, "❗❗❗Лимит до 12 символов❗❗❗")

                    elif user_select == 'create_project_price_intermediate':
                        if len(msg) < 18:
                            if len(msg.rsplit("-")) == 2 and msg.rsplit("-")[0] != '':
                                add_info_in_project_sample(id, "project_price", msg)
                                with open(f"json/creating_project/{id}.json") as file:
                                    content = json.load(file)
                                if len(content["project_media"]) == 5:
                                    change_select(id, "create_project_final_step")
                                    await bot.send_message(id, get_project_about_sample(id), reply_markup=ending_creating_project_menu)
                                    photos = get_photo_from_project_sample(id)
                                    if photos != 0:
                                        for photo in photos:
                                            with open(f"photos/creating_project/{photo}.png", "rb") as file:
                                                await bot.send_photo(id, file)
                                    video_menu = get_video_from_project_sample(id)
                                    if video_menu != None:
                                        await bot.send_message(id, "Видео:", reply_markup=video_menu)
                                else:
                                    change_select(id, "create_project_media")
                                    await bot.send_message(id, "Отправте до 5 фото/видео\nВидео необходимо отправить в виде ссылки на видеохостинг YouTube.com", reply_markup=next_and_back_and_back_to_main_menu_menu)
                            else:
                                await bot.send_message(id, '❗❗❗Обязательно используйте один символ "-" для обозначения промежутка❗❗❗')
                        else:
                            await bot.send_message(id, "❗❗❗Лимит до 18 символов❗❗❗")
                    
                    elif user_select == 'create_project_media':
                        if 'youtube.com' in msg.lower():
                            add_media_in_project_sample(id, 'video', message.text)
                            with open(f"json/creating_project/{id}.json", "r") as file:
                                structure = json.load(file)
                                file.close()
                            len_array = len(structure["project_media"])
                            if len_array == 5:
                                change_select(id, "create_project_final_step")
                                await bot.send_message(id, get_project_about_sample(id), reply_markup=ending_creating_project_menu)
                                photos = get_photo_from_project_sample(id)
                                if videos != 0:
                                    for photo in photos:
                                        with open(f"photos/creating_project/{photo}.png", "rb") as file:
                                            await bot.send_photo(id, file)
                                video_menu = get_video_from_project_sample(id)
                                if video_menu != None:
                                    await bot.send_message(id, "Видео:", reply_markup=video_menu)
                            else:
                                await bot.send_message(id, f"Отправте еще фото/видео")
                        else:
                            await bot.send_message(id, "Отправте ссылку на видео или отправте фото")
                
                    elif user_select == 'create_project_final_step':
                        if msg == 'Заполнить заново':
                            change_select(id, "create_project_name")
                            if os.path.exists(f"json/creating_project/{id}.json"):
                                os.remove(f"json/creating_project/{id}.json")
                            project_id = randint(1111111111, 9999999999)
                            create_project_sample(id, project_id)
                            await bot.send_message(id, 'Введите название проекта', reply_markup=next_and_back_and_back_to_main_menu_menu)
                        elif msg == 'Изменить медиа':
                            change_select(id, "create_project_media")
                            with open(f"json/creating_project/{id}.json", "r") as file:
                                content = json.load(file)
                            content["project_media"] = []
                            with open(f"json/creating_project/{id}.json", "w") as file:
                                file.write(json.dumps(content))
                            await bot.send_message(id, "Отправте до 5 фото/видео\nВидео необходимо отправить в виде ссылки на видеохостинг YouTube.com", reply_markup=next_and_back_and_back_to_main_menu_menu)
                        elif msg == 'Изменить название':
                            change_select(id, "create_project_name")
                            await bot.send_message(id, "Введите название проекта", reply_markup=next_and_back_and_back_to_main_menu_menu)
                        elif msg == 'Изменить описание':
                            change_select(id, "create_project_description")
                            await bot.send_message(id, "Введите описание проекта", reply_markup=next_and_back_and_back_to_main_menu_menu)
                        elif msg == 'Изменить все категории':
                            change_select(id, "create_project_category")
                            await bot.send_message(id, "Выберите категорию проета", reply_markup=select_category_for_project)
                        elif msg == 'Изменить вознаграждение':
                            change_select(id, "create_project_price")
                            await bot.send_message(id, "Выберите вознаграждение", reply_markup=select_type_of_payment_for_project)
                        elif msg == 'Отправить':
                            change_select(id, "")
                            send_project_sample(id)
                            project_id = randint(1111111111, 9999999999)
                            create_project_sample(id, project_id)
                            await bot.send_message(id, 'Ваш проект отображается в разделе "Мои запросы". После проверки администрацией ваш проект станет доступным для других пользователей', reply_markup=get_main_menu(id))
                
                elif 'create_question' in user_select:
                    if user_select == 'create_question_category_1' or user_select == 'create_question_category_2':
                        await bot.delete_message(id, message.message_id)
                        if check_category(msg):
                            category = msg
                            if user_select == 'create_question_category_1':
                                change_select(id, 'create_question_category_2')
                                add_info_in_creating_question(id, 'question_category_1', msg)
                                await bot.send_message(id, f'Вы выбрали {category}. Выберите еще одну категорию или нажмите Далее', reply_markup=select_category_for_profile)
                            elif user_select == 'create_question_category_2':
                                change_select(id, 'create_question_input_question')
                                add_info_in_creating_question(id, 'question_category_2', msg)
                                await bot.send_message(id, f'Вы выбрали {category}. Введите вопрос.', reply_markup=next_and_back_menu)
                    elif user_select == 'create_question_input_question':
                        if len(msg) <= 100:
                            change_select(id, 'create_question_add_photo_file_1')
                            add_info_in_creating_question(id, 'question_text', msg)
                            await bot.send_message(id, 'Добавте до 3-еx фото или нажмите Далее', reply_markup=next_and_back_menu)
                        else:
                            await bot.send_message(id, 'Что-то пошло не так, введите вопрос заново. Лимит: 100 символов', reply_markup=next_and_back_menu)
                    elif user_select == 'create_question_add_photo_file_1' or user_select == 'create_question_add_photo_file_2' or user_select == 'create_question_add_photo_file_3':
                        await bot.send_message(id, 'Добавте до 3-ех фото или нажмите Далее', reply_markup=next_and_back_menu)

                elif msg == '📘 Задача':
                    await bot.delete_message(id, message.message_id)
                    await bot.send_message(id, '📘 Задача:')

                elif msg == '❓ Вопрос':
                    await bot.delete_message(id, message.message_id)
                    await bot.send_message(id, '❓ Вопрос:')
                
                elif msg == '🔖️ Избранное':
                    await bot.delete_message(id, message.message_id)
                    await bot.send_message(id, '🔖 Избранное:') 

                elif msg == '📧 Отклики':
                    await bot.delete_message(id, message.message_id)
                    await bot.send_message(id, '📧 Отклики:') 

                elif msg == '🏢 В работе':
                    await bot.delete_message(id, message.message_id)
                    await bot.send_message(id, '🏢 В работе:') 

                
                
                elif 'admin_' in user_select:
                    if check_admin_level(id):
                        if msg == '👨‍💼 Админ панель':
                            await bot.delete_message(id, message.message_id)
                            level = check_admin_level(id)
                            print(level)
                            if level == 1:
                                change_select(id, "admin_panel")
                                await bot.send_message(message.from_user.id, 'Панель Администратора.', reply_markup=admin_panel_1_menu)
                            elif level == 2:
                                change_select(id, "admin_panel")
                                await bot.send_message(message.from_user.id, 'Панель Главного Администратора.', reply_markup=admin_panel_2_menu)
                        if user_select == 'admin_panel':
                            if msg == 'Подтвердить':
                                await bot.delete_message(id, message.message_id)
                                change_select(id, "admin_accept")
                                await bot.send_message(id, "Выберите что необходимо подтвердить", reply_markup=admin_accept_menu)
                                pass 
                        elif user_select == 'admin_accept':
                            if check_admin_level(id, 1):
                                if msg == '📁 Проект':
                                    project_text, project_id, succes = get_project_to_accept()
                                    if succes:
                                        change_select(id, f"admin_accept_project_{project_id}")
                                        await bot.send_message(id, project_text, reply_markup=accept_menu)
                                    else:
                                        await bot.send_message(id, "Все проекты проверены", reply_markup=get_admin_panel(id))
                            elif msg == '❓ Вопрос':
                                pass
                            elif msg == '✔️ Верификация':
                                pass
                        elif 'admin_accept_project_' in user_select:
                            project_id = user_select[21:]

                            if msg == 'Подтвердить':
                                update_status_project(project_id, 'accept')
                                await bot.send_message(id, "Вы успешно подтвердили проект")
                            else:
                                update_status_project(project_id, 'unaccept', msg)
                                await bot.send_message(id, "Вы успешно отменили проект")
                            await bot.send_message(id, "Все проекты проверены", reply_markup=get_admin_panel(id))


                elif '✏️' in msg:
                    if msg == '✏️ Редактировать':
                        if user_select == 'profile_menu':
                            change_select(id, 'edit_profile_menu')
                            await bot.send_message(id, 'Выберите пункт для редактирования.', reply_markup=edit_profile_item_menu)
                    else:
                        edit = msg[3:]
                        if edit == 'Фото':
                            change_select(id, f'edit_item_profile_menu_photo')
                            await bot.send_message(id, 'Отправьте новое фото профиля.', reply_markup=back_menu)
                        elif edit == 'Описание':
                            change_select(id, f'edit_item_profile_menu_description')
                            await bot.send_message(id, 'Введите новое описание профиля.', reply_markup=back_menu)
                        elif edit == 'Категории профиля':
                            change_select(id, f'edit_item_profile_menu_category_profile')
                            await bot.send_message(id, 'Выберите новые категории профиля.', reply_markup=select_category_for_profile)
                        elif edit == 'Категории интересов':
                            change_select(id, f'edit_item_profile_menu_category_interests')
                            await bot.send_message(id, 'Выберите новые категории профиля.', reply_markup=select_category_for_profile)
                elif msg == '✔️ Верификация':
                    if user_select == 'profile_menu':
                        change_select(id, 'verification_profile_menu')
                        with open(f'json/profile/{id}.json', 'r') as file:
                            content = json.load(file)
                            file.close()
                        if content["verification"] == '-':
                            await bot.send_message(id, 'Вас успешно верефицировали', reply_markup=back_menu)
                            set_verification(id)
                elif msg == '📩 Уведомления':
                    if user_select == 'profile_menu':
                        change_select(id, 'notifications_profile_menu')
                        await bot.send_message(id, get_notifications(id), reply_markup=back_menu)
                elif msg == 'Баланс':
                    change_select(id, "balance_menu_balance")
                    await bot.delete_message(id, message.message_id)
                    await bot.send_message(id, f"Баланс:\n{get_balance(id)}₽", reply_markup=balance_menu)
                elif msg == 'Пополнить':
                    change_select(id, "balance_menu_replenish")
                    await bot.delete_message(id, message.message_id)
                    await bot.send_message(id, f"Пополнить:\nВведите сумму для пополнения от 100₽", reply_markup=replenish_menu)
                elif msg == 'Движение средств':
                    change_select(id, "balance_menu_payments_log")
                    await bot.delete_message(id, message.message_id)
                    await bot.send_message(id, f"Движение средств:\nВыберите пункт.", reply_markup=purse_log_menu)
                elif msg == 'Зачисление':
                    text = get_payments_log_by_action(id, "replenish")
                    text = 'Зачисления:' + text
                    change_select(id, "balance_menu_payments_log_replenish")
                    await bot.send_message(id, text, reply_markup=back_button)
                elif msg == 'Списание':
                    text = get_payments_log_by_action(id, "spending")
                    text = 'Списания:' + text
                    change_select(id, "balance_menu_payments_log_replenish")
                    await bot.send_message(id, text, reply_markup=back_button)
                elif msg == '🏠 На главную':
                    await bot.delete_message(id, message.message_id)
                    await bot.send_message(id, 'Главное меню:', reply_markup=get_main_menu(id))
                elif msg.isdigit():
                    if 'balance_menu_replenish' in user_select:
                        await bot.delete_message(id, message.message_id)
                        sum = msg
                        if sum.isdigit():
                            if int(sum) >= 100 and int(sum) <= 10000:
                                await bot.send_invoice(chat_id=message.from_user.id, title=f"Пополнить баланс на {sum}₽", description=f"Пополнить баланс на {sum}₽", payload=f"buy_{sum}", provider_token=PAYMENT_TOKEN, currency="RUB", start_parameter="buy", prices=[{"label": "Py6", "amount": int(sum)*100}], reply_markup=back_button)
                            else:
                                await bot.send_message(id, "Сумма должна быть от 100₽ до 10,000₽", reply_markup=back_button)
                        else:
                            await bot.send_message(id, "Отправте число")
        else:
            await bot.send_message(id, "Введите /start")




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = False)