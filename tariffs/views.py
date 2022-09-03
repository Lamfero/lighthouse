from django.shortcuts import render, redirect
from . import funcs
import math

# Create your views here.
"""?telegram_id=123&secret_key=1234"""
def tariffs(request):
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
        
            if 'view_tariff' in request.POST and 'tariff_name' in request.POST:
                tariff_name = request.POST["tariff_name"]
                tariff = funcs.get_tariff_by_name(tariff_name)
                if tariff != None:
                    context = {
                        "tariff": tariff,
                    }
                    return render(request, "tariffs/tariff.html", context=context)
            elif 'month_count' in request.POST and 'tariff_name' in request.POST and 'buy_tariff' in request.POST:
                month_count = request.POST["month_count"]
                tariff_name = request.POST["tariff_name"]
                buy_tariff = request.POST["buy_tariff"]
                balance = funcs.get_user_balance(telegram_id=request.session["telegram_id"])
                tariff_info = funcs.get_tariff_by_name(tariff_name=tariff_name)
                if tariff_info != None and month_count.isdigit() and month_count.isnumeric():
                    if len(str(month_count)) > 0:
                        tariff_price = tariff_info.price
                        summary_price = int(tariff_price) * int(month_count)
                        if summary_price <= funcs.get_user_balance(telegram_id=telegram_id):
                            funcs.withdraw_from_user_balance(telegram_id=telegram_id, sum=summary_price)
                            if funcs.check_possibility_of_set_tariff(telegram_id=telegram_id, tariff_name=tariff_name):
                                funcs.add_tariff(telegram_id=telegram_id, tariff_name=tariff_name)

            elif 'back' in request.POST:
                return redirect("index")
            elif 'back_to_tariffs' in request.POST:
                return redirect("tariffs")
            tariffs = funcs.get_all_tariffs()
            context = {
                "tariffs": tariffs,
            }
            return render(request, "tariffs/tariffs.html", context=context)
        else:
            return render(request, "errors/invalid_secret_key.html")
    else:
        return render(request, "errors/without_id_error.html")
