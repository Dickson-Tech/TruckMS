from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test # Import decorators for user authentication and permissions
from django.contrib.auth import authenticate, login, logout # Import authentication functions
from .models import Truck, Driver, Trip, TruckLocation
from .forms import TruckForm, DriverForm, TripForm, UserForm, UserProfileForm, SignUpForm, LoginForm # Import forms for handling data

# Check if the user is Admin or Staff
def is_admin(user):
    return user.is_admin

# Home Page View
@login_required
def home(request):
    trucks = Truck.objects.all() # Get all trucks from the database
    drivers = Driver.objects.all() # Get all drivers from the database
    trips = Trip.objects.all() # Get all trips from the database
    return render(request, 'fleetApp/home.html', { # Render the home page with truck, driver, and trip data
        'trucks': trucks,
        'drivers': drivers,
        'trips': trips
    })

# Truck List View
@login_required
def truck_list(request):
    trucks = Truck.objects.all()
    return render(request, 'fleetApp/truck_list.html', {'trucks': trucks})

# Truck Create View
@login_required
@user_passes_test(is_admin)
def truck_create(request):
    if request.method == 'POST': # Check if the request method is POST
        form = TruckForm(request.POST)  # Create form
        if form.is_valid(): # Validate form data
            form.save()  # Save truck
            messages.success(request, 'Truck added successfully!') # Show success message
            return redirect('truck_list')
    else:
        form = TruckForm()  # Empty form
    return render(request, 'fleetApp/truck_form.html', {'form': form, 'title': 'Add Truck'})

# Truck Update View
@login_required
def truck_update(request, pk):
    truck = get_object_or_404(Truck, pk=pk) # Get truck by primary key
    if request.method == 'POST':
        form = TruckForm(request.POST, instance=truck) # Create form with truck instance
        if form.is_valid():
            form.save()
            messages.success(request, 'Truck updated successfully!')
            return redirect('truck_list')
    else:
        form = TruckForm(instance=truck)
    return render(request, 'fleetApp/truck_form.html', {'form': form, 'title': 'Edit Truck'})

# Truck Delete View
@login_required
def truck_delete(request, pk):
    truck = get_object_or_404(Truck, pk=pk) # Get truck by primary key
    if request.method == 'POST':  # Check if the request method is POST
        truck.delete()
        messages.success(request, 'Truck deleted successfully!')
        return redirect('truck_list')
    return render(request, 'fleetApp/truck_confirm_delete.html', {'truck': truck})

# Truck Track View
@login_required
def truck_track(request, pk): # Get truck by primary key
    truck = get_object_or_404(Truck, pk=pk)
    locations = TruckLocation.objects.filter(truck=truck).order_by('-timestamp')[:10] # Get last 10 locations of the truck
    return render(request, 'fleetApp/truck_track.html', {
        'truck': truck,
        'locations': locations, # Pass locations to the template
        'initial_location': locations.first() if locations else None # Get initial location if available
    })

# User Profile View
@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)  # Form for user data
        profile_form = UserProfileForm(request.POST, instance=request.user)  # Form for profile data
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()  # Save user data
            profile_form.save()  # Save profile data
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user) # Form for user data
        profile_form = UserProfileForm(instance=request.user) # Form for profile data
    return render(request, 'fleetApp/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form # Pass forms to the template
    })

# Sign Up View
def signup(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect if already logged in
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save new user
            login(request, user)  # Log in user
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'fleetApp/signup.html', {'form': form})

 #Login view
def login_view(request):
    if request.user.is_authenticated: # Check if user is already logged in
        return redirect('home')  # Redirect if already logged in
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'] # Get email from form data
            password = form.cleaned_data['password'] # Get password from form data
            user = authenticate(request, email=email, password=password)  # Authenticate user
            if user:
                login(request, user)  # Log in user
                messages.success(request, 'Logged in successfully!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password')
    else:
        form = LoginForm() # Create empty form
    return render(request, 'fleetApp/login.html', {'form': form})

# Logout view
@login_required
def logout_view(request):
    logout(request)  # Log out user
    messages.success(request, 'Logged out successfully!')
    return redirect('login')

# Approve trip view
@login_required
@user_passes_test(is_admin) # Check if user is admin
def trip_approve(request, pk): # Get trip by primary key
    trip = get_object_or_404(Trip, pk=pk) # Get trip by primary key
    if request.method == 'POST':
        trip.status = 'APPROVED'  # Set trip status
        trip.approved_by = request.user  # Set approver
        trip.save()
        messages.success(request, 'Trip approved successfully!')
        return redirect('home')
    return render(request, 'fleetApp/trip_approve.html', {'trip': trip})

# Cancel trip view
@login_required
@user_passes_test(is_admin) # Check if user is admin
def trip_cancel(request, pk):
    trip = get_object_or_404(Trip, pk=pk)
    if request.method == 'POST':
        trip.status = 'CANCELLED'
        trip.save()
        messages.success(request, 'Trip cancelled successfully!')
        return redirect('home')
    return render(request, 'fleetApp/trip_cancel.html', {'trip': trip})