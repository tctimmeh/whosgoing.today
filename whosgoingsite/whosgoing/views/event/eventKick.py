from dcbase.views.generic.popupFormView import PopupFormMixin

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.generic import UpdateView
from whosgoing.forms.kick import KickForm
from whosgoing.models import Event


class EventKickView(PopupFormMixin, UpdateView):
    model = Event
    pk_url_kwarg = 'eventId'
    form_class = KickForm
    template_name = 'whosgoing/fragments/kick_confirm_dialog.html'
    submit_style = 'danger'
    submit_text = 'Kick'

    def get_form(self, form_class):
        return form_class(**self.get_form_kwargs())

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not obj.is_member(self.request.user):
            raise PermissionDenied()
        return obj

    def form_valid(self, form):
        user = form.cleaned_data['kick_user']
        self.object.remove_member(user)
        messages.success(self.request, 'User "{}" kicked from event'.format(user.username))
        return self.popup_form_valid()


eventKickView = login_required(EventKickView.as_view())
