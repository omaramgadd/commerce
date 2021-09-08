from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
	pass

class Club(models.Model):
	club_id = models.IntegerField(primary_key = True)
	name = models.CharField(max_length = 100)
	logo = models.CharField(max_length = 100)

class Star(models.Model):
	user = models.ForeignKey("User", on_delete = models.CASCADE)
	match = models.IntegerField()
	