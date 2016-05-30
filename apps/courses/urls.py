
from django.conf.urls import url

from .views import *

app_name = 'courses'

urlpatterns = [
    url(r'course/detail/(?P<slug>[-_\w]+)/$', CourseDetailView.as_view(), {}, 'course_detail'),
    url(r'lesson/detail/(?P<slug>[-_\w]+)/(?P<number>\d+)/$', LessonDetailView.as_view(), {}, 'lesson_detail'),
]
