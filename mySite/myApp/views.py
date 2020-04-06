from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

from . import models
from . import forms

import json

# Create your views here.
def index(request, page=0):
    if request.method == "POST":
        form = forms.SuggestionForm(request.POST)
        if form.is_valid():
            form.save()
            form = forms.SuggestionForm()
    else:
        form = forms.SuggestionForm()
    # suggestion_list = models.Suggestion_Model.objects.all()
    suggestion_objects = models.Suggestion_Model.objects.all()
    suggestion_list = []
    for sugg in suggestion_objects:
        # not using comments in this assignment right now
        # comment_objects = models.CommentModel.objects.filter(suggestion=sugg)
        temp_sugg = {}
        temp_sugg["suggestion"] = sugg.suggestion
        # temp_sugg["author"] = sugg.author.username
        # temp_sugg["comments"] = comment_objects
        suggestion_list += [temp_sugg]
    
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
        "form":form,
        "explain":"This JS simply refreshes the client side page with info from other client's suggestions in another browser window"
    }
    return render(request, "index.html", context=context)

def get_suggestions(request):
    suggestion_objects = models.Suggestion_Model.objects.all()
    suggestion_list={}
    suggestion_list["suggestions"] = []
    for sugg in suggestion_objects:
        # comment_objects = models.CommentModel.objects.filter(suggestions)
        temp_sugg = {}
        temp_sugg["suggestion"]=sugg.suggestion
        #temp_sugg["author"]=sugg.author.username
        # temp_sugg["comments"]=comment_objects
        suggestion_list["suggestions"]+=[temp_sugg]
    return JsonResponse(suggestion_list)

def chat(request):
    return render(request, 'chat/chat.html')
