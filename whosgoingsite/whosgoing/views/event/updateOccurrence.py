from dcbase.views.generic.popupFormView import PopupFormMixin, PopupValidAction
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _
from django.views.generic import UpdateView
from whosgoing.forms.occurrence import OccurrenceForm
from whosgoing.models import EventOccurrence


class UpdateOccurrenceView(PopupFormMixin, UpdateView):
    model = EventOccurrence
    pk_url_kwarg = 'occurrenceId'
    form_valid_action = PopupValidAction.reload
    submit_text = _('Update')
    dialog_title = _('Change Occurrence Time')
    form_class = OccurrenceForm
    template_name = 'whosgoing/fragments/occurrence_update.html'
    success_url = 'nuthin'

    def get_object(self, queryset=None):
        occurrence = super().get_object(queryset)
        if not occurrence.event.is_member(self.request.user):
            raise PermissionDenied()
        return occurrence


updateOccurrenceView = login_required(UpdateOccurrenceView.as_view())
