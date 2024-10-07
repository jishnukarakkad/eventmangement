from django.contrib import admin
from .models import Events, Booking, Feedback 
from .models import Contact 
from . models import Profile
# Register the Event model with custom display in the admin

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'location', 'price_per_person')
    fields = ('name', 'description', 'date', 'location', 'price_per_person')


# Register the Booking model with custom display in the admin
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'created_at')  # Display booking info in admin list
    search_fields = ('user__username', 'event__name')  # Search by username or event name
    list_filter = ('event', 'created_at')  # Add filters for events and creation date

# Register the Feedback model with custom display in the admin
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at')  # Columns to display in the admin list view
    search_fields = ('name', 'email', 'feedback')  # Add search functionality
    list_filter = ('submitted_at',)  # Filter feedback by submission date

from .models import Contact

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'contactnumber', 'subject', 'created_at')
    search_fields = ('name', 'email', 'contact_number', 'subject')
    list_filter = ('created_at',)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact_number')  # Display these fields in the admin list view
    search_fields = ('user__username', 'user__email', 'contact_number')  # Enable searching



# Register models to the admin site
admin.site.register(Events,EventAdmin)
admin.site.register(Booking,BookingAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Feedback, FeedbackAdmin)  # Register the Feedback model
admin.site.register(Profile,ProfileAdmin)
