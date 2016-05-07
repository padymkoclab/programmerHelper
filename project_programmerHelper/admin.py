
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

# auth
from apps.app_accounts.models import Account
from apps.app_accounts.admin import AccountAdmin  # , AccountAdminArticles
from django.contrib.auth.models import Group
#
from apps.app_generic_models.models import UserComment_Generic, UserOpinion_Generic, UserLike_Generic
from apps.app_generic_models.admin import UserComment_GenericAdmin, UserOpinion_GenericAdmin, UserLike_GenericAdmin
from apps.app_polls.models import Poll, Choice, VoteInPoll
from apps.app_polls.admin import PollAdmin, VoteInPollAdmin, ChoiceAdmin
from apps.app_books.models import Book, Writter, OpinionAboutBook, BookComment
from apps.app_books.admin import BookAdmin, BookCommentAdmin, WritterAdmin, OpinionAboutBookAdmin
from apps.app_cources.models import Course, Lesson, Sublesson, OpinionAboutLesson, LessonComment
from apps.app_snippets.models import Snippet, SnippetComment, OpinionAboutSnippet
from apps.app_snippets.admin import SnippetAdmin, SnippetCommentAdmin, OpinionAboutSnippetAdmin
from apps.app_programming_tester.models import TestSuit, TestQuestion, Variant
from apps.app_programming_tester.admin import TestSuitAdmin, TestQuestionAdmin, VariantAdmin
from apps.app_badges.models import Badge, GettingBadge
from apps.app_badges.admin import BadgeAdmin, GettingBadgeAdmin
from apps.app_programming_utilities.models import ProgrammingCategory, ProgrammingUtility
from apps.app_programming_utilities.admin import ProgrammingCategoryAdmin, ProgrammingUtilityAdmin
from apps.app_web_links.admin import WebLinkAdmin
from apps.app_web_links.models import WebLink
from apps.app_tags.admin import TagAdmin
from apps.app_tags.models import Tag
from apps.app_forum.models import ForumTopic, ForumTheme, ForumPost
from apps.app_forum.admin import ForumThemeAdmin, ForumTopicAdmin, ForumPostAdmin
from apps.app_articles.models import Article, OpinionAboutArticle, ArticleSubsection, ArticleComment
from apps.app_articles.admin import ArticleAdmin, OpinionAboutArticleAdmin, ArticleSubsectionAdmin, ArticleCommentAdmin
from apps.app_solutions.models import SolutionCategory, Solution, Question, Answer
from apps.app_solutions.admin import SolutionCategoryAdmin, SolutionAdmin, QuestionAdmin, AnswerAdmin
from apps.app_newsletters.models import Newsletter
from apps.app_newsletters.admin import NewsletterAdmin


class MyAdminSite(admin.AdminSite):
    site_header = _('Admin part of website')
    site_title = _('Monty Python administration')
    index_title = _('Website ProgrammerHelper')
    empty_value_display = '-'


ProgrammerHelper_AdminSite = MyAdminSite(name='ProgrammerHelper')
ProgrammerHelper_AdminSite.register(Group)
# app_accounts
ProgrammerHelper_AdminSite.register(Account, AccountAdmin)
# ProgrammerHelper_AdminSite.register(Account, AccountAdminArticles)
# app_badges
ProgrammerHelper_AdminSite.register(Badge, BadgeAdmin)
ProgrammerHelper_AdminSite.register(GettingBadge, GettingBadgeAdmin)
# app_programming_utilities
ProgrammerHelper_AdminSite.register(ProgrammingCategory, ProgrammingCategoryAdmin)
ProgrammerHelper_AdminSite.register(ProgrammingUtility, ProgrammingUtilityAdmin)
# app_web_links
ProgrammerHelper_AdminSite.register(WebLink, WebLinkAdmin)
# app_programming_tester
ProgrammerHelper_AdminSite.register(TestSuit, TestSuitAdmin)
ProgrammerHelper_AdminSite.register(TestQuestion, TestQuestionAdmin)
ProgrammerHelper_AdminSite.register(Variant, VariantAdmin)
# app_solution
ProgrammerHelper_AdminSite.register(SolutionCategory, SolutionCategoryAdmin)
ProgrammerHelper_AdminSite.register(Solution, SolutionAdmin)
# ProgrammerHelper_AdminSite.register(OpinionAboutSolution, OpinionAboutSolutionAdmin)
# ProgrammerHelper_AdminSite.register(SolutionComment, SolutionCommentAdmin)
ProgrammerHelper_AdminSite.register(Question, QuestionAdmin)
# ProgrammerHelper_AdminSite.register(OpinionAboutQuestion, OpinionAboutQuestionAdmin)
ProgrammerHelper_AdminSite.register(Answer, AnswerAdmin)
# ProgrammerHelper_AdminSite.register(AnswerComment, AnswerCommentAdmin)
# app_articles
ProgrammerHelper_AdminSite.register(Article, ArticleAdmin)
ProgrammerHelper_AdminSite.register(OpinionAboutArticle, OpinionAboutArticleAdmin)
ProgrammerHelper_AdminSite.register(ArticleSubsection, ArticleSubsectionAdmin)
ProgrammerHelper_AdminSite.register(ArticleComment, ArticleCommentAdmin)
# app_tags
ProgrammerHelper_AdminSite.register(Tag, TagAdmin)
# app_forum
ProgrammerHelper_AdminSite.register(ForumTheme, ForumThemeAdmin)
ProgrammerHelper_AdminSite.register(ForumTopic, ForumTopicAdmin)
ProgrammerHelper_AdminSite.register(ForumPost, ForumPostAdmin)
# app_snippets
ProgrammerHelper_AdminSite.register(Snippet, SnippetAdmin)
ProgrammerHelper_AdminSite.register(OpinionAboutSnippet, OpinionAboutSnippetAdmin)
ProgrammerHelper_AdminSite.register(SnippetComment, SnippetCommentAdmin)
# app_newsletters
ProgrammerHelper_AdminSite.register(Newsletter, NewsletterAdmin)
# app_books
ProgrammerHelper_AdminSite.register(Book, BookAdmin)
ProgrammerHelper_AdminSite.register(Writter, WritterAdmin)
ProgrammerHelper_AdminSite.register(OpinionAboutBook, OpinionAboutBookAdmin)
ProgrammerHelper_AdminSite.register(BookComment, BookCommentAdmin)
# app_cources
ProgrammerHelper_AdminSite.register(Course,)
ProgrammerHelper_AdminSite.register(Lesson,)
ProgrammerHelper_AdminSite.register(Sublesson,)
ProgrammerHelper_AdminSite.register(OpinionAboutLesson,)
ProgrammerHelper_AdminSite.register(LessonComment)
# app_polls
ProgrammerHelper_AdminSite.register(Poll, PollAdmin)
ProgrammerHelper_AdminSite.register(Choice, ChoiceAdmin)
ProgrammerHelper_AdminSite.register(VoteInPoll, VoteInPollAdmin)
# app_generic_models
ProgrammerHelper_AdminSite.register(UserComment_Generic, UserComment_GenericAdmin)
ProgrammerHelper_AdminSite.register(UserOpinion_Generic, UserOpinion_GenericAdmin)
ProgrammerHelper_AdminSite.register(UserLike_Generic, UserLike_GenericAdmin)
