
from django.views.generic import DetailView

from .models import Book, Writter


class BookDetailView(DetailView):
    model = Book
    template_name = "books/book_detail.html"


class WritterDetailView(DetailView):
    model = Writter
    template_name = "books/writter_detail.html"
