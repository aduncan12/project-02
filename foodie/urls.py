from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
<<<<<<< HEAD
    path('about', views.about, name="about"),
    path('register', views.register, name='register'),
    path('user_login', views.user_login, name="user_login"),
    path('logout', views.user_logout, name='logout'),
=======
    path('/about', views.about, name="about"),
>>>>>>> c6d1ce5fd696900c060e7196f48d2030eb7a0a1f
]