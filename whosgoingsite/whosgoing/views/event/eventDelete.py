from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.utils.translation import ugettext as _
from django.views.generic import DeleteView
from whosgoing.models import Event


class EventDeleteView(DeleteView):
    model = Event
    template_name = "whosgoing/pages/delete_form.html"
    pk_url_kwarg = 'eventId'

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        return JsonResponse({'action': 'redirect', 'url': reverse('whosgoing:home')})

    def get_success_url(self):
        return ''

    def get_object(self, queryset=None):
        event = super().get_object(queryset)
        if not event.is_member(self.request.user):
            raise PermissionDenied()
        return event

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['submit_text'] = _("Delete")
        data['submit_style'] = 'danger'
        return data


eventDeleteView = login_required(EventDeleteView.as_view())
