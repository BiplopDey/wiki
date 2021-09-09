from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from encyclopedia import util

# Create your views here.

def getTitle(request, title):
    content = util.get_entry(title)
    if(content):
        return HttpResponse(content)
    else:
        return HttpResponse("Entry not found")