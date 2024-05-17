from django.shortcuts import render, redirect, get_object_or_404
import calendar
from calendar import HTMLCalendar 
from datetime import date, datetime, timedelta
from django.http import HttpResponseRedirect
from .models import Event, Venue, MyClubUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import VenueForm, EventForm, EventRegistrationForm, VenueFormAdmin, EventFormAdmin
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import format_html
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


import hmac
import hashlib
import base64
import uuid


def get_event_details(request):
	event_id = request.GET.get('event_id')
	event = get_object_or_404(Event, id=event_id)
	data = {
		'name': event.name,
		'event_date': event.event_date,
		'registration_fee': event.registration_fee,  # Assuming venue is related to Event model
		'description': event.description  # Assuming manager is related to User model
	}
	return JsonResponse(data)

def get_venue_details(request):
	venue_id = request.GET.get('venue_id')
	venue = get_object_or_404(Venue, id=venue_id)
	data = {
		'name': venue.name,
		'address': venue.address,
		'zip_code': venue.zip_code,
		'phone': venue.phone,
		'email_address': venue.email_address,
		'web': venue.web,
		'description': venue.venue_description,
	}
	return JsonResponse(data)

def admin_approval(request):
	if request.method == 'POST':
		event_form = EventFormAdmin(request.POST)
		venue_form = VenueFormAdmin(request.POST)
		if event_form.is_valid():
			event_id = request.POST.get('event_id')
			event = get_object_or_404(Event, pk=event_id)
			event_form = EventFormAdmin(request.POST, instance=event)
			if event_form.is_valid():
				event_form.save()
				return redirect('admin_approval')
		elif venue_form.is_valid():
			venue_id = request.POST.get('venue_id')
			venue = get_object_or_404(Venue, pk=venue_id)
			venue_form = VenueFormAdmin(request.POST, instance=venue)
			if venue_form.is_valid():
				venue_form.save()
				return redirect('admin_approval')
	else: 
		event_form = EventFormAdmin()
		venue_form = VenueFormAdmin()

	event_count = Event.objects.all().count()
	venue_count = Venue.objects.all().count()
	#user_count = User.objects.all().count()
	user_count = User.objects.exclude(is_superuser=True).count()

	event_list = Event.objects.all().order_by('-event_date')
	venue_list = Venue.objects.all().order_by('name')
	users = User.objects.all()

	return render(request, 'events/admin_approval.html', {"event_count":event_count, "venue_count":venue_count, "user_count":user_count, "event_list":event_list, 'venue_list':venue_list, 'users':users, 'event_form':event_form, 'venue_form':venue_form})

def delete_user(request, user_id):
	user = User.objects.get(pk=user_id)

	if request.user.is_superuser:
		user.delete()
		return redirect('admin_approval')
	else:
		messages.error(request, "You are not authorized to delete this user")
		return redirect('home')

def event_form_view(request, event_id):
	# Assuming the user is authenticated
	if request.user.is_authenticated:
		event_instance = get_object_or_404(Event, pk=event_id)
		#event_instance = Event.objects.get(pk=event_id)

		if event_instance.event_date < date.today():
			event_closed = True
			form = None

		else:
			event_closed = False
			form = EventRegistrationForm(event_instance=event_instance, user=request.user)
			if request.method == 'POST':
				form = EventRegistrationForm(request.POST, event_instance=event_instance, user=request.user)
				if form.is_valid():
					# Get form data
					event_name = event_instance.name 
					event_date = event_instance.event_date
					venue = event_instance.venue.name if event_instance.venue else "N/A"
					first_name = request.user.first_name
					last_name = request.user.last_name
					user_email = request.user.email

					# Compose email message
					subject = 'Event Registration Confirmation'
					message = f'Thank you, {first_name} {last_name}, for registering for the event "{event_name}".\n'
					message += f'Event Date: {event_date}\n'
					message += f'Venue: {venue}\n'
					# Include other event details as needed

					# Send email
					send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email])

					# Add success message
					messages.success(request, 'Registration Successful! A mail has been sent to your email...')
					# Redirect to event list page
					return redirect('list-events')

		# Redirect or render a success message
		return render(request, 'events/event_form.html', {'form': form, 'event_closed': event_closed})
	else:
		return redirect('login')


def my_venues(request):
	venue_list = Venue.objects.all()

	#set up pagination
	p = Paginator(Venue.objects.all(), 10)
	page = request.GET.get('page')
	venues = p.get_page(page)
	nums = "a" * venues.paginator.num_pages

	return render(request, 'events/my_venues.html', 
		{'venue_list': venue_list, 'venues': venues, 'nums':nums})

def my_events(request):
	event_list = Event.objects.all().order_by('-event_date')

	#set up pagination
	p = Paginator(Event.objects.all(), 10)
	page = request.GET.get('page')
	events = p.get_page(page)
	nums = "a" * events.paginator.num_pages

	return render(request, 'events/my_events.html', 
		{'event_list': event_list, 'events': events, 'nums':nums}) 

#delete an venue
def delete_venue(request, venue_id):
	venue = Venue.objects.get(pk=venue_id)
	
	if request.user.is_superuser:
		venue.delete()
		return redirect('admin_approval')
	elif request.user.id == venue.owner:
		venue.delete()
		messages.success(request, ("Your venue has been deleted"))
		return redirect('my_venues')
	else:
		messages.success(request, ("You are not authorized to delete this venue"))
		return redirect('my_venues')

#delete an event
"""def delete_event(request, event_id):
	event = Event.objects.get(pk=event_id)
	if request.user == event.manager:
		event.delete()
		messages.success(request, ("Your event has been deleted"))
		return redirect('my_events')
	else:
		messages.success(request, ("You are not authorized to delete this event"))
		return redirect('my_events')"""

def delete_event(request, event_id):
	event = Event.objects.get(pk=event_id)

	if request.user.is_superuser:
		event.delete()
		return redirect('admin_approval')  # Redirect to admin_approval page for superuser
	elif request.user == event.manager:
		event.delete()
		messages.success(request, "Your event has been deleted")
		return redirect('my_events')
	else:
		messages.error(request, "You are not authorized to delete this event")
		return redirect('my_events')


def update_event(request, event_id):
	event = Event.objects.get(pk=event_id)
	if request.user.is_superuser:
		form = EventForm(request.POST or None, instance=event)
	else:
		form = EventForm(request.POST or None, instance=event)
	
	if form.is_valid():
		form.save()
		messages.success(request, ("Your event has been updated"))
		return redirect('my_events')

	return render(request, 'events/update_event.html', 
		{'event': event, 'form':form}) 

def add_event(request):
	submitted = False
	if request.method == "POST":
		if request.user.is_superuser:
			#form = EventFormAdmin(request.POST)
			form = EventForm(request.POST, request.FILES)
			if form.is_valid():
				#form.save()
				event = form.save(commit=False)
				event.manager = request.user    #logged in user
				event.save()
				return HttpResponseRedirect('/add_event?submitted=True')
		else:
			form = EventForm(request.POST, request.FILES)
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
	form = VenueForm(request.POST or None, request.FILES or None, instance=venue)
	if form.is_valid():
		form.save()
		messages.success(request, ("Your venue has been updated"))
		return redirect('my_venues')

	return render(request, 'events/update_venue.html', 
		{'venue': venue, 'form':form}) 

def search_venues(request):
	if request.method == "POST":
		searched = request.POST.get('searched', '')
		# Search in both name and address fields
		venues = Venue.objects.filter(Q(name__icontains=searched) | Q(address__icontains=searched))

		return render(request, 'events/search_venues.html', {'searched': searched, 'venues': venues}) 
	else:
		return render(request, 'events/search_venues.html', {})

def search_events(request):
	if request.method == "POST":
		searched = request.POST.get('searched', '')
		# Search in name, venue, and description fields
		events = Event.objects.filter(Q(name__icontains=searched) | Q(venue__name__icontains=searched) | Q(description__icontains=searched))

		return render(request, 'events/search_events.html', {'searched': searched, 'events': events}) 
	else:
		return render(request, 'events/search_events.html', {})

def show_venue(request, venue_id):
	venue = Venue.objects.get(pk=venue_id)
	venue_owner = User.objects.get(pk=venue.owner)
	return render(request, 'events/show_venue.html', 
		{'venue': venue,
		'venue_owner': venue_owner}) 

def genSha256(key, message):
	key = key.encode('utf-8')
	message = message.encode('utf-8')

	hmac_sha256 = hmac.new(key, message, hashlib.sha256)
	digest = hmac_sha256.digest()

	# Convert the digest to a Base64-encoded string
	signature = base64.b64encode(digest).decode('utf-8')

	return signature
"""
def show_event(request, event_id):
	event = get_object_or_404(Event, pk=event_id)

	# Generate UUID
	uuid_val = uuid.uuid4() 

	# Example usage:
	secret_key = "8gBm/:&EnhH.1/q"
	data_to_sign = f"total_amount={event.registration_fee},transaction_uuid={uuid_val},product_code=EPAYTEST"

	# Generate signature
	signature = genSha256(secret_key, data_to_sign)

	return render(request, 'events/show_event.html', {'event': event, 'signature': signature, 'transaction_uuid': uuid_val})

""" 
def show_event(request, event_id):
	event = get_object_or_404(Event, pk=event_id)
	return render(request, 'events/show_event.html', {'event': event})

@login_required
def register_for_event(request, event_id):
	event = get_object_or_404(Event, pk=event_id)

	# Generate UUID
	uuid_val = uuid.uuid4() 

	# Example usage:
	secret_key = "8gBm/:&EnhH.1/q"
	data_to_sign = f"total_amount={event.registration_fee},transaction_uuid={uuid_val},product_code=EPAYTEST"

	# Generate signature
	signature = genSha256(secret_key, data_to_sign)

	venue = event.venue

	# Check if the event date has passed
	if event.event_date < date.today():
		event_closed = True
		form = None
	else:
		event_closed = False
		form = EventRegistrationForm(event=event, user=request.user)
		if request.method == 'POST':
			form = EventRegistrationForm(request.POST, user=request.user, event=event)
			if form.is_valid():
				# Check if the venue capacity has been reached
				if MyClubUser.objects.filter(event=event).count() >= venue.capacity:
					messages.error(request, "Registration failed! Sorry, the venue is already full.")
					return redirect('list-events')
				else:
					MyClubUser.objects.create(user=request.user, event=event)
					messages.success(request, "You have successfully registered for the event.")
					return redirect('list-events')  # Redirect to a success page or event list

	return render(request, 'events/register_for_event.html', {'form': form, 'event': event, 'event_closed': event_closed, 'signature': signature, 'transaction_uuid': uuid_val})

@login_required
def joined_events_list(request):
	# Get the events joined by the current user
	joined_events = MyClubUser.objects.filter(user=request.user)

	# Set up pagination
	p = Paginator(joined_events, 6)
	page = request.GET.get('page')
	joined_events_paginated = p.get_page(page)

	# Create a dummy string for pagination display
	nums = "a" * joined_events_paginated.paginator.num_pages

	return render(request, 'events/joined_events_list.html', {'joined_events': joined_events_paginated, 'nums': nums})

@login_required
def generate_joined_event_pdf(request, event_id):
	# Get the joined event for the current user by event ID
	joined_event = get_object_or_404(MyClubUser, user=request.user, event_id=event_id)

	# Create PDF
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = f'attachment; filename="{joined_event.event.name}_details.pdf"'

	# Create canvas
	p = canvas.Canvas(response, pagesize=letter)
	width, height = letter

	# Define the box dimensions
	box_top = height - 100
	box_left = 80
	box_right = width - 80
	box_bottom = box_top - 180  # Increased height to accommodate title and intro text

	# Draw box for event details
	p.rect(box_left, box_bottom, box_right - box_left, box_top - box_bottom)

	# Add title inside the box
	p.setFont('Helvetica-Bold', 20)
	p.drawString(box_left + 10, box_top - 30, "Social Club Management")

	# Add introductory text inside the box
	p.setFont('Helvetica', 12)
	p.drawString(box_left + 10, box_top - 60, "You have registered for the event:")

	# Write event details inside the box
	y = box_top - 90  # Adjusted position to fit below the introductory text
	x = box_left + 10
	event = joined_event.event
	p.setFont('Helvetica', 12)
	p.drawString(x, y, f"Event Name: {event.name}")
	p.drawString(x, y - 20, f"Event Date: {event.event_date}")
	p.drawString(x, y - 40, f"Venue: {event.venue}")
	p.drawString(x, y - 60, f"Manager: {event.manager}")

	p.showPage()
	p.save()

	return response

def list_venues(request):
	venue_list = Venue.objects.all().order_by('name')

	#set up pagination
	p = Paginator(Venue.objects.all(), 6)
	page = request.GET.get('page')
	venues = p.get_page(page)
	nums = "a" * venues.paginator.num_pages

	return render(request, 'events/venue.html', 
		{'venue_list': venue_list, 'venues': venues, 'nums':nums}) 

def add_venue(request):
	submitted = False
	if request.method == "POST":
		form = VenueForm(request.POST, request.FILES)
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
	event_list = Event.objects.all().order_by('-event_date')

	#set up pagination
	p = Paginator(Event.objects.all(), 6)
	page = request.GET.get('page')
	events = p.get_page(page)
	nums = "a" * events.paginator.num_pages

	return render(request, 'events/event_list.html', 
		{'event_list': event_list, 'events': events, 'nums':nums}) 

def generate_calendar(year, month, event_dates):
	month_name = calendar.month_name[month]
	month_abbr = calendar.month_abbr[month]

	cal = format_html('<table class="calendar-table table table-bordered table-responsive-sm">')
	cal += format_html('<tr><th colspan="7">{0} {1}</th></tr>', month_name, year)
	cal += format_html('<tr><th class="day-header">{0}</th><th>{1}</th><th>{2}</th><th>{3}</th><th>{4}</th><th>{5}</th><th>{6}</th></tr>',
						*calendar.day_abbr)

	num_days = calendar.monthrange(year, month)[1]
	first_weekday = calendar.monthrange(year, month)[0]

	day_count = 1
	for i in range(6):
		cal += '<tr>'
		for j in range(7):
			if (i == 0 and j < first_weekday) or (day_count > num_days):
				cal += '<td></td>'
			else:
				if day_count in event_dates:
					cal += format_html(
					    '<td class="calendar-cell" style="cursor:pointer; background-color: #47bfff; '
					    'transition: background-color 0.3s;" '
					    'onclick="window.location=\'/events/{0}/{1}/{2}/\'" '
					    'onmouseover="this.style.backgroundColor=\'#70cdff\'" '
					    'onmouseout="this.style.backgroundColor=\'#47bfff\'">{2}</td>',
					    year, month, day_count
					)
				else:
					cal += '<td>{}</td>'.format(day_count)
				day_count += 1
		cal += '</tr>'
		if day_count > num_days:
			break  # Stop generating rows if all days have been processed
	cal += '</table>'

	return cal

def home(request, year=None, month=None):
	if request.user.is_superuser:
		return redirect('admin_approval')
	else:
		if year is None or month is None:
			now = datetime.now()
			year = now.year
			month = now.month
		else:
			year = int(year)
			month = int(month)

		prev_month = (datetime(year, month, 1) - timedelta(days=1)).strftime('%Y/%m')
		next_month = (datetime(year, month, calendar.monthrange(year, month)[1]) + timedelta(days=1)).strftime('%Y/%m')

		current_event_dates = set(Event.objects.filter(event_date__year=year, event_date__month=month).values_list('event_date__day', flat=True))
		prev_event_dates = set(Event.objects.filter(event_date__year=int(prev_month.split('/')[0]), event_date__month=int(prev_month.split('/')[1])).values_list('event_date__day', flat=True))
		next_event_dates = set(Event.objects.filter(event_date__year=int(next_month.split('/')[0]), event_date__month=int(next_month.split('/')[1])).values_list('event_date__day', flat=True))

		current_month_calendar = generate_calendar(year, month, current_event_dates)
		prev_month_calendar = generate_calendar(*map(int, prev_month.split('/')), prev_event_dates)
		next_month_calendar = generate_calendar(*map(int, next_month.split('/')), next_event_dates)

		event_list = Event.objects.filter(event_date__year=year, event_date__month=month)
		time = datetime.now().strftime('%I:%M %p')

		return render(request, 'events/home.html', {
					"year": year,
					"month": month,
					"current_month_calendar": current_month_calendar,
					"prev_month_calendar": prev_month_calendar,
					"next_month_calendar": next_month_calendar,
					"event_list": event_list,
					"time": time,
					"prev_month": prev_month,
					"next_month": next_month,
					})
    
def events_for_date(request, year, month, day):
	event_list = Event.objects.filter(
		event_date__year=year,
		event_date__month=month,
		event_date__day=day
	)
	return render(request, 'events/events_for_date.html', {
		'event_list': event_list,
		'year': year,
		'month': month,
		'day': day,
	})