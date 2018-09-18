from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
# Create your views here.

def index(request):
    return render(request, 'reddit/index.html')

def about(request):
    return  render(request, 'reddit/about.html')
