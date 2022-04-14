
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path

from chat import auth
from . import views

urlpatterns = [
    path('', views.home, name='chat-home'),
    path('login/', auth_views.LoginView.as_view(template_name="chat/login.html"), name='chat-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name="chat/logout.html"), name='chat-logout'),
    path('register/', views.register, name='chat-register'),
    path('home/', views.home, name='chat-home'),
    path('profile/', views.profile, name='chat-profile'),
    path('send/', views.send_chat, name='chat-send'),
    path('renew/', views.get_messages, name='chat-renew'),


    ##API_URLS
    path('api/login', auth.loginUser),
    path('api/register', auth.registerUser),
    path('api/chats/<id>', views.apiChats),
    path('api/people', views.getPeople),
]
