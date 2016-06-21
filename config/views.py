
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.views.generic import TemplateView

from PIL import Image, ImageDraw

# from apps.accounts.models import Account


class IndexView(TemplateView):
    """
    View for present main page of website.
    """

    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        xdata = ["Apple", "Apricot", "Avocado", "Banana", "Boysenberries", "Blueberries", "Dates", "Grapefruit", "Kiwi", "Lemon"]
        ydata = [52, 48, 160, 94, 75, 70, 49, 82, 46, 17]
        data = {
            'charttype': "pieChart",
            'chartdata': {'x': xdata, 'y': ydata},
            'chartcontainer': 'piechart_container',
            'extra': {
            }
        }
        context.update(data)
        return context

    def get(self, request, *args, **kwargs):

        return super(IndexView, self).get(request, *args, **kwargs)

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
