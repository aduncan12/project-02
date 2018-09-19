from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('about', views.about, name="about"),
    path('register', views.register, name='register'),
    path('user_login', views.user_login, name="user_login"),
    path('logout', views.user_logout, name='logout'),
]