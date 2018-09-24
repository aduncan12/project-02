from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Preference(models.Model):
    api_id = models.CharField(max_length=100)
    cuisine = models.CharField(max_length=100)

    def __str__(self):
        return self.cuisine

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    preferences = models.ManyToManyField(Preference,blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)

    def __str__(self):
        return self.user.username

class Restaurant(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE, related_name='restaurant')
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    cuisine = models.CharField(max_length=30)
    menu_url = models.URLField()

    def __str__(self):
        return self.name

class Review(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE, related_name='review')
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE, related_name='review')
    content = models.TextField(blank=True)
    rating = models.PositiveSmallIntegerField(default=1,
        validators=[MaxValueValidator(5), MinValueValidator(1)])

    def __str__(self):
        return f'{self.restaurant} {self.rating} {self.content} {self.user}'


