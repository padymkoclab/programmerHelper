
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from django.utils.translation import ugettext_lazy as _

from PIL import Image, ImageDraw

from .forms import PlaceholderForm


class IndexView(TemplateView):
    """
    View for present main page of website.
    """

    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        context['title'] = _('Index')

        return context

    def get(self, request, *args, **kwargs):

        return super(IndexView, self).get(request, *args, **kwargs)

        request.session.set_test_cookie()
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
            return HttpResponse('Cookie worked')
        else:
            return HttpResponse('Please enebled cookie')

    def post(self, request, *args, **kwargs):
        INK = ["red", "blue", "green", "yellow"]
        size = (100, 50)             # size of the image to create
        im = Image.new('RGB', size)  # create the image
        draw = ImageDraw.Draw(im)  # create a drawing object that is used to draw on the new image
        red = (255, 0, 0)  # color of our text
        text_pos = (10, 10)  # top-left position of our text
        text = "Hello World!"  # text to draw
        # Now, we'll do the drawing:
        draw.text(text_pos, text, fill=red)

        del draw  # I'm done drawing so I don't need this anymore
        response = HttpResponse(content_type="image/png")
        im.save(response, "PNG")
        return HttpResponse(c, content_type="text/plain")
        return super(IndexView, self).post(request, *args, **kwargs)


# Today newly objects


class PlaceholderView(View):

    def get(self, request, *args, **kwargs):

        form = PlaceholderForm(kwargs)
        if form.is_valid():
            image = form.generate()
            return HttpResponse(image, content_type='image/png')
        return HttpResponse('Not OK')
