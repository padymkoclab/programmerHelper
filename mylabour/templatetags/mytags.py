
from django.template import Library, Node, resolve_variable
from django import template

from pygments import highlight
from pygments import lexers
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

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
            language = resolve_variable(self.vlist[0], context)
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
