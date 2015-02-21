from django.utils.translation import ugettext as _
from django.views.generic import UpdateView
from whosgoing.models import Event


class EventUpdateView(UpdateView):
    model = Event
    pk_url_kwarg = 'id'
    template_name = 'whosgoing/event_form.html'
    fields = ['name', 'description']

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = _('%(eventName)s - Edit') % {'eventName': self.object.name}
        data['submitText'] = _('Update')
        return data


eventUpdateView = EventUpdateView.as_view()
