from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.forms.utils import to_current_timezone
from django.http import JsonResponse
from django.utils.translation import ugettext as _
from django.views.generic import UpdateView
from whosgoing.forms.event import EventForm
from whosgoing.models import Event


class EventUpdateView(UpdateView):
    model = Event
    pk_url_kwarg = 'eventId'
    template_name = 'dcbase/form/popup-form.html'
    form_class = EventForm

    def get_initial(self):
        return {'time': to_current_timezone(self.object.time).time()}

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['form_url'] = reverse('whosgoing:event:update', kwargs={'eventId': self.object.id})
        data['dialog_title'] = _('%(eventName)s - Edit') % {'eventName': self.object.name}
        data['submit_text'] = _('Update')
        return data

    def get_object(self, queryset=None):
        event = super().get_object(queryset)
        if not event.is_member(self.request.user):
            raise PermissionDenied()
        return event

    def form_valid(self, form):
        super().form_valid(form)
        return JsonResponse({'action': 'reload'})


eventUpdateView = login_required(EventUpdateView.as_view())
