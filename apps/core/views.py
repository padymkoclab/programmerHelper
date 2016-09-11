
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.views.generic import TemplateView, View

from PIL import Image, ImageDraw

from .forms import PlaceholderForm


class IndexView(TemplateView):
    """
    View for present main page of website.
    """

    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):

        return super(IndexView, self).get(request, *args, **kwargs)

        from django_gravatar.helpers import get_gravatar_url, has_gravatar, get_gravatar_profile_url, calculate_gravatar_hash

        url = get_gravatar_url('alice@example.com', size=150)
        gravatar_exists = has_gravatar('bob@example.com')
        profile_url = get_gravatar_profile_url('alice@example.com')
        email_hash = calculate_gravatar_hash('alice@example.com')

        a = {'email': 'дроздоваплатон@yahoo.com', 'password': 'lv210493'}
        a = {'email': 'pситников@дьячков-дьячкова.com', 'password': 'lv210493'}
        a = {'email': 'setivolkylany@gmail.com', 'password': 'lv210493'}
        account = authenticate(**a)
        if account:
            login(request, account)
            logout(request)
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
