
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _


class UserCommentModelMixin(object):
    """

    """

    def get_count_comments_on_articles_other_users(self):

        from apps.articles.models import Article

        if hasattr(self, 'count_comments_on_articles_other_users'):
            return self.count_comments_on_articles_other_users

        return self.comments.filter(content_type=ContentType.objects.get_for_model(Article)).count()
    get_count_comments_on_articles_other_users.short_description = _('Count comments on articles')
    get_count_comments_on_articles_other_users.admin_order_field = 'count_comments_on_articles_other_users'

    def get_count_comments_on_solutions_other_users(self):

        from apps.solutions.models import Solution

        if hasattr(self, 'count_comments_on_solutions_other_users'):
            return self.count_comments_on_solutions_other_users

        return self.comments.filter(content_type=ContentType.objects.get_for_model(Solution)).count()
    get_count_comments_on_solutions_other_users.short_description = _('Count comments on solutions')
    get_count_comments_on_solutions_other_users.admin_order_field = 'count_comments_on_solutions_other_users'

    def get_count_comments_on_snippets_other_users(self):

        from apps.snippets.models import Snippet

        if hasattr(self, 'count_comments_on_snippets_other_users'):
            return self.count_comments_on_snippets_other_users

        return self.comments.filter(content_type=ContentType.objects.get_for_model(Snippet)).count()
    get_count_comments_on_snippets_other_users.short_description = _('Count comments on snippets')
    get_count_comments_on_snippets_other_users.admin_order_field = 'count_comments_on_snippets_other_users'

    def get_count_comments_on_answers_other_users(self):

        from apps.questions.models import Answer

        if hasattr(self, 'count_comments_on_answers_other_users'):
            return self.count_comments_on_answers_other_users

        return self.comments.filter(content_type=ContentType.objects.get_for_model(Answer)).count()
    get_count_comments_on_answers_other_users.short_description = _('Count comments on answers')
    get_count_comments_on_answers_other_users.admin_order_field = 'count_comments_on_answers_other_users'

    def get_count_comments_on_utilities(self):

        from apps.utilities.models import Utility

        if hasattr(self, 'count_comments_on_utilities'):
            return self.count_comments_on_utilities

        return self.comments.filter(content_type=ContentType.objects.get_for_model(Utility)).count()
    get_count_comments_on_utilities.short_description = _('Count comments on utilities')
    get_count_comments_on_utilities.admin_order_field = 'count_comments_on_utilities'

    def get_total_count_comments(self):
        """ """

        if hasattr(self, 'total_count_comments'):
            return self.total_count_comments

        return self.comments.count()
    get_total_count_comments.short_description = _('Total count comments')
    get_total_count_comments.admin_order_field = 'total_count_comments'

    def get_date_latest_comment(self):
        """ """

        if hasattr(self, 'date_latest_comment'):
            return self.date_latest_comment

        return self.comments.aggregate(
            date_latest_comment=models.Max('created')
        )['date_latest_comment'], self.date_latest_comment
    get_date_latest_comment.short_description = _('Latest comment')
    get_date_latest_comment.admin_order_field = 'date_latest_comment'


class CommentModelMixin(object):
    """

    """

    pass
