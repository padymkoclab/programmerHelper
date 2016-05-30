
from django.conf.urls import url

from .views import QuestionDetailView


app_name = 'questions'

urlpatterns = [
    url(r'question/(?P<slug>[-_\w]+)/$', QuestionDetailView.as_view(), {}, 'question'),
]
