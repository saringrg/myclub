from django import forms
from django.forms import ModelForm
from .models import Venue, Event, MyClubUser
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from datetime import date


class EventRegistrationForm(ModelForm):
	first_name = forms.CharField(label='First Name', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
	last_name = forms.CharField(label='Last Name', max_length=30, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
	email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
	event_name = forms.CharField(label='Event Name', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
	event_venue = forms.CharField(label='Venue', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
	event_date = forms.DateField(label='Event Date', required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
	registration_fee = forms.IntegerField(label='Registration Fee', required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))

	class Meta:
		model = MyClubUser
		fields = []

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		self.event = kwargs.pop('event', None)
		super(EventRegistrationForm, self).__init__(*args, **kwargs)

		if self.user:
			self.fields['first_name'].initial = self.user.first_name
			self.fields['last_name'].initial = self.user.last_name
			self.fields['email'].initial = self.user.email

		if self.event:
			self.fields['event_name'].initial = self.event.name
			self.fields['event_venue'].initial = self.event.venue.name
			self.fields['event_date'].initial = self.event.event_date
			self.fields['registration_fee'].initial = self.event.registration_fee

	def clean(self):
		cleaned_data = super().clean()

		if MyClubUser.objects.filter(user=self.user, event=self.event).exists():
			raise forms.ValidationError("You are already registered for this event.")

		# Check if the user is the event manager
		if self.event.manager == self.user:
			raise forms.ValidationError("You are the owner of this event.")

		return cleaned_data

"""
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
"""

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
			'registration_fee': forms.NumberInput(attrs={'class': 'form-control'}),
			'description': forms.Textarea(attrs={'class':'form-control'}),
		}

	def clean_registration_fee(self):
		registration_fee = self.cleaned_data['registration_fee']
		if registration_fee < 0:
			raise forms.ValidationError("Registration fee cannot be negative")
		return registration_fee

	def clean_venue(self):
		venue = self.cleaned_data.get('venue')
		if not venue:
			raise forms.ValidationError("Please select a venue")
		return venue

	def clean_event_date(self):
		event_date = self.cleaned_data.get('event_date')
		if event_date < date.today():
			raise ValidationError("Event date cannot be in the past.")
		return event_date

	def clean(self):
		cleaned_data = super().clean()
		event_date = cleaned_data.get('event_date')
		if self.instance and self.instance.pk and event_date and self.instance.event_date < date.today():
			raise ValidationError("You cannot update a past event.")
		return cleaned_data

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
			'registration_fee': forms.NumberInput(attrs={'class': 'form-control'}),
			'description': forms.Textarea(attrs={'class':'form-control'}),
		}

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(EventForm, self).__init__(*args, **kwargs)

	def clean_registration_fee(self):
		registration_fee = self.cleaned_data['registration_fee']
		if registration_fee < 0:
			raise forms.ValidationError("Registration fee cannot be negative")
		return registration_fee

	def clean_venue(self):
		venue = self.cleaned_data.get('venue')
		if not venue:
			raise forms.ValidationError("Please select a venue")
		
		# Check if the venue is private and the user is not the owner
		if venue and not venue.make_public and self.user.id != venue.owner:
			raise forms.ValidationError('You are not authorized to create an event for this venue.')

		return venue

	def clean_event_date(self):
		event_date = self.cleaned_data.get('event_date')
		if event_date < date.today():
			raise ValidationError("Event date cannot be in the past.")
		return event_date

	def clean(self):
		cleaned_data = super().clean()
		if self.instance and self.instance.event_date < date.today():
			raise ValidationError("You cannot update a past event.")
		return cleaned_data
		
#create a venue form
class VenueForm(ModelForm):
	class Meta:
		model = Venue
		fields = ('name', 'address', 'zip_code', 'phone', 'web', 'email_address', 'venue_description', 'venue_image', 'capacity', 'make_public')
		labels = {
			'name': 'Venue Name',
			'address': 'Venue Address',
			'zip_code': 'Zip Code',
			'phone': 'Phone',
			'web': 'Web Address',
			'email_address': 'Email',
			'venue_description': 'Venue Description',
			'venue_image': 'Venue Image',
			'capacity': 'capacity',
			'make_public': 'Make Public',
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
			'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
			'make_public': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
		}

	def clean_capacity(self):
		capacity = self.cleaned_data.get('capacity')
		if capacity is not None and capacity < 0:
			raise ValidationError("Capacity cannot be negative")
		return capacity

#create a venue form
class VenueFormAdmin(ModelForm):
	class Meta:
		model = Venue
		fields = ('name', 'address', 'zip_code', 'phone', 'web', 'email_address', 'capacity', 'venue_description')
		labels = {
			'name': 'Venue Name',
			'address': 'Venue Address',
			'zip_code': 'Zip Code',
			'phone': 'Phone',
			'web': 'Web Address',
			'email_address': 'Email',
			'capacity': 'Capacity',
			'venue_description': 'Venue Description',
		}

		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control'}),
			'address': forms.TextInput(attrs={'class':'form-control'}),
			'zip_code': forms.TextInput(attrs={'class':'form-control'}),
			'phone': forms.TextInput(attrs={'class':'form-control'}),
			'web': forms.TextInput(attrs={'class':'form-control'}),
			'email_address': forms.EmailInput(attrs={'class':'form-control'}),
			'capacity': forms.NumberInput(attrs={'class':'form-control'}),
			'venue_description': forms.Textarea(attrs={'class':'form-control'}),
		}

	def clean_capacity(self):
		capacity = self.cleaned_data.get('capacity')
		if capacity is not None and capacity < 0:
			raise ValidationError("Capacity cannot be negative")
		return capacity
		