
from django.views.generic import DetailView

from .models import Book


class BookDetailView(DetailView):
    model = Book
    template_name = "books/detail.html"
