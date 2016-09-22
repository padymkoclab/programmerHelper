
import random

from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth import get_user_model

import factory

from .models import Diary


class DiaryFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Diary
