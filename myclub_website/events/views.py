from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar 
from datetime import datetime
from django.http import HttpResponseRedirect
from .models import Event, Venue
from .forms import VenueForm, EventForm, EventFormAdmin
from django.contrib import messages

#import pagination stuff
from django.core.paginator import Paginator



#delete an venue
def delete_venue(request, venue_id):
	venue = Venue.objects.get(pk=venue_id)
	venue.delete()
	return redirect('list-venues')

#delete an event
def delete_event(request, event_id):
	event = Event.objects.get(pk=event_id)
	if request.user == event.manager:
		event.delete()
		messages.success(request, ("Event Deleted"))
		return redirect('list-events')
	else:
		messages.success(request, ("You are not authorized to Delete this event"))
		return redirect('list-events')


def update_event(request, event_id):
	event = Event.objects.get(pk=event_id)
	if request.user.is_superuser:
		form = EventFormAdmin(request.POST or None, instance=event)
	else:
		form = EventForm(request.POST or None, instance=event)
	
	if form.is_valid():
		form.save()
		return redirect('list-events')

	return render(request, 'events/update_event.html', 
		{'event': event, 'form':form}) 

def add_event(request):
	submitted = False
	if request.method == "POST":
		if request.user.is_superuser:
			form = EventFormAdmin(request.POST)
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
			form = EventFormAdmin
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


def show_venue(request, venue_id):
	venue = Venue.objects.get(pk=venue_id)
	return render(request, 'events/show_venue.html', 
		{'venue': venue}) 


def list_venues(request):
	venue_list = Venue.objects.all().order_by('name')

	#set up pagination
	p = Paginator(Venue.objects.all(), 10)
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
	p = Paginator(Event.objects.all(), 10)
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
	cal = HTMLCalendar().formatmonth(year, month_number)

	#get current year
	now = datetime.now()
	current_year = now.year

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
		})
