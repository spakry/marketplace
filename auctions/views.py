from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core import serializers
from .models import User, Listing
import time


def index(request):
    #the main landing page
    return render(request, "auctions/index.html")

def listings(request,start,end): 
    if request.method == 'GET':
        NUM=9

        listings=Listing.objects.all()
        size=listings.count()
        if(start>=size):
            return HttpResponse([], content_type='application/json')
        if(start<size and end<size):
            listings=listings[start:end]
        if(start<size and end>=size):
            listings=listings[start:size]

        time.sleep(1)
        data = serializers.serialize('json', listings)
        return HttpResponse(data, content_type='application/json')

def single_listing(request,mId):
    if(request.method=='GET'):
        l=Listing.objects.filter(pk=mId)
        data = serializers.serialize('json', l)
        return HttpResponse(data, content_type='application/json')




def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            #redirect to index
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
