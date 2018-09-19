from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

urlpatterns=[
    path('admin/', admin.site.urls),
    path('', include('foodie.urls')),
<<<<<<< HEAD
    # path('special', views.special, name='special'),
    # path('foodie/', include('foodie.urls')),
    # path('logout', views.user_logout, name='logout'),
]
=======
]
>>>>>>> adbd4b62d5788f3ad55c9241f665c0a86efedc72
