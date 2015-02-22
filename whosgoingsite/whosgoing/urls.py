from django.conf.urls import patterns, url, include
from whosgoing.views.createEvent import createEventView
from whosgoing.views.createOccurrence import createOccurrenceView
from whosgoing.views.eventDelete import eventDeleteView
from whosgoing.views.eventDetail import eventDetailView
from whosgoing.views.eventInvite import eventInviteView
from whosgoing.views.eventKick import eventKickView
from whosgoing.views.eventUpdate import eventUpdateView
from whosgoing.views.home import homeView
from whosgoing.views.invitiation import invitationView

eventUrls = patterns('',
    url(r'^$', eventDetailView, name='detail'),
    url(r'^edit/$', eventUpdateView, name='update'),
    url(r'^delete/$', eventDeleteView, name='delete'),
    url(r'^invite/$', eventInviteView, name='invite'),
    url(r'^kick/$', eventKickView, name='kick'),
    url(r'^createOccurrence/$', createOccurrenceView, name='createOccurrence'),
)

urlpatterns = patterns('',
    url(r'^$', homeView, name='home'),
    url(r'^events/create/$', createEventView, name='createEvent'),
    url(r'^events/(?P<eventId>\d+)/', include(eventUrls, namespace='event')),
    url(r'^invitations/(?P<inviteId>[\w-]{36})/', invitationView, name='invitation'),
)
