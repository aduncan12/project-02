from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

# the bottom + static() is for imagefield, static means public, make those path public
urlpatterns = [
    path('', views.index, name="index"),
    path('about/', views.about, name="about"),
    path('register', views.register, name='register'),
    path('login', views.user_login, name="user_login"),
    path('logout', views.user_logout, name='logout'),
    path('userprofile', views.userprofile, name='userprofile'),
    path('profile_edit', views.profile_edit, name='profile_edit'),
    path('restaurants', views.restaurants, name='restaurants'),

    path('api/users/<int:pk>/preferences', views.user_preferences)


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)