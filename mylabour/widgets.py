
from django.utils.html import mark_safe
from django.contrib.admin.widgets import AdminFileWidget


class AdminImageThumbnail(AdminFileWidget):

    def render(self, name, value, attrs=None):

        # get a HTML output
        html = super().render(name, value, attrs)

        # if an object has image
        if value:
            img_styles = 'float: left; margin-right: 15px; width: 100px; height: 100px;'
            html = mark_safe(
                '<image src="{0}" style="{1}"></image>{2}'.format(value.url, img_styles, html)
            )
        return html
