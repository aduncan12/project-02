from django.shortcuts import render, redirect
from foodie.forms import UserForm, UserProfileForm, ReviewForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404
from .models import UserProfile, User, Review
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
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
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
    user = User.objects.get(id=request.user.id)
    userprofile , created = UserProfile.objects.get_or_create(user=user)
    print(request.user.id)
    # user_reviews = Review.objects.get(id=request.user.id)
    # print("REVIEW:")
    # print(user_reviews.content)
    # return render(request, 'foodie/userprofile.html', {'userprofile': userprofile, 'user_reviews': user_reviews})
    
    return render(request, 'foodie/userprofile.html', {'userprofile': userprofile})

@login_required
def profile_edit(request):
    user = User.objects.get(id=request.user.id)
    user , created = UserProfile.objects.get_or_create(user=user)
    user.save()
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

# query preferences by user, put them into array, 
# format as json object, 
# display json object in route 'api/users/<int:pk>/preferences'
# def user_preferences(request, pk):
#     user = User.objects.get(id=pk)
#     preferences = user.userprofile.preferences.all()
#     pref_array = []
#     for pref in preferences:
#         print("pref.api_i::",pref.api_id)
#         pref_array.append(int(pref.api_id))
#     print('test::',pref_array)
#     return JsonResponse({"preferences": pref_array})

def user_preferences(request):
    if request.method == 'GET':
        user = User.objects.get(id=request.user.id)
        preferences = user.userprofile.preferences.all()
        pref_array = []
        for pref in preferences:
            print(pref.api_id)
            pref_array.append(int(pref.api_id))
        print(pref_array)
        return JsonResponse({"preferences": pref_array})

@login_required
def create_review(request):
    review = request
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            request.user = review.user
            review.save()
            return redirect('userprofile')
        else:
            print('\nform is invalid\n')
    else:
        form = ReviewForm()
    return render(request, 'foodie/review_form.html', {'form': form})

def review_view(request, pk):
    review = Review.objects.get(id=pk)
    return render(request, 'foodie/review_view.html', {'review': review})

def user_reviews(request):
    user_review = Review.objects.get(id=request.user.id)
    print(user_review)
    return render(request, 'foodie/userprofile.html', {'user_review': user_review})
