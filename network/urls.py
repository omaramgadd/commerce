
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.add_post, name="create"),
    path("page/<str:username>", views.user_page, name="page"),
    path("follow/<str:action>", views.follow, name="page"),
    path("check/<str:user>", views.check_follow, name="check"),
    path("followers_number/<str:user>", views.followers_number, name="number"),
    path("following_page/<str:userr>", views.following_page, name="following_page"),
    path("date/<str:date>", views.convert_date, name="date"),
    path("likes/<str:user>/<int:post>", views.likes, name = "likes"),
    path("all_posts", views.all_posts, name = "all_posts"),
    path("edit_post/<str:post>", views.edit_post, name = "edit")
]