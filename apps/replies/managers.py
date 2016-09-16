
from django.db import models


class ReplyManager(models.Manager):
    """

    """

    def most_common_words_in_advantages(self):
        pass

    def most_common_words_in_disadvantages(self):
        pass

    def objects_with_count_replies(self):
        """ """

        return self.annotate(count_replies=models.Count('replies', distinct=True))
