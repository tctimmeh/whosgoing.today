from allauth.account.models import EmailAddress
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from whosgoing.models import Event


class ToggleNotifyAddressView(View):
    def post(self, request, eventId, **kwargs):
        event = get_object_or_404(Event, id=eventId)
        if not event.is_member(self.request.user):
            raise PermissionDenied()

        address = self.request.POST.get('address')
        if address is None:
            raise PermissionDenied()

        try:
            email = EmailAddress.objects.get(user=self.request.user, email__iexact=address)
        except EmailAddress.DoesNotExist:
            raise PermissionDenied()

        if event.notify_addresses.filter(id=email.id).exists():
            event.notify_addresses.remove(email)
        else:
            event.notify_addresses.add(email)

        context = {
            'notifyAddresses': event.get_notify_addresses_for_user(self.request.user)
        }

        return render(request, 'whosgoing/fragments/notify_address_widget.html', context)


toggleNotifyAddressView = ToggleNotifyAddressView.as_view()
