
from django.views.generic import DetailView

from .models import Article


class ArticleDetailView(DetailView):
    model = Article
    template_name = "programming_tester/test_suit_detail.html"
