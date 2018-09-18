from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
<<<<<<< HEAD
    path('/about', views.about, name="about"),
=======
    path('about/', views.about, name="about"),
>>>>>>> 349ef14eb83b4b19e7acdba4972b89f9692c3d01
]