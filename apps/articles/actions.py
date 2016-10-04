
from django.utils.translation import ungettext_lazy
from django.utils.translation import ugettext_lazy

from .models import Article


def update_status_and_return_msg(model_admin, request, queryset, status):
    """ """

    queryset = queryset.model._default_manager.filter(pk__in=queryset)
    rows_updated = queryset.update(status=status)

    msg = ungettext_lazy(
        'Updated {} article',
        'Updated {} articles',
        rows_updated,
    ).format(rows_updated)

    model_admin.message_user(request, msg, extra_tags='updated')


def make_articles_as_draft(model_admin, request, queryset):
    """ """

    update_status_and_return_msg(model_admin, request, queryset, Article.DRAFT)
make_articles_as_draft.short_description = ugettext_lazy('Make articles as draft')


def make_articles_as_published(model_admin, request, queryset):
    """ """

    update_status_and_return_msg(model_admin, request, queryset, Article.PUBLISHED)
make_articles_as_published.short_description = ugettext_lazy('Make articles as published')
