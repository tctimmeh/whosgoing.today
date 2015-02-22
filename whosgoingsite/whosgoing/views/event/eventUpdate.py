from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.forms.utils import to_current_timezone
from django.utils.translation import ugettext as _
from django.views.generic import UpdateView
from whosgoing.forms.event import EventForm
from whosgoing.models import Event


class EventUpdateView(UpdateView):
    model = Event
    pk_url_kwarg = 'eventId'
    template_name = 'whosgoing/event_update.html'
    form_class = EventForm

    def get_initial(self):
        return {'time': to_current_timezone(self.object.time).time()}

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = _('%(eventName)s - Edit') % {'eventName': self.object.name}
        data['submitText'] = _('Update')
        return data

    def get_object(self, queryset=None):
        event = super().get_object(queryset)
        if not event.is_member(self.request.user):
            raise PermissionDenied()
        return event


eventUpdateView = login_required(EventUpdateView.as_view())
