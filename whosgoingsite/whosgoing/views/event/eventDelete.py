from dcbase.views.generic.popupFormView import PopupFormMixin, PopupValidAction

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.views.generic import DeleteView
from whosgoing.models import Event


class EventDeleteView(PopupFormMixin, DeleteView):
    model = Event
    template_name = "whosgoing/fragments/delete_event.html"
    pk_url_kwarg = 'eventId'
    form_valid_action = PopupValidAction.redirect
    submit_text = _('Delete')
    submit_style = 'danger'

    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        messages.success(request, 'Successfully deleted event "{}"'.format(self.object.name))
        return self.popup_form_valid()

    def get_success_url(self):
        return reverse('whosgoing:home')

    def get_object(self, queryset=None):
        event = super().get_object(queryset)
        if not event.is_member(self.request.user):
            raise PermissionDenied()
        return event


eventDeleteView = login_required(EventDeleteView.as_view())
