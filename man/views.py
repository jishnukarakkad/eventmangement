from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .forms import BookingForm, FeedbackForm, ContactForm  
from .models import Events, Booking, Feedback 
from django.contrib.auth import logout 
from django.contrib import messages
from .models import Profile, Booking  # Ensure the Profile model is imported
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib import messages
from .models import Booking
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Events
from .forms import EventForm
from django import forms
from django.contrib.auth.models import User



# Home page
def index(request):
    return render(request, 'index.html')

# Event listing page
def events(request):
    events = Events.objects.all()
    return render(request, 'events.html', {'events': events})

# Feedback page
def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()  # Save the feedback to the database
            return redirect('feedback_success')  # Redirect after successful submission
        else:
            print(form.errors)  # Log any validation errors for debugging
    else:
        form = FeedbackForm()

    return render(request, 'feedback.html', {'form': form})

# View to display all feedback submissions
def view_feedback(request):
    feedback_list = Feedback.objects.all().order_by('-submitted_at')
    return render(request, 'view_feedback.html', {'feedback_list': feedback_list})


# Contact page
def contacts(request):
    return render(request, 'contacts.html')


@login_required
def confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    # Calculate the total price
    total_price = booking.event.price_per_person * booking.num_tickets  # Calculate based on num_tickets

    # Prepare email details (optional)
    subject = 'Your Ticket Confirmation'
    to_email = booking.email
    email_content = render_to_string('ticket_email.html', {
        'booking': booking,
        'user_email': booking.email,
        'total_price': total_price  # Pass the total price to the email template
    })

    # Send confirmation email (optional)
    try:
        email = EmailMultiAlternatives(subject, '', 'testing450439@gmail.com', [to_email])
        email.attach_alternative(email_content, "text/html")
        email.send(fail_silently=False)
        messages.success(request, 'A confirmation email has been sent to your email address.')
    except Exception as e:
        messages.error(request, f'Error sending email: {e}')

    return render(request, 'confirmation.html', {
        'booking': booking,
        'user_email': booking.email,
        'total_price': total_price  # Pass the total price to the template
    })






# Ticket email page
def ticket_email(request):
    return render(request, 'ticket_email.html')

def contact_success(request):
    return render(request, 'contact_success.html')

# Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect(request.GET.get('next', 'index'))  # Redirect to the next page or index
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')


# Register view
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user and get the instance
            # Create a Profile for the new user
            Profile.objects.create(user=user)  # Initialize profile with default values
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})

# Book an event
@login_required
def bookings(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking_date = form.cleaned_data['booking_date']
            event = form.cleaned_data['event']
            num_tickets = form.cleaned_data['num_tickets']  # Get number of tickets

            # Check for existing bookings
            existing_booking = Booking.objects.filter(
                user=request.user,
                event=event,
                booking_date=booking_date
            ).first()

            if existing_booking:
                messages.warning(request, 'You already have a booking for this event on the selected date.')
                return redirect('events')

            # Create new booking
            booking = form.save(commit=False)
            booking.user = request.user
            total_price = event.price_per_person * num_tickets  # Calculate total price
            booking.total_price = total_price  # Assuming you have a total_price field
            booking.save()

            messages.success(request, 'Your booking has been created successfully!')
            return redirect('confirmation', booking_id=booking.id)

    else:
        form = BookingForm()

    events = Events.objects.all()
    return render(request, 'bookings.html', {'form': form, 'events': events})





# Create a new view to handle the login redirect from bookings
def redirect_to_login(request):
    messages.info(request, "Please log in to view the bookings.")  # Set the message
    return redirect('login')

def submit_contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_success')  
    else:
        form = ContactForm()

    return render(request, 'contacts.html', {'form': form})

@login_required
def profile(request):
    # Retrieve bookings for the logged-in user
    bookings = Booking.objects.filter(user=request.user)

    # Pass the user information to the template
    return render(request, 'profile.html', {'bookings': bookings, 'user': request.user})

def logout_view(request):
    logout(request)  # Log out the user
    return redirect('index') 

def about(request):
    return render(request,'about.html')








# Admin panel to display all events
@login_required
def admin_panel(request):
    events = Events.objects.all()  # Fetch all events
    return render(request, 'admin.html', {'events': events})


# Add Event View
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    else:
        form = EventForm()
    return render(request, 'add_event.html', {'form': form})

# Edit Event View
def edit_event(request, event_id):
    event = get_object_or_404(Events, pk=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('admin_panel')
    else:
        form = EventForm(instance=event)
    return render(request, 'edit_event.html', {'form': form, 'event': event})

# Delete Event View
def delete_event(request, event_id):
    event = get_object_or_404(Events, pk=event_id)
    if request.method == 'POST':
        event.delete()
        return redirect('admin_panel')
    return render(request, 'delete_event.html', {'event': event})


def booking_view(request):
    events = Events.objects.all()  # Fetch all events from the database

    if request.method == 'POST':
        new_event_name = request.POST.get('new_event_name')
        new_event_date = request.POST.get('new_event_date')
        selected_event_id = request.POST.get('event')
        
        # Check if a new event is being created
        if new_event_name and new_event_date:
            # Create a new event
            new_event = Events(name=new_event_name, date=new_event_date)
            new_event.save()

            # Now create a booking for the new event
            booking = Booking.objects.create(
                event=new_event,
                name=request.POST.get('name'),
                email=request.POST.get('email'),
                contact=request.POST.get('contact'),
                booking_date=request.POST.get('booking_date')
            )

            # Send confirmation email
            send_booking_confirmation(booking)
            messages.success(request, f'New event "{new_event.name}" created and booked successfully!')
            return redirect('events')  # Redirect to events page after booking

        # Otherwise, handle booking for the selected event
        if selected_event_id:
            event = Events.objects.get(id=selected_event_id)
            booking = Booking.objects.create(
                event=event,
                name=request.POST.get('name'),
                email=request.POST.get('email'),
                contact=request.POST.get('contact'),
                booking_date=request.POST.get('booking_date')
            )

            # Send confirmation email
            send_booking_confirmation(booking)
            messages.success(request, f'Booking for "{event.name}" has been confirmed!')
            return redirect('events')  # Redirect to events page after booking

    return render(request, 'booking.html', {'events': events})  # Render the booking page

def send_booking_confirmation(booking):
    subject = 'Booking Confirmation'
    message = f'Hello {booking.name},\n\nYour booking for the event "{booking.event.name}" on {booking.event.date} has been confirmed!\n\nThank you for choosing us!\nJK Events'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [booking.email]
    
    send_mail(subject, message, email_from, recipient_list)

def feedback_success(request):
    return render(request,'feedback_success.html')





