
from django.conf.urls import url

from .views import SolutionCategoryDetailView, SolutionDetailView, QuestionDetailView


app_name = 'app_solutions'

urlpatterns = [
    url(r'solution/(?P<slug>[-_\w]+)/$', SolutionDetailView.as_view(), {}, 'solution'),
    url(r'solution_category/(?P<slug>[-_\w]+)/$', SolutionCategoryDetailView.as_view(), {}, 'solution_category'),
    url(r'question/(?P<slug>[-_\w]+)/$', QuestionDetailView.as_view(), {}, 'question'),
]
