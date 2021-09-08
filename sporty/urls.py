from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("match/<str:id>", views.match, name="match"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register_view, name="register"),
    path("starred", views.starred, name="starred"),
    path("club/<str:club_id>", views.club_matches, name="club"),
]