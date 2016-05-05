
from django.views.generic import DetailView

from .models import ForumTheme, ForumTopic


class TopicDetailView(DetailView):
    model = ForumTopic
    template_name = "app_programming_tester/test_suit_detail.html"


class ThemeDetailView(DetailView):
    model = ForumTheme
    template_name = "TEMPLATE_NAME"
