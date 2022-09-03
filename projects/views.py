from django.shortcuts import render
from . import funcs 
# Create your views here.

def index(request):
    context = {
        "projects": funcs.get_projects()
    }
    return render(request, 'projects/index.html', context=context)