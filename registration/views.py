import sys
from django.shortcuts import render, redirect
from main.models import Users, UserSettings
from random import randint
from . import forms
from . import funcs
# Create your views here.



def index(request):


    if 'telegram_id' in request.GET and 'secret_key' in request.GET:
        request.session["secret_key"] = request.GET['secret_key']
        if 'telegram_id' in request.session:
            pass
        else:
            request.session["telegram_id"] = request.GET['telegram_id']
            
    if 'telegram_id' in request.session and 'secret_key' in request.session:
        if funcs.check_exist_user(telegram_id=request.session["telegram_id"], secret_key=request.session["secret_key"]) == None: #Проверка на наличие записи с юзером с таким id
            return render(request, "errors/invalid_secret_key.html")
        if funcs.check_secret_key(id=request.session["telegram_id"], secret_key=request.session["secret_key"]) == False:
            return render(request, "errors/invalid_secret_key.html")
        
        db = Users.objects.get(telegram_id=request.session["telegram_id"])
        if db.select == 'registration':
            if 'enter_userphoto.x' in request.POST and 'enter_userphoto.y' in request.POST:
                request.POST = {}
                form = forms.UserPhoto()
                context = {
                    "form": form,
                }
                return render(request, "registration/userphoto.html", context=context)
            
            elif 'UserPhotoForm' in request.POST:
                db = Users.objects.get(telegram_id=request.session["telegram_id"])
                form = forms.UserPhoto(request.POST, request.FILES)
                if form.is_valid():
                    userphoto = form.cleaned_data.get("userphoto")
                    funcs.delete_last_userphoto_from_disk(db)
                    db.img = userphoto
                    filename = f"{randint(1111111111, 9999999999)}.png"
                    db.img.name = filename
                    db.save()
                request.POST = {}
                context = {
                    "userinfo": funcs.get_userinfo_for_registration(db)
                }
                return render(request, "registration/index.html", context=context)

            elif 'enter_name_surname' in request.POST:
                request.POST = {}
                form = forms.NameSurnameForm()
                context = {
                    "form": form,
                }
                return render(request, "registration/name_surname.html", context=context)

            elif 'NameSurnameForm' in request.POST:
                error = ''
                form = forms.NameSurnameForm(request.POST)
                db = Users.objects.get(telegram_id=request.session["telegram_id"])
                if funcs.check_valid_name_surname(form.data.get("name_surname")):
                    db.name_surname = form.data.get("name_surname")
                    db.save()
                    request.POST = {}
                    context = {
                        "userinfo": funcs.get_userinfo_for_registration(db)
                    }
                    return render(request, "registration/index.html", context=context)
                else:
                    error = 'Введите корректное Имя Фамилию'
                form = forms.NameSurnameForm()
                context = {
                    "form": form,
                    "error": error
                }
                return render(request, "registration/name_surname.html", context=context)

            elif 'enter_date_birth' in request.POST:
                form = forms.DateBirthForm()
                context = {
                    "form": form,
                }
                request.POST = {}
                return render(request, "registration/date_birth.html", context=context)

            elif 'DateBirthForm' in request.POST:
                error = ''
                form = forms.NameSurnameForm(request.POST)
                db = Users.objects.get(telegram_id=request.session["telegram_id"])
                if funcs.check_valid_date(str(form.data.get("date_birth"))):
                    if funcs.check_age_by_date(str(form.data.get("date_birth"))):
                        db.date_birth = str(form.data.get("date_birth"))
                        db.save()
                        context = {
                            "userinfo": funcs.get_userinfo_for_registration(db)
                        }
                        request.POST = {}
                        return render(request, "registration/index.html", context=context)
                    else:
                        error = 'Наш сервис открыт для пользователей от 16 лет'
                else:
                    error = 'Введите корректную дату в формате ДД.ММ.ГГГГ'
                form = forms.DateBirthForm()
                context = {
                    "form": form,
                    "error": error
                }
                return render(request, "registration/date_birth.html", context=context)
            
            elif 'enter_city' in request.POST:
                error = ''
                context = {
                    "error": error
                }
                request.POST = {}
                return render(request, "registration/city.html", context=context)
            
            elif 'CityForm' in request.POST and 'city_name' in request.POST:
                error = ''
                db = Users.objects.get(telegram_id=request.session["telegram_id"])
                if funcs.check_valid_city(str(request.POST["city_name"])):
                    db.city = str(request.POST["city_name"])
                    db.save()
                    context = {
                        "userinfo": funcs.get_userinfo_for_registration(db)
                    }
                    return render(request, "registration/index.html", context=context)
                else:
                    error = 'Ошибка'
                context = {
                    "error": error
                }
                return render(request, "registration/city.html", context=context)
            
            elif 'enter_category' in request.POST:
                form = forms.CategoryForm()
                error = ''
                context = {
                    "error": error,
                    "form": form
                }
                return render(request, "registration/category.html", context=context)
            

            elif 'CategoryForm' in request.POST and 'category' in request.POST:
                error = ''
                db = Users.objects.get(telegram_id=request.session["telegram_id"])
                if funcs.check_valid_category(request.POST["category"]):
                    db.category = request.POST["category"]
                    db.save()
                    context = {
                        "userinfo": funcs.get_userinfo_for_registration(db)
                    }
                    request.POST = {}
                    return render(request, "registration/index.html", context=context)
                
                form = forms.CategoryForm()
                error = 'Выберите одну категорию из списка'
                context = {
                    "error": error,
                    "form": form
                }
                return render(request, "registration/category.html", context=context)
            

            elif 'enter_subcategories' in request.POST:
                form = forms.SubCategoriesForm()
                error = ''
                context = {
                    "error": error,
                    "form": form
                }
                return render(request, "registration/subcategories.html", context=context)
            

            elif 'SubCategoriesForm' in request.POST:
                form = forms.SubCategoriesForm(request.POST)
                error = 'Постарайтесь ввести все верно'
                if form.is_valid():
                    if len(form.cleaned_data["subcategories"]) >= 1 and len(form.cleaned_data["subcategories"]) <= 4:
                        if funcs.check_valid_subcategories(form.cleaned_data["subcategories"]):
                            db = Users.objects.get(telegram_id=request.session["telegram_id"])
                            subcategories = ''
                            for subcategory in form.cleaned_data["subcategories"]:
                                subcategories = f"{subcategories}{subcategory} "
                            db.subcategories = subcategories
                            db.save()
                            context = {
                                "userinfo": funcs.get_userinfo_for_registration(db)
                            }
                            request.POST = {}
                            return render(request, "registration/index.html", context=context)
                        else:
                            error = 'Выберите из представленных подкатегорий'
                    else:
                        error = 'Выберите от одной подкатегории до четырех подкатегорий'
                context = {
                    "error": error,
                    "form": form
                }
                return render(request, "registration/subcategories.html", context=context)


            elif 'enter_interests' in request.POST:
                form = forms.InterestsForm()
                error = ''
                context = {
                    "error": error,
                    "form": form
                }
                return render(request, "registration/interests.html", context=context)
            

            elif 'InterestsForm' in request.POST:
                form = forms.InterestsForm(request.POST)
                error = 'Постарайтесь ввести все верно'
                if form.is_valid():
                    if len(form.cleaned_data["interests"]) >= 1 and len(form.cleaned_data["interests"]) <= 7:
                        if funcs.check_valid_interests(form.cleaned_data["interests"]):
                            db = Users.objects.get(telegram_id=request.session["telegram_id"])
                            interests = ''
                            for interest in form.cleaned_data["interests"]:
                                interests = f"{interests}{interest} "
                            db.interests = interests
                            db.save()
                            context = {
                                "userinfo": funcs.get_userinfo_for_registration(db)
                            }
                            request.POST = {}
                            return render(request, "registration/index.html", context=context)
                        else:
                            error = 'Выберите из представленных интересов'
                    else:
                        error = 'Выберите от одного интереса до семи интересов'
                context = {
                    "error": error,
                    "form": form
                }
                return render(request, "registration/interests.html", context=context)


            elif 'enter_description' in request.POST:
                error = ''
                db = Users.objects.get(telegram_id=request.session["telegram_id"])
                context = {
                    "userinfo": funcs.get_userinfo_for_fields(db),
                    "error": error,
                }
                request.POST = {}
                return render(request, "registration/description.html", context=context)
            
            elif 'DescriptionForm' in request.POST:
                error = ''
                db = Users.objects.get(telegram_id=request.session["telegram_id"])
                if 'description' in request.POST:
                    if len(request.POST["description"]) > 10 and len(request.POST["description"]) < 600:
                        db.description = request.POST["description"]
                        db.save()
                        context = {
                            "error": error,
                            "userinfo": funcs.get_userinfo_for_registration(db)
                        }
                        request.POST = {}
                        return render(request, "registration/index.html", context=context)
                    else:
                        error = 'Длина описания должна быть от 10 до 600 символов'
                        db = Users.objects.get(telegram_id=request.session["telegram_id"])
                        context = {
                            "error": error,
                        }
                        request.POST = {}
                        return render(request, "registration/description.html", context=context)
                else:
                    error = 'Введите описание'
                    context = {
                        "error": error,
                    }
                    return render(request, "registration/description.html", context=context)
                
            
            elif 'enter_portfolio' in request.POST:
                error = ''
                db = Users.objects.get(telegram_id=request.session["telegram_id"])
                form = forms.PortfolioForm()
                context = {
                    "error": error,
                    "form": form,
                    "userinfo": funcs.get_userinfo_for_fields(db),
                }
                return render(request, "registration/portfolio.html", context=context)

            
            elif 'PortfolioForm' in request.POST:
                form = forms.PortfolioForm(request.POST)
                error = funcs.get_links_error(form)
                if error == None:
                    db = Users.objects.get(telegram_id=request.session["telegram_id"])
                    portfolio = funcs.get_dict_portfolio(form)
                    db.portfolio = portfolio
                    db.save()
                    context = {
                        "userinfo": funcs.get_userinfo_for_registration(db)
                    }
                    return render(request, "registration/index.html", context=context)
                else:
                    db = Users.objects.get(telegram_id=request.session["telegram_id"])
                    context = {
                        "error": error,
                        "form": form,
                        "userinfo": funcs.get_userinfo_for_fields(db),
                    }
                    return render(request, "registration/portfolio.html", context=context)
            

            elif 'accept' in request.POST:
                db = Users.objects.get(telegram_id=request.session["telegram_id"])
                error = funcs.check_full_registration_form(db)
                if error == None:
                    db.select = ""
                    db.save()
                    usersettings_db = UserSettings(user=db, save_cards="False")
                    usersettings_db.save()
                    return redirect("index")
                else:
                    context = {
                        "error": error,
                        "userinfo": funcs.get_userinfo_for_registration(db)
                    }
                    request.POST = {}
                    return render(request, "registration/index.html", context=context)
        elif db.select == 'banned':
            pass
        else:
            return redirect("index")

        
        db = Users.objects.get(telegram_id=request.session["telegram_id"])
        context = {
            "userinfo": funcs.get_userinfo_for_registration(db)
        }
        return render(request, "registration/index.html", context=context)
    else:
        return render(request, "errors/without_id_error.html")
