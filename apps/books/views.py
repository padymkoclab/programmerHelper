
from django.views.generic import DetailView

from .models import Book, Writer, Publisher


class BookDetailView(DetailView):
    model = Book
    template_name = "books/book_detail.html"


class WriterDetailView(DetailView):
    model = Writer
    template_name = "books/writer_detail.html"


class PublisherDetailView(DetailView):
    model = Publisher
    template_name = "books/publisher_detail.html"
