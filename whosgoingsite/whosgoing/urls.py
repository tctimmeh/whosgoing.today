from django.conf.urls import patterns, url
from whosgoing.views.createEvent import CreateEventView
from whosgoing.views.eventDetail import EventDetailView
from whosgoing.views.home import HomeView


urlpatterns = patterns('',
   url(r'^$', HomeView.as_view(), name='home'),
   url(r'^events/create/$', CreateEventView.as_view(), name='createEvent'),
   url(r'^events/(?P<id>\d+)/$', EventDetailView.as_view(), name='eventDetail'),
)
