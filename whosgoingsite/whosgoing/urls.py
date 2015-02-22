from django.conf.urls import patterns, url
from whosgoing.views.createEvent import createEventView
from whosgoing.views.createOccurrence import createOccurrenceView
from whosgoing.views.eventDelete import eventDeleteView
from whosgoing.views.eventDetail import eventDetailView
from whosgoing.views.eventInvite import eventInviteView
from whosgoing.views.eventKick import eventKickView
from whosgoing.views.eventUpdate import eventUpdateView
from whosgoing.views.home import homeView
from whosgoing.views.invitiation import invitationView


urlpatterns = patterns('',
   url(r'^$', homeView, name='home'),
   url(r'^events/create/$', createEventView, name='createEvent'),
   url(r'^events/(?P<id>\d+)/$', eventDetailView, name='eventDetail'),
   url(r'^events/(?P<id>\d+)/edit/$', eventUpdateView, name='eventUpdate'),
   url(r'^events/(?P<id>\d+)/delete/$', eventDeleteView, name='eventDelete'),
   url(r'^events/(?P<eventId>\d+)/invite/$', eventInviteView, name='eventInvite'),
   url(r'^events/(?P<eventId>\d+)/kick/$', eventKickView, name='eventKick'),
   url(r'^events/(?P<eventId>\d+)/createOccurrence/$', createOccurrenceView, name='createOccurrence'),
   url(r'^invitations/(?P<inviteId>[\w-]{36})/', invitationView, name='invitation'),
)
