from django.urls import path, include
from . import views

# Define your urlpatterns here.
"""
    This is the URL file for the Auth app.
    This file contains all the URL patterns for the Auth app.
"""

app_name = 'Auth'  # This is the namespace for the app.

urlpatterns = [  # List of URL patterns for the Auth app.
    path("", views.index, name="authIndex"),  # URL for the index page.
    path("login/", views.loginUser, name="login"),  # URL for the login method used.
    path("logout/", views.logoutUser, name="logout"),  # URL for the logout method used.
    path("admin/", views.admin, name="admin"),  # URL to add the Camera Ip.
]

