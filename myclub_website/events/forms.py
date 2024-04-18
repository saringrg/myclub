from django import forms
from django.forms import ModelForm
from .models import Venue, Event
from django.contrib.auth.models import User

class EventRegistrationForm(forms.Form):
	event_name = forms.CharField(label='Event Name', widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True}))
	event_date = forms.DateField(label='Event Date', widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'readonly': True}))
	venue = forms.CharField(label='Venue', widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True}))
	registration_fee = forms.IntegerField(label='Registration Fee', widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': True}))
	first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True}))
	last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True}))
	email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control', 'readonly': True}))

	def __init__(self, *args, **kwargs):
		event_instance = kwargs.pop('event_instance', None)  # Get the event instance from the kwargs
		user = kwargs.pop('user', None)  # Get the user from the kwargs
		super(EventRegistrationForm, self).__init__(*args, **kwargs)
		if event_instance:
			# If event instance is provided, populate the event name, event date, and venue fields
			self.fields['event_name'].initial = event_instance.name
			self.fields['event_date'].initial = event_instance.event_date
			self.fields['venue'].initial = event_instance.venue
			self.fields['registration_fee'].initial = event_instance.registration_fee
		if user:
			# If user is authenticated, populate the first name, last name, and email fields
			self.fields['first_name'].initial = user.first_name
			self.fields['last_name'].initial = user.last_name
			self.fields['email'].initial = user.email

#admin event form
"""
class EventFormAdmin(ModelForm):
	class Meta:
		model = Event
		fields = ('name', 'event_date', 'venue', 'manager', 'attendees', 'description')
		labels = {
			'name': '',
			'event_date': 'YYYY-MM-DD HH:MM:SS',
			'venue': 'Venue',
			'manager': 'Manager',
			'attendees': 'Attendees',
			'description': '',
		}
 
		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Event Name'}),
			'event_date': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Event Date'}),
			'venue': forms.Select(attrs={'class':'form-select', 'placeholder':'Venue'}),
			'manager': forms.Select(attrs={'class':'form-select', 'placeholder':'Manager'}),
			'attendees': forms.SelectMultiple(attrs={'class':'form-select', 'placeholder':'Attendees'}),
			'description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Description'}),
		}
"""

class EventFormAdmin(ModelForm):
	class Meta:
		model = Event
		fields = ('name', 'event_date', 'registration_fee', 'description')
		labels = {
			'name': 'Event Name',
			'event_date': 'Event Date',
			'registration_fee': 'Registration Fee',
			'description': 'Event Description',
		}

		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control'}),
			'event_date': forms.TextInput(attrs={'class':'form-control', 'placeholder':'YYYY-MM-DD'}),
			'registration_fee': forms.TextInput(attrs={'class': 'form-control'}),
			'description': forms.Textarea(attrs={'class':'form-control'}),
		}

#user event form
class EventForm(ModelForm):
	class Meta:
		model = Event
		fields = ('name', 'event_date', 'venue', 'registration_fee', 'description')
		labels = {
			'name': 'Event Name',
			'event_date': 'Event Date',
			'venue': 'Venue',
			#'attendees': 'Attendees',
			'registration_fee': 'Registration Fee',
			'description': 'Event Description',
		}

		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control'}),
			'event_date': forms.TextInput(attrs={'class':'form-control', 'placeholder':'YYYY-MM-DD'}),
			'venue': forms.Select(attrs={'class':'form-select'}),
			#'attendees': forms.SelectMultiple(attrs={'class':'form-select'}),
			'registration_fee': forms.TextInput(attrs={'class': 'form-control'}),
			'description': forms.Textarea(attrs={'class':'form-control'}),
		}
		
#create a venue form
class VenueForm(ModelForm):
	class Meta:
		model = Venue
		fields = ('name', 'address', 'zip_code', 'phone', 'web', 'email_address', 'venue_description', 'venue_image')
		labels = {
			'name': 'Venue Name',
			'address': 'Venue Address',
			'zip_code': 'Zip Code',
			'phone': 'Phone',
			'web': 'Web Address',
			'email_address': 'Email',
			'venue_description': 'Venue Description',
			'venue_image': 'Venue Image',
		}

		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control'}),
			'address': forms.TextInput(attrs={'class':'form-control'}),
			'zip_code': forms.TextInput(attrs={'class':'form-control'}),
			'phone': forms.TextInput(attrs={'class':'form-control'}),
			'web': forms.TextInput(attrs={'class':'form-control'}),
			'email_address': forms.EmailInput(attrs={'class':'form-control'}),
			'venue_description': forms.Textarea(attrs={'class':'form-control'}),
			'venue_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
		}

#create a venue form
class VenueFormAdmin(ModelForm):
	class Meta:
		model = Venue
		fields = ('name', 'address', 'zip_code', 'phone', 'web', 'email_address', 'venue_description')
		labels = {
			'name': 'Venue Name',
			'address': 'Venue Address',
			'zip_code': 'Zip Code',
			'phone': 'Phone',
			'web': 'Web Address',
			'email_address': 'Email',
			'venue_description': 'Venue Description',
		}

		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control'}),
			'address': forms.TextInput(attrs={'class':'form-control'}),
			'zip_code': forms.TextInput(attrs={'class':'form-control'}),
			'phone': forms.TextInput(attrs={'class':'form-control'}),
			'web': forms.TextInput(attrs={'class':'form-control'}),
			'email_address': forms.EmailInput(attrs={'class':'form-control'}),
			'venue_description': forms.Textarea(attrs={'class':'form-control'}),
		}
		