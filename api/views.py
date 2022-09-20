from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from . import funcs
# Create your views here.


def update_secret_key(request):
    if 'telegram_id' in request.POST and 'secret_key' in request.POST and 'SECRET_KEY_DJANGO' in request.POST:
        if request.POST["SECRET_KEY_DJANGO"] == '2444':
            status = funcs.update_secret_key(telegram_id=request.POST["telegram_id"], secret_key=request.POST["secret_key"])
            return JsonResponse(data=json.dumps({"status": status}))
    return HttpResponse(status=404)