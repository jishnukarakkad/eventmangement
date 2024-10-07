from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('events/', views.events, name='events'),
    path('bookings/',views.bookings, name='bookings'),  # Booking page for logged-in users
    path('contacts/', views.contacts, name='contacts'),
    path('submit_contact/', views.submit_contact, name='submit_contact'),
    path('contact_success/', views.contact_success, name='contact_success'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('feedback/', views.feedback, name='feedback'),  # Feedback submission page
    path('feedback_success/', views.feedback_success, name='feedback_success'), 
    path('view-feedback/', views.view_feedback, name='view_feedback'),  # Feedback viewing page
    path('confirm/<int:booking_id>/', views.confirmation, name='confirmation'),
    path('ticket_email/<int:booking_id>/', views.ticket_email, name='ticket_email'),
    path('profile/', views.profile, name='profile'),  # User profile
    path('about/',views.about,name='about'),
    path('admin_panel/', views.admin_panel, name='admin_panel'),
    path('admin_panel/add_event/', views.add_event, name='add_event'),
    path('admin_panel/edit_event/<int:event_id>/', views.edit_event, name='edit_event'),
    path('admin_panel/delete_event/<int:event_id>/', views.delete_event, name='delete_event'),
    
]
