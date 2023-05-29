# Assignment

In this project, a Django web application's Google Calendar API integration is being done. In order to access their calendar events and show them on the web application, users must verify their Google accounts.

Three views—implemented as Django class-based views and appropriately styled with decorators from the Django and Django REST Framework libraries—make up the project:

This view, the GoogleCalendarInitView, starts the authentication procedure. Client secrets from the secret.json file are used to build a Flow object when a user reaches the corresponding URL (/v1/calendar/init/). It creates the permission URL and defines the redirect URI. The user is forwarded to the authorization URL while the state parameter is saved in the session for subsequent verification.

Google redirects the user back to this view (/v1/calendar/redirect/) after receiving authorization from the user for the application. For verification, the state parameter is contrasted with the one kept in the session. If they do, a new instance of the Flow object is generated and the token is converted into credentials. The user is routed to the /v1/calendar/events/ URL after the authenticated credentials are stored in the session for future usage.

GoogleCalendarEventsView: This view pulls the session's authorised credentials. The Calendar API service is created if the credentials are available. Using the service and a given time frame, the view obtains a list of calendar events from the user's main calendar. The response includes the incidents.

The urlpatterns list contains the URLs that map the views to their appropriate URLs.

In summary, this project offers users a method to log in using their Google accounts and retrieve their calendar events using the Google Calendar API inside of a Django web application.


![image](https://github.com/aryan-vigyat2001/Assignment/assets/88244719/4c8cb4c1-12b0-439e-8f22-4f347ead7e81)

