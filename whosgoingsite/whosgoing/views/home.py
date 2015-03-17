from django.views.generic import TemplateView
from whosgoing.models import Invitation
from zinnia.models import Entry, Category


class HomeView(TemplateView):
    template_name = 'whosgoing/pages/home.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if not self.request.user.is_anonymous():
            data['news'] = self._get_news()
            data['events'] = self.request.user.events.order_by('name')
        return data

    def _get_news(self):
        try:
            newsCategory = Category.objects.get(slug='news')
        except Category.DoesNotExist:
            return None

        news = newsCategory.entries_published().order_by('-creation_date')[:1]
        if news:
            return news[0]


homeView = HomeView.as_view()
