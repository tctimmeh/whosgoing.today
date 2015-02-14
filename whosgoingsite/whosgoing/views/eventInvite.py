from django.http import HttpResponse
from django.views.generic import View


class EventInviteView(View):
    def post(self, request, eventId):
        return HttpResponse('whatever')

eventInviteView = EventInviteView.as_view()
