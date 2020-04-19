"""mySite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # path('', views.index, name='chat'),
    path('', views.index),
    path('page/', views.page),
    path('chat/', views.chat),
    #moved to chaturls.py
    # path('chat/<str:room_name>/', views.room, name='room'),
    # path('<int:page>/', views.index),
    path('suggestions/', views.get_suggestions),
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('profile/', views.get_profile, name='profile'),
    path('register/', views.register, name="register"),
    path('logout/', views.logout_view, name="logout"),
    path('suggestions/', views.get_suggestions),
    path('suggestion/', views.make_suggestion),
    path('comment/<int:sugg_id>/', views.comment),
    path('newSub/', views.make_subreddit),
    path('subList/', views.get_subreddits),
    path('newThread/', views.make_thread, name="make_thread"),
    path('threadList/', views.get_threads, name="get_threads"),
    path('list/', views.list_subreddits, name='list_subreddits'),
    path('list/<str:sub>/', views.subreddit_main_page, name='subreddit'),
    path('list/<str:sub>/posts/<int:post_id>/', views.show_posts, name='root_post'),
    path('list/<str:sub>/newPost/', views.create_post, name='create_post'),
    path('list/<str:sub>/<int:post_id>/reply/', views.create_reply, name='create_reply'),
    path('upvote/<int:post_id>', views.upvote_post_view, name='upvote'),
    path('downvote/<int:post_id>', views.downvote_post_view, name='downvote'),
    path('score/<int:post_id>', views.get_score, name='score'),
]
# <int:sub_id>
# <int:post_id>