from django.views.generic import TemplateView
from whosgoing.models import Invitation


class HomeView(TemplateView):
    template_name = 'whosgoing/pages/home.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if not self.request.user.is_anonymous():
            data['events'] = self.request.user.events.order_by('name')
        return data

homeView = HomeView.as_view()
