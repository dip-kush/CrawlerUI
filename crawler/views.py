from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.

def launch(request):
    return render(request, "index.html")
