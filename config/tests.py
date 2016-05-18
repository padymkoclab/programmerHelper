
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group, Permission


"""
Permissions control what you can do on ProgrammerHelper.com.
Gain more permissions by increasing your reputation
(points you receive from your fellow users for asked interesting questions
 and replied useful answers, curious articles and helpful snippets).
"""

# Created basics groups


group = Group.objects.create(name=_('Commentators'))
group.permissions = [
    Permission.objects.get(codename='add_articlecomment'),
    Permission.objects.get(codename='change_articlecomment'),
    Permission.objects.get(codename='delete_articlecomment'),
    Permission.objects.get(codename='add_bookcomment'),
    Permission.objects.get(codename='change_bookcomment'),
    Permission.objects.get(codename='delete_bookcomment'),
    Permission.objects.get(codename='add_lessoncomment'),
    Permission.objects.get(codename='change_lessoncomment'),
    Permission.objects.get(codename='delete_lessoncomment'),
    Permission.objects.get(codename='add_programmingutilitycomment'),
    Permission.objects.get(codename='change_programmingutilitycomment'),
    Permission.objects.get(codename='delete_programmingutilitycomment'),
    Permission.objects.get(codename='add_snippetcomment'),
    Permission.objects.get(codename='change_snippetcomment'),
    Permission.objects.get(codename='delete_snippetcomment'),
    Permission.objects.get(codename='add_answercomment'),
    Permission.objects.get(codename='change_answercomment'),
    Permission.objects.get(codename='delete_answercomment'),
    Permission.objects.get(codename='add_solutioncomment'),
    Permission.objects.get(codename='change_solutioncomment'),
    Permission.objects.get(codename='delete_solutioncomment'),
]

group = Group.objects.create(name=_('Respondents'))
group.permissions = [
    Permission.objects.get(codename='add_answer'),
    Permission.objects.get(codename='change_answer'),
    Permission.objects.get(codename='delete_answer'),
]

group = Group.objects.create(name=_('Creators articles'))
group.permissions = [
    Permission.objects.get(codename='add_article'),
    Permission.objects.get(codename='change_article'),
    Permission.objects.get(codename='delete_article'),
    Permission.objects.get(codename='add_articlesubsection'),
    Permission.objects.get(codename='change_articlesubsection'),
    Permission.objects.get(codename='delete_articlesubsection'),
    Permission.objects.get(codename='add_weblink'),
    Permission.objects.get(codename='change_weblink'),
    Permission.objects.get(codename='delete_weblink'),
]

group = Group.objects.create(name=_('Have may opinions'))
group.permissions = [
    Permission.objects.get(codename='add_opinionaboutsnippet'),
    Permission.objects.get(codename='change_opinionaboutsnippet'),
    Permission.objects.get(codename='delete_opinionaboutsnippet'),
    Permission.objects.get(codename='add_opinionaboutanswer'),
    Permission.objects.get(codename='change_opinionaboutanswer'),
    Permission.objects.get(codename='delete_opinionaboutanswer'),
    Permission.objects.get(codename='add_opinionaboutquestion'),
    Permission.objects.get(codename='change_opinionaboutquestion'),
    Permission.objects.get(codename='delete_opinionaboutquestion'),
    Permission.objects.get(codename='add_opinionaboutsolution'),
    Permission.objects.get(codename='change_opinionaboutsolution'),
    Permission.objects.get(codename='delete_opinionaboutsolution'),
    Permission.objects.get(codename='add_opinionaboutarticle'),
    Permission.objects.get(codename='change_opinionaboutarticle'),
    Permission.objects.get(codename='delete_opinionaboutarticle'),
    Permission.objects.get(codename='add_opinionaboutbook'),
    Permission.objects.get(codename='change_opinionaboutbook'),
    Permission.objects.get(codename='delete_opinionaboutbook'),
    Permission.objects.get(codename='add_opinionaboutlesson'),
    Permission.objects.get(codename='change_opinionaboutlesson'),
    Permission.objects.get(codename='delete_opinionaboutlesson'),
    Permission.objects.get(codename='add_opinionaboutprogrammingutility'),
    Permission.objects.get(codename='change_opinionaboutprogrammingutility'),
    Permission.objects.get(codename='delete_opinionaboutprogrammingutility'),
]

group = Group.objects.create(name=_('Creators testsuits'))
group.permissions = [
    Permission.objects.get(codename='add_testquestion'),
    Permission.objects.get(codename='change_testquestion'),
    Permission.objects.get(codename='delete_testquestion'),
    Permission.objects.get(codename='add_testsuit'),
    Permission.objects.get(codename='change_testsuit'),
    Permission.objects.get(codename='delete_testsuit'),
    Permission.objects.get(codename='add_variant'),
    Permission.objects.get(codename='change_variant'),
    Permission.objects.get(codename='delete_variant'),
]

group = Group.objects.create(name=_('Creators courses'))
group.permissions = [
    Permission.objects.get(codename='add_course'),
    Permission.objects.get(codename='change_course'),
    Permission.objects.get(codename='delete_course'),
    Permission.objects.get(codename='add_lesson'),
    Permission.objects.get(codename='change_lesson'),
    Permission.objects.get(codename='delete_lesson'),
    Permission.objects.get(codename='add_sublesson'),
    Permission.objects.get(codename='change_sublesson'),
    Permission.objects.get(codename='delete_sublesson'),
]

group = Group.objects.create(name=_('ForumUsers'))
group.permissions = [
    Permission.objects.get(codename='add_forumpost'),
    Permission.objects.get(codename='change_forumpost'),
    Permission.objects.get(codename='delete_forumpost'),
]


group = Group.objects.create(name=_('ForumSuperUsers'))
group.permissions = [
    Permission.objects.get(codename='add_forumtopic'),
    Permission.objects.get(codename='change_forumtopic'),
    Permission.objects.get(codename='delete_forumtopic'),
]

group = Group.objects.create(name=_('Snippeters'))
group.permissions = [
    Permission.objects.get(codename='add_snippet'),
    Permission.objects.get(codename='change_snippet'),
    Permission.objects.get(codename='delete_snippet'),
]

group = Group.objects.create(name=_('Questioners'))
group.permissions = [
    Permission.objects.get(codename='add_question'),
    Permission.objects.get(codename='change_question'),
    Permission.objects.get(codename='delete_question'),
]

group = Group.objects.create(name=_('Solutioners'))
group.permissions = [
    Permission.objects.get(codename='add_solution'),
    Permission.objects.get(codename='change_solution'),
    Permission.objects.get(codename='delete_solution'),
    Permission.objects.get(codename='add_weblink'),
    Permission.objects.get(codename='change_weblink'),
    Permission.objects.get(codename='delete_weblink'),
]

group = Group.objects.create(name=_('Creators tags'))
group.permissions = [
    Permission.objects.get(codename='add_tag'),
    Permission.objects.get(codename='change_tag'),
    Permission.objects.get(codename='delete_tag'),
]

group = Group.objects.create(name=_('Can view opinions about'))
group.permissions = Permission.objects.filter(codename='can_view_opinions')
