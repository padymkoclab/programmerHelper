
from .models import Visit


def count_visits(request):
    try:
        visits_this_url = Visit.objects.get(url=request.path_info)
    except Visit.DoesNotExist:
        count_visits_this_page = 0
    else:
        count_visits_this_page = visits_this_url.users.count()
    context = {'count_visits_this_page': count_visits_this_page}
    return context
