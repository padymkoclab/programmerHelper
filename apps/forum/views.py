
from django.views.generic import DetailView

from .models import ForumSection, ForumTopic


class TopicDetailView(DetailView):
    model = ForumTopic
    template_name = "programming_tester/test_suit_detail.html"


class SectionDetailView(DetailView):
    model = ForumSection
    template_name = "TEMPLATE_NAME"
