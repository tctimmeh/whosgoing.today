from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'', include('dcbase.urls')),
    url(r'', include('whosgoing.urls', namespace='whosgoing')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('zinnia.urls', namespace='zinnia')),
    url(r'^blog/comments/', include('django_comments.urls')),
)
