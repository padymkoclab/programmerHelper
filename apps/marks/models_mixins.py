
from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.django.functions_db import Round


class MarksModelMixin:

    def get_count_marks(self):
        """ """

        if hasattr(self, 'count_marks'):
            return self.count_marks

        return self.marks.count()
    get_count_marks.admin_order_field = 'count_marks'
    get_count_marks.short_description = _('Count marks')

    def get_rating(self):
        """ """

        if hasattr(self, 'rating'):
            return self.rating

        return self.marks.aggregate(rating=Round(models.Avg('mark')))['rating']
    get_rating.admin_order_field = 'rating'
    get_rating.short_description = _('Rating')
