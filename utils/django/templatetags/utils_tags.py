
import logging
import warnings
import random
from calendar import LocaleHTMLCalendar

from django.utils.http import urlencode
from django.utils.translation import get_language, activate, to_locale
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.html import format_html_join, format_html
from django.template import Library, Node, Variable
from django import template
from django.conf import settings
from django.core.urlresolvers import reverse

# from bs4 import BeautifulSoup
from pygments import highlight
from pygments import lexers
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

from ...python.constants import PRETTY_COLORS


logger = logging.getLogger('django.development')
register = Library()


DICT_NAME_AND_LEXER_NAME = {lexer[0]: lexer[1][0] for lexer in lexers.get_all_lexers()}


# Source https://djangosnippets.org/snippets/1213/
# Usage: {% code 'lang'%} {% endcode %}
@register.tag(name='code')
def do_code(parser, token):
    code = token.split_contents()[-1]
    nodelist = parser.parse(('endcode',))
    parser.delete_first_token()
    return CodeNode(code, nodelist)


class CodeNode(template.Node):

    def __init__(self, lang, code):
        self.lang = lang
        self.nodelist = code

    def render(self, context):
        try:
            language = template.Variable(self.lang).resolve(context)
        except:
            language = self.lang
        code = self.nodelist.render(context)
        code = code.strip()
        try:
            lexer = get_lexer_by_name(language)
        except:
            try:
                lexer = lexers.guess_lexer(code)
            except:
                lexer = lexers.PythonLexer()
        return highlight(code, lexer, HtmlFormatter(linenos='div', cssclass="wrapper_for_code_with_pre"))


# Source https://djangosnippets.org/snippets/350/

# usage: {% stylize "language" %}...language text...{% endstylize %}
@register.tag(name='stylize')
class StylizeNode(Node):
    def __init__(self, nodelist, *varlist):
        self.nodelist, self.vlist = (nodelist, varlist)

    def render(self, context):
        if len(self.vlist) > 0:
            language = Variable(self.vlist[0]).resolve(context)
            lexer_name = DICT_NAME_AND_LEXER_NAME[language]
            try:
                lexer = get_lexer_by_name(lexer_name, encoding='UTF-8')
            except:
                try:
                    lexer = lexers.guess_lexer(context, encoding='UTF-8')
                except:
                    lexer = lexers.Python3Lexer(encoding='UTF-8')
        html_markup = self.nodelist.render(context).strip()
        return highlight(html_markup, lexer, HtmlFormatter())


def stylize(parser, token):
    nodelist = parser.parse(('endstylize',))
    parser.delete_first_token()
    return StylizeNode(nodelist, *token.contents.split()[1:])

stylize = register.tag(stylize)


@register.simple_tag(takes_context=True)
def url_get_kwargs(context, url_for_reverse, **kwargs):
    """ """

    # make reverse from url
    url = reverse(url_for_reverse)

    # convert dict to urlencode
    get_kwargs = urlencode(kwargs)

    # return full url
    return '{0}?{1}'.format(url, get_kwargs)


@register.inclusion_tag('snippets/temp.html', takes_context=True)
def templated_list(context, listing):
    return {
        'listing': listing,
        'user': context['user'],
    }


@register.tag(name='tag_cloud_as_listing')
def tag_cloud_as_listing(parser, token):
    """
    Display listing of a tags by sizes. A input variable must be as a sequence (TagObj, number).
    A values an arguments 'show_url' must be 'None', 'Admin', 'Absolute'.
    A values an arguments 'colors' must be 'Black', 'Standart', 'Colored'.
    """

    try:
        contents = token.split_contents()
        tag_name = contents[0]
        variable_name = contents[1]
        show_url = contents[2].split('=', 1)[1].strip('\'')
        colors = contents[3].split('=', 1)[1].strip('\'')
    except ValueError:
        raise template.TemplateSyntaxError(
            '{tag_name} tag requires are three arguments: variable_name, show_url, colors'.format(
                tag_name=tag_name
            )
        )
    if show_url not in ['None', 'Admin', 'Absolute']:
        raise template.TemplateSyntaxError(
            "Parameter 'show_url' must be 'None', 'Admin' or 'Absolute', not {0}".format(show_url)
        )
    if colors not in ['Black', 'Standart', 'Colored']:
        raise template.TemplateSyntaxError(
            "Parameter 'colors' must be 'Black', 'Standart' or 'Colored', not {0}".format(show_url)
        )
    return TagNode(variable_name, show_url, colors)


class TagNode(template.Node):

    logger.debug('"remove_tags" was remove in Django 1.10.')

    def __init__(self, variable_name, show_url, colors):
        self.variable_name = template.Variable(variable_name)
        self.show_url = show_url
        self.colors = colors

    def render(self, context):
        try:
            #
            value_variable_name = self.variable_name.resolve(context)
            #
            html_spans = list()
            pattern = \
            '<span style="font-size: {size}em;color: {color};"><a href="{url}" style="color: {color};">{name} ({number})</a></span>'
            for obj, number in value_variable_name:

                if self.colors == 'Black':
                    color = '#222'
                elif self.colors == 'Standart':
                    color = ''
                elif self.colors == 'Colored':
                    color = random.choice(PRETTY_COLORS)

                if self.show_url == 'Absolute':
                    url = obj.get_absolute_url()
                elif self.show_url == 'Admin':
                    url = '#'
                else:
                    url = '#'

                size = number / 1000 + 1

                html_span = pattern.format(size=size, url=url, name=obj.__str__(), color=color, number=number)

                if self.show_url == 'None':
                    html_span = remove_tags(html_span, 'a')
                html_spans.append(html_span)

            listing_tags = mark_safe(', '.join(html_spans))
            container_for_listing_tags = format_html('<div class="container_for_listing_tags">{0}</div>', listing_tags)

            return container_for_listing_tags
        except template.VariableDoesNotExist:
            return ''
            # if settings.DEBUG is False:


class CalendarNode(template.Node):
    def __init__(self, year, month, theme):
        self.year = year
        self.month = month
        self.theme = theme

    def render(self, context):
        try:
            activate('ru-ru')
            current_locale_name = get_language()
            current_locale_name = to_locale(current_locale_name)
            charset = settings.DEFAULT_CHARSET.upper()
            calendar = LocaleHTMLCalendar(
                firstweekday=settings.FIRST_DAY_OF_WEEK,
                locale=(current_locale_name, charset)
            )
            weeks_current_month = calendar.formatmonth(self.year, self.month)

            logger.critical('BeautifulSoup is not used here.')
            weeks_current_month = BeautifulSoup(weeks_current_month, 'html.parser')
            #
            weeks_current_month.find('table')['class'].append(self.theme)
            today = timezone.now().today()
            #
            if today.year == self.year and today.month == self.month:
                weeks_current_month_today = weeks_current_month.find('td', string=today.day)
                weeks_current_month_today['class'].append('this_is_now_day')
            #
            calendar_template = context.template.engine.get_template('mylabour/calendar.html')
            html = calendar_template.render(
                template.Context(
                    {
                        'weeks_current_month': mark_safe(weeks_current_month),
                    },
                    autoescape=context.autoescape)
            )
            return html
        except Exception as e:
            if settings.DEBUG is True:
                raise Exception(e)
            warnings.warn('Something went wrong. Debug the code instantly (right now)!')
            return ''


@register.tag(name='calendar')
def calendar(parser, token):
    """Show calendar"""

    #
    try:
        tag_name, year, month, theme = token.split_contents()
    except ValueError:
        today = timezone.now().today()
        theme = 'light_theme'
        return CalendarNode(today.year, today.month, theme)
        # raise template.TemplateSyntaxError(
        #   '"{0}" tag required two arguments: year and month'.format(token.contents.split()[0]))
    else:
        try:
            year = int(year)
            month = int(month)
        except TypeError:
            raise template.TemplateSyntaxError(
                'An arguments "year" and "month" must be integer'.format())

        theme = theme.strip('\'')
        if theme not in ['dark_theme', 'light_theme']:
            raise template.TemplateSyntaxError(
                'Acceced only two theme for calendar "light_theme" and "dark_theme"'.format())

        #
        if not 1 <= year <= 9999:
            raise ValueError('"year" is out of range (1, ... 9999)')
        if not 1 <= month <= 12:
            raise ValueError('"month" must be in 1..12')

        return CalendarNode(year, month, theme)


@register.simple_tag(takes_context=True)
def ipdb(context):
    """ """

    import ipdb;
    ipdb.set_trace()
