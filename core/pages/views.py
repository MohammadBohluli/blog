from typing import Any
from django.views.generic import TemplateView

class HomePageView(TemplateView):

    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'خانه'
        return context


class AboutPageView(TemplateView):

    template_name = 'pages/about.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'درباره ما'
        return context
