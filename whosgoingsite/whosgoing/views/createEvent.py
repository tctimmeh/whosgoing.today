import datetime
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.utils.translation import ugettext as _
from django.views.generic import CreateView
from whosgoing.forms.event import EventForm
from whosgoing.models import Event


class CreateEventView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'dcbase/form/popup-form.html'

    def get_initial(self):
        dt = datetime.datetime.now()
        dt = dt.replace(hour=12, minute=0, second=0)
        return {'time': dt}

    def form_valid(self, form):
        out = super().form_valid(form)
        self.object.add_member(self.request.user)
        return JsonResponse({'action': 'redirect', 'url': reverse('whosgoing:event:detail', kwargs={'eventId': self.object.id})})

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['form_url'] = reverse('whosgoing:createEvent')
        data['dialog_title'] = _('Create Event')
        data['submit_text'] = _('Create')
        return data


createEventView = login_required(CreateEventView.as_view())
