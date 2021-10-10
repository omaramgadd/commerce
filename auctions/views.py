from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Listing, Bid, Comment, Watchlist, Category



def index(request):
    return render(request, "auctions/index.html",{
        "listings" : Listing.objects.all()
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


@login_required(login_url='login')
def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        url = request.POST["url"]
        category = request.POST["category"]
        category = Category.objects.get(name = category)
        if title == "":
            return render(request, "auctions/create.html",{
                "message": "Please provide a title"
                })
        if starting_bid == "":
            return render(request, "auctions/create.html",{
                "message": "Please provide a bid"
                })
        t = Listing(user = request.user, title = title, description = description, starting_bid = starting_bid, url = url, category = category, sold = False)
        t.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html",{
            "categories": Category.objects.all()
            })

@login_required(login_url='login')
def listing(request, title):
    item = Listing.objects.get(title = title)
    comments = Comment.objects.filter(item = item)
    user_watchlist = Watchlist.objects.filter(user = request.user)
    if item.sold == True:
        try: highest_bid = Bid.objects.get(bid = item.starting_bid, item = item)
        except :
            return render(request, "auctions/listing.html",{
                "listing" : item,
                "message" : "No one won the auction",
                "comments" : comments
                })
    
        highest_bid.won = True
        
        if request.user == highest_bid.user:
            return render(request, "auctions/listing.html",{
            "listing" : item,
            "message" : "You won the bid",
            "comments" : comments
            })
        
        return render(request, "auctions/listing.html",{
        "listing" : item,
        "message" : "Item is Sold",
        "comments" : comments
        })

    if request.method == "POST":
        current_bid = request.POST["bid"]
        item.starting_bid = current_bid
        item.save()
        b = Bid(user = request.user, bid = current_bid, item = item)
        b.save()

    for liked in user_watchlist:
        if liked.item == item:
            return render(request, "auctions/listing.html",{
                "listing" : item,
                "min" : int(item.starting_bid) + 1,
                "comments" : comments,
                "in_watchlist": True
            })
    return render(request, "auctions/listing.html",{
            "listing" : item,
            "min" : int(item.starting_bid) + 1,
            "comments" : comments
        })

def close(request, title):
    item = Listing.objects.get(title= title)
    item.sold = True
    item.save()
    return(HttpResponseRedirect(reverse("listing", args= [title])))

def comment(request, title):
    item = Listing.objects.get(title= title)
    comment = request.POST["comment"]
    c = Comment(user = request.user, item = item, comment = comment)
    c.save()
    return(HttpResponseRedirect(reverse("listing", args= [title])))

@login_required(login_url='login')
def watchlist(request):
    items = Watchlist.objects.filter(user = request.user)
    return render(request, "auctions/watchlist.html", {
        "items" : items
        })

def add_to_watchlist(request, title):
    item = Listing.objects.get(title= title)
    w = Watchlist(user = request.user, item = item)
    w.save()
    return(HttpResponseRedirect(reverse("listing", args= [title])))

def remove_from_watchlist(request, title):
    item = Listing.objects.get(title= title)
    w = Watchlist.objects.get(user = request.user, item = item)
    w.delete()
    return(HttpResponseRedirect(reverse("listing", args= [title])))

def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html",{
        "categories": categories
        })

def view_category(request, category_name):
    category = Category.objects.get(name = category_name)
    return render(request, "auctions/index.html",{
        "listings" : Listing.objects.filter(category = category)
        })
'''
<option value="shoes">shoes</option>
                <option value="tshirts">tshirt</option>
                <option value="jeans">jeans</option>
                <option value="jackets">jacket</option>
                '''