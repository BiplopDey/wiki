from django.forms import widgets
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from . import util
from entryPage import views

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search(request):
    if request.method == "POST":
        title = str(request.POST["q"])
        titles = util.list_entries();
        if(title in titles):
            return HttpResponseRedirect(reverse("title", args=(title,)))
            #return views.getTitle(request,title) #puede funcionar pero estariamos en el link /search, pero no es buena practica
        else:
            substring=[]
            for name in titles:
                if title in name:
                    substring+=[name]
            #mas rapido: [name for name in titles if title in name ]
            return render(request, "encyclopedia/index.html", {
                "entries": substring
            })

class Page(forms.Form):
    title = forms.CharField(label="Title:")
    content = forms.CharField(widget=forms.Textarea)

def newPage(request):
    if request.method == "POST":
        page = Page(request.POST)
        if page.is_valid():
            title = page.cleaned_data["title"]
            if util.get_entry(title):
                return render(request, "entryPage/title.html", {
                    "title": "Error",
                    "content": "The page already exists"
                })
            else:
                content = page.cleaned_data["content"]
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("title", args=(title,)))
                
        else:
            return render(request, "encyclopedia/add.html", {
                'page': page
            })
    
    return render(request,"encyclopedia/add.html",{
            'page': Page()
    })