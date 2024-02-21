from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar 
from datetime import datetime
from django.http import HttpResponseRedirect
from .models import Event, Venue
from django.contrib.auth.models import User
from .forms import VenueForm, EventForm, EventFormAdmin
from django.contrib import messages

#import pagination stuff
from django.core.paginator import Paginator

#create my events page
def my_events(request):
	if request.user.is_authenticated:
		me = request.user.id
		events = Event.objects.filter(attendees= me)

		return render(request, 'events/my_events.html', {"events":events})
	else:
		messages.success(request, ("You are not authorized to view this page"))
		return redirect('home')

#delete an venue
def delete_venue(request, venue_id):
	venue = Venue.objects.get(pk=venue_id)
	if request.user == venue.owner:
		venue.delete()
		messages.success(request, ("Your venue has been deleted"))
		return redirect('list-venues')
	else:
		messages.success(request, ("You are not authorized to delete this venue"))
		return redirect('list-venues')

#delete an event
def delete_event(request, event_id):
	event = Event.objects.get(pk=event_id)
	if request.user == event.manager:
		event.delete()
		messages.success(request, ("Your event has been deleted"))
		return redirect('list-events')
	else:
		messages.success(request, ("You are not authorized to delete this event"))
		return redirect('list-events')


def update_event(request, event_id):
	event = Event.objects.get(pk=event_id)
	if request.user.is_superuser:
		#form = EventFormAdmin(request.POST or None, instance=event)
		form = EventForm(request.POST or None, instance=event)
	else:
		form = EventForm(request.POST or None, instance=event)
	
	if form.is_valid():
		form.save()
		messages.success(request, ("Your event has been updated"))
		return redirect('list-events')

	return render(request, 'events/update_event.html', 
		{'event': event, 'form':form}) 

def add_event(request):
	submitted = False
	if request.method == "POST":
		if request.user.is_superuser:
			#form = EventFormAdmin(request.POST)
			form = EventForm(request.POST)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/add_event?submitted=True')
		else:
			form = EventForm(request.POST)
			if form.is_valid():
				#form.save()
				event = form.save(commit=False)
				event.manager = request.user    #logged in user
				event.save()
				return HttpResponseRedirect('/add_event?submitted=True')
	else:
		#just going to the page, not submitting
		if request.user.is_superuser:
			#form = EventFormAdmin
			form = EventForm
		else:
			form = EventForm

		if 'submitted' in request.GET:
			submitted = True
			
	return render(request, 'events/add_event.html', {'form':form, 'submitted':submitted}) 


def update_venue(request, venue_id):
	venue = Venue.objects.get(pk=venue_id)
	form = VenueForm(request.POST or None, instance=venue)
	if form.is_valid():
		form.save()
		messages.success(request, ("Your venue has been updated"))
		return redirect('list-venues')

	return render(request, 'events/update_venue.html', 
		{'venue': venue, 'form':form}) 

def search_venues(request):
	if request.method == "POST":
		searched = request.POST['searched']
		venues = Venue.objects.filter(name__contains=searched)

		return render(request, 'events/search_venues.html', {'searched':searched, 'venues':venues}) 
	else:
		return render(request, 'events/search_venues.html', {}) 

def search_events(request):
	if request.method == "POST":
		searched = request.POST['searched']
		events = Event.objects.filter(description__contains=searched)

		return render(request, 'events/search_events.html', {'searched':searched, 'events':events}) 
	else:
		return render(request, 'events/search_events.html', {}) 


def show_venue(request, venue_id):
	venue = Venue.objects.get(pk=venue_id)
	venue_owner = User.objects.get(pk=venue.owner)
	return render(request, 'events/show_venue.html', 
		{'venue': venue,
		'venue_owner': venue_owner}) 


def list_venues(request):
	venue_list = Venue.objects.all().order_by('name')

	#set up pagination
	p = Paginator(Venue.objects.all(), 1)
	page = request.GET.get('page')
	venues = p.get_page(page)
	nums = "a" * venues.paginator.num_pages

	return render(request, 'events/venue.html', 
		{'venue_list': venue_list, 'venues': venues, 'nums':nums}) 

def add_venue(request):
	submitted = False
	if request.method == "POST":
		form = VenueForm(request.POST)
		if form.is_valid():
			venue = form.save(commit=False)
			venue.owner = request.user.id    #logged in user
			venue.save()
			#form.save()
			return HttpResponseRedirect('/add_venue?submitted=True')
	else:
		form = VenueForm
		if 'submitted' in request.GET:
			submitted = True
			
	return render(request, 'events/add_venue.html', {'form':form, 'submitted':submitted}) 


def all_events(request):
	event_list = Event.objects.all().order_by('event_date')

	#set up pagination
	p = Paginator(Event.objects.all(), 4)
	page = request.GET.get('page')
	events = p.get_page(page)
	nums = "a" * events.paginator.num_pages

	return render(request, 'events/event_list.html', 
		{'event_list': event_list, 'events': events, 'nums':nums}) 

def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	name = "sarin"
	month = month.capitalize()
	#convert month from name to number
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	#create a calendar
	#cal = HTMLCalendar().formatmonth(year, month_number)
	# Create a calendar with Bootstrap classes and custom styling for sizing
	cal = HTMLCalendar().formatmonth(year, month_number).replace(
	    '<table',
	    '<table class="table table-bordered table-responsive-sm" style="width:30%; text-align:center;"')

	#get current year
	now = datetime.now()
	current_year = now.year

	# query the events model for dates
	event_list = Event.objects.filter(
		event_date__year = year,
		event_date__month = month_number)

	#get current time
	time = now.strftime('%I:%M %p')

	return render(request, 
		'events/home.html', {
		"name" : name,
		"year" : year,
		"month" : month,
		"month_number" : month_number,
		"cal" : cal,
		"current_year" : current_year,
		"time" : time,
		"event_list": event_list,
		})
