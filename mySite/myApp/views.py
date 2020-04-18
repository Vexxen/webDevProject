from datetime import datetime, timezone
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import JsonResponse

from . import models
from . import forms

import json

def logout_view(request):
    logout(request)
    return redirect("/")

def comment(request, sugg_id):
    if not request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        if request.user.is_authenticated:
            form = forms.CommentForm(request.POST)
            if form.is_valid():
                form.save(request, sugg_id)
                return redirect("/")
        else:
            form = forms.CommentForm()
    else:
        form = forms.CommentForm()
    context = {
        "title":"Comment",
        "sugg_id":sugg_id,
        "form":form
    }
    return render(request, "comment.html", context=context)

def make_suggestion(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            form = forms.SuggestionForm(request.POST, request.FILES)
            if form.is_valid():
                form.save(request)
                return redirect("/")
        else:
            form = forms.SuggestionForm()
    else:
        form = forms.SuggestionForm()
    context = {
        "title":"Add Suggestion",
        "form":form
    }
    return render(request, "suggestion.html", context=context)

def make_subreddit(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            form = forms.SubredditForm(request.POST)
            if form.is_valid():
                form.save(request)
                
                return redirect("/list/") #return to home for now, change to the sub just created later
        else:
            form = forms.SubredditForm()
    else:
        form = forms.SubredditForm()
    context = {
        "title":"Create New Sub",
        "form":form
    }
    return render(request, "newSub.html", context=context)

def get_subreddits(request):
    subreddit_objects = models.Subreddit.objects.all().order_by(
        '-published_on'
    )
    subreddit_list = {}
    subreddit_list["subreddits"] = []
    #fetch all subs
    for sub in subreddit_objects:
        temp_sub = {}
        temp_sub["title"] = sub.title
        temp_sub["description"] = sub.description
        temp_sub["id"] = sub.id
        temp_sub["creator"] = sub.creator.username
        subreddit_list["subreddits"] += [temp_sub]
    return JsonResponse(subreddit_list)

# Create your views here.
def index(request):
    # suggestion_objects = models.Suggestion_Model.objects.all()
    # suggestion_list = []
    # for sugg in suggestion_objects:
    #     comment_objects = models.Comment_Model.objects.filter(suggestion=sugg)
    #     temp_sugg = {}
    #     temp_sugg["suggestion"] = sugg.suggestion
    #     temp_sugg["author"] = sugg.author.username
    #     temp_sugg["comments"] = comment_objects
    #     suggestion_list += [temp_sugg]

    context = {
        "title":"Tempate Demo",
        "body":"<p> Hello Body</p>",
        # "suggestion_list":suggestion_list,
    }
    return render(request, "index.html", context=context)

def list_subreddits(request):
    subreddit_objects = models.Subreddit.objects.all().order_by(
        '-published_on'
    )
    subreddit_list = {}
    subreddit_list["subreddits"] = []
    #fetch all subs
    for sub in subreddit_objects:
        temp_sub = {}
        temp_sub["title"] = sub.title
        temp_sub["description"] = sub.description
        temp_sub["id"] = sub.id
        temp_sub["creator"] = sub.creator.username
        subreddit_list["subreddits"] += [temp_sub]
    context = {
        "title":"Subreddit List",
        "welcome":"All Subreddits",
        "subreddits":subreddit_list,
    }
    return render(request, "subreddits/subredditList.html", context=context)

def get_threads(request):
    thread_objects = models.Thread.objects.all().order_by(
        '-pulished_on'
    )
    thread_list = {}
    thread_list["threads"] = []
    #fetch all threads

def make_thread(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            form = forms.SubredditForm(request.POST)
            if form.is_valid():
                form.save(request)
                return redirect("/") #return to home for now, change to the sub just created later
        else:
            form = forms.SubredditForm()
    else:
        form = forms.SubredditForm()
    context = {
        "title":"Create New Thread",
        "form":form
    }
    return render(request, "newThread.html", context=context)

def get_suggestions(request):
    suggestion_objects = models.Suggestion_Model.objects.all().order_by(
        '-published_on'
    )
    suggestion_list = {}
    suggestion_list["suggestions"] = []
    for sugg in suggestion_objects:
        comment_objects = models.Comment_Model.objects.filter(
            suggestion=sugg
        ).order_by(
            '-published_on'
        )
        temp_sugg = {}
        temp_sugg["suggestion"] = sugg.suggestion
        temp_sugg["author"] = sugg.author.username
        temp_sugg["id"] = sugg.id
        try:
            temp_sugg["image"] = sugg.image.url
            temp_sugg["image_desc"] = sugg.image_description
        except Exception as err:
            print(err)
            temp_sugg["image"] = ""
            temp_sugg["image_desc"] = ""
        # except BaseException:
        #     temp_sugg["image"] = ""
        #     temp_sugg["image_desc"] = ""
        # except Exception as err:
        #     print(err)
        #     temp_sugg["image"] = ""
        #     temp_sugg["image_desc"] = ""
        temp_sugg["date"] = sugg.published_on.strftime("%Y-%m-%d %H:%M:%S")
        temp_sugg["comments"] = []
        for comm in comment_objects:
            temp_comm = {}
            temp_comm["comment"] = comm.comment
            temp_comm["id"] = comm.id
            temp_comm["author"] = comm.author.username
            temp_comm["date"] = datetime.now(timezone.utc) - comm.published_on
            # temp_comm["date"] = comm.published_on.strftime("%Y-%m-%d %H:%M:%S")
            temp_sugg["comments"] += [temp_comm]
        suggestion_list["suggestions"] += [temp_sugg]
    return JsonResponse(suggestion_list)

@login_required
def page(request):
    if request.method == "POST":
        form = forms.SuggestionForm(request.POST)
        if form.is_valid():
            form.save(request)
            form = forms.SuggestionForm()
    else:
        form = forms.SuggestionForm()
    suggestion_objects = models.Suggestion_Model.objects.all()
    suggestion_list = []
    for sugg in suggestion_objects:
        comment_objects = models.Comment_Model.objects.filter(suggestion=sugg)
        temp_sugg = {}
        temp_sugg["suggestion"] = sugg.suggestion
        temp_sugg["author"] = sugg.author.username
        temp_sugg["comments"] = comment_objects
        suggestion_list += [temp_sugg]

    context = {
        "title":"Tempate Demo",
        "body":"<p> Hello Body</p>",
        "suggestion_list":suggestion_list,
        "form":form
    }
    return render(request, "index.html", context=context)

def register(request):
    if request.method == "POST":
        form_instance = forms.RegistrationForm(request.POST)
        if form_instance.is_valid():
            form_instance.save()
            return redirect("/login/")
            # print("Hi")
    else:
        form_instance = forms.RegistrationForm()
    context = {
        "form":form_instance,
    }
    return render(request, "registration/register.html", context=context)

def chat(request):
    return render(request, 'chat/chat.html')

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })

def subreddit_main_page(request, sub):
    subreddit = models.Subreddit.objects.get(title=sub)
    context={
        'subreddit':subreddit,
        'posts': models.Post.objects.filter(subreddit=subreddit)
        # 'title':subreddit.title,
    }
    return render(request, 'subreddits/topic.html', context=context)

def show_posts(request, sub, post_id):
    subreddit_instance = models.Subreddit.objects.get(title=sub)
    root_post = models.Post.objects.get(id=post_id, subreddit=subreddit_instance)
    posts = root_post.get_descendants(include_self=True)
    
    context = {
        'posts':posts,
        'subreddit':subreddit_instance
    }
    return render(request, 'subreddits/posts.html', context=context)

def create_post(request, sub):
    if not request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        if request.user.is_authenticated:
            form = forms.PostForm(request.POST)
            if form.is_valid():
                form.save(sub)
                return redirect("/list/" + sub + "/")
        else:
            form = forms.PostForm()
    else:
        form = forms.PostForm()
    context = {
        "title":"New Post",
        "form":form,
        "sub":sub
    }
    return render(request, "subreddits/newPost.html", context=context)

#pass root node ID to see your response?
def create_reply(request, sub, post_id):
    if not request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        if request.user.is_authenticated:
            form = forms.ReplyForm(request.POST)
            if form.is_valid():
                form.save(sub, post_id)
                return redirect("/list/" + sub + "/posts/" + str(post_id) +"/")
        else:
            form = forms.ReplyForm()
    else:
        form = forms.ReplyForm()
    context = {
        "title":"New Reply",
        "form":form,
        "sub":sub,
        "post_id":post_id
    }
    return render(request, "subreddits/reply.html", context=context)


# @login_required
# @transaction.atomic
# def update_profile(request):
#     if request.method == 'POST':
#         user_form = UserForm(request.POST, instance=request.user)
#         profile_form = ProfileForm(request.POST, instance=request.user.profile)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request, _('Your profile was successfully updated!'))
#             return redirect('settings:profile')
#         else:
#             messages.error(request, _('Please correct the error below.'))
#     else:
#         user_form = UserForm(instance=request.user)
#         profile_form = ProfileForm(instance=request.user.profile)
#     return render(request, 'profiles/profile.html', {
#         'user_form': user_form,
#         'profile_form': profile_form
#     })