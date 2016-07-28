
from collections import namedtuple

from .models import UserLevel


# Attributes for default superuser
DEFAULT_SUPERUSER_DATA = dict(
    email='setivolkylany@gmail.com',
    username='setivolkylany',
    password='PyJS210493',
    date_birthday='2000-12-12',
)


# Data for creating levels of users
UserLevelData = namedtuple('UserLevelData', ('name', 'color', 'description'))
USER_LEVEL_DATAS = [
    UserLevelData(
        name=UserLevel.CHOICES_LEVEL.platinum, color='#D8BFD8', description='Regular level of user'
    ),
    UserLevelData(
        name=UserLevel.CHOICES_LEVEL.golden, color='#FFD700', description='Golder level of user'
    ),
    UserLevelData(
        name=UserLevel.CHOICES_LEVEL.silver, color='#C0C0C0', description='Silver level of user'
    ),
    UserLevelData(
        name=UserLevel.CHOICES_LEVEL.diamond, color='#4B0082', description='Diamond level of user'
    ),
    UserLevelData(
        name=UserLevel.CHOICES_LEVEL.ruby, color='#DC143C', description='Ruby level of user'
    ),
    UserLevelData(
        name=UserLevel.CHOICES_LEVEL.sapphire, color='#483D8B', description='Sapphire level of user'
    ),
    UserLevelData(
        name=UserLevel.CHOICES_LEVEL.malachite, color='#3CB371', description='Malachite level of user'
    ),
    UserLevelData(
        name=UserLevel.CHOICES_LEVEL.amethyst, color='#800080', description='Amethyst level of user'
    ),
    UserLevelData(
        name=UserLevel.CHOICES_LEVEL.emerald, color='#00FA9A', description='Emerald level of user'
    ),
    UserLevelData(
        name=UserLevel.CHOICES_LEVEL.agate, color='#2F4F4F', description='Agate level of user'
    ),
    UserLevelData(
        name=UserLevel.CHOICES_LEVEL.turquoise, color='#40E0D0', description='Turquoise level of user'
    ),
    UserLevelData(
        name=UserLevel.CHOICES_LEVEL.amber, color='#FF8C00', description='Amber level of user'
    ),
    UserLevelData(
        name=UserLevel.CHOICES_LEVEL.opal, color='#FF7F50', description='Opal level of user'
    ),
    UserLevelData(
        name=UserLevel.CHOICES_LEVEL.regular, color='#F0F8FF', description='Regular level of user'
    ),
]
