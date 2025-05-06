from django.db import models # Import Django's models model for database interaction
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin # Import auth base classes for custom user model
from django.utils import timezone # Import timezone utilities for date/time handling

# Create your models here.
# Defining the Driver model
# Custom user manager for User model
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:  # Validate email
            raise ValueError('Email is required')
        email = self.normalize_email(email)  # Normalize email address
        user = self.model(email=email, **extra_fields)  # Create user instance
        user.set_password(password)  # Hash and set password
        user.save(using=self._db)  # Save user to database
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)  # Set staff status
        extra_fields.setdefault('is_superuser', True)  # Set superuser status
        extra_fields.setdefault('is_admin', True)  # Set admin role
        return self.create_user(email, password, **extra_fields)  # Create user

# Custom User model
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)  # Store unique email
    first_name = models.CharField(max_length=50)  # Store first name
    last_name = models.CharField(max_length=50)  # Store last name
    phone = models.CharField(max_length=15, blank=True)  # Store optional phone
    is_active = models.BooleanField(default=True)  # Track active status
    is_staff = models.BooleanField(default=False)  # Track staff status
    is_admin = models.BooleanField(default=False)  # Track admin role
    date_joined = models.DateTimeField(default=timezone.now)  # Store join date

    objects = UserManager()  # Assign custom manager
    USERNAME_FIELD = 'email'  # Use email as username
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Required fields for superuser

    def __str__(self):
        return f"{self.first_name} {self.last_name}"  # Return full name
class Driver(models.Model):
    name = models.CharField(max_length=100) # Store driver's name, max 100 characters
    license_number = models.CharField(max_length=50, unique=True) # Store unique license number, max 50 characters
    phone = models.CharField(max_length=15) # Store driver's phone number, max 15 characters
    created_at = models.DateTimeField(auto_now_add=True) # Automatically set creation date/time

    def __str__(self):
        return self.name # String representation of the driver

# Defining the Truck model
class Truck(models.Model):
    registration_number = models.CharField(max_length=20, unique=True) # Store unique registration number, max 20 characters
    model = models.CharField(max_length=50) # Store truck model, max 50 characters
    capacity = models.FloatField()  # store capacity in tons
    status = models.CharField(max_length=20, choices=[
        ('AVAILABLE', 'Available'), # Truck is available for trips
        ('IN_TRANSIT', 'In Transit'), # Truck is currently on a trip
        ('MAINTENANCE', 'Maintenance'), # Truck is under maintenance
    ], default='AVAILABLE') # Default status is available
    created_at = models.DateTimeField(auto_now_add=True) # Automatically set creation date/time

    def __str__(self):
        return f"{self.model} ({self.registration_number})" # Return model and registration number as string representation

# Defining the Trip model
class Trip(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE) # Link to Truck model, delete trip if truck is deleted
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE) # Link to Driver model, delete trip if driver is deleted
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True) # Store trip end date, can be null or blank
    cargo_weight = models.FloatField()
    status = models.CharField(max_length=20, choices=[
        ('PLANNED', 'Planned'), # Trip is planned but not started yet
        ('APPROVED', 'Approved'), # Trip has started but not completed yet
        ('IN_PROGRESS', 'In Progress'), # Trip is currently in progress
        ('COMPLETED', 'Completed'), # Trip has been completed
        ('CANCELLED', 'Cancelled'), # Trip has been cancelled
        ('DELAYED', 'Delayed'), # Trip is delayed
        ('ON_HOLD', 'On Hold'), # Trip is on hold
    ], default='PLANNED')
    created_at = models.DateTimeField(auto_now_add=True) # Automatically set creation date/time
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
    related_name='created_trips')  # Link to creator
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
    related_name='approved_trips')  # Link to approver
    def __str__(self):
        return f"Trip from {self.origin} to {self.destination}" # Return trip details as string representation
    
# Defining the TruckLocation model for tracking truck locations
class TruckLocation(models.Model):
    truck = models.ForeignKey(Truck, on_delete=models.CASCADE) # Link to Truck model, delete location if truck is deleted
    latitude = models.FloatField() # Store latitude of truck location
    longitude = models.FloatField() # Store longitude of truck location
    timestamp = models.DateTimeField(auto_now_add=True) # Automatically set creation date/time

    def __str__(self):
        return f"{self.truck} at ({self.latitude}, {self.longitude})" # Return truck and location as string representation