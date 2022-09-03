

import sqlite3 as sql
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, message, WebAppInfo


# profile -  Профиль
# purse -  Кошелек
# tariff -  Тарифы
# ref_program -  Реф. прогр.
# faq -  FAQ


registration_site_menu = InlineKeyboardMarkup(row_width=1)
open_site = InlineKeyboardButton(text="Регистрация", web_app=WebAppInfo(url="https://xn80aue1.vh104.hosterby.com"))
registration_site_menu.add(open_site)

# my_visa = KeyboardButton('💳 Моя Виза')
events = KeyboardButton('🎫 Мероприятия')
crowd_funding = KeyboardButton('💸 Краудфандинг')
buy_service = KeyboardButton('🏪 Магазин')
partner_panel = KeyboardButton('👨‍💼 Панель Организатора')
apanel = KeyboardButton('👨‍💼 Админ панель')
project = KeyboardButton('📁 Проект')
task = KeyboardButton('📘 Задача')
question = KeyboardButton('Услуга')
favorites = KeyboardButton('🔖️ Избранное')
responses = KeyboardButton('📧 Отклики')
in_work = KeyboardButton('🏢 В работе')


create = KeyboardButton(text='Создать')
find = KeyboardButton(text='Найти')

back_to_main_menu_button = KeyboardButton(text='Вернуться в главное меню')
back_to_main_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
back_to_main_menu.add(back_to_main_menu_button)
start_finding = KeyboardButton(text='Начать поиск')

next_button = KeyboardButton(text='Далее')
back_button = KeyboardButton(text='Назад')


next_and_back_and_back_to_main_menu_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
next_and_back_and_back_to_main_menu_menu.add(back_button, next_button, back_to_main_menu_button)

project_menu_in_find = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
follow_project_button = KeyboardButton(text='Откликнуться')
warn_project_button = KeyboardButton(text='Пожаловаться')
next_project_button = KeyboardButton(text='Следующий')
project_menu_in_find.add(follow_project_button, warn_project_button, next_project_button, back_to_main_menu_button)


next_menu = ReplyKeyboardMarkup(resize_keyboard=True)
next_menu.add(next_button)


start_menu = ReplyKeyboardMarkup(resize_keyboard=True)
start = KeyboardButton('Начать')
start_menu.add(start)


i_read_menu = ReplyKeyboardMarkup(resize_keyboard=True)
i_read = KeyboardButton(text='Согласен с условиями')
i_read_menu.add(i_read)


registration_menu = ReplyKeyboardMarkup(resize_keyboard=True)
registration_menu.add(back_button, next_button)


back_menu = ReplyKeyboardMarkup(resize_keyboard=True)
back_menu.add(back_button)


main_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
main_menu.add(create, find, responses, in_work, favorites)


back_to_main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
back_to_main_menu.add(back_button)


edit_profile_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
recreate_profie_button = KeyboardButton(text='Создать заново')
edit_description_profile_button = KeyboardButton(text='Поменять описание')
accept_creation_profile_button = KeyboardButton(text='Подтвердить')
edit_profile_menu.add(recreate_profie_button, edit_description_profile_button, accept_creation_profile_button)


edit_profile_item_menu = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
edit_name_surname = KeyboardButton(text='✏️ Фото')
edit_description = KeyboardButton(text='✏️ Описание')
edit_category_profile = KeyboardButton(text='✏️ Категории профиля')
edit_category_interests = KeyboardButton(text='✏️ Категории интересов')
edit_profile_item_menu.add(edit_name_surname, edit_description, edit_category_profile, edit_category_interests, back_button)


purse_menu = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
balance = KeyboardButton('Баланс')
replenish = KeyboardButton('Пополнить')
purse_log = KeyboardButton('Движение средств')
purse_menu.add(balance, replenish, purse_log)
purse_menu.add(back_button)


balance_menu = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
balance_menu.add(back_button)


replenish_menu = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
replenish_menu.add(back_button)


purse_log_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
money_on = KeyboardButton('Зачисление')
money_off = KeyboardButton('Списание')
purse_log_menu.add(money_on, money_off)
purse_log_menu.add(back_button)


ref_menu = ReplyKeyboardMarkup(row_width=3 ,resize_keyboard=True)
ref_link = KeyboardButton('Ссылка')
appruf = KeyboardButton('Аппрувнуто')
in_hold = KeyboardButton('В холде')
terms_ref = KeyboardButton('Условия и правила реф. программы')
ref_menu.add(ref_link, appruf, in_hold)
ref_menu.add(terms_ref)
ref_menu.add(back_button)


tariff_menu = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
tariff_1 = KeyboardButton(text='🚀 Тариф Стандарт')
tariff_2 = KeyboardButton(text='🚀 Тариф Расширенный')
tariff_3 = KeyboardButton(text='🚀 Тариф PRO')
tariff_menu.add(tariff_1, tariff_2, tariff_3)


tariffs_edit_menu = InlineKeyboardMarkup(row_width=1)
tariff_1 = InlineKeyboardButton(text='Стандарт', callback_data='admin_edit_tariff_standart')
tariff_2 = InlineKeyboardButton(text='Расширенный', callback_data='admin_edit_tariff_extended')
tariff_3 = InlineKeyboardButton(text='PRO', callback_data='admin_edit_tariff_pro')
tariffs_edit_menu.add(tariff_1, tariff_2, tariff_3)





_project = KeyboardButton(text='📁 Проект')
_task = KeyboardButton(text='📘 Задача')
_question = KeyboardButton(text='❓ Вопрос')
_find_user = KeyboardButton(text='Каталог пользователей')


warn_project_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
warn_project_menu.add(back_button, next_project_button, back_to_main_menu_button)


create_menu = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
create_menu.add(_project, _task, _question, back_to_main_menu_button)

find_menu = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
find_menu.add(_project, _task, _question, _find_user, back_to_main_menu_button)

offer_menu = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
offer_menu.add(_project, _task, _question, back_to_main_menu_button)

find_project_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
online_project = KeyboardButton(text='Онлайн')
offline_project = KeyboardButton(text='Оффлайн')
find_project_menu.add(online_project, offline_project)

find_project_categories_menu = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
by_my_categories = KeyboardButton(text='Мои категории')
by_all_categories = KeyboardButton(text='Все категории')
find_project_categories_menu.add(by_my_categories, by_all_categories, back_to_main_menu_button)

start_finding_menu = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
start_finding_menu.add(start_finding, back_button, back_to_main_menu_button)

create_project_type_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
create_project_type_menu.add(online_project, offline_project, back_button)

next_and_back_menu = ReplyKeyboardMarkup(resize_keyboard=True)
next_and_back_menu.add(back_button, next_button)

create_project_price_menu = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
without_payment = KeyboardButton(text='Без оплаты')
barter = KeyboardButton(text='По бартеру')
by_agreement = KeyboardButton(text='По договоренности')
input_sum = KeyboardButton(text='Ввести сумму')
create_project_price_menu.add(without_payment, barter, by_agreement, input_sum, back_button)

project_deadline_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
project_deadline_button = KeyboardButton(text='Без ограничений')
project_deadline_menu.add(project_deadline_button)
project_deadline_menu.add(next_button, back_button)

find_user_type_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
find_by_name = KeyboardButton(text='Найти по имени')
find_in_general_catalog = KeyboardButton(text='Общий каталог')
find_user_type_menu.add(find_by_name, find_in_general_catalog, back_button)

next_and_back_to_main_menu_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
next_and_back_to_main_menu_menu.add(back_to_main_menu_button, next_button)

see_finding_user_profile = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
see_finding_user_profile.add(back_to_main_menu_button, next_button)

understand_menu = ReplyKeyboardMarkup(resize_keyboard=True)
i_understand = KeyboardButton(text='Понятно')
understand_menu.add(i_understand)

ending_creating_project_menu = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
recreate_project = KeyboardButton(text='Заполнить заново')
change_img = KeyboardButton(text='Изменить медиа')
change_name = KeyboardButton(text='Изменить название')
change_description = KeyboardButton(text='Изменить описание')
change_categories = KeyboardButton('Изменить все категории')
change_price = KeyboardButton(text='Изменить вознаграждение')
send_button = KeyboardButton(text='Отправить')
ending_creating_project_menu.add(recreate_project, change_img, change_name, change_description, change_categories, change_price, back_button ,back_to_main_menu_button, send_button)

# new_menu = Markup

admin_accept_menu = InlineKeyboardMarkup(resize_keyboard=True, row_width=1)
accept_projects = InlineKeyboardButton(text='Проекты', callback_data='admin_accept_project')
accept_warn_project = InlineKeyboardButton(text='Жалобы', callback_data='admin_accept_warn')
accept_tasks = InlineKeyboardButton(text='Задачи', callback_data='admin_accept_task')
accept_questions = InlineKeyboardButton(text='Вопросы', callback_data='admin_accept_questions')
admin_accept_menu.add(accept_projects, accept_tasks, accept_questions, accept_warn_project)

#BEGIN ADMIN PANEL
main_menu_apanel = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
main_menu_apanel.add(create, find, responses, in_work, favorites)
main_menu_apanel.add(apanel)


partner_panel_menu = InlineKeyboardMarkup(row_width=1)
link = InlineKeyboardButton(text='Перейти.', url="https://t.me/Koworking_Partner_bot")
partner_panel_menu.add(link)


admin_panel_1_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
accept = KeyboardButton(text='Подтвердить')
administrate = KeyboardButton(text='Управление')
admin_panel_1_menu.add(accept)


admin_panel_2_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
admin_panel_2_menu.add(accept, administrate)

admin_accept_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
accept_project = _project
accept_question = _question
accept_verification = KeyboardButton(text='✔️ Верификация')
admin_accept_menu.add(accept_project, accept_question, accept_verification)

#END ADMIN PANEL


accept_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
accept = KeyboardButton(text='Подтвердить')
accept_menu.add(accept, back_button)

remove_reply_keyboard = ReplyKeyboardRemove()





event_menu = ReplyKeyboardMarkup(resize_keyboard=True)
next = KeyboardButton('Дальше ➤')
to_main = KeyboardButton('🏠 На главную')
event_menu.add(next, to_main)


select_category_for_profile = ReplyKeyboardMarkup(row_width=2)
painter = KeyboardButton(text='Художник')
smm =  KeyboardButton(text='СММ Специалист')
photograph =  KeyboardButton(text='Фотограф')
videograph =  KeyboardButton(text='Видеограф')
operator =  KeyboardButton(text='Оператор')
music =  KeyboardButton(text='Музыкант')
sound_eding =  KeyboardButton(text='Звукорежисер')
singer =  KeyboardButton(text='Певец')
choreographer =  KeyboardButton(text='Хореограф')
dancer =  KeyboardButton(text='Танцовщик')
sculptor =  KeyboardButton(text='Скульптор')
interior_designer =  KeyboardButton(text='Дизайнер интерьера')
architect =  KeyboardButton(text='Архитектор')
game_designer =  KeyboardButton(text='Гейм-дизайнер')
graphic_designer =  KeyboardButton(text='Графический дизайн')
web_designer =  KeyboardButton(text='Веб-дизайнер')
сlothes_designer =  KeyboardButton(text='Дизайнер одежды')
art_director =  KeyboardButton(text='Арт-директор')
journalist =  KeyboardButton(text='Журналист')
poet =  KeyboardButton(text='Поэт')
writer =  KeyboardButton(text='Писатель')
screenwriter =  KeyboardButton(text='Сценарист')
producer_r =  KeyboardButton(text='Режиссер')
producer_p =  KeyboardButton(text='Продюсер')
lecturer =  KeyboardButton(text='Лектор')
coach =  KeyboardButton(text='Коуч')
coworker =  KeyboardButton(text='Коворкер')
leading =  KeyboardButton(text='Ведущий')
blogger =  KeyboardButton(text='Блогер')
actor =  KeyboardButton(text='Актер')
model =  KeyboardButton(text='Модель')
barman =  KeyboardButton(text='Бармен')
guest =  KeyboardButton(text='Гость')
select_category_for_profile.add(next_button)
select_category_for_profile.add(painter, smm, photograph, videograph, operator, music, sound_eding, singer, choreographer, dancer, sculptor, interior_designer, architect, game_designer, graphic_designer, web_designer, сlothes_designer, art_director, journalist, poet, writer, screenwriter, producer_r, producer_p, lecturer, coach, coworker, leading, blogger, actor, model, barman, guest)
select_category_for_profile.add(back_button)

select_category_for_project = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
category_1 = KeyboardButton(text='Категория 1')
category_2 = KeyboardButton(text='Категория 2')
category_3 = KeyboardButton(text='Категория 3')
category_4 = KeyboardButton(text='Категория 4')
select_category_for_project.add(next_button)
select_category_for_project.add(category_1, category_2, category_3, category_4)
select_category_for_project.add(back_button)


select_type_for_need_categories_of_project = ReplyKeyboardMarkup(row_width=1)
select_categories = KeyboardButton(text='Выбрать интересы')
without_select = KeyboardButton(text='Без выбора')
my_interests = KeyboardButton(text='Мои интересы')
select_type_for_need_categories_of_project.add(next_button)
select_type_for_need_categories_of_project.add(select_categories, without_select, my_interests)
select_type_for_need_categories_of_project.add(back_button)


select_type_of_payment_for_project = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
fix_price = KeyboardButton(text='Фикс цена без искажения')
intermediate_price = KeyboardButton(text='Размытый ценник')
without_price = KeyboardButton(text='Безвозмездное оказание услуги')
select_type_of_payment_for_project.add(next_button)
select_type_of_payment_for_project.add(fix_price, intermediate_price, without_price)
select_type_of_payment_for_project.add(back_button)

cancel_menu = ReplyKeyboardMarkup(row_width=1)
cancel = KeyboardButton(text='❌ Отмена')
cancel_menu.add(cancel)