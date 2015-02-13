from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'', include('dcbase.urls')),
    url(r'', include('whosgoing.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
