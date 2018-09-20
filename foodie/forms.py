from django import forms
from .models import UserProfile, Review
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','password','email')

class UserProfileForm(forms.ModelForm):
    class Meta():
        model = UserProfile
        fields = ('description','preferences','profile_pic')

class ReviewForm(forms.ModelForm):
    class Meta():
        model = Review
        fields = ('user', 'restaurant', 'content', 'rating')