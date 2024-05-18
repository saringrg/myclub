from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class Venue(models.Model):
	name = models.CharField('Venue Name', max_length=120)
	address = models.CharField(max_length=300)
	zip_code = models.CharField('Zip Code', max_length=15)
	phone_regex = RegexValidator(regex=r'^\d{10}$', message="Phone number must be exactly 10 digits.")
	phone = models.CharField('Contact Phone', max_length=10, validators=[phone_regex]) 
	web = models.URLField('Website Address', blank=False)
	email_address = models.EmailField('Email Address', blank=False)
	owner = models.IntegerField("Venue Owner", blank=False, default=1)
	venue_description = models.TextField(blank=False)
	venue_image = models.ImageField(null=True, blank=True, upload_to="images/")
	capacity = models.IntegerField("Capacity", blank=False)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['name']

class Event(models.Model):
	name = models.CharField('Event Name', max_length=120)
	event_date = models.DateField('Event Date', blank=False)
	venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
	#venue = models.CharField(max_length=120)
	#manager = models.CharField(max_length=60)
	manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
	description = models.TextField(blank=False)
	#attendees = models.ManyToManyField(MyClubUser, blank=True)
	registration_fee = models.IntegerField('Registration Fee', blank=False)


	def __str__(self):
		return self.name

	def clean(self):
		# Check if there's already an event for the same venue and date
		if Event.objects.filter(venue=self.venue, event_date=self.event_date).exclude(pk=self.pk).exists():
			raise ValidationError('Sorry! An event for this venue on this date already exists.')

	@property
	def Days_till(self):
		today = date.today()
		if self.event_date == today:
			return "Today"
		elif self.event_date < today:
			return "Registration Closed"
		else:
			days_till = self.event_date - today
			if days_till.days == 1:
				return f"{days_till.days} day left"
			else:
				return f"{days_till.days} days left"
	
	class Meta:
		ordering = ['-event_date']

class MyClubUser(models.Model):
	user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
	event = models.ForeignKey(Event, blank=True, null=True, on_delete=models.CASCADE)

	def clean(self):
		# Check if the user is already registered for this event
		if MyClubUser.objects.filter(user=self.user, event=self.event).exists():
			raise ValidationError(('You are already registered for this event.'))

	def __str__(self):
		return f"{self.user.username} - {self.event.name}"

	class Meta:
		unique_together = ('user', 'event')