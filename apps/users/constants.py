
from .models import Level


# Attributes for default superuser
TEST_SUPERUSER_DATA = dict(
    email='admin@admin.com',
    username='admin',
    password='admin',
    alias='Admin',
)


# Data for creating levels of users
LEVELS = (
    {
        'name': Level.PLATINUM,
        'color': '#D8BFD8',
        'description': 'Platinum level of user',
    },
    {
        'name': Level.GOLDEN,
        'color': '#FFD700',
        'description': 'Golder level of user',
    },
    {
        'name': Level.SILVER,
        'color': '#C0C0C0',
        'description': 'Silver level of user',
    },
    {
        'name': Level.DIAMOND,
        'color': '#4B0082',
        'description': 'Diamond level of user',
    },
    {
        'name': Level.RUBY,
        'color': '#DC143C',
        'description': 'Ruby level of user',
    },
    {
        'name': Level.SAPPHIRE,
        'color': '#483D8B',
        'description': 'Sapphire level of user',
    },
    {
        'name': Level.MALACHITE,
        'color': '#3CB371',
        'description': 'Malachite level of user',
    },
    {
        'name': Level.AMETHYST,
        'color': '#800080',
        'description': 'Amethyst level of user',
    },
    {
        'name': Level.EMERALD,
        'color': '#00FA9A',
        'description': 'Emerald level of user',
    },
    {
        'name': Level.AGATE,
        'color': '#2F4F4F',
        'description': 'Agate level of user',
    },
    {
        'name': Level.TURQUOISE,
        'color': '#40E0D0',
        'description': 'Turquoise level of user',
    },
    {
        'name': Level.AMBER,
        'color': '#FF8C00',
        'description': 'Amber level of user',
    },
    {
        'name': Level.OPAL,
        'color': '#FF7F50',
        'description': 'Opal level of user',
    },
    {
        'name': Level.REGULAR,
        'color': '#F0F8FF',
        'description': 'Regular level of user',
    },
)


GROUPS_NAMES = (
    'moderators',
    'superusers',
    # 'publicists',
    # 'Suggest book',
    'regular',
    'banned',
)


CALCULATION_REPUTATION = {
    'VOTE': 1,
}
