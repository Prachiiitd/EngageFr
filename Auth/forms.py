from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class CreateUserForm(UserCreationForm):
    """
    Form for creating a new user.
    .username_clean() and .email_clean() are custom validation methods
    .clean_password2() is custom validation method for password matching
    .save() is custom save method
    .username: is the username field
    .email: is the email field
    .password1: is the password field
    .password2: is the password confirmation field
    .first_name: is the first name field
    .last_name: is the last name field
    """

    username = forms.CharField(label='username', min_length=2, max_length=150, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Your Username', 'required': 'required', 'minlength': '2', 'maxlength': '150', 'type': 'text'}))
    first_name = forms.CharField(label='first_name', min_length=2, max_length=150, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Your First Name', 'required': 'required', 'minlength': '2', 'maxlength': '150', 'type': 'text'}))
    last_name = forms.CharField(label='last_name', min_length=2, max_length=150, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Your Last Name', 'required': 'required', 'minlength': '2', 'maxlength': '150', 'type': 'text'}))
    email = forms.EmailField(label='email', min_length=6, max_length=150, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Your Email', 'required': 'required', 'minlength': '6', 'maxlength': '150', 'type': 'email'}))
    password1 = forms.CharField(label='password1', min_length=5, max_length=150, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Enter Your Password', 'required': 'required', 'minlength': '5', 'maxlength': '150', 'type': 'password'}))
    password2 = forms.CharField(label='password2', min_length=5, max_length=150, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirm Your Password', 'required': 'required', 'minlength': '5', 'maxlength': '150', 'type': 'password'}))

    class Meta:
        """
        Metaclass for CreateUserForm
        .model: is the User model
        .fields: is the fields to be used in the form
        """

        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def username_clean(self):
        """
        Custom validation method for username
        .username_clean() is called in the clean() method
        .username: is the username field
        """

        # Get the username from the form data and convert it to lowercase
        username = self.cleaned_data['username'].lower()
        # Check if the username is already in use by another user
        new = User.objects.filter(username=username)

        if new.count():
            # If it is, raise a ValidationError
            # (This will raise an error and prevent the form from being submitted)
            raise ValidationError("User Already Exist")

        # If the username is valid, return the cleaned data
        return username  # (This will allow the form to be submitted)

    def email_clean(self):
        """
        Custom validation method for email
        .email_clean() is called in the clean() method
        .email: is the email field
        """

        # Get the email from the form data and convert it to lowercase
        email = self.cleaned_data['email'].lower()
        # Check if the email is already in use by another user
        new = User.objects.filter(email=email)

        if new.count():
            # If it is, raise a ValidationError
            # (This will raise an error and prevent the form from being submitted)
            raise ValidationError(" Email Already Exist")

        # If the email is valid, return the cleaned data
        return email  # (This will allow the form to be submitted)

    def clean_password2(self):
        """
        Custom validation method for password matching
        .clean_password2() is called in the clean() method
        .password1: is the password field
        .password2: is the password confirmation field
        """

        password1 = self.cleaned_data['password1']  # Get the password from the form data
        password2 = self.cleaned_data['password2']  # Get the password confirmation from the form data

        if password1 and password2 and password1 != password2:  # If the two passwords do not match
            # If the two passwords do not match, raise a ValidationError
            # (This will raise an error and prevent the form from being submitted)
            raise ValidationError("Password don't match")

        # If the two passwords match, return the cleaned data
        return password2  # (This will allow the form to be submitted)

    def save(self, commit=True):
        """
        Custom save method for CreateUserForm
        .save() is called in the save() method
        .commit: is the commit parameter
        .user: user to be created in the database.
        """

        # Get the cleaned data from the form and create a new user
        # Add the first_name and last_name to the user as these are not stored in the User model by default.
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
        )
        return user  # Return the created user

