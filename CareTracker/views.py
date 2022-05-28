from django.shortcuts import redirect
# Create your views here.


def index(request):
    """
    This is the method just to redirect the entry url of view for the Care Tracker app to
    index page of Auth application.
    """
    return redirect("Auth:authIndex")  # Redirect to the index page of Auth app.
