from django.conf.urls import patterns, url
from whosgoing.views.home import HomeView


urlpatterns = patterns('',
   url(r'^$', HomeView.as_view(), name='home'),
)
