from django.conf.urls import patterns, url
from whosgoing.views.createEvent import createEventView
from whosgoing.views.eventDetail import eventDetailView
from whosgoing.views.home import homeView


urlpatterns = patterns('',
   url(r'^$', homeView, name='home'),
   url(r'^events/create/$', createEventView, name='createEvent'),
   url(r'^events/(?P<id>\d+)/$', eventDetailView, name='eventDetail'),
)
