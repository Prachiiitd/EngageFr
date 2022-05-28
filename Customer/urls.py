from django.urls import path
from . import views

# Define your urlpatterns here.

"""
    This is the URL file for the Customer app.
    This file contains all the URL patterns for the Customer app.
"""

app_name = 'Customer'  # This is the namespace for the app.

urlpatterns = [  # List of URL patterns for the Customer app.
    path("", views.dashboard, name="dashboard"),  # URL for the dashboard page.
    path("remove/", views.remove, name="remove"),  # URL for the changeStatus method used.
]

