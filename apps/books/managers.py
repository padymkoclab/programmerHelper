
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


class WritterManager(models.Manager):
    """
    Custom manager of model Writter.
    """

    def mark_writter_dead_in_this_year(self, writter):
        """Mark writter as dead in this year if he don`t deed early."""

        if writter.deathyear is not None:
            raise ValidationError(_('This writter already dead.'))
        writter.deathyear = datetime.datetime.now().year
        writter.full_clean()
        writter.save()
