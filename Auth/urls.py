from django.urls import path, include
from . import views

app_name = 'Auth'
urlpatterns = [
    path("", views.index, name="authIndex"),
    path("login/", views.loginUser, name="login"),
    path("logout/", views.logoutUser, name="logout"),
]
