from main.models import Users, Project, ProjectFiles
from .models import CreatingProject
import os
from pathlib import Path
from random import randint

CATEGORIES = ['категория 1', 'категория 2']
SUBCATEGORIES = {"категория 1":  ["Подкатегория 1.1", "Подкатегория 1.2" ], "категория 2":  ["Подкатегория 2.1", "Подкатегория 2.2" ] }
SUBSUBCATEGORIES = {"подкатегория 1.1": ["Подподкатегория 1.1.1", "Подподкатегория 1.1.2", ], "подкатегория 2.1": ["Подподкатегория 2.1.1", "Подподкатегория 2.1.2", ]}



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


def check_exist_category(category):
    if category.lower() in CATEGORIES:
        return True
    return False

def get_subcategories_by_category(category):
    if check_exist_category(category):
        return SUBCATEGORIES[f"{category.lower()}"]
    return ["Пусто..."]


def check_valid_subcategory(category, subcategory):
    if subcategory in SUBCATEGORIES[f"{category.lower()}"]:
        return True
    return False


def check_valid_price_no_more(price_no_more, currency):
    if len(price_no_more) > 10:
        print(1)
        return False
    if currency != "$" and currency != "₽":
        print(1)
        return False
    elif price_no_more.replace(" ", "").isdigit():
        return True
    print(price_no_more.replace(" ", ""))
    return False


def get_subsubcategories_by_subcategory(subcategory):
    
    if f'{subcategory.lower()}' in SUBSUBCATEGORIES:
        print(SUBSUBCATEGORIES[f"{subcategory.lower()}"])
        return SUBSUBCATEGORIES[f"{subcategory.lower()}"]   
    return None


def check_valid_subsubcategory(subcategory, subsubcategory):
    if f'{subsubcategory}' in SUBSUBCATEGORIES[f"{subcategory.lower()}"]:
        return True
    return False

def add_file_to_creating_project_files_db(telegram_id, file, extension):
    user_db = Users.objects.get(telegram_id=telegram_id)
    creating_project_db = CreatingProject.objects.get(creator=user_db)
    file_db = ProjectFiles(owner=user_db, file=file, extension=extension)
    file_db.file.name = f"{randint(1111111111, 9999999999)}.{extension}"
    file_db.save()
    if creating_project_db.file_1 == "" or creating_project_db.file_1 == None:
        creating_project_db.file_1 = file_db
    elif creating_project_db.file_2 == "" or creating_project_db.file_2 == None:
        creating_project_db.file_2 = file_db
    elif creating_project_db.file_3 == "" or creating_project_db.file_3 == None:
        creating_project_db.file_3 = file_db
    elif creating_project_db.file_4 == "" or creating_project_db.file_4 == None:
        creating_project_db.file_4 = file_db
    elif creating_project_db.file_5 == "" or creating_project_db.file_5 == None:
        creating_project_db.file_5 = file_db
    creating_project_db.save()


def get_creating_project_files(telegram_id, files_id):
    user_db = Users.objects.get(telegram_id=telegram_id)
    files = []
    for file_id in files_id:
        if ProjectFiles.objects.filter(owner=user_db, pk=file_id).exists():
            file_db = ProjectFiles.objects.get(owner=user_db, pk=file_id)
            files.append(file_db)
    return files

def delete_creating_project_file(telegram_id, file_id):

    user_db = Users.objects.get(telegram_id=telegram_id)
    creating_project_db = CreatingProject.objects.get(creator=user_db)
    if file_id == 1:
        if creating_project_db.file_1 != '' and creating_project_db.file_1 != None:
            path = f"{Path(__name__).resolve().parent}{creating_project_db.file_1.file.url}".replace("\\", "/")
            os.remove(path)
            id = creating_project_db.file_1.pk
            ProjectFiles.objects.filter(pk=id).delete()
    if file_id == 2:
        if creating_project_db.file_2 != '' and creating_project_db.file_2 != None:
            path = f"{Path(__name__).resolve().parent}{creating_project_db.file_2.file.url}".replace("\\", "/")
            os.remove(path)
            id = creating_project_db.file_2.pk
            ProjectFiles.objects.filter(pk=id).delete()
    if file_id == 3:
        if creating_project_db.file_3 != '' and creating_project_db.file_3 != None:
            path = f"{Path(__name__).resolve().parent}{creating_project_db.file_3.file.url}".replace("\\", "/")
            os.remove(path)
            id = creating_project_db.file_3.pk
            ProjectFiles.objects.filter(pk=id).delete()    
    if file_id == 4:
        if creating_project_db.file_4 != '' and creating_project_db.file_4 != None:
            path = f"{Path(__name__).resolve().parent}{creating_project_db.file_4.file.url}".replace("\\", "/")
            os.remove(path)
            id = creating_project_db.file_4.pk
            ProjectFiles.objects.filter(pk=id).delete()
    if file_id == 5:
        if creating_project_db.file_5 != '' and creating_project_db.file_5!= None:
            path = f"{Path(__name__).resolve().parent}{creating_project_db.file_5.file.url}".replace("\\", "/")
            os.remove(path)
            id = creating_project_db.file_2.pk
            ProjectFiles.objects.filter(pk=id).delete()


def final_check_list(db):
    errors = {}
    if db.name == "":
        errors["name"] = "Заполните поле Название"
    
    if db.description == "":
        errors["description"] = "Заполните поле Описание"
    
    if db.type == "":
        errors["type"] = "Выберите тип проекта"
    
    if db.category == "":
        errors["category"] = "Выберите категорию проекта"
    
    if db.subcategory == "":
        errors["subcategory"] = "Выберите подкатегорию проекта"

    else:

        if db.subcategory.lower() in SUBSUBCATEGORIES:
            if db.subsubcategory == "":
                errors["subsubcategory"] = "Выберите подподкатегорию проекта"

    
    if db.employee_interests == "":
        errors["employee_interests"] = "Выберите от одного до трех интересов исполнителя проекта"
    else:
        if eval(db.employee_interests)[0] == "" and eval(db.employee_interests)[1] == "" and eval(db.employee_interests)[2] == "":
            errors["employee_interests"] = "Выберите от одного до трех интересов исполнителя проекта"
    
    if db.price_no_more == "":
        errors["price_no_more"] = "Введите цену за проект"

    return errors
    

def create_project(telegram_id, db):
    user_db = Users.objects.get(telegram_id=telegram_id)
    project_db = Project()
    project_db.creator = user_db
    project_db.name = db.name
    project_db.description = db.description
    project_db.type = db.type
    project_db.category = db.category
    project_db.subcategory = db.subcategory
    project_db.subsubcategory = db.subsubcategory
    project_db.employee_interests = db.employee_interests
    project_db.price_no_more = db.price_no_more
    project_db.enable_price_upper = db.enable_price_upper
    project_db.file_1 = db.file_1
    project_db.file_2 = db.file_2
    project_db.file_3 = db.file_3
    project_db.file_4 = db.file_4
    project_db.file_5 = db.file_5
    project_db.save()
    db.delete()