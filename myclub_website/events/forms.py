from django import forms
from django.forms import ModelForm
from .models import Venue, Event

#admin event form
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

#user event form
class EventForm(ModelForm):
	class Meta:
		model = Event
		fields = ('name', 'event_date', 'venue', 'description')
		labels = {
			'name': 'Event Name',
			'event_date': 'Event Date',
			'venue': 'Venue',
			#'attendees': 'Attendees',
			'description': 'Event Description',
		}

		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control'}),
			'event_date': forms.TextInput(attrs={'class':'form-control', 'placeholder':'YYYY-MM-DD'}),
			'venue': forms.Select(attrs={'class':'form-select'}),
			#'attendees': forms.SelectMultiple(attrs={'class':'form-select'}),
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
		