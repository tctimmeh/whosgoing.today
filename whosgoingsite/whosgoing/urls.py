from django.conf.urls import patterns, url, include
from whosgoing.views.createEvent import createEventView
from whosgoing.views.deleteInvitation import deleteInvitationView
from whosgoing.views.event.createOccurrence import createOccurrenceView
from whosgoing.views.event.eventDelete import eventDeleteView
from whosgoing.views.event.eventDetail import eventDetailView
from whosgoing.views.event.eventInvite import eventInviteView
from whosgoing.views.event.eventKick import eventKickView
from whosgoing.views.event.eventUpdate import eventUpdateView
from whosgoing.views.event.toggleNotifyAddress import toggleNotifyAddressView
from whosgoing.views.home import homeView
from whosgoing.views.invitiation import invitationView
from whosgoing.views.setAttendance import setAttendanceView


eventUrls = patterns('',
    url(r'^$', eventDetailView, name='detail'),
    url(r'^edit/$', eventUpdateView, name='update'),
    url(r'^delete/$', eventDeleteView, name='delete'),
    url(r'^invite/$', eventInviteView, name='invite'),
    url(r'^kick/$', eventKickView, name='kick'),
    url(r'^createOccurrence/$', createOccurrenceView, name='createOccurrence'),
    url(r'^toggleNotifyAddress/$', toggleNotifyAddressView, name='toggleNotifyAddress'),
)

urlpatterns = patterns('',
    url(r'^$', homeView, name='home'),
    url(r'^events/create/$', createEventView, name='createEvent'),
    url(r'^events/(?P<eventId>\d+)/', include(eventUrls, namespace='event')),
    url(r'^invitations/(?P<inviteId>[\w-]{36})/$', invitationView, name='invitation'),
    url(r'^invitations/(?P<inviteId>[\w-]+)/cancel/$', deleteInvitationView, name='deleteInvitation'),
    url(r'^occurrences/(?P<occurrenceId>\d+)/setAttendance/$', setAttendanceView, name='setAttendance'),
)
