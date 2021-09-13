from django.forms import widgets
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from markdown2 import Markdown

from . import util

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
                return render(request, "encyclopedia/error.html", {
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
    
class EditPageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)

def edit(request, title):
    if request.method == "POST":
        page = EditPageForm(request.POST)
        if page.is_valid():
            content = page.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("title", args=[title]))
        else:
            #messages.error(request, f'Editing form not valid, please try again!')
            return render(request, "encyclopedia/edit.html",{
                'page': page,
                'title': title
                })
    # si se accede del entry page
    elif request.method == "GET":
        # si no existe la pag
        content = util.get_entry(title)
        if ( content == None):
            return render(request, "encyclopedia/error.html", {
            "title": "Error 404",
            "content": "page not found"
            })

        return render(request, "encyclopedia/edit.html",{
            'page': EditPageForm(initial={'content': content}),
            'title': title
        })

def getTitle(request, title):
    content = util.get_entry(title)
    if(content):
        content_HTML = Markdown().convert(content)#convierte md en html
        return render(request, "encyclopedia/title.html", {
        "title": title,
        # luego en entry.html para que dentro del corchete compile html 
        # y no nos muestre raw html se pone {{content|safe}}
        "content": content_HTML
        })
    else:   
        return render(request, "encyclopedia/error.html", {
        "title": "Error 404",
        "content": "page not found"
        })

