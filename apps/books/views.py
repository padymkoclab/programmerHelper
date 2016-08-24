
from django.views.generic import DetailView

from .models import Book, Writer


class BookDetailView(DetailView):
    model = Book
    template_name = "books/book_detail.html"


class WriterDetailView(DetailView):
    model = Writer
    template_name = "books/writer_detail.html"
