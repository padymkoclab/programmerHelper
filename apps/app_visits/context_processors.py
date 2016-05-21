
from .models import Visit


def count_visits(request):
    count_visits_this_page = Visit.objects.get_count_visits_by_url(url=request.path_info)
    context = {'count_visits_this_page': count_visits_this_page}
    return context
