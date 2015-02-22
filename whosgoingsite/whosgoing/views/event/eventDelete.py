from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.views.generic import DeleteView
from whosgoing.models import Event


class EventDeleteView(DeleteView):
    model = Event
    template_name = "whosgoing/delete_form.html"
    pk_url_kwarg = 'eventId'

    def get_success_url(self):
        messages.success(self.request, _("Successfully deleted Event %(eventName)s") % {'eventName': self.object.name})
        return reverse('whosgoing:home')

    def get_object(self, queryset=None):
        event = super().get_object(queryset)
        if not event.is_member(self.request.user):
            raise PermissionDenied()
        return event

eventDeleteView = login_required(EventDeleteView.as_view())
