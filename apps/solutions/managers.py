
from django.db import models


class SolutionCategoryManager(models.Manager):
    """
    Model manager for categories of solutions.
    """

    pass


class SolutionManager(models.Manager):
    """
    Model manager for solutions.
    """

    def complain_on_the_solution(self, solution):
        """Complain on the solution sended admin and author corresponding notification."""

        raise NotImplementedError
