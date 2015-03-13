import datetime

from dcbase.views.generic.popupFormView import PopupFormMixin, PopupValidAction

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.views.generic import CreateView
from whosgoing.forms.event import EventForm
from whosgoing.models import Event


class CreateEventView(PopupFormMixin, CreateView):
    model = Event
    form_class = EventForm
    form_valid_action = PopupValidAction.redirect
    dialog_title = _('Create Event')
    submit_text = _('Create')

    def get_initial(self):
        dt = datetime.datetime.now()
        dt = dt.replace(hour=12, minute=0, second=0)
        return {'time': dt}

    def get_success_url(self):
        return reverse('whosgoing:event:detail', kwargs={'eventId': self.object.id})

    def form_valid(self, form):
        out = super().form_valid(form)
        self.object.add_member(self.request.user)
        return out


createEventView = login_required(CreateEventView.as_view())
