
from collections import namedtuple

from .models import UserLevel


# Attributes for default superuser
TEST_SUPERUSER_DATA = dict(
    email='admin@admin.com',
    username='admin',
    password='admin',
    date_birthday='2000-12-12',
)


# Data for creating levels of users
UserLevelData = namedtuple('UserLevelData', ('name', 'color', 'description'))
USER_LEVEL_DATAS = [
    UserLevelData(
        name=UserLevel.PLATINUM, color='#D8BFD8', description='Regular level of user'
    ),
    UserLevelData(
        name=UserLevel.GOLDEN, color='#FFD700', description='Golder level of user'
    ),
    UserLevelData(
        name=UserLevel.SILVER, color='#C0C0C0', description='Silver level of user'
    ),
    UserLevelData(
        name=UserLevel.DIAMOND, color='#4B0082', description='Diamond level of user'
    ),
    UserLevelData(
        name=UserLevel.RUBY, color='#DC143C', description='Ruby level of user'
    ),
    UserLevelData(
        name=UserLevel.SAPPHIRE, color='#483D8B', description='Sapphire level of user'
    ),
    UserLevelData(
        name=UserLevel.MALACHITE, color='#3CB371', description='Malachite level of user'
    ),
    UserLevelData(
        name=UserLevel.AMETHYST, color='#800080', description='Amethyst level of user'
    ),
    UserLevelData(
        name=UserLevel.EMERALD, color='#00FA9A', description='Emerald level of user'
    ),
    UserLevelData(
        name=UserLevel.AGATE, color='#2F4F4F', description='Agate level of user'
    ),
    UserLevelData(
        name=UserLevel.TURQUOISE, color='#40E0D0', description='Turquoise level of user'
    ),
    UserLevelData(
        name=UserLevel.AMBER, color='#FF8C00', description='Amber level of user'
    ),
    UserLevelData(
        name=UserLevel.OPAL, color='#FF7F50', description='Opal level of user'
    ),
    UserLevelData(
        name=UserLevel.REGULAR, color='#F0F8FF', description='Regular level of user'
    ),
]
