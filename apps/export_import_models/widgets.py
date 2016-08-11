
from django import forms


class BeautyFileInput(forms.FileInput):

    class Media:
        css = {
            'all': ('export_import_models/css/beauty_fileinput.css', ),
        }
        js = ('export_import_models/js/beauty_fileinput.js', )
