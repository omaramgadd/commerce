from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
	name = models.CharField(max_length = 64, blank = False)	

class Listing(models.Model):
	user = models.ForeignKey(User, on_delete= models.CASCADE, blank=False, default = "")
	title = models.CharField(max_length = 64, blank=False)
	description = models.CharField(max_length = 200, blank=False)
	starting_bid = models.IntegerField(blank = False)
	url = models.CharField(max_length = 500, blank = True)
	category = models.ForeignKey(Category, on_delete = models.CASCADE, default = "")
	sold = models.BooleanField(default = False)

class Bid(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE, default = "")
	bid = models.IntegerField(blank = True)
	item = models.ForeignKey(Listing, on_delete = models.CASCADE, default = "")
	won = models.BooleanField(default = False)

class Comment(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE, default = "")
	item = models.ForeignKey(Listing, on_delete = models.CASCADE, default = "")
	comment = models.CharField(max_length = 100, blank = False)

class Watchlist(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE, default = "")
	item = models.ForeignKey(Listing, on_delete = models.CASCADE, default = "")
	