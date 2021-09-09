from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from encyclopedia import util

# Create your views here.

def getTitle(request, title):
    content = util.get_entry(title)
    if(content):
        return render(request, "entryPage/title.html", {
        "title": title,
        "content": content
        })
    else:
        return render(request, "entryPage/title.html", {
        "title": "Error 404",
        "content": "page not found"
        })