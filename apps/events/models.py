
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator, MaxValueValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

from utils.django.models import TimeFrameable


class Event(TimeFrameable):
    """
    app events PyCon EuroDjango DjangoUSA
        date - templatetag filter "timeuntil"
        location GeoDjango Leaflet
        use scrapy
    """

    pass
