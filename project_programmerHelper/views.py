
import random

from django.http import HttpResponse
from django.views.generic import TemplateView

from PIL import Image, ImageDraw

# class IndexView(TemplateView):
#     template_name = "TEMPLATE_NAME"

INK = ["red", "blue", "green", "yellow"]
def IndexView(request):
    # size = (100,50)             # size of the image to create
    # im = Image.new('RGB', size) # create the image
    # draw = ImageDraw.Draw(im)   # create a drawing object that is
    #                             # used to draw on the new image
    # red = (255,0,0)    # color of our text
    # text_pos = (10,10) # top-left position of our text
    # text = "Hello World!" # text to draw
    # # Now, we'll do the drawing:
    # draw.text(text_pos, text, fill=red)

    # del draw # I'm done drawing so I don't need this anymore
    # response = HttpResponse(content_type="image/png")
    # im.save(response, "PNG")
    # return response
    a = 1
    b = 0
    import pdb; pdb.set_trace()
    c = a / b
    return HttpResponse(c, content_type="text/plain")
