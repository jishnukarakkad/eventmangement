from django import forms
from .models import Booking, Events, Feedback, Contact

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['event', 'name', 'contact', 'email', 'booking_date', 'num_tickets']

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['event'].queryset = Events.objects.all()
        self.fields['name'].widget.attrs.update({'placeholder': 'Your Name'})
        self.fields['contact'].widget.attrs.update({'placeholder': 'Your Contact Information'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Your Email Address'})
        self.fields['booking_date'].widget.attrs.update({'placeholder': 'YYYY-MM-DD'})
        self.fields['num_tickets'].widget.attrs.update({'placeholder': 'Number of Tickets'})  # Add placeholder



# Feedback form


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'feedback']  # Updated to 'feedback'

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'placeholder': 'Your Name'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Your Email'})
        self.fields['feedback'].widget.attrs.update({'placeholder': 'Your Feedback'})  # Updated to 'feedback'


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'contactnumber', 'subject', 'message']

class EventForm(forms.ModelForm):
    class Meta:
        model = Events  # Make sure to use the updated singular name
        fields = ['name', 'description', 'date', 'location', 'price_per_person']  # Adjust these fields according to your model
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),  # HTML5 date picker
        }
