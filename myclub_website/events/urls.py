from django.urls import path
from . import views
from .views import home, events_for_date  # Import the events_for_date view function

urlpatterns = [
    path('', views.home, name="home"),
    path('<int:year>/<str:month>/', views.home, name="home"),
    path('events', views.all_events, name="list-events"),
    path('add_venue', views.add_venue, name='add-venue'),
    path('list_venues', views.list_venues, name='list-venues'),
    path('show_event/<int:event_id>', views.show_event, name='show-event'),    
    path('show_venue/<venue_id>', views.show_venue, name='show-venue'),
    path('search_venues', views.search_venues, name='search-venues'),
    path('update_venue/<venue_id>', views.update_venue, name='update-venue'),
    path('add_event', views.add_event, name='add-event'),
    path('update_event/<event_id>', views.update_event, name='update-event'),
    path('delete_event/<event_id>', views.delete_event, name='delete-event'),
    path('delete_venue/<venue_id>', views.delete_venue, name='delete-venue'),
    path('my_events', views.my_events, name='my_events'),
    path('my_venues', views.my_venues, name='my_venues'),
    path('search_events', views.search_events, name='search_events'),
    path('event-form/<int:event_id>/', views.event_form_view, name='event-form'),
    path('events/<int:year>/<int:month>/<int:day>/', events_for_date, name='events_for_date'),
    #path('alert_date/<int:year>/<int:month>/<int:day>/', views.alert_date, name='alert-date'),
    #path('events/day/<int:year>/<int:month>/<int:day>/', views.events_for_day, name='events-for-day'),
]
