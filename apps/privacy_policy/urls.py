
from django.conf.urls import url

from . import views

name = 'privacy_policy'

urlpatterns = [
    url(r'^$', views.ViewPrivacyPolicy.as_view(), {}, 'privacy_policy'),
]
