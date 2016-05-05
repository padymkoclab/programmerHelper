
from django.conf.urls import url

from . import views

app_name = 'app_privacy_policy'

urlpatterns = [
    url(r'^$', views.ViewPrivacyPolicy.as_view(), {}, 'privacy_policy'),
]
