# views.py contain all the logic, it request data from database, pass to template or front end.
# render() display html to browser
#   3 parameters:
#   -request: request passed in
#   -template_name: html file use the display in route
#   -response: send back a dictionary to request
# redirect() launch to another route / url
#   2 parameters:
#   -to: either a url or to call views.py function
#   -arguments: pass variables
# we use django form to create forms.
# authenticate() return user object by user name and password.
# login() save user id in a session, so user don't need to reauthenticate.
# logout() remove user id in a session.
# @login_required checks if use is logged in.
# serializers use to convert django querydict to json, or json to django querydict.
# reverse url name (urls.py path()'s 3rd parameter) to url (real url like urls.py path()'s 1st parameter)
# HttpResponse() instead of render a html file, response back a string content.
# HttpResponseRedirect() after does HttpResponse(), it also does redirect().
# JsonResponse() when pass in a dictionary, it will serialize to json, if use HttpResponse() we need to serialize dictionary ourself before sending.
# get_object_or_404() is a queryset, way to filter the object you are querying, when object not found give 404 error
from django.shortcuts import render, redirect
from foodie.forms import UserForm, UserProfileForm, ReviewForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, QueryDict
from django.shortcuts import get_object_or_404
from .models import UserProfile, User, Review, Restaurant
from django.views.decorators.csrf import csrf_exempt

# render home page
def index(request):
    return render(request, 'foodie/index.html')

# render about page
def about(request):
    return  render(request, 'foodie/about.html')

@login_required
def special(request):
    return HttpResponse("You are logged in !")

# logout user session, display home page
@login_required
def user_logout(request):
    logout(request)
    return redirect('index')

# register() function will signup a new user.
# these 3 things work together: froms.py UserForm class, views.py register() function, and registration.html
# this control how froms.py UserForm work with registration.html.
# registered vaiable tell if new user finished registration.
# check if registration.html's form method type is POST (means hit submit),
#   create new instance of UserForm link to UserForm(), get form data with request.POST,
#   is_valid() is buildin checks for form input and duplicarte user, etc..., 
#   save() will save form data to the database, then assign to another variable user,
#   set_password() will hash the password, then save to database again, now user is registered.
#   user_form.errors will give some buildin error message,
# else if not a POST reqiest, we going to link to empty UserForm(),
# render registration.html, pass in user_form, and registered
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

# when urls.py access userprofile route, 
# @login_required will make sure there is a registered user.
# get() return 1 user that match current user id (pk), assign to user variable,
# get_or_create() return a tuple, 1 userprofile and 1 boolean,
#   if user created userprofile in database, retrieve that userprofile and created = false, 
#   else create new an empty userprofile for that use and created = true,
#   user.save() will save userprofile to database.
#   when profileForm.html form submit POST request to forms.py UserProfileForm, 
#       pass in form field data,
#       pass in 'instance' keyword with this userprofile's user,
#   if form data is_valid() then save() to database,
#       request.FILES is keyword similar to request.POS, it checks the files instead of input field,
#       it take new uploaded image to replace the existing image, and save to database,
#       redirect to userprofile page,
#   else not a POST request then link to empty forms.py UserProfileForm,
# render the userprofile.html, pass in UserProfileForm and userprofile.
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

@login_required
def userprofile(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    userprofile , created = UserProfile.objects.get_or_create(user=user)
    user_reviews = Review.objects.filter(user_id = user_id)
    user_saved_rest = Restaurant.objects.filter(user_id = user_id)
    return render(request, 'foodie/userprofile.html', {'userprofile': userprofile, 'user_reviews': user_reviews,'user_saved_rest':user_saved_rest})

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
    user = User.objects.get(id=request.user.id)
    userprofile , created = UserProfile.objects.get_or_create(user=user)
    return render(request, 'foodie/restaurants.html')

# get Current logged in user by id: User.objects.get(id=request.user.id)
# get all preferences of the use: user.userprofile.preferences.all()
# sent response back serialize given dictionary to json object
@login_required
def user_preferences(request):
    if request.method == 'GET':
        user = User.objects.get(id=request.user.id)
        preferences = user.userprofile.preferences.all()
        pref_array = []
        for pref in preferences:
            pref_array.append(int(pref.api_id))
        return JsonResponse({"preferences": pref_array})

@login_required
def review_edit(request, pk):
    review = Review.objects.get(id=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save()
            return redirect('userprofile', pk=review.id)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'foodie/review_form.html', {'form': form})

@login_required
def create_review(request,pk):
    user = UserProfile.objects.get(id=request.user.id)
    restaurant = Restaurant.objects.get(id=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = user
            review.restaurant = restaurant
            review.save()
            return redirect('userprofile')
        else:
            print('\nform is invalid\n')
    else:
        form = ReviewForm()
    return render(request, 'foodie/review_form.html', {'form': form , 'restaurant':restaurant})

@login_required
def review_view(request, pk):
    review = Review.objects.get(id=pk)
    return render(request, 'foodie/review_view.html', {'review': review})

@login_required
def review_edit(request,id):
    review = Review.objects.get(id=id)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save()
            review.save()
            return redirect('userprofile')
    else:
        form = ReviewForm(instance=review)
    return render(request, 'foodie/review_form.html', {'form': form, 'review': review})

@csrf_exempt
@login_required
def save_restaurant(request):
    user = UserProfile.objects.get(id=request.user.id)
    if request.method == 'POST':
        restaurant = Restaurant.objects.create(user=user)
        restaurant.name = QueryDict(request.body)['array[restaurant][name]']
        restaurant.description = QueryDict(request.body)['array[restaurant][location][address]']
        restaurant.menu_url = QueryDict(request.body)['array[restaurant][menu_url]']
        restaurant.cuisine = QueryDict(request.body)['array[restaurant][cuisines]']
        restaurant.save()
        return HttpResponse(QueryDict(request.body))

@login_required
def review_delete(request, id):
    Review.objects.get(id=id).delete()
    return redirect('userprofile')

@login_required
def restaurant_delete(request, id):
    Restaurant.objects.get(id=id).delete()
    return redirect('userprofile')