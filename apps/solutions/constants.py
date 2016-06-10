

from django.utils.translation import ugettext_lazy as _

CATEGORIES_OF_SOLUTIONS = [
    'AngularJS',
    'BackboneJS',
    'Bootstrap',
    'Bower',
    'CSS',
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


class Quality:
    """

    """

    def __init__(self, name, description, color):
        super().__init__()
        self.name = name
        self.description = description
        self.color = color

    def __str__(self):
        return '{0.name}'.format(self)

    def __repr__(self):
        return '{0}({1})'.format(self.__class__.__name__, self)

WrongQuality = Quality(name=_('Wrong'), description=_('WrongQuality'), color='darkred')
BadQuality = Quality(name=_('Bad'), description=_('BadQuality'), color='red')
VagueQuality = Quality(name=_('Vague'), description=_('VagueQuality'), color='black')
GoodQuality = Quality(name=_('Good'), description=_('GoodQuality'), color='green')
ApprovedQuality = Quality(name=_('Approved'), description=_('ApprovedQuality'), color='darkgreen')


QUALITIES_DETAILS = {
    'wrong': WrongQuality,
    'bad': BadQuality,
    'vague': VagueQuality,
    'good': GoodQuality,
    'approved': ApprovedQuality,
}
