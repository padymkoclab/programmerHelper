
import io

from PIL import Image, ImageDraw

from django import forms
from django.core.cache import cache


class PlaceholderForm(forms.Form):

    height = forms.IntegerField(min_value=1, max_value=500)
    width = forms.IntegerField(min_value=1, max_value=500)

    def generate(self, image_format='PNG'):

        height = self.cleaned_data['height']
        width = self.cleaned_data['width']

        key = '{0} {1} {2}'.format(width, height, image_format)
        content = cache.get(key)

        if content is None:
            image = Image.new('RGB', (width, height))
            draw = ImageDraw.Draw(image)

            text = '{0} X {1}'.format(width, height)
            textwidth, textheight = draw.textsize(text)
            if textwidth < width and textheight < height:
                texttoppadding = (height - textheight) // 2
                textleftpadding = (width - textwidth) // 2
                draw.text((textleftpadding, texttoppadding), text, fill=(255, 255, 255))

            filebuffer = io.BytesIO()

            image.save(filebuffer, format=image_format)

            filebuffer.seek(0)

        return content
