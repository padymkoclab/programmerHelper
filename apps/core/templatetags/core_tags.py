
import logging

from django import template

from ..admin import AdminSite

logger = logging.getLogger('django.development')
register = template.Library()


@register.simple_tag
def has_registered_app_admin(app_label):

    return app_label in AdminSite._regiter_app_admin.keys()


class MakeMarkupTableTag(template.Node):
    """ """

    def __init__(self, tables_data, *args, **kwargs):
        self.tables_data = template.Variable(tables_data)

    def render(self, context):

        try:
            tables_data = self.tables_data.resolve(context)

            template_ = template.loader.get_template('core/admin/_statistics_tables.html')

            return template_.render(
                template.Context({
                    'tables_data': tables_data,
                })
            )
        except:
            logger.error('Templatetag does not working')
            return ''


class StatisticsTableAndChartTag(template.Node):

    def __init__(self, tables_charts_data, *args, **kwargs):
        self.tables_charts_data = template.Variable(tables_charts_data)

    def render(self, context):

        try:
            tables_charts_data = self.tables_charts_data.resolve(context)
            template_ = template.loader.get_template('core/admin/_statistics_charts.html')
            return template_.render(
                template.Context({
                    'tables_charts_data': tables_charts_data,
                })
            )
        except:
            logger.error('Templatetag does not working')
            return ''


@register.tag
def generate_statistics_table(parser, token):

    try:
        tag_name, tables_data = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            '{0} tag requires exactly one argument.'.format(
                token.contents.split()[0]
            )
        )

    return MakeMarkupTableTag(tables_data)


@register.tag
def generate_statistics_tables_with_charts(parser, token):
    """ """

    try:
        tag_name, tables_charts_data = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            '{0} tag requires exactly one argument.'.format(
                token.contents.split()[0]
            )
        )

    return StatisticsTableAndChartTag(tables_charts_data)
