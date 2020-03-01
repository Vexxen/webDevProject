from django.shortcuts import render, HttpResponse

from . import models
from . import forms

# Create your views here.
def index(request, page=0):
    if request.method == "POST":
        form = forms.SuggestionForm(request.POST)
        if form.is_valid():
            form.save()
            form = forms.SuggestionForm()
    else:
        form = forms.SuggestionForm()
    suggestion_list = models.Suggestion_Model.objects.all()
    
    my_list=[]
    for i in range(20):
            i+=(page*10+1)
            my_list+=[{
                "first_name": "Name"+str(i),
                "last_name": "Surname"+str(i),
            }
        ]
    context = {
        #variable definitions go in here
        "title":"Template Demo",
        "body":"Hello Template",
        "suggestion_list":suggestion_list,
        "hello":"CINS465 Hello World",
        "form":form
    }
    return render(request, "index.html", context=context)