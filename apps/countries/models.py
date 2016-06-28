
import uuid

from django.core.urlresolvers import reverse
from django.core.validators import MinLengthValidator
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings


# Simple ChoicesCountryFiled
# or RelatedModel
# using @property for reading population, name and other self-changing data
