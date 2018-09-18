from django.contrib import admin
from .models import Preference, Restaurant, Review, UserProfile

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Preference)
admin.site.register(Review)
admin.site.register(Restaurant)