from django.conf.urls import patterns, url
from whosgoing.views import home

urlpatterns = patterns('',
   url(r'^$', home),
)
