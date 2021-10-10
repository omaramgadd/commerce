from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("lisitng/<str:title>", views.listing, name= "listing"),
    path("close/<str:title>", views.close, name= "close"),
    path("comment/<str:title>", views.comment, name = "comment"),
    path("watchlist", views.watchlist, name = "watchlist"),
    path("add/<str:title>", views.add_to_watchlist, name = "add_to_watchlist"),
    path("remove/<str:title>", views.remove_from_watchlist, name = "remove_from_watchlist"),
    path("categories", views.categories, name = "categories"),
    path("view_category/<str:category_name>", views.view_category, name= "view_category")
]
