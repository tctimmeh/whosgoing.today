from django.views.generic import TemplateView
from whosgoing.models import Invitation


class HomeView(TemplateView):
    template_name = 'whosgoing/home.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if not self.request.user.is_anonymous():
            data['events'] = self.request.user.events.order_by('name')
            data['invitations'] = Invitation.objects.for_user(self.request.user).order_by('event__name')
        return data

homeView = HomeView.as_view()
