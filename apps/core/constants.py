
import enum


@enum.unique
class UpdateReputation(enum.Enum):
    """
    Getting reputation of user for activity on website:
    marks of published snippets, answers, questions and rating of articles,
    participate in polls.
    ---------------------------------------
        Evaluate reputation for activity
    ---------------------------------------
    Mark answers                   = sum()
    Mark questions                 = *1
    Mark solutions                 = *3
    Rating articles                 = sum()
    Mark snippets                  = *2
    Filled profile                  = *1
    Participate in poll             = *1
    Popular topic                   = 1000 views = + 1

    Vote in poll +1

    ---------------------------------------
    """

    ADDED_VOTE = 1
    DELETED_VOTE = -1

    @classmethod
    def get_table_charge_reputation(cls):
        pass
