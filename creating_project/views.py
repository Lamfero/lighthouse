from django.shortcuts import render, redirect

from main.models import Users
from . import funcs
from . import forms
from .models import CreatingProject
# Create your views here.

ALLOWED_EXTENSIONS = ["pdf", "docx", "xlsx", "png", "jpg", "jpeg"]
EMPLOYEE_INTERESTS = ["Интерес 1", "Интерес 2", "Интерес 3", "Интерес 4", ""]

def index(request):

    for post in request.POST:
        print(post)
    if 'telegram_id' in request.GET and 'secret_key' in request.GET:
        request.session["secret_key"] = request.GET['secret_key']
        if 'telegram_id' in request.session:
            pass
        else:
            request.session["telegram_id"] = request.GET['telegram_id']


    if "telegram_id" in request.session and "secret_key" in request.session:
        telegram_id = request.session["telegram_id"]
        secret_key = request.session["secret_key"]
        
        
        if 'creating_project' not in request.session:
            request.session["creating_project"] = {}
        
        if 'files' not in request.session["creating_project"]:
            request.session["creating_project"]["files"] = []

        if 'enable_price_upper' not in request.session["creating_project"]:
            request.session["creating_project"]["enable_price_upper"] = "off"
        
        

        if funcs.check_exist_user(telegram_id=telegram_id, secret_key=secret_key):

            user_db = Users.objects.get(telegram_id=telegram_id)

            if CreatingProject.objects.filter(creator=user_db).exists() == False:
                creating_project_db = CreatingProject(creator=user_db)
                creating_project_db.save()
            else:
                creating_project_db = CreatingProject.objects.get(creator=user_db)
        
            context = {
                "projectinfo": { },
                "errors": {}
            }
            context["edit"] = "project_add_files"

            # Название
            if 'enter_project_name' in request.POST:
                context["edit"] = "project_name"
            elif 'project_name' in request.POST and 'enter_project_name.y' in request.POST:
                if len(request.POST["project_name"]) <= 30 and len(request.POST["project_name"]) >= 5:
                    creating_project_db.name = request.POST["project_name"]
                    creating_project_db.save()
                else:
                    context["edit"] = "project_name"
                    context["errors"]["name"] = "Длина от 5 до 30 символов"
            
            # Тип
            if 'enter_project_type' in request.POST:
                context["edit"] = "project_type"
            elif 'project_type_online' in request.POST:
                creating_project_db.type = 'Онлайн'
                creating_project_db.save()
            elif 'project_type_offline' in request.POST:
                creating_project_db.type = 'Оффлайн'
                creating_project_db.save()
            
            # Категория
            if 'enter_project_category' in request.POST:
                context["edit"] = "project_category"
            elif 'project_category' in request.POST and 'enter_project_category.y' in request.POST:
                if funcs.check_exist_category(category=request.POST["project_category"]):
                    if creating_project_db.category != request.POST["project_category"]:
                        creating_project_db.subcategory = ""
                    creating_project_db.category = request.POST["project_category"]
                    creating_project_db.save()
                else:
                    context["edit"] = "project_category"
                    context["errors"]["category"] = "Выберите из списка"
            
            # Подкатегория
            if 'enter_project_subcategory' in request.POST:
                
                if creating_project_db.category != "":
                    context["edit"] = "project_subcategory"
                    context["subcategories"] = funcs.get_subcategories_by_category(category=creating_project_db.category)
                else:
                    context["edit"] = "project_category"
                    context["errors"]["category"] = "Выберите вначале Категорию"
            elif 'project_subcategory' in request.POST and 'enter_project_subcategory.y' in request.POST:
                if funcs.check_valid_subcategory(category=creating_project_db.category, subcategory=request.POST["project_subcategory"]):
                    if creating_project_db.subcategory != "":
                        if creating_project_db.subcategory != request.POST["project_subcategory"]:
                            creating_project_db.subsubcategory = ""
                    creating_project_db.subcategory = request.POST["project_subcategory"]
                    creating_project_db.save()
                else:
                    if creating_project_db.category != "":
                        context["edit"] = "project_subcategory"
                        context["subcategories"] = funcs.get_subcategories_by_category(category=creating_project_db.category)
                        context["errors"]["subcategory"] = "Выберите из списка"
         
            # Подподкатегория
            if 'enter_project_subsubcategory' in request.POST:
                
                if creating_project_db.subcategory != "":
                     
                    context["edit"] = "project_subsubcategory"
                     
                else:
                    context["edit"] = "project_category"
                    context["errors"]["subcategory"] = "Выберите вначале Подкатегорию"
            elif 'project_subsubcategory' in request.POST and 'enter_project_subsubcategory.y' in request.POST:
                if funcs.check_valid_subsubcategory(subcategory=creating_project_db.subcategory, subsubcategory=request.POST["project_subsubcategory"]):
                    creating_project_db.subsubcategory = request.POST["project_subsubcategory"]
                    creating_project_db.save()
                else:
                    if creating_project_db.subcategory != "":
                        context["edit"] = "project_subsubcategory"
                        context["subcategories"] = funcs.get_subsubcategories_by_subcategory(subcategory=creating_project_db.subcategory)
                        context["errors"]["subsubcategory"] = "Выберите из списка"

            # Описание
            if 'enter_project_description' in request.POST:
                context["edit"] = "project_description"
            elif 'project_description' in request.POST and 'enter_project_description.y' in request.POST:
                if len(request.POST["project_description"]) <= 300 and len(request.POST["project_description"]) >= 5:
                    creating_project_db.description = request.POST["project_description"]
                    creating_project_db.save()
                else:
                    context["edit"] = "project_description"
                    context["errors"]["description"] = "Длина от 5 до 300 символов"

            # Интересы исполнителя
            if 'enter_project_employee_interests' in request.POST:
                context["edit"] = "project_employee_interests"
                context["employee_interests"] = EMPLOYEE_INTERESTS
            elif 'project_employee_interest_1' in request.POST and 'project_employee_interest_2' in request.POST and 'project_employee_interest_3' in request.POST and 'enter_project_employee_interests.y' in request.POST:
                if request.POST["project_employee_interest_1"] in EMPLOYEE_INTERESTS and request.POST["project_employee_interest_2"] in EMPLOYEE_INTERESTS and request.POST["project_employee_interest_3"] in EMPLOYEE_INTERESTS:
                    coincidences = False
                    if request.POST["project_employee_interest_1"] !=  "" and request.POST["project_employee_interest_2"] != "":
                        if request.POST["project_employee_interest_1"] == request.POST["project_employee_interest_2"]:
                            coincidences = True
                    if request.POST["project_employee_interest_1"] !=  "" and request.POST["project_employee_interest_3"] != "":
                        if request.POST["project_employee_interest_1"] == request.POST["project_employee_interest_3"]:
                            coincidences = True
                    if request.POST["project_employee_interest_2"] !=  "" and request.POST["project_employee_interest_3"] != "":
                        if request.POST["project_employee_interest_2"] == request.POST["project_employee_interest_3"]:
                            coincidences = True
                    if coincidences == False:
                        creating_project_db.employee_interests = [request.POST["project_employee_interest_1"], request.POST["project_employee_interest_2"], request.POST["project_employee_interest_3"]]
                        creating_project_db.save()
                    else:
                        context["edit"] = "project_employee_interests"
                        context["employee_interests"] = EMPLOYEE_INTERESTS
                        context["errors"]["employee_interests"] = "Интересы не должны совпадать"
                else:
                    context["edit"] = "project_employee_interests"
                    context["employee_interests"] = EMPLOYEE_INTERESTS
                    context["errors"]["employee_interests"] = "Ошибка"

            # Цена не более
            if 'enter_project_price_no_more' in request.POST:
                context["edit"] = "project_price_no_more"
            elif 'project_price_no_more' in request.POST and 'currency' in request.POST and 'enter_project_price_no_more.y' in request.POST:
                if funcs.check_valid_price_no_more(price_no_more=request.POST["project_price_no_more"], currency=request.POST["currency"]):
                    creating_project_db.price_no_more = request.POST["project_price_no_more"]
                    creating_project_db.currency = request.POST["currency"]
                    creating_project_db.save()
                    
                else:
                    context["edit"] = "project_price_no_more"
                    context["errors"]["price_no_more"] = 'Введите все верно. Кроме символа валюты "$" или "₽" не должно быть что-то кроме цифр' 

            # Добавить файлы
            if 'enter_project_add_files' in request.POST:
                context["edit"] = "project_add_files"

            if 'enable_price_upper' in request.POST:
                if request.POST["enable_price_upper"] == "on":
                    creating_project_db.enable_price_upper = "on"
                elif request.POST["enable_price_upper"] == "off":
                    creating_project_db.enable_price_upper = "off"
                creating_project_db.save()

            
            if creating_project_db.subcategory != "":
                context["subsubcategories"] = funcs.get_subsubcategories_by_subcategory(creating_project_db.subcategory)
            else:
                context["subsubcategories"] = None
            
            if 'file' in request.FILES:
                form = forms.FileInputForm(request.POST, request.FILES)
                if form.is_valid():
                    if str(form.cleaned_data.get("file")).rsplit(".")[1] in ALLOWED_EXTENSIONS:
                        if creating_project_db.file_1 == "" or creating_project_db.file_1 == None:
                            funcs.add_file_to_creating_project_files_db(telegram_id=request.session["telegram_id"], file=form.cleaned_data.get("file"), extension=str(form.cleaned_data.get("file")).rsplit(".")[1])
                        elif creating_project_db.file_2 == "" or creating_project_db.file_2 == None:
                            funcs.add_file_to_creating_project_files_db(telegram_id=request.session["telegram_id"], file=form.cleaned_data.get("file"), extension=str(form.cleaned_data.get("file")).rsplit(".")[1])
                        elif creating_project_db.file_3 == "" or creating_project_db.file_3 == None:
                            funcs.add_file_to_creating_project_files_db(telegram_id=request.session["telegram_id"], file=form.cleaned_data.get("file"), extension=str(form.cleaned_data.get("file")).rsplit(".")[1])
                        elif creating_project_db.file_4 == "" or creating_project_db.file_4 == None:
                            funcs.add_file_to_creating_project_files_db(telegram_id=request.session["telegram_id"], file=form.cleaned_data.get("file"), extension=str(form.cleaned_data.get("file")).rsplit(".")[1])
                        elif creating_project_db.file_5 == "" or creating_project_db.file_5 == None:
                            funcs.add_file_to_creating_project_files_db(telegram_id=request.session["telegram_id"], file=form.cleaned_data.get("file"), extension=str(form.cleaned_data.get("file")).rsplit(".")[1])
                        else:
                            context["errors"]["enter_project_add_files"] = "Не более 5 файлов"
                        return redirect('creating_project')
                    else:
                        context["errors"]["enter_project_add_files"] = "Недопустимый формат файла. Разрешенные форматы .pdf .docx .xlsx .png .jpg .jpeg"
                
                context["edit"] = "project_add_files"
            
            if 'delete_file_1.y' in request.POST:
                funcs.delete_creating_project_file(telegram_id=telegram_id, file_id=1)
                context["edit"] = "project_add_files"
            elif 'delete_file_2.y' in request.POST:
                funcs.delete_creating_project_file(telegram_id=telegram_id, file_id=2)
                context["edit"] = "project_add_files"
            elif 'delete_file_3.y' in request.POST:
                funcs.delete_creating_project_file(telegram_id=telegram_id, file_id=3)
                context["edit"] = "project_add_files"
            elif 'delete_file_4.y' in request.POST:
                funcs.delete_creating_project_file(telegram_id=telegram_id, file_id=4)
                context["edit"] = "project_add_files"
            elif 'delete_file_5.y' in request.POST:
                funcs.delete_creating_project_file(telegram_id=telegram_id, file_id=5)
                context["edit"] = "project_add_files"

            if 'accept' in request.POST:
                errors = funcs.final_check_list(db=creating_project_db)
                print(errors)
                if len(errors) == 0:
                    funcs.create_project(telegram_id=telegram_id, db=creating_project_db)
                
                    return redirect('index')
                else:
                    context["final_check_list_errors"] = errors

            creating_project_db = CreatingProject.objects.get(creator=user_db)
            context["form"] = forms.FileInputForm()
            context["files"] = creating_project_db
            context["projectinfo"] = creating_project_db
            if creating_project_db.employee_interests != "":
                context["user_interests"] = eval(str(creating_project_db.employee_interests))
            else:
                context["user_interests"] = None
            return render(request, "creating_project/index.html", context=context)
            

            

            
            
        else:
            return render(request, "errors/invalid_secret_key.html")
    else:
        return render(request, "errors/without_id_error.html")


 