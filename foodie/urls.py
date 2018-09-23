# urls.py in project folder take care the domain name part of url
# this urls.py in app folder take care of routes there are on the right handside of domain name
# path() joins the 2 urls.py
#   3 parameters:
#   -route: right handside of domain name, to each render html page
#   -view: refer to function inside views.py, to response to request
#   -name: identify where to lookup, use by html template, views.py reverse lookup
# at the bottom + static() is for imagefield, static means public, make those path public
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('about/', views.about, name="about"),
    path('register', views.register, name='register'),
    path('login', views.user_login, name="user_login"),
    path('logout', views.user_logout, name='logout'),

    path('userprofile', views.userprofile, name='userprofile'),
    path('profile_edit', views.profile_edit, name='profile_edit'),
    path('restaurants', views.restaurants, name='restaurants'),
    path('preferences', views.user_preferences, name='preferences'),

    path('restaurant/<int:pk>/review/new', views.create_review, name='create_review'),
    path('review/<int:pk>', views.review_view, name='review_view'),
    path('review/<int:id>/edit', views.review_edit, name='review_edit'),
    path('review/<int:id>/delete', views.review_delete, name='review_delete'),
    path('restaurant/<int:id>/delete', views.restaurant_delete, name='restaurant_delete'),

    path('save_restaurant',views.save_restaurant, name='save_restaurant')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)