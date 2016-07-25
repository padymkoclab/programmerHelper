
from collections import namedtuple

from .models import AccountLevel


AccountLevelData = namedtuple('AccountLevelData', ('name', 'color', 'description'))

# Data for creating levels of accounts
ACCOUNT_LEVEL_DATAS = [
    AccountLevelData(
        name=AccountLevel.CHOICES_LEVEL.platinum, color='#D8BFD8', description='Regular level of account'
    ),
    AccountLevelData(
        name=AccountLevel.CHOICES_LEVEL.golden, color='#FFD700', description='Golder level of account'
    ),
    AccountLevelData(
        name=AccountLevel.CHOICES_LEVEL.silver, color='#C0C0C0', description='Silver level of account'
    ),
    AccountLevelData(
        name=AccountLevel.CHOICES_LEVEL.diamond, color='#4B0082', description='Diamond level of account'
    ),
    AccountLevelData(
        name=AccountLevel.CHOICES_LEVEL.ruby, color='#DC143C', description='Ruby level of account'
    ),
    AccountLevelData(
        name=AccountLevel.CHOICES_LEVEL.sapphire, color='#483D8B', description='Sapphire level of account'
    ),
    AccountLevelData(
        name=AccountLevel.CHOICES_LEVEL.malachite, color='#3CB371', description='Malachite level of account'
    ),
    AccountLevelData(
        name=AccountLevel.CHOICES_LEVEL.amethyst, color='#800080', description='Amethyst level of account'
    ),
    AccountLevelData(
        name=AccountLevel.CHOICES_LEVEL.emerald, color='#00FA9A', description='Emerald level of account'
    ),
    AccountLevelData(
        name=AccountLevel.CHOICES_LEVEL.agate, color='#2F4F4F', description='Agate level of account'
    ),
    AccountLevelData(
        name=AccountLevel.CHOICES_LEVEL.turquoise, color='#40E0D0', description='Turquoise level of account'
    ),
    AccountLevelData(
        name=AccountLevel.CHOICES_LEVEL.amber, color='#FF8C00', description='Amber level of account'
    ),
    AccountLevelData(
        name=AccountLevel.CHOICES_LEVEL.opal, color='#FF7F50', description='Opal level of account'
    ),
    AccountLevelData(
        name=AccountLevel.CHOICES_LEVEL.regular, color='#F0F8FF', description='Regular level of account'
    ),
]

# Attributes for default superuser
DEFAULT_SUPERUSER_DATA = dict(
    email='setivolkylany@gmail.com',
    username='setivolkylany',
    password='lv210493',
    date_birthday='2000-12-12',
)
