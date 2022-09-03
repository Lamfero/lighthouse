from django.shortcuts import render, redirect
from . import funcs
# Create your views here.


def index(request):
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
            return render(request, "main/index.html")
        else:
            return render(request, "errors/invalid_secret_key.html")
    else:
        return render(request, "errors/without_id_error.html")


