from django.urls import path
from . import views

app_name = 'Customer'
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("changeStatus/", views.changeStatus, name="changeStatus"),
]
