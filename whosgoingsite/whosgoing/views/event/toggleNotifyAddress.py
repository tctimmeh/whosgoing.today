from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from whosgoing.models import Event


class ToggleNotifyAddressView(View):
    def post(self, request, eventId, **kwargs):
        event = get_object_or_404(Event, id=eventId)

        context = {
            'notifyAddresses': event.get_notify_addresses_for_user(self.request.user)
        }

        return render(request, 'whosgoing/fragments/notify_address_widget.html', context)


toggleNotifyAddressView = login_required(ToggleNotifyAddressView.as_view())
