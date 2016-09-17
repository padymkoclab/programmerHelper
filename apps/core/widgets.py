
import json
import uuid

from django.utils.safestring import mark_safe

from suit_ckeditor.widgets import CKEditorWidget


# Problem CREditor and field 'content' and 'header'
# see https://github.com/darklow/django-suit/issues/182
class CKEditorAdminWidget(CKEditorWidget):

    def render(self, name, value, attrs=None):
        output = super().render(name, value, attrs)

        field_id = self.attrs.get('id', None)

        if field_id in ['content', 'header'] or field_id is None:
            field_id = uuid.uuid4()

        output += mark_safe(
            '<script type="text/javascript">CKEDITOR.replace("%s", %s);</script>' %
            (field_id, json.dumps(self.editor_options))
        )
        return output
