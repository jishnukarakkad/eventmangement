from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

class Events(models.Model):
    EVENT_TYPES = [
        ('wedding', 'Wedding'),
        ('birthday', 'Birthday Party'),
        ('reception', 'Reception'),
        ('conference', 'Conference'),
        ('other', 'Other Event'),
    ]

    name = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default='other')
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=100)
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    def clean(self):
        # Ensure the event date is not in the past
        if self.date < timezone.now().date():
            raise ValidationError("Event date cannot be in the past.")

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='Anonymous')
    contact = models.CharField(max_length=200, default='contactnumber')
    booking_date = models.DateField(blank=True, null=False)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    num_tickets = models.PositiveIntegerField(default=1)  # Number of tickets for the booking

    class Meta:
        unique_together = ('user', 'event', 'booking_date')

    def __str__(self):
        return f'Booking for {self.event.name} by {self.user.username}'


from django.db import models

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    feedback = models.TextField()  # Updated to 'feedback'
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contactnumber = models.CharField(max_length=15, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15, blank=True)  # Add other fields as needed

    def __str__(self):
        return self.user.username
