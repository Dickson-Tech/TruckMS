from django import forms # Import Django forms module
from django.contrib.auth.forms import UserCreationForm # Import User model for user-related forms
from .models import Truck, Driver, Trip, User # Import models for form definitions

class TruckForm(forms.ModelForm):
    class Meta:
        model = Truck # Associate form with Truck model
        fields = ['registration_number', 'model', 'capacity', 'status']

# Form for creating/updating drivers
class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver # Associate form with Driver model
        fields = ['name', 'license_number', 'phone'] # Include specified fields

# Form for creating/updating trips
class TripForm(forms.ModelForm):
    class Meta: 
        models = Trip # Associate form with Trip model
        fields = ['truck', 'driver', 'origin', 'destination', 'start_date', 'end_date', 'cargo_weight', 'status']  # Include specified fields
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),  # Use datetime-local input for start date
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),  # Use datetime-local input for end date
        }

# User form for profile
class UserForm(forms.ModelForm):
    class Meta:
        model = User  # Associate form with User model
        fields = ['first_name', 'last_name', 'email', 'phone']  # Include specified fields

# Profile form
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User  # Associate form with User model
        fields = ['first_name', 'last_name', 'email', 'phone']  # Include specified fields

# Signup form for user registration
class SignUpForm(UserCreationForm):
    class Meta:
        model = User  # Associate form with User model
        fields = ['email', 'first_name', 'last_name', 'phone', 'password1', 'password2']  # Include specified fields
        widgets = {
            'password1': forms.PasswordInput(),  # Use password input for password1
            'password2': forms.PasswordInput(),  # Use password input for password2
        }
# Login form for user authentication
class LoginForm(forms.Form):
    email = forms.EmailField()  # Email field for user login
    password = forms.CharField(widget=forms.PasswordInput())  # Password field for user login
    remember_me = forms.BooleanField(required=False)  # Checkbox for "remember me" option
    