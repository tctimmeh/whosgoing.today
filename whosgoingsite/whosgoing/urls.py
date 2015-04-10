from django.conf.urls import patterns, url, include
from django.views.generic import RedirectView
from rest_framework.routers import DefaultRouter
from whosgoing.views.api import UserViewSet, EventViewSet
from whosgoing.views.createEvent import createEventView
from whosgoing.views.deleteInvitation import deleteInvitationView
from whosgoing.views.event.createOccurrence import createOccurrenceView
from whosgoing.views.event.eventDelete import eventDeleteView
from whosgoing.views.event.eventDetail import eventDetailView
from whosgoing.views.event.eventInvite import eventInviteView
from whosgoing.views.event.eventKick import eventKickView
from whosgoing.views.event.eventUpdate import eventUpdateView
from whosgoing.views.event.toggleNotifyAddress import toggleNotifyAddressView
from whosgoing.views.event.updateOccurrence import updateOccurrenceView
from whosgoing.views.home import homeView
from whosgoing.views.invitiation import invitationView
from whosgoing.views.setAttendance import setAttendanceView
from whosgoing.views.userReadTip import userReadTipView


api_router = DefaultRouter()
api_router.register('users', UserViewSet)
api_router.register('events', EventViewSet)

occurrenceUrls = patterns('',
    url(r'^edit/$', updateOccurrenceView, name='update'),
    url(r'^setAttendance/$', setAttendanceView, name='setAttendance'),
)

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
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/img/favicon.ico')),
    url(r'^$', homeView, name='home'),
    url(r'^readTip/', userReadTipView, name='userReadTip'),
    url(r'^events/create/$', createEventView, name='createEvent'),
    url(r'^events/(?P<eventId>\d+)/', include(eventUrls, namespace='event')),
    url(r'^invitations/(?P<inviteId>[\w-]{36})/$', invitationView, name='invitation'),
    url(r'^invitations/(?P<inviteId>[\w-]+)/cancel/$', deleteInvitationView, name='deleteInvitation'),
    url(r'^occurrences/(?P<occurrenceId>\d+)/', include(occurrenceUrls, namespace='occurrence')),
    url(r'^api/', include(api_router.urls, namespace='api')),
)
