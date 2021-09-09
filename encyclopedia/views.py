from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

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
