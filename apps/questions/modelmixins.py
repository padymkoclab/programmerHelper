
from django.db import models
from django.utils.translation import ugettext_lazy as _

from utils.django.functions_db import Round

from apps.tags.utils import get_favorite_tags


class QuestionModelMixin(object):
    """
    """

    def get_count_questions(self):
        """ """

        if hasattr(self, 'count_questions'):
            return self.count_questions

        return self.questions.count()
    get_count_questions.admin_order_field = 'count_questions'
    get_count_questions.short_description = _('Count questions')

    def get_total_count_answers_on_questions(self):

        if hasattr(self, 'count_answers_on_questions'):
            return self.count_answers_on_questions

        return self.questions.aggregate(
            count_answers_on_questions=models.Count('answers', distinct=True)
        )['count_answers_on_questions']
    get_total_count_answers_on_questions.short_description = _('Count answers on questions')
    get_total_count_answers_on_questions.admin_order_field = 'count_answers_on_questions'

    def get_favorite_tags_on_questions(self):
        """ """

        qs_tags_pks = self.questions.values_list('tags__pk', flat=True)
        favorite_tags = get_favorite_tags(qs_tags_pks)

        return favorite_tags
    get_favorite_tags_on_questions.short_description = _('Favorite tag')

    def get_date_latest_question(self):
        """ """

        if hasattr(self, 'date_latest_question'):
            return self.date_latest_question

        return self.questions.aggregate(
            date_latest_question=models.Max('created')
        )['date_latest_question']
    get_date_latest_question.admin_order_field = 'date_latest_question'
    get_date_latest_question.short_description = _('Latest question')

    def get_total_rating_on_questions(self):
        """ """

        if hasattr(self, 'total_rating_questions'):
            return self.total_rating_questions

        questions = self.questions.annotate(rating=models.Sum(models.Case(
            models.When(opinions__is_useful=True, then=1),
            models.When(opinions__is_useful=False, then=-1),
            output_field=models.IntegerField()
        )))

        return questions.aggregate(total_rating=Round(models.Avg('rating')))['total_rating']
    get_total_rating_on_questions.short_description = _('Total rating')
    get_total_rating_on_questions.admin_order_field = 'total_rating_questions'

    def get_count_opinions_on_questions(self):

        if hasattr(self, 'count_opinions_on_questions'):
            return self.count_opinions_on_questions

        return self.questions.aggregate(count_opinions=models.Count('opinions'))['count_opinions']
    get_count_opinions_on_questions.short_description = _('Count opinions')
    get_count_opinions_on_questions.admin_order_field = 'count_opinions_on_questions'

    def get_count_good_opinions_on_questions(self):

        if hasattr(self, 'count_good_opinions_on_questions'):
            return self.count_good_opinions_on_questions

        return self.questions.filter(opinions__is_useful=True).count()
    get_count_good_opinions_on_questions.short_description = _('Count good opinions')
    get_count_good_opinions_on_questions.admin_order_field = 'count_good_opinions_on_questions'

    def get_count_bad_opinions_on_questions(self):

        if hasattr(self, 'count_bad_opinions_on_questions'):
            return self.count_bad_opinions_on_questions

        return self.questions.filter(opinions__is_useful=False).count()
    get_count_bad_opinions_on_questions.short_description = _('Count bad opinions')
    get_count_bad_opinions_on_questions.admin_order_field = 'count_bad_opinions_on_questions'


class AnswerModelMixin(object):
    """
    """

    def get_count_answers(self):
        """ """

        if hasattr(self, 'count_answers'):
            return self.count_answers

        return self.answers.count()
    get_count_answers.admin_order_field = 'count_answers'
    get_count_answers.short_description = _('Count answers')

    def get_favorite_tags_on_answers(self):
        """ """

        qs_tags_pks = self.answers.values_list('question__tags', flat=True)
        favorite_tags = get_favorite_tags(qs_tags_pks)

        return favorite_tags
    get_favorite_tags_on_answers.short_description = _('Favorite tag')

    def get_date_latest_answer(self):
        """ """

        if hasattr(self, 'date_latest_answer'):
            return self.date_latest_answer

        return self.answers.aggregate(
            date_latest_answer=models.Max('created')
        )['date_latest_answer']
    get_date_latest_answer.admin_order_field = 'date_latest_answer'
    get_date_latest_answer.short_description = _('Latest answer')

    def get_total_rating_on_answers(self):

        if hasattr(self, 'total_rating_answers'):
            return self.total_rating_answers

        answers = self.answers.annotate(rating=models.Sum(models.Case(
            models.When(opinions__is_useful=True, then=1),
            models.When(opinions__is_useful=False, then=-1),
            output_field=models.IntegerField()
        )))

        return answers.aggregate(total_rating=Round(models.Avg('rating')))['total_rating']
    get_total_rating_on_answers.short_description = _('Total rating')
    get_total_rating_on_answers.admin_order_field = 'total_rating_answers'

    def get_count_good_opinions_on_answers(self):

        if hasattr(self, 'count_good_opinions'):
            return self.count_good_opinions

        return self.answers.filter(opinions__is_useful=True).count()
    get_count_good_opinions_on_answers.admin_order_field = 'count_good_opinions'
    get_count_good_opinions_on_answers.short_description = _('Count good opinions')

    def get_count_bad_opinions_on_answers(self):

        if hasattr(self, 'count_bad_opinions'):
            return self.count_bad_opinions

        return self.answers.filter(opinions__is_useful=False).count()
    get_count_bad_opinions_on_answers.admin_order_field = 'count_bad_opinions'
    get_count_bad_opinions_on_answers.short_description = _('Count bad opinions')

    def get_count_opinions_on_answers(self):

        if hasattr(self, 'count_opinions'):
            return self.count_opinions

        return self.answers.aggregate(count_opinions=models.Count('opinions'))['count_opinions']
    get_count_opinions_on_answers.admin_order_field = 'count_opinions'
    get_count_opinions_on_answers.short_description = _('Count opinions')

    def get_count_comments_on_its_answers(self):
        """ """

        if hasattr(self, 'count_comments_answers'):
            return self.count_comments_answers

        return self.answers.aggregate(count_comments=models.Count('comments'))['count_comments']
    get_count_comments_on_its_answers.short_description = _('Count comments on answers')
    get_count_comments_on_its_answers.admin_order_field = 'count_comments_answers'
