# Project 2: foodie (fourager)
##### by Alan Duncan, Francisco Sandoval, Wai Ka Wong Situ, and Yi Liu
## foodie (4Ager) is a full stack web application that allows you to randomly generate a list of four restaurants in your area, based off of your preference. You can leave a review on a restaurant you have saved.

## Technologies Used
- __Django__: Core framework for Python.
- __PostgreSQL__: Our database in development and production.
- __Data Models__:
- __Data Validation__: Validate incoming data before entering it into the database.
- __Error Handling__: Validate form data, handle incorrect inputs, and provide user feedback on the client side.
- __Views__: Use partials to follow DRY development in our views.
- __Home Page__: Homepage that explains our app's value proposition and guides the user.
- __About Page__: About page that includes photos and brief bios of our team members
- __User Experience__: Ensure a pleasing and logical user experience. Use a framework like Bootstrap to enhance and ease our CSS styling.
- __Responsive Design__: Make sure our app looks great on a phone or tablet.
- __Heroku__: Deploy our app to Heroku. Ensure no app secrets are exposed. Do not commit secret keys to GitHub!

- __User Login__: Use Django user authentication and authorization.
- __AJAX__: Use AJAX to communicate with the server without reloading the page when appropriate.
- __External APIs__: Third-party APIs: [Zomato link](https://developers.zomato.com/documentation#/), [Yelp link](https://www.yelp.com/developers/documentation/v3/business_search).
- __JavaScript & jQuery__: Add dynamic client-side behavior with event-driven functionality.
- __User-Friendly URLs__:.

## code snippet
- Inorder to create a review.
- First create django roiute, (Review, Restaurant) models in database, ReviewForm django form, user, and save a restaurant to userprofile,

- In urls.py, this is the route.
```
from django.urls import path
from . import views
path('restaurant/<int:pk>/review/new', views.create_review, name='create_review'),
```

- In userprofile.html, each saved restaurants has a link connect to views.py create_review(request,pk) passing in the clicked rest.id.
```
<div id="user_saved">
    {% for rest in user_saved_rest %}
        <h4>{{rest.name}}</h4>
        <h5>{{rest.description}}</h5>
        <h5>{{rest.cuisine}}</h5>
        <a href="{% url 'create_review' pk=rest.id %}">Review {{rest.name}}</a>
        <a href="{% url 'restaurant_delete' id=rest.id %}">Remove</a>
        <hr>
    {% endfor %}
</div>
```

- In views.py, get userprofile by logged in user id,
- get restaurant by the pass in rest.id,
- launch the ReviewForm() which will generate the form in review_form.html, connect the form data to Review model in database, assign to form variable,
- check the form data, add form data to Review model, save to database,
- error check, else let user do review form again.
```
from django.shortcuts import render, redirect
from foodie.forms import ReviewForm
from django.contrib.auth.decorators import login_required
from .models import UserProfile, User, Review, Restaurant
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
```

- In forms.py, django form that connect to database
```
from django import forms
from .models import Review
class ReviewForm(forms.ModelForm):
    class Meta():
        model = Review
        fields = ('content', 'rating')
```

- In review_form.html, html file with django code
```
{% extends "foodie/base.html" %}
{% load staticfiles %}
{% block content %}
<div class="container picture4">
    <div class="jumbotron review">
        <h1>Review for {{ review.restaurant }} {{ restaurant.name }}</h1>
        <form class='reviewform' enctype="multipart/form-data" method="POST">
            {% csrf_token %}
            {{ form.as_p }}
            <input type="submit" name="" value="Post">
        </form>
    </div>
</div>
{% endblock %}
```

## Sprint 1:
- project planning approval
- user authentication
- openstreetmap/leaflet api
- zomato api

## Sprint 2:
- base (header and footage), landing page, user profile, results (map and restaurant list), and about templates
- create models
- set up database
- CRUD users, reviews

## Sprint 3:
- jQuery animations
- Bootstrap, Fontawesome
- customize icons/pins on map
- selected restaurant modal

## Sprint 4:
- add restaurant rating
- add price range indicator for restaurants
- add distance radius
- style website

## Sprint 5:
- create About page and readme
- finalize app name
- add loading/splash page
- deploy to heroku


## Our progress:
### 9-17-2018
- Came up with app idea
- Set up git repo
- Created models, views, and urls

### 9-18-2018
- Seeded database with cuisine types and IDs from Zomato API
- Created About page
- Added user authentication
- Created base and index templates

### 9-19-2018
- Added map from leaflet
- Fixed registration form and began updating profile form
- Converted styling to Sass
- Added dropdown profile info box
- Research food / restaurant related api
- Create Trollo
- Create sprint
- create wireframe
- Create user story

### 9-18-2018
- Create github repo
- Create ERD
- Check in with teacher got aprovel
- create database and seed

### 9-19-2018
- User Profile figured out
- Map on results page up and running
- Home page template finished
- Database connects user and empty userprofile

### 9-20-2018
- Check box for prefrences https://stackoverflow.com/questions/1760421/how-can-i-render-a-manytomanyfield-as-checkboxes
- User Reviews
- Sent an array of prefrence id's to app.js

### 9-21-2018
- Getting User Reviews on everyone's projects was difficult but we had to drop our databases and start over for it to work.
- In order to get some changes we learned that we have to clear our cache.
- Most of our features are done, but we had to form a clear plan for our remaining time.

### 9-22-2018
- Saved restaurants on user profiles
- Review button for those restaurants
- Html Scroll bar for displayed restaurants on generator page
- User does not need to update profile at all in order to find and save restaurant

### 9-23-2018
- Fixed image on user profiles
- Edit profiles
- Create, edit, and delete review link for restaurants
- Code cleaning
- Try to upgrade random generated restaurants.
- Adding documentation (only in release branch)
- Added modal
- Fixed update image

### 9-24-2018
- added zoom to map
- change map to takeup whole page, overlay restaurants list on top
- added fade in restaurants list
- deploy to Heroku
- title icon
- fixed model
- added rating

## Challenges/Successes

### Challenges
- Getting prefrences on Userprofile to show up as check boxes
- Sending Json from back end to front end
- User reviews to show up on userprofile
- Trouble shooting and debugging
- Pushing to heroku

### Successes
- Getting database set up quickly
- Finally setting up the checkbox field for userprofile's prefrences https://stackoverflow.com/questions/1760421/how-can-i-render-a-manytomanyfield-as-checkboxes
- Being able to intentionally break our code to find errors and fix them

