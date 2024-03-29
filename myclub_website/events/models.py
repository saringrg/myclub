from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Venue(models.Model):
	name = models.CharField('Venue Name', max_length=120)
	address = models.CharField(max_length=300)
	zip_code = models.CharField('Zip Code', max_length=15)
	phone = models.CharField('Contact Phone', max_length=25, blank=True) 
	web = models.URLField('Website Address', blank=True)
	email_address = models.EmailField('Email Address', blank=True)
	owner = models.IntegerField("Venue Owner", blank=False, default=1)
	venue_description = models.TextField(blank=True)
	venue_image = models.ImageField(null=True, blank=True, upload_to="images/")

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['name']

class MyClubUser(models.Model):
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	email = models.EmailField('User Email')

	def __str__(self):
		return self.first_name + ' ' + self.last_name


class Event(models.Model):
	name = models.CharField('Event Name', max_length=120)
	event_date = models.DateField('Event Date', blank=False)
	venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
	#venue = models.CharField(max_length=120)
	#manager = models.CharField(max_length=60)
	manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
	description = models.TextField(blank=True)
	attendees = models.ManyToManyField(MyClubUser, blank=True)


	def __str__(self):
		return self.name

	@property
	def Days_till(self):
		today = date.today()
		if self.event_date < today:
			return "Registration Closed"
		else:
			days_till = self.event_date - today
			if days_till.days == 1:
				return f"{days_till.days} day left"
			else:
				return f"{days_till.days} days left"
	
	class Meta:
		ordering = ['-event_date']