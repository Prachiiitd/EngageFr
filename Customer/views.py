from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .decorators import allowed_users, haveFaces
from .forms import ApplicationForm
from .models import Application

# Create your views here.

"""
.@allowed_users: This decorator is used to prevent users from accessing the login page.
.@login_required: This decorator is used to prevent users from accessing the login page
 if they are not logged and redirect them to the login page.
.haveFaces(img): This method is used to check if the user has faces in their newly applied application.
"""


@login_required(login_url='Auth:login')
@allowed_users(allowed_roles=['customer'])  # Allow only customers to access this page.
def dashboard(request):
    """
    This method is used to display the dashboard page and register the Application applied by the user.
    .form: This is the form used for new application.
    .form.is_valid(): This is used to check if the form is valid
    (a valid from is form which fulfills all the pre-defined conditions in the ApplicationForm class of forms.py class).
    .POST: This is used to check if the form has been submitted.
    """

    user = request.user  # Get the user object from the request.
    customer = User.objects.get(username=user)  # Get the customer object from the user from the database.

    # Create a form object for the customer dashboard to accept new application request page.
    form = ApplicationForm(instance=customer)
    # Get all the applications submitted by the logged in customer from the database.
    prevApp = Application.objects.filter(customer=user)

    # If the request is a POST request, then process the form data as below.
    if request.method == 'POST':
        # Create a form object with the POST data, Files submitted and assign it to the form variable
        # for future use of the data
        form = ApplicationForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():  # Check if the form is valid.
            user = form.save()  # Save the form data to the database.
            fName = form.cleaned_data.get('fName')  # Get the first name from the form data.
            lName = form.cleaned_data.get('lName')  # Get the last name from the form data.
            image = form.cleaned_data.get('images')  # Get the image from the form data.

            # Create a new application object and save it to the database with the fields in the database.
            application = Application(fName=fName, lName=lName, images=image, customer=user)
            application.save()  # Save the application object to the database.

            if haveFaces(application.images.name):
                # if the image have single face crop and save that face to the database
                # and display a success message.
                messages.success(request, f'Applied successfully for {fName} {lName}!')
            else:
                application.delete()  # Delete the application object if the image does not have a single face.
                # Display a message to the user that the image does not have a single face.
                messages.error(request, f'Application failed! Upload image containing face of only one person.')

        else:
            # Display a message to the user that the form is invalid.
            for field, errors in form.errors.items():
                # For each erroneous field in the form, display the error message.
                messages.error(request, f'{field}: {errors}')

        return redirect('Customer:dashboard')  # Redirect the user to the dashboard page.

    else:  # If the request is not a POST request, then display the login page.
        return render(request, "customer/dashboard.html", {'Customer': customer, 'form': form, 'prevApp': prevApp})


@login_required(login_url='Auth:login')
@allowed_users(allowed_roles=['customer'])  # Allow only customers to access this page.
def remove(request):
    """
    This method is used to remove the application from the database and display a success message.
    """
    if request.method == 'POST':  # Check if the request is a POST request.
        appId = request.POST.get('appId')  # Get the application id from the request.
        Application.objects.get(appId=appId).delete()  # Delete the application from the database.
        messages.success(request, f'Removed successfully!')  # Display a success message.

    return redirect('Customer:dashboard')  # Redirect the user to the dashboard page.
