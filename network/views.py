import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.core import serializers
from django.http import JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime
def index(request):
	return render(request, "network/index.html", {
		"posts" : Post.objects.all()
		})


def login_view(request):
	if request.method == "POST":

		# Attempt to sign user in
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(request, username=username, password=password)

		# Check if authentication successful
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse("index"))
		else:
			return render(request, "network/login.html", {
				"message": "Invalid username and/or password."
			})
	else:
		return render(request, "network/login.html")

def add_post(request):
	if request.method == "POST":
		user = request.user
		content = request.POST["content"]
		p = Post(user = user, content = content)
		p.save()
		return HttpResponseRedirect(reverse("index"))

def all_posts(request):
	posts = Post.objects.all().order_by("-timestamp")
	post_list = serializers.serialize('json', posts)
	return HttpResponse(post_list, content_type="text/json-comment-filtered")

def user_page(request, username):
	posts = Post.objects.filter(user = username).order_by("-timestamp")
	post_list = serializers.serialize('json', posts)
	return HttpResponse(post_list, content_type="text/json-comment-filtered")

@login_required
def following_page(request, userr):
	user_followings = Follower.objects.filter(follower = request.user)
	Following = User.objects.filter(following__in = user_followings)
	user_posts = Post.objects.filter(user__in = Following).order_by('-timestamp')
	user_list = serializers.serialize('json', user_posts)
	return HttpResponse(user_list, content_type="text/json-comment-filtered")

def convert_date(request, date):
	new_date = datetime.strptime( date, '%Y-%m-%dT%H:%M:%S.%fZ').strftime("%b %-d %Y, %-I:%M %p")
	return JsonResponse({"date": f"{new_date}"}, status = 201)

@csrf_exempt
@login_required
def follow(request, action):

	if request.method != "POST":
		return JsonResponse({"error": "POST request required."}, status=400)

	data = json.loads(request.body)
	userName = data.get("user", "")
	user = User.objects.get(username = userName)

	if action == "follow":
		f = Follower(user = user, follower = request.user)
		f.save()
		return JsonResponse({"message": "you followed this user"}, status=201)
	elif action == "unfollow":
		f = Follower.objects.get(user = user, follower = request.user)
		f.delete()
		return JsonResponse({"message": "you unfollowed this user"}, status=201)

def check_follow(request, user):
	userObj = User.objects.get(username = user)
	try:
		match = Follower.objects.get(user = userObj.id , follower = request.user)
		return JsonResponse({"message": "you follow this user"}, status=201)
	except Follower.DoesNotExist:
		return JsonResponse({"message": "you don't follow this user"}, status=201)

def followers_number(request, user):
	userObj = User.objects.get(username = user)
	followers = Follower.objects.filter(user = userObj.id).count()
	following = Follower.objects.filter(follower = userObj.id).count()

	return JsonResponse((followers,following), safe = False)

@csrf_exempt
@login_required
def likes(request, user, post):
	if request.method == "GET":
		number = Like.objects.filter(like = post).count()
		try:
			l = Like.objects.get(user = user, like = post)
			return JsonResponse({"liked" : True, "number" : f"{number}"}, status = 201)
		except Like.DoesNotExist:
			return JsonResponse({"liked" : False, "number" : f"{number}"}, status = 201)

	if request.method == "POST":
		try:
			l = Like.objects.get(user = user, like = post)
			l.delete()
			number = Like.objects.filter(like = post).count()
			return JsonResponse({"liked" : False, "number" : f"{number}"}, status = 201)
		except Like.DoesNotExist:
			user = User.objects.get(username = user)
			post = Post.objects.get(pk = post)
			l = Like(user = user, like = post)
			l.save()
			number = Like.objects.filter(like = post).count()
			return JsonResponse({"liked" : True, "number" : f"{number}"}, status = 201)


@csrf_exempt
def edit_post(request, post):
	p = Post.objects.get(pk = post)
	user = p.user
	if f"{request.user.username}" == f"{user}" and request.method == "PUT":
		data = json.loads(request.body)
		p.content = data["new_content"]
		p.save()
		return HttpResponse(status = 204)

	return JsonResponse({
			"error": "You can't edit this post"
		}, status=400)

def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse("login"))

def register(request):
	if request.method == "POST":
		username = request.POST["username"]
		email = request.POST["email"]

		# Ensure password matches confirmation
		password = request.POST["password"]
		confirmation = request.POST["confirmation"]
		if password != confirmation:
			return render(request, "network/register.html", {
				"message": "Passwords must match."
			})

		# Attempt to create new user
		try:
			user = User.objects.create_user(username, email, password)
			user.save()
		except IntegrityError:
			return render(request, "network/register.html", {
				"message": "Username already taken."
			})
		login(request, user)
		return HttpResponseRedirect(reverse("index"))
	else:
		return render(request, "network/register.html")

