from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
# Create your views here.

def user(request):
    template=loader.get_template('login.html')
    return HttpResponse(template.render())