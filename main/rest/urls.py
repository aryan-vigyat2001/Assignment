from django.urls import path
from .views import GoogleCalendarInitView, GoogleCalendarRedirectView, GoogleCalendarEventsView


urlpatterns = [
    path('rest/v1/calendar/init/', GoogleCalendarInitView.as_view(), name='calendar_init'),
    path('rest/v1/calendar/redirect/', GoogleCalendarRedirectView, name='calendar_redirect'),
    path('rest/v1/calendar/events/', GoogleCalendarEventsView, name='calendar_events'),
]