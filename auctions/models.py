from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime

CHAR_MAX_LENGTH=150

class User(AbstractUser):
    pass

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_posted= models.DateTimeField(auto_now_add=True)
    isOpen=models.BooleanField()
    item_name = models.CharField(max_length=30)
    item_description= models.CharField(max_length=300,default="")
    item_image_url = models.CharField(max_length=64,default=None,blank=True,null=True)

class Bids(models.Model):
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    posted_user = models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(models.Model):
    text= models.CharField(max_length=CHAR_MAX_LENGTH)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    posted_user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_updated = models.DateTimeField(auto_now=True)
    

