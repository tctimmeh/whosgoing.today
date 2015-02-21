from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.views.generic import DeleteView
from whosgoing.models import Event


class EventDeleteView(DeleteView):
    model = Event
    template_name = "whosgoing/delete_form.html"
    pk_url_kwarg = 'id'

    def get_success_url(self):
        messages.success(self.request, _("Successfully deleted Event %(eventName)s") % {'eventName': self.object.name})
        return reverse('home')


eventDeleteView = EventDeleteView.as_view()
