from django.shortcuts import render, redirect
from foodie.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .models import UserProfile
# Create your views here.

def index(request):
    return render(request, 'foodie/index.html')

def about(request):
    return  render(request, 'foodie/about.html')

@login_required
def special(request):
    return HttpResponse("You are logged in !")

@login_required
def user_logout(request):
    logout(request)
    return redirect('index')

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request, 'foodie/registration.html', {'user_form':user_form,'registered':registered})

# when urls.pv access userprofile route, 
# this function get 1 userprofile data that match current user id (pk),
# (django know which userprofile internally) from database 
# render the userprofile.html, pass in userprofile
@login_required
def userprofile(request):
    userprofile = UserProfile.objects.get(id=request.user.id)
    print(userprofile)
    return render(request, 'foodie/userprofile.html', {'userprofile': userprofile})

@login_required
def profile_edit(request):
    user = UserProfile.objects.get(id=request.user.id)
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            if 'profile_pic' in request.FILES:
                user.profile_pic = request.FILES['profile_pic']
            user.save()
            return redirect('userprofile')
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'foodie/profileForm.html', {'form': form, 'user': user})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return redirect('index')
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print(f'They used username: {username} and password: {password}')
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'foodie/login.html', {})

@login_required
def restaurants(request):
    return render(request, 'foodie/restaurants.html')
