from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
	pass

class Post(models.Model):
	user = models.ForeignKey('user', on_delete = models.CASCADE, to_field = 'username')
	content = models.CharField(max_length = 280)
	timestamp = models.DateTimeField(auto_now_add = True)

class Follower(models.Model):
	user = models.ForeignKey('user', on_delete = models.CASCADE, related_name = 'following')
	follower = models.ForeignKey('user', on_delete = models.CASCADE, related_name = "follower")

class Like(models.Model):
	user = models.ForeignKey('user', on_delete = models.CASCADE, to_field = 'username')
	like = models.ForeignKey('Post', on_delete = models.CASCADE, related_name = 'like')