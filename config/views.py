
# import random

from django.contrib.auth import login, authenticate
# from django.http import HttpResponse
from django.views.generic import TemplateView

# from PIL import Image, ImageDraw


class IndexView(TemplateView):
    """
    View for present main page of website.
    """

    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        a = {'email': 'setivolkylany@gmail.com', 'password': 'lv210493'}
        account = authenticate(**a)
        if account:
            login(request, account)
        a = {'email': '2vlysenko@gmail.com', 'password': 'lv210493'}
        account = authenticate(**a)
        if account:
            login(request, account)
        # import ipdb; ipdb.set_trace()
        # request.session.set_test_cookie()
        # if request.session.test_cookie_worked():
        #     request.session.delete_test_cookie()
        #     return HttpResponse('Cookie worked')
        # else:
        #     return HttpResponse('Please enebled cookie')
        return super(IndexView, self).get(request, *args, **kwargs)

    # def post(self, request, *args, **kwargs):
    #     INK = ["red", "blue", "green", "yellow"]
    #     size = (100,50)             # size of the image to create
    #     im = Image.new('RGB', size) # create the image
    #     draw = ImageDraw.Draw(im)   # create a drawing object that is
    #                                 # used to draw on the new image
    #     red = (255,0,0)    # color of our text
    #     text_pos = (10,10) # top-left position of our text
    #     text = "Hello World!" # text to draw
    #     # Now, we'll do the drawing:
    #     draw.text(text_pos, text, fill=red)

    #     del draw # I'm done drawing so I don't need this anymore
    #     response = HttpResponse(content_type="image/png")
    #     im.save(response, "PNG")
    #     return HttpResponse(c, content_type="text/plain")
    #     return super(IndexView, self).post(request, *args, **kwargs)

