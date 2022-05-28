from django.shortcuts import render, redirect  # Import the render and redirect functions.
from django.contrib.auth import authenticate, login, logout  # Import to authenticate, login, and logout methods.
from django.contrib import messages  # Import the messages' framework.
from django.contrib.auth.models import Group  # Import the Group model.

from .forms import CreateUserForm  # Import the CreateUserForm class from the forms.py file.
from .decorators import unauthenticated_user  # Import the required decorator.
from .models import Customer  # Import the Customer model from the models.py file.

# Create your views here.

"""
.@unauthenticated_user: This decorator is used to prevent users from accessing the login page 
                        if they are already logged in. 
"""


@unauthenticated_user
def index(request):
    """
    This method is used to display the Index page and register a new user.
    .form: This is the form used to login.
    .form.is_valid(): This is used to check if the form is valid
    (a valid from is form which fulfills all the pre-defined conditions in the CreateUserForm class of forms.py class).
    .POST: This is used to check if the form has been submitted.
    """

    form = CreateUserForm()  # Create a form object for the login page.

    # If the request is a POST request, then process the form data as below.
    if request.method == 'POST':
        # Create a form object with the POST data and assign it to the form variable for future use of the data
        # received from user in the post request(i.e. submitted form).
        form = CreateUserForm(request.POST)

        if form.is_valid():  # Check if the form is valid.
            user = form.save()  # Save the form data to the database.
            username = form.cleaned_data.get('username')  # Get the username from the form data.

            try:   # Try to get the group named with customer.
                group = Group.objects.get(name='customer')  # Get the group named with customer.
            except Group.DoesNotExist:  # If the group does not exist, then create it.
                Group.objects.create(name='customer')  # Create the group named with customer.
                group = Group.objects.get(name='customer')  # Get the group named with customer.

            user.groups.add(group)  # Add the user to the group named as customer.

            # Create a Customer object for the user and save it to the database with the fields in the database.
            customer = Customer(user=user, fName=user.first_name, lName=user.last_name, email=user.email)
            customer.save()  # Save the customer object to the database.

            messages.success(request, f'Account created for {username}!')  # Display a success message to the user.

        else:  # If the form is not valid, then display the appropriate error message to the user.
            for field, errors in form.errors.items():
                # For each erroneous field in the form, get the errors and display them to the user.
                messages.error(request, f'{field}: {errors}')

        return redirect('Auth:authIndex')  # Redirect the user to the index page again.

    else:  # If the request is not a POST request, then display the login page.
        return render(request, 'auth/index.html', {'form': form})   # Render the index page.


@unauthenticated_user
def loginUser(request):
    """
    This method is used to handle login of the user.
    .POST: This is used to check if the form has been submitted.
    .authenticate: Checks if a user with the given credentials exists and return the user object if it does.
    """

    # If the request is a POST request, then process the form data as below.
    if request.method == 'POST':
        username = request.POST.get('username')  # Get the username from the POST request data.
        password = request.POST.get('password')  # Get the password from the POST request data.

        user = authenticate(request, username=username, password=password)  # Authenticate the user.

        if user is not None:
            # If the user exists, then log them in.
            login(request, user)  # Log the user in.
            return redirect('Customer:dashboard')  # Redirect the user to the dashboard page in Customer app.
        else:
            # If the user does not exist, then display an error message to the user.
            messages.error(request, f'Login failed! Please try again.')

    # If the request is not a POST request, then display the login page.
    return redirect('Auth:authIndex')  # Redirect the user to the login present in index page again.


def logoutUser(request):
    """
    This method is used to handle logout of the user.
    """
    if request.user.is_authenticated:
        # If the user is authenticated, then log them out.
        logout(request)  # Log the user out.
        messages.success(request, f'Logout successful!')  # Display a success message to the user.

    return redirect('Auth:authIndex')   # Redirect the user to the login present in index page again.
