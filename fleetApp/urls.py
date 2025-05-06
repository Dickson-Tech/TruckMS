from django.urls import path  # Import path for URL routing
from . import views # Import views from trucks app

urlpatterns = [
    path('', views.home, name='home'), #Route root to home view
    path('fleetApp/', views.truck_list, name='truck_list'), # Route /trucks/ to truck list view
    path('fleetApp/new/', views.truck_create, name='truck_create'), # Route /trucks/new/ to create truck view
    path('fleetApp/<int:pk>/edit/', views.truck_update, name='truck_update'), # Route /trucks/<id>/edit/ to update truck view
    path('fleetApp/<int:pk>/delete/', views.truck_delete, name='truck_delete'), # Route /trucks/<id>/delete/ to delete truck view
    path('fleetApp/<int:pk>/track/', views.truck_track, name='truck_track'), # Route /trucks/<id>/track/ to track truck view
    path('profile/', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('trips/<int:pk>/approve/', views.trip_approve, name='trip_approve'), # Route /trips/<id>/approve/ to approve trip view
    path('trips/<int:pk>/cancel/', views.trip_cancel, name='trip_cancel'),
]

    # Add similar patterns for driver and trip URLss