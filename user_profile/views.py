
from xmlrpc.client import boolean
from django.shortcuts import render, redirect
from . import funcs
from . import forms
from main.models import Users, DiplomsSertificats, Service
from random import randint
# Create your views here

def view_user_profile_by_telegram_id_by_owner(request):

    if 'telegram_id' in request.GET and 'secret_key' in request.GET:
        request.session["secret_key"] = request.GET['secret_key']
        if 'telegram_id' in request.session:
            pass
        else:
            request.session["telegram_id"] = request.GET['telegram_id']


    if "telegram_id" in request.session and "secret_key" in request.session:
        telegram_id = request.session["telegram_id"]
        secret_key = request.session["secret_key"]
        if funcs.check_exist_user(telegram_id=telegram_id, secret_key=secret_key):
            db = Users.objects.get(telegram_id=telegram_id)

            # for post in request.POST:
            #     print(post)
            
            if 'back' in request.POST:
                if 'savecards' in request.POST:
                    if request.POST["savecards"] == "no":
                        funcs.update_user_settings_save_cards(telegram_id, "False")
                    elif request.POST["savecards"] == "yes":
                        funcs.update_user_settings_save_cards(telegram_id, "True")
                
                context = {
                    "cards": funcs.get_user_cards(telegram_id=telegram_id),
                    "usersettings_save_cards": funcs.get_user_settings_save_cards(telegram_id)
                }
                context = {
                    "userinfo": funcs.get_userinfo_by_telegram_id_by_owner(telegram_id=telegram_id)
                }
                return render(request, "user_profile/view_user_profile_by_telegram_id_by_owner.html", context=context)



            elif 'verification' in request.POST or 'back_to_verification' in request.POST:
                context = {
                    "error": ''
                }
                return render(request, "user_profile/verification.html", context=context)
            


            elif 'view_status' in request.POST:
                context = {
                "userinfo": funcs.get_userinfo_by_telegram_id_by_owner(telegram_id=telegram_id)
                }
                return render(request, "user_profile/view_status.html", context=context)
            


            elif 'verification_with_sber_id' in request.POST:
                context = {
                    "error": ''
                }
                return render(request, "user_profile/verification_with_sber_id.html", context=context)
            


            elif 'verification_with_gosservice' in request.POST:
                context = {
                    "error": ''
                }
                return render(request, "user_profile/verification_with_gosservice.html", context=context)
            


            elif 'verification_with_documents' in request.POST:
                context = {
                    "error": ''
                }
                return render(request, "user_profile/verification_with_documents.html", context=context)



            elif 'my_cards' in request.POST:
                context = {
                    "cards": funcs.get_user_cards(telegram_id=telegram_id),
                    "usersettings_save_cards": funcs.get_user_settings_save_cards(telegram_id)
                }
                return render(request, "user_profile/my_cards.html", context=context)


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
                    "userinfo": funcs.get_userinfo_by_telegram_id_by_owner(telegram_id=telegram_id)
                    }
                    return render(request, "user_profile/view_user_profile_by_telegram_id_by_owner.html", context=context)
                else:
                    error = 'Необходимо выбрать метку в городе. Постарайтесь поставить метку как можно ближе к центру необходимого населенного пункта.'
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
                            "userinfo": funcs.get_userinfo_by_telegram_id_by_owner(telegram_id=telegram_id)
                        }
                        request.POST = {}
                        return render(request, "user_profile/view_user_profile_by_telegram_id_by_owner.html", context=context)
                    
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
                                "userinfo": funcs.get_userinfo_by_telegram_id_by_owner(telegram_id=telegram_id)
                            }
                            request.POST = {}
                            return render(request, "user_profile/view_user_profile_by_telegram_id_by_owner.html", context=context)
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
                                "userinfo": funcs.get_userinfo_by_telegram_id_by_owner(telegram_id=telegram_id)
                            }
                            request.POST = {}
                            return render(request, "user_profile/view_user_profile_by_telegram_id_by_owner.html", context=context)
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
                            "userinfo": funcs.get_userinfo_by_telegram_id_by_owner(telegram_id=telegram_id)
                        }
                        request.POST = {}
                        return render(request, "user_profile/view_user_profile_by_telegram_id_by_owner.html", context=context)
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
                    redirect("profile")
                else:
                    db = Users.objects.get(telegram_id=request.session["telegram_id"])
                    context = {
                        "error": error,
                        "form": form
                    }
                    return render(request, "registration/portfolio.html", context=context)
            


            elif 'view_service' in request.POST:
                context = {
                    "info": funcs.get_info_about_user_service(telegram_id=telegram_id)
                }
                return render(request, "user_profile/view_service_by_owner.html", context=context)
            

            elif 'add_service.x' in request.POST:
                form = forms.ServiceForm()
                context = {
                    "form": form,
                    "error": '' 
                }
                return render(request, "user_profile/add_service.html", context=context)


            elif 'add_new_service' in request.POST:
                form = forms.ServiceForm(request.POST, request.FILES)
                if form.is_valid():
                    if 'title_of_service' in request.POST and 'purpose_of_service' in request.POST:
                        if len(request.POST["title_of_service"]) >= 5  and len(request.POST["title_of_service"]) <= 50:
                            if len(request.POST["purpose_of_service"]) >= 10  and len(request.POST["purpose_of_service"]) <= 500:
                                service_image = form.cleaned_data.get("service_image")
                                service_db = Service(user=db)
                                service_db.save()
                                service_db.title = request.POST["title_of_service"]
                                service_db.purpose = request.POST["purpose_of_service"]
                                service_db.image = service_image
                                filename = f"{randint(1111111111, 9999999999)}.png"
                                service_db.image.name = filename
                                service_db.save()
                                return redirect("profile")
                            else:
                                error = 'Длина описания может быть от 10 до 500 символов'
                        else:
                            error = 'Длина названия может быть от 5 до 50 символов'
                else:
                    error = 'Выберите изображение'
                context = {
                    "form": form,
                    "error": error 
                }
                return render(request, "user_profile/add_service.html", context=context)

            
            elif 'delete_service.x' in request.POST and 'service_id' in request.POST:
                if Service.objects.filter(user = db, pk=request.POST["service_id"]).exists():
                    service_db = Service.objects.get(user = db, pk=request.POST["service_id"])
                    funcs.delete_service_photo(service_db)
                    service_db.delete()
                context = {
                    "info": funcs.get_info_about_user_service(telegram_id=telegram_id)
                }
                return render(request, "user_profile/view_service_by_owner.html", context=context)


            elif 'edit_diploms_and_sertificats' in request.POST:
                request.POST = {}
                context = {
                    "userinfo": funcs.get_diploms_and_sertificats_files(telegram_id=telegram_id)
                }
                return render(request, "user_profile/edit_diploms_and_sertificats.html", context=context)
            

            elif 'add_diploms_and_sertificats.x' in request.POST and 'add_diploms_and_sertificats.y' in request.POST:
                request.POST = {}
                context = {
                    "form": forms.DiplomsSertificatsForm(),
                    "userinfo": funcs.get_diploms_and_sertificats_files(telegram_id=telegram_id)
                }
                return render(request, "user_profile/add_diploms_and_sertificats.html", context=context)
            

            elif 'add_new_diplom' in request.POST:
                form = forms.DiplomsSertificatsForm(request.POST, request.FILES)
                if form.is_valid():
                    if "name_of_doc" in request.POST:
                        if len(request.POST["name_of_doc"]) >= 5 and len(request.POST["name_of_doc"]) <= 30:
                            diplom = form.cleaned_data.get("diplom")
                            diplom_db = DiplomsSertificats(user=db)
                            diplom_db.save()
                            diplom_db.text = request.POST["name_of_doc"]
                            diplom_db.img = diplom
                            filename = f"{randint(1111111111, 9999999999)}.png"
                            diplom_db.img.name = filename
                            diplom_db.save()
                            return redirect("profile")
                        else:
                            error = 'Длина названия должна быть от 5 до 30 символов'
                    else:
                        error = ''
                else:
                    error = "Выберите файл"
                context = {
                "form": form,
                "userinfo": funcs.get_diploms_and_sertificats_files(telegram_id=telegram_id),
                "error": error
                }
                return render(request, "user_profile/add_diploms_and_sertificats.html", context=context)
            

            elif 'delete_diplom.x' in request.POST and 'diplom_id' in request.POST:
                if DiplomsSertificats.objects.filter(user = db, pk=request.POST["diplom_id"]).exists():
                    diplom_db = DiplomsSertificats.objects.get(user = db, pk=request.POST["diplom_id"])
                    funcs.delete_diplom_photo(diplom_db)
                    diplom_db.delete()
                    request.POST = {}
                context = {
                    "userinfo": funcs.get_diploms_and_sertificats_files(telegram_id=telegram_id)
                }
                return render(request, "user_profile/edit_diploms_and_sertificats.html", context=context)
            

            elif 'view_feedbacks' in request.POST:
                feedbacks = funcs.get_feedbacks_list(telegram_id=telegram_id)
                context = {
                    "feedbacks": feedbacks,
                }
                return render(request, "user_profile/view_feedback_by_owner.html", context=context)
            


            elif 'bankdetails' in request.POST:
                return render(request, "user_profile/add_new_bank_card.html")\
            

            elif 'back_to_main_page' in request.POST:
                return redirect("index")

            


            context = {
                "userinfo": funcs.get_userinfo_by_telegram_id_by_owner(telegram_id=telegram_id)
            }
            return render(request, "user_profile/view_user_profile_by_telegram_id_by_owner.html", context=context)
        
        else:
            return render(request, "user_profile/no_such_user.html")
    else:
        return render(request, "errors/without_id_error.html")


def view_user_profile_by_telegram_id_from_outside(request, telegram_id_for_view):

    if 'telegram_id' in request.GET and 'secret_key' in request.GET:
        request.session["secret_key"] = request.GET['secret_key']
        if 'telegram_id' in request.session:
            pass
        else:
            request.session["telegram_id"] = request.GET['telegram_id']
        
    if 'telegram_id' in request.session and 'secret_key' in request.session:
        if funcs.check_exist_user(telegram_id=request.session["telegram_id"], secret_key=request.session["secret_key"]) == None: #Проверка на наличие записи с юзером с таким id
            return render(request, "errors/invalid_secret_key.html")


    if funcs.check_exist_user_for_view(telegram_id=telegram_id_for_view):
        if "telegram_id" in request.session and "secret_key" in request.session:
            telegram_id = request.session["telegram_id"]
            funcs.set_view_by_user(telegram_id, view_telegram_id=telegram_id_for_view)
            if 'view_portfolio' in request.POST:
                portfolio = funcs.get_user_portfolio(telegram_id=telegram_id)
                context = {
                    "portfolio": portfolio
                }
                return render(request, "user_profile/view_portfolio.html", context=context)

                
            elif 'view_diploms' in request.POST:
                context = {
                    "userinfo": funcs.get_diploms_and_sertificats_files(telegram_id=telegram_id_for_view)
                }
                return render(request, "user_profile/view_user_diploms_by_outside.html", context=context)
            

            elif 'view_feedbacks' in request.POST:
                feedbacks = funcs.get_feedbacks_list(telegram_id=telegram_id_for_view)
                context = {
                    "feedbacks": feedbacks,
                }
                return render(request, "user_profile/view_feedback_from_outside.html", context=context)
            

            elif 'view_service' in request.POST:
                context = {
                    "info": funcs.get_info_about_user_service(telegram_id=telegram_id_for_view),
                }
                return render(request, "user_profile/view_servise_from_outside.html", context=context)
            

            elif 'back_to_main_page' in request.POST:
                return redirect("index")



            context = {
                "userinfo": funcs.get_userinfo_by_telegram_id_from_outside(telegram_id=telegram_id_for_view)
            }
            return render(request, "user_profile/view_user_profile_by_telegram_id_from_outside.html", context=context)
        else:
            return render(request, "errors/without_id_error.html")
    else:
        return render(request, "user_profile/no_such_user.html")