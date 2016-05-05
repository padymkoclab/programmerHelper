
from django.conf.urls import url

from .views import NewsletterDetailView, NewslettersListView


app_name = 'app_newsletters'

urlpatterns = [
    url(r'newsletters/$', NewslettersListView.as_view(), {}, 'newsletters'),
    url(r'newsletter/(?P<slug>[_\w]+)/$', NewsletterDetailView.as_view(), {}, 'newsletter'),
]
