# this is buildin django form, it config how the input field to display as, and which form data should add into our model.
# crate a class for each form,
# forms.ModelForm tells django data by form.
# config how each form field should look in html template, (if not config each field will use default)
#   EX: preferences will query all preferences from database, show them as checkboxes.
# in inner Meta class, point to our models, and which field should collect data.
from django import forms
from .models import UserProfile, Preference, Review
from django.contrib.auth.models import User

# these 3 things work together: froms.py UserForm class, views.py register() function, and registration.html
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','password','email')

class UserProfileForm(forms.ModelForm):
    preferences = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple,queryset=Preference.objects.all())
    class Meta():
        model = UserProfile
        fields = ('description','preferences','profile_pic')

class ReviewForm(forms.ModelForm):
    class Meta():
        model = Review
        fields = ('content', 'rating')