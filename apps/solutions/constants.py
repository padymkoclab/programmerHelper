
import collections

from django.utils.translation import ugettext_lazy as _

# Names categories for solutions by default

CATEGORIES_OF_SOLUTIONS = [
    'AngularJS',
    'BackboneJS',
    'Bootstrap',
    'Bower',
    'CSS',
    'Coffescript',
    'Django',
    'Gevent',
    'Git',
    'Google Chrome',
    'Grunt',
    'Gunicorn',
    'HTML',
    'Heroku',
    'JavaScript',
    'Linux',
    'Matplotlib',
    'Mozzila',
    'MySQL',
    'Nginx',
    'Numpy',
    'Opera',
    'PIL',
    'Postgres SQL',
    'PyQt5',
    'Python',
    'PythonAnyWhere',
    'Regex Expressions',
    'SQLite',
    'Scipy',
    'Selenium',
    'Tornado',
    'Vagrant',
    'Windows',
    'jQuery',
    'jQueryUI',
    'wxPython',
]

# Details about quality of solution

Quality = collections.namedtuple('Quality', ['type', 'description', 'color'])

WrongQuality = Quality(
    type=_('Wrong'),
    description=_('Wrong quality solution, tells about what solution is have many negative opinions of users.'),
    color='darkred'
)
BadQuality = Quality(
    type=_('Bad'),
    description=_('Bad quality solution, tells about what solution is have more negative opinions of users, than possitive.'),
    color='red'
)
VagueQuality = Quality(
    type=_('Vague'),
    description=_('Vague quality solution, tells about what solution is have not clear definition of quality.'),
    color='black'
)
GoodQuality = Quality(
    type=_('Good'),
    description=_('Good quality solution, tells about what solution is have more possitive opinions of users. than negative.'),
    color='green'
)
ApprovedQuality = Quality(
    type=_('Approved'),
    description=_('Approved quality solution, tells about what solution is have many possitive opinions from users.'),
    color='darkgreen'
)

QUALITIES_DETAILS = {
    'wrong': WrongQuality,
    'bad': BadQuality,
    'vague': VagueQuality,
    'good': GoodQuality,
    'approved': ApprovedQuality,
}
