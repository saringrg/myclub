# events/signals.py

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver, Signal
from django.core.mail import send_mail
from django.conf import settings
from .models import Event, MyClubUser

# Signal for notifying the event creator when a user joins an event
user_joined_event = Signal()

@receiver(pre_save, sender=Event)
def notify_users_on_event_update(sender, instance, **kwargs):
    if not instance.pk:
        # If the instance is new, there's no need to notify
        return

    # Fetch the old instance to compare changes
    try:
        old_instance = Event.objects.get(pk=instance.pk)
    except Event.DoesNotExist:
        return

    # Compare the old and new instances
    changed_fields = []
    if old_instance.name != instance.name:
        changed_fields.append('name')
    if old_instance.event_date != instance.event_date:
        changed_fields.append('event_date')
    if old_instance.venue != instance.venue:
        changed_fields.append('venue')
    if old_instance.description != instance.description:
        changed_fields.append('description')
    if old_instance.registration_fee != instance.registration_fee:
        changed_fields.append('registration_fee')

    if changed_fields:
        # Get users who joined this event
        joined_users = MyClubUser.objects.filter(event=instance)
        user_emails = [user.user.email for user in joined_users]

    if user_emails:
        send_mail(
            subject='Event Update Notification',
            message=f'The following fields of the event "{instance.name}" have been updated: {", ".join(changed_fields)}.\n\nKindly, check the app for more details\n\n\n\n\nThank you,\nThe myClub Team',
            from_email='your-email@example.com',
            recipient_list=user_emails,
        )

@receiver(user_joined_event)
def notify_event_creator(sender, **kwargs):
    event = kwargs.get('event')
    user = kwargs.get('user')

    if event and user:
        creator_email = event.manager.email
        subject = f"New Attendee for Your Event: {event.name}"
        message = f"{user.get_full_name()} has joined your event: {event.name}."
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [creator_email])

@receiver(post_save, sender=Event)
def notify_venue_owner(sender, instance, created, **kwargs):
    if created:
        venue = instance.venue
        venue_owner_email = venue.email_address  # Get venue owner's email

        subject = f"New Event Created at Your Venue: {instance.name}"
        message = f"A new event '{instance.name}' has been created at your venue '{venue.name}'.\n\nThank you,\nThe myClub Team"

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [venue_owner_email],
        )