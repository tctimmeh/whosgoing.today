from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'whosgoing/home.html'

homeView = HomeView.as_view()
