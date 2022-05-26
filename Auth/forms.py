from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError


class CreateUserForm(UserCreationForm):
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
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def username_clean(self):
        username = self.cleaned_data['username'].lower()
        new = User.objects.filter(username=username)
        if new.count():
            raise ValidationError("User Already Exist")
        return username

    def email_clean(self):
        email = self.cleaned_data['email'].lower()
        new = User.objects.filter(email=email)
        if new.count():
            raise ValidationError(" Email Already Exist")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
        )
        return user

