
import datetime


SITE_NAME = 'ProgrammerHelper.com'

CAN_DELETE_USER = False

COUNT_DAYS_DISTINGUISH_ELEMENTS_AS_NEW = 7

MIN_LENGTH_FOR_NAME_OR_TITLE_OBJECT = 10

MIN_COUNT_TAGS_ON_OBJECT = 1

MAX_COUNT_TAGS_ON_OBJECT = 5

DATE_CREATING_SITE = datetime.date(year=2016, month=3, day=1)

IGNORABLE_URLS_FOR_COUNT_VISITS = (
    r'admin/[\w]*',
    r'*\.jpeg$',
    r'*\.png$',
    r'*\.jpg$',
    r'*\.gif$',
    r'/favicon.ico$',
    r'/(robots.txt)|(humans.txt)$',
)
