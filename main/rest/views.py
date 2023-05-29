from django.shortcuts import redirect
from django.views import View
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse

import google.oauth2.credentials
from google_auth_oauthlib.flow import Flow
import googleapiclient.discovery
import os
import requests

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
#define the Scope or the urls which we want to access

scopes=['https://www.googleapis.com/auth/calendar.events']

#Defining the class based views
class GoogleCalendarInitView(View):
    def get(self,request,*args,**kwargs):
        flow=Flow.from_client_secrets_file(
        'main/credentials/client_secret.json',
        scopes=scopes)
        flow.redirect_uri = 'http://localhost:8000/rest/v1/calendar/redirect'
        authorization_url, state = flow.authorization_url(
            # Enable offline access to refresh access tokens without user prompt
            access_type='offline',
            # Enable incremental authorization as a best practice
            include_granted_scopes='true'
        )
        # Store the state in the session or database for verification later
        request.session['isAuthenticated'] = state

        # Redirect the user to the authorization URL
        return redirect(authorization_url)

@api_view(['GET'])
def GoogleCalendarRedirectView(request):
    state = request.session.get('isAuthenticated', '')
    if state != request.GET.get('state', ''):
        return JsonResponse({'error': 'Invalid state parameter'})

    # Create a Flow object using the client secrets file and use the scopes defined above
    flow = Flow.from_client_secrets_file(
        'main/credentials/client_secret.json',
        scopes=scopes
    )
    flow.redirect_uri = 'http://localhost:8000/rest/v1/calendar/redirect'
    flow.fetch_token(authorization_response=request.build_absolute_uri())

    # Store the credentials in the session or database for later use
    credentials = flow.credentials
    request.session['authenticated_credentials'] = credentials.to_json()

    return redirect('http://localhost:8000/rest/v1/calendar/events')

@api_view(['GET'])
def GoogleCalendarEventsView(request):
    API="calendar"
    API_VERSION="v3"
    credentials_json = request.session.get('authenticated_credentials', '')
    if not credentials_json:
        return JsonResponse({'error': 'Credentials mismatch is seen.'})
    credentials = google.oauth2.credentials.Credentials.from_json(credentials_json)
     # Create the Calendar API service using the credentials
    service = googleapiclient.discovery.build(API,API_VERSION, credentials=credentials)
    timeMin = '2023-01-01T00:00:00-09:00'
    events_store = service.events().list(calendarId='primary',timeMin=timeMin,
                                              maxResults=10).execute()
    events = events_store.get('items', [])
    return JsonResponse({'status': 'success',
                         'response_code':200,
                             'message': 'These are the Events',
                             'data': events
                             })

