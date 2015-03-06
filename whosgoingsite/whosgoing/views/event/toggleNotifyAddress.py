from allauth.account.models import EmailAddress
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import View
from whosgoing.models import Event


class ToggleNotifyAddressView(View):
    def post(self, request, eventId, **kwargs):
        event = get_object_or_404(Event, id=eventId)
        if not event.is_member(request.user):
            raise PermissionDenied()

        address = request.POST.get('address')
        if address is None:
            raise PermissionDenied()

        try:
            email = EmailAddress.objects.get(user=request.user, email__iexact=address)
        except EmailAddress.DoesNotExist:
            raise PermissionDenied()

        if event.notify_addresses.filter(id=email.id).exists():
            event.notify_addresses.remove(email)
            selected = False
        else:
            event.notify_addresses.add(email)
            selected = True

        return render(request, "whosgoing/fragments/notify_address_indicator.html", {'address': email.email, 'selected': selected})


toggleNotifyAddressView = ToggleNotifyAddressView.as_view()
