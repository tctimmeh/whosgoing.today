from django.views.generic import TemplateView
from whosgoing.models import UserReadTip
from zinnia.models import Category


class HomeView(TemplateView):
    template_name = 'whosgoing/pages/home.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if not self.request.user.is_anonymous():
            data['news'] = self._get_news()
            data['tip'] = self._get_tip()
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

    def _get_tip(self):
        try:
            tipsCategory = Category.objects.get(slug='tips')
        except Category.DoesNotExist:
            return None

        readTips = UserReadTip.objects.filter(user=self.request.user).values_list('entry__id', flat=True)
        tips = tipsCategory.entries_published().order_by('-creation_date').exclude(id__in=readTips)[:1]
        if tips:
            return tips[0]


homeView = HomeView.as_view()
