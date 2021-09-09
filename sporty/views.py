from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta, timezone
from .models import *
import requests
import pytz

tz = pytz.timezone('Africa/Cairo')

def register_view(request):
	if request.method == "POST":
		username = request.POST["username"]
		email = request.POST["email"]

		# Ensure password matches confirmation
		password = request.POST["password"]
		confirmation = request.POST["confirmation"]
		if password != confirmation:
			return render(request, "sporty/register.html", {
				"message": "Passwords must match."
			})

		# Attempt to create new user
		try:
			user = User.objects.create_user(username, email, password)
			user.save()
		except IntegrityError:
			return render(request, "sporty/register.html", {
				"message": "Username already taken."
			})
		login(request, user)
		return HttpResponseRedirect(reverse("home"))
	else:
		return render(request, "sporty/register.html")

def login_view(request):
	if request.method == "POST":

		# Attempt to sign user in
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(request, username=username, password=password)

		# Check if authentication successful
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse("home"))
		else:
			return render(request, "sporty/login.html", {
				"message": "Invalid username and/or password."
			})
	else:
		return render(request, "sporty/login.html")

def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse("home"))
	
def home(request):
	if request.is_ajax():
		template = 'matchweek.html'
		direction = request.GET.get('dir')
		if direction == 'n':
			request.session['weekoffset'] += 1
		elif direction == 'p':
			request.session['weekoffset'] -= 1
	else:
		template = 'home.html'
		request.session['weekoffset'] = 0
	offset = request.session['weekoffset']
	start = datetime.now(tz).date() + timedelta(days=7*offset-1)
	end = start + timedelta(days=9)


	matches = request_games(start, end)

	start += timedelta(1)
	end -= timedelta(2)

	return render(request, f"sporty/{template}",{
		"matches": matches,
		"start": start,
		"end": end
	})


def match(request, id):
	match_id = id 

	# match stats request
	headers = {"apikey": "a0f2e7c0-6bf2-11eb-9adf-a199a60fa5d3"}
	response = requests.get(f'https://app.sportdataapi.com/api/v1/soccer/matches/{match_id}', headers=headers, params=())
	
	r = response.json()
	data = r.get("data")

	if data is None:
		return

	full_date = data["match_start_iso"]
	dt = datetime.strptime(full_date, '%Y-%m-%dT%H:%M:%S%z')
	dt = dt.astimezone(tz)
	m_date = dt.date()
	m_time = dt.time()

	home_team = data["home_team"]
	away_team = data["away_team"]

	# leauge standings request 
	params = (
 	  ("season_id","2029"),
	);

	standings_response = requests.get('https://app.sportdataapi.com/api/v1/soccer/standings', headers=headers, params=params);

	s = standings_response.json()
	s_data = s.get("data")
	standings = s_data.get("standings")

	starred = None

	if request.user.is_authenticated:
		try:
			starred = Star.objects.get(user = request.user, match = match_id)
		except Star.DoesNotExist:
			starred = None

	
	for club in standings:
		'''
		reg_response = requests.get(f'https://app.sportdataapi.com/api/v1/soccer/teams/{club["team_id"]}', headers=headers, params=params);
		reg = reg_response.json()
		reg_data = reg.get("data")
		regi = Club(club_id = club["team_id"], name = reg_data["name"], logo = reg_data['logo'])
		regi.save()
		'''

		obj = Club.objects.get(club_id = club["team_id"])
		club['name'] = obj.name
		club['logo'] = obj.logo

	
	return render(request, "sporty/match.html",{
		"starred": starred,
		"data" : data,
		"match_events" : data["match_events"],
		"home_id" : home_team["team_id"],
		"away_id" : away_team['team_id'],
		"m_time" : m_time,
		"m_date" : m_date,
		"standings" : standings
	})


def request_games(start, end):

	params = (
	   ("season_id","2029"),
	   ("date_from",start.strftime("%Y-%m-%d")),
	   ("date_to",end.strftime("%Y-%m-%d"))
	);

	headers = {
	"apikey": "a0f2e7c0-6bf2-11eb-9adf-a199a60fa5d3"
	}

	response = requests.get('https://app.sportdataapi.com/api/v1/soccer/matches', headers=headers, params=params)
	r = response.json()

	data = r.get("data")

	if data is None:
		return

	number = len(data)
	matches = []
	for i in range(number):
		match = {}

		full_date = data[i]["match_start_iso"]
		dt = datetime.strptime(full_date, '%Y-%m-%dT%H:%M:%S%z')
		dt = dt.astimezone(tz)
		
		if dt.date() < start + timedelta(1):
			del match
			continue

		if dt.date() > end - timedelta(2):
			del match
			continue

		match['date'] = dt.date()
		match['time'] = dt.time()
		match['start'] = full_date

		match['id'] = data[i]['match_id']

		match['status'] = data[i]["status"]
		match['status_code'] = data[i]["status_code"]
		match['minute'] = data[i]['minute']

		home_team = data[i]["home_team"]
		match['home_name'] = home_team['name']
		match['home_logo'] = home_team['logo']

		away_team = data[i]["away_team"]
		match['away_name'] = away_team['name']
		match['away_logo'] = away_team['logo']

		stats = data[i]['stats']
		match['home_score'] = stats['home_score']
		match['away_score'] = stats['away_score']
		matches.append(match)

	
	matches.sort(key = lambda x: datetime.strptime(x['start'], '%Y-%m-%dT%H:%M:%S%z'))

	return matches


def starred(request):
	if request.is_ajax():
		match_id = request.GET.get('match_id')
		try:
			starred = Star.objects.get(user = request.user, match = match_id)
			starred.delete()

		except Star.DoesNotExist:
			star_game = Star(user = request.user, match = match_id)
			star_game.save()

		return HttpResponse(status=201)
	else:
		starred_games = Star.objects.all().filter(user = request.user)

		headers = {"apikey": "a0f2e7c0-6bf2-11eb-9adf-a199a60fa5d3"}

		matches_list = []

		for game in starred_games:
			match = {}
			response = requests.get(f'https://app.sportdataapi.com/api/v1/soccer/matches/{game.match}', headers=headers, params=())
			r = response.json()
			data = r.get("data")

			if data is None:
				return

			full_date = data["match_start_iso"]
			dt = datetime.strptime(full_date, '%Y-%m-%dT%H:%M:%S%z')
			dt = dt.astimezone(tz)

			match['date'] = dt.date()
			match['time'] = dt.time()
			match['data'] = data

			matches_list.append(match)

		return render(request, "sporty/starred.html", {
			"matches_list" : matches_list
			})

def club_matches(request, club_id):

	params = (
		   ("season_id","2029"),
		   ("date_from","2020-08-12"),
	);

	headers = {
	"apikey": "a0f2e7c0-6bf2-11eb-9adf-a199a60fa5d3"
	}

	response = requests.get('https://app.sportdataapi.com/api/v1/soccer/matches', headers=headers, params=params)
	r = response.json()

	data = r.get("data")

	matches_list = []
	

	for match in data:
		if match['home_team']['team_id'] == int(club_id) or match['away_team']['team_id'] == int(club_id) :
			match_dict = {}
			match_dict["data"] = match

			full_date = match["match_start_iso"]
			dt = datetime.strptime(full_date, '%Y-%m-%dT%H:%M:%S%z')
			dt = dt.astimezone(tz)

			match_dict['date'] = dt.date()
			match_dict['time'] = dt.time()

			matches_list.append(match_dict)

	return render(request, 'sporty/club.html', {
			"matches_list" : matches_list,
		})












