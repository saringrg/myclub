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
    path('events/<int:year>/<int:month>/<int:day>/', views.events_for_date, name='events_for_date'),
    path('admin_approval', views.admin_approval, name='admin_approval'),
    path('get_event_details/', views.get_event_details, name='get_event_details'),
    path('get_venue_details/', views.get_venue_details, name='get_venue_details'),
    path('delete_user/<user_id>', views.delete_user, name='delete_user'),
    path('event/register/<int:event_id>/', views.register_for_event, name='register_for_event'),
    path('events/esewa_payment_success/', views.esewa_payment_success, name='esewa_payment_success'),
    path('events/esewa_payment_failure/', views.esewa_payment_failure, name='esewa_payment_failure'),
    path('events/joined/', views.joined_events_list, name='joined_events_list'),
    path('generate-pdf/<int:event_id>/', views.generate_joined_event_pdf, name='generate_pdf'),
]
