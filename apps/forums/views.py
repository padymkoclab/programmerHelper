
from django.views.generic import DetailView

from .models import Forum, Topic


class ForumDetailView(DetailView):

    model = Forum
    template_name = "forums/forum_detail.html"


class TopicDetailView(DetailView):

    model = Topic
    template_name = "forums/topic_detail.html"
