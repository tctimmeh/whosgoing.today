from dcbase.views.generic.popupFormView import PopupFormMixin, PopupValidAction

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.forms.utils import to_current_timezone
from django.utils.translation import ugettext as _
from django.views.generic import UpdateView
from whosgoing.forms.event import EventForm
from whosgoing.models import Event


class EventUpdateView(PopupFormMixin, UpdateView):
    model = Event
    pk_url_kwarg = 'eventId'
    form_class = EventForm
    form_valid_action = PopupValidAction.reload
    submit_text = _('Update')

    def get_initial(self):
        return {'time': to_current_timezone(self.object.time).time()}

    def get_dialog_title(self):
        return _('%(eventName)s - Edit') % {'eventName': self.object.name}

    def get_object(self, queryset=None):
        event = super().get_object(queryset)
        if not event.is_member(self.request.user):
            raise PermissionDenied()
        return event


eventUpdateView = login_required(EventUpdateView.as_view())
