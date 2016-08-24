
import datetime

from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.db import models


class BookManager(models.Manager):
    """
    Custom manager of model Book.
    """

    def made_all_books_as_wrote_on_english(self):
        """Mark all books as wrote on english."""

        self.update(language='en')


class WriterManager(models.Manager):
    """
    Custom manager of model Writer.
    """

    def mark_writer_dead_in_this_year(self, writer):
        """Mark writer as dead in this year if he don`t deed early."""

        if writer.years_life.upper is not None:
            raise ValidationError(_('This writer already dead.'))
        writer.years_life = (writer.years_life.lower, datetime.datetime.now().year)
        writer.full_clean()
        writer.save()
