
from django.views.generic import DetailView

from .models import Poll


class PollDetailView(DetailView):
    """
    View for detail page of poll.
    """

    model = Poll
    pk_url_kwarg = 'pk'
    template_name = 'polls/poll_detail.html'
