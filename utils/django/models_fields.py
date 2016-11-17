
import copy
import datetime

from django.core import checks
from django import forms
from django.utils.text import capfirst
from django.core.exceptions import ValidationError
from django.core.validators import validate_unicode_slug
from django.db.models import NullBooleanField
from django.utils.translation import ugettext as _
from django.db import models
from django.utils.encoding import smart_text

from autoslug import AutoSlugField
# import markdown
# import textile
# from docutils.core import publish_parts

from .forms_fields import CharFieldFixed
from .widgets import ColorInput
from .descriptors import ReverseOneToOneDescriptorWithAutoCreate


__all__ = ['CountryField', 'ConfiguredAutoSlugField']


class CountryField(models.CharField):

    # ISO 3166-1 country names and codes adapted from http://opencountrycodes.appspot.com/python/
    COUNTRIES = (
        ('GB', _('United Kingdom')),
        ('AF', _('Afghanistan')),
        ('AX', _('Aland Islands')),
        ('AL', _('Albania')),
        ('DZ', _('Algeria')),
        ('AS', _('American Samoa')),
        ('AD', _('Andorra')),
        ('AO', _('Angola')),
        ('AI', _('Anguilla')),
        ('AQ', _('Antarctica')),
        ('AG', _('Antigua and Barbuda')),
        ('AR', _('Argentina')),
        ('AM', _('Armenia')),
        ('AW', _('Aruba')),
        ('AU', _('Australia')),
        ('AT', _('Austria')),
        ('AZ', _('Azerbaijan')),
        ('BS', _('Bahamas')),
        ('BH', _('Bahrain')),
        ('BD', _('Bangladesh')),
        ('BB', _('Barbados')),
        ('BY', _('Belarus')),
        ('BE', _('Belgium')),
        ('BZ', _('Belize')),
        ('BJ', _('Benin')),
        ('BM', _('Bermuda')),
        ('BT', _('Bhutan')),
        ('BO', _('Bolivia')),
        ('BA', _('Bosnia and Herzegovina')),
        ('BW', _('Botswana')),
        ('BV', _('Bouvet Island')),
        ('BR', _('Brazil')),
        ('IO', _('British Indian Ocean Territory')),
        ('BN', _('Brunei Darussalam')),
        ('BG', _('Bulgaria')),
        ('BF', _('Burkina Faso')),
        ('BI', _('Burundi')),
        ('KH', _('Cambodia')),
        ('CM', _('Cameroon')),
        ('CA', _('Canada')),
        ('CV', _('Cape Verde')),
        ('KY', _('Cayman Islands')),
        ('CF', _('Central African Republic')),
        ('TD', _('Chad')),
        ('CL', _('Chile')),
        ('CN', _('China')),
        ('CX', _('Christmas Island')),
        ('CC', _('Cocos (Keeling) Islands')),
        ('CO', _('Colombia')),
        ('KM', _('Comoros')),
        ('CG', _('Congo')),
        ('CD', _('Congo, The Democratic Republic of the')),
        ('CK', _('Cook Islands')),
        ('CR', _('Costa Rica')),
        ('CI', _('Cote d\'Ivoire')),
        ('HR', _('Croatia')),
        ('CU', _('Cuba')),
        ('CY', _('Cyprus')),
        ('CZ', _('Czech Republic')),
        ('DK', _('Denmark')),
        ('DJ', _('Djibouti')),
        ('DM', _('Dominica')),
        ('DO', _('Dominican Republic')),
        ('EC', _('Ecuador')),
        ('EG', _('Egypt')),
        ('SV', _('El Salvador')),
        ('GQ', _('Equatorial Guinea')),
        ('ER', _('Eritrea')),
        ('EE', _('Estonia')),
        ('ET', _('Ethiopia')),
        ('FK', _('Falkland Islands (Malvinas)')),
        ('FO', _('Faroe Islands')),
        ('FJ', _('Fiji')),
        ('FI', _('Finland')),
        ('FR', _('France')),
        ('GF', _('French Guiana')),
        ('PF', _('French Polynesia')),
        ('TF', _('French Southern Territories')),
        ('GA', _('Gabon')),
        ('GM', _('Gambia')),
        ('GE', _('Georgia')),
        ('DE', _('Germany')),
        ('GH', _('Ghana')),
        ('GI', _('Gibraltar')),
        ('GR', _('Greece')),
        ('GL', _('Greenland')),
        ('GD', _('Grenada')),
        ('GP', _('Guadeloupe')),
        ('GU', _('Guam')),
        ('GT', _('Guatemala')),
        ('GG', _('Guernsey')),
        ('GN', _('Guinea')),
        ('GW', _('Guinea-Bissau')),
        ('GY', _('Guyana')),
        ('HT', _('Haiti')),
        ('HM', _('Heard Island and McDonald Islands')),
        ('VA', _('Holy See (Vatican City State)')),
        ('HN', _('Honduras')),
        ('HK', _('Hong Kong')),
        ('HU', _('Hungary')),
        ('IS', _('Iceland')),
        ('IN', _('India')),
        ('ID', _('Indonesia')),
        ('IR', _('Iran, Islamic Republic of')),
        ('IQ', _('Iraq')),
        ('IE', _('Ireland')),
        ('IM', _('Isle of Man')),
        ('IL', _('Israel')),
        ('IT', _('Italy')),
        ('JM', _('Jamaica')),
        ('JP', _('Japan')),
        ('JE', _('Jersey')),
        ('JO', _('Jordan')),
        ('KZ', _('Kazakhstan')),
        ('KE', _('Kenya')),
        ('KI', _('Kiribati')),
        ('KP', _('Korea, Democratic People\'s Republic of')),
        ('KR', _('Korea, Republic of')),
        ('KW', _('Kuwait')),
        ('KG', _('Kyrgyzstan')),
        ('LA', _('Lao People\'s Democratic Republic')),
        ('LV', _('Latvia')),
        ('LB', _('Lebanon')),
        ('LS', _('Lesotho')),
        ('LR', _('Liberia')),
        ('LY', _('Libyan Arab Jamahiriya')),
        ('LI', _('Liechtenstein')),
        ('LT', _('Lithuania')),
        ('LU', _('Luxembourg')),
        ('MO', _('Macao')),
        ('MK', _('Macedonia, The Former Yugoslav Republic of')),
        ('MG', _('Madagascar')),
        ('MW', _('Malawi')),
        ('MY', _('Malaysia')),
        ('MV', _('Maldives')),
        ('ML', _('Mali')),
        ('MT', _('Malta')),
        ('MH', _('Marshall Islands')),
        ('MQ', _('Martinique')),
        ('MR', _('Mauritania')),
        ('MU', _('Mauritius')),
        ('YT', _('Mayotte')),
        ('MX', _('Mexico')),
        ('FM', _('Micronesia, Federated States of')),
        ('MD', _('Moldova')),
        ('MC', _('Monaco')),
        ('MN', _('Mongolia')),
        ('ME', _('Montenegro')),
        ('MS', _('Montserrat')),
        ('MA', _('Morocco')),
        ('MZ', _('Mozambique')),
        ('MM', _('Myanmar')),
        ('NA', _('Namibia')),
        ('NR', _('Nauru')),
        ('NP', _('Nepal')),
        ('NL', _('Netherlands')),
        ('AN', _('Netherlands Antilles')),
        ('NC', _('New Caledonia')),
        ('NZ', _('New Zealand')),
        ('NI', _('Nicaragua')),
        ('NE', _('Niger')),
        ('NG', _('Nigeria')),
        ('NU', _('Niue')),
        ('NF', _('Norfolk Island')),
        ('MP', _('Northern Mariana Islands')),
        ('NO', _('Norway')),
        ('OM', _('Oman')),
        ('PK', _('Pakistan')),
        ('PW', _('Palau')),
        ('PS', _('Palestinian Territory, Occupied')),
        ('PA', _('Panama')),
        ('PG', _('Papua New Guinea')),
        ('PY', _('Paraguay')),
        ('PE', _('Peru')),
        ('PH', _('Philippines')),
        ('PN', _('Pitcairn')),
        ('PL', _('Poland')),
        ('PT', _('Portugal')),
        ('PR', _('Puerto Rico')),
        ('QA', _('Qatar')),
        ('RE', _('Reunion')),
        ('RO', _('Romania')),
        ('RU', _('Russian Federation')),
        ('RW', _('Rwanda')),
        ('BL', _('Saint Barthelemy')),
        ('SH', _('Saint Helena')),
        ('KN', _('Saint Kitts and Nevis')),
        ('LC', _('Saint Lucia')),
        ('MF', _('Saint Martin')),
        ('PM', _('Saint Pierre and Miquelon')),
        ('VC', _('Saint Vincent and the Grenadines')),
        ('WS', _('Samoa')),
        ('SM', _('San Marino')),
        ('ST', _('Sao Tome and Principe')),
        ('SA', _('Saudi Arabia')),
        ('SN', _('Senegal')),
        ('RS', _('Serbia')),
        ('SC', _('Seychelles')),
        ('SL', _('Sierra Leone')),
        ('SG', _('Singapore')),
        ('SK', _('Slovakia')),
        ('SI', _('Slovenia')),
        ('SB', _('Solomon Islands')),
        ('SO', _('Somalia')),
        ('ZA', _('South Africa')),
        ('GS', _('South Georgia and the South Sandwich Islands')),
        ('ES', _('Spain')),
        ('LK', _('Sri Lanka')),
        ('SD', _('Sudan')),
        ('SR', _('Suriname')),
        ('SJ', _('Svalbard and Jan Mayen')),
        ('SZ', _('Swaziland')),
        ('SE', _('Sweden')),
        ('CH', _('Switzerland')),
        ('SY', _('Syrian Arab Republic')),
        ('TW', _('Taiwan, Province of China')),
        ('TJ', _('Tajikistan')),
        ('TZ', _('Tanzania, United Republic of')),
        ('TH', _('Thailand')),
        ('TL', _('Timor-Leste')),
        ('TG', _('Togo')),
        ('TK', _('Tokelau')),
        ('TO', _('Tonga')),
        ('TT', _('Trinidad and Tobago')),
        ('TN', _('Tunisia')),
        ('TR', _('Turkey')),
        ('TM', _('Turkmenistan')),
        ('TC', _('Turks and Caicos Islands')),
        ('TV', _('Tuvalu')),
        ('UG', _('Uganda')),
        ('UA', _('Ukraine')),
        ('AE', _('United Arab Emirates')),
        ('US', _('United States')),
        ('UM', _('United States Minor Outlying Islands')),
        ('UY', _('Uruguay')),
        ('UZ', _('Uzbekistan')),
        ('VU', _('Vanuatu')),
        ('VE', _('Venezuela')),
        ('VN', _('Viet Nam')),
        ('VG', _('Virgin Islands, British')),
        ('VI', _('Virgin Islands, U.S.')),
        ('WF', _('Wallis and Futuna')),
        ('EH', _('Western Sahara')),
        ('YE', _('Yemen')),
        ('ZM', _('Zambia')),
        ('ZW', _('Zimbabwe')),
    )

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('max_length', 2)
        kwargs.setdefault('choices', self.COUNTRIES)

        super(CountryField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return "CharField"


class PhoneField(models.CharField):
    """

    """

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 40
        super(PhoneField, self).__init__(*args, **kwargs)
        # is_digits()


class ConfiguredAutoSlugField(AutoSlugField):
    """

    """

    def __init__(self, *args, **kwargs):

        kwargs['verbose_name'] = _('Slug')
        kwargs['max_length'] = kwargs.get('max_length', 300)
        kwargs['blank'] = True
        kwargs['editable'] = True
        kwargs['always_update'] = True
        kwargs['db_index'] = True
        kwargs['allow_unicode'] = True
        kwargs['help_text'] = _('Slug will be generate automaticaly, on based main field.')

        super(ConfiguredAutoSlugField, self).__init__(*args, **kwargs)
        # replace SlugValidator and SlugUnicodeValidator
        self.validators[0] = validate_unicode_slug


class YearField(models.IntegerField):

    description = _("Year ")

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = ''
        kwargs['max_length'] = 4
        super(YearField, self).__init__(*args, **kwargs)


class YearsLifeField:

    pass


class MarkupField(models.CharField):

    description = _('Pretty markup field')

    MARKDOWN = 'markdown'
    TEXTILE = 'texttile'
    ReST = 'restructuredtext'

    MARKUP_CHOICES = (
        (MARKDOWN, _('Markdown')),
        (TEXTILE, _('Textile')),
        (ReST, _('reStructuredText')),
    )

    def __init__(self, *args, **kwargs):

        kwargs['verbose_name'] = _('Markup')
        kwargs['max_length'] = 20
        kwargs['choices'] = self.MARKUP_CHOICES
        kwargs['default'] = self.MARKDOWN

        self.fill_from = kwargs.pop('fill_from', None)
        self.fill_to = kwargs.pop('fill_to', None)

        super().__init__(*args, **kwargs)

    def deconstruct(self):

        name, path, args, kwargs = super().deconstruct()

        del kwargs['verbose_name']
        del kwargs['max_length']
        del kwargs['choices']
        del kwargs['default']

        return name, path, args, kwargs

    def pre_save(self, model_instance, add):

        content = getattr(model_instance, self.fill_from)

        selected_markup = getattr(model_instance, self.attname)

        if selected_markup == self.MARKDOWN:
            content_html = markdown.markdown(content)
        elif selected_markup == self.TEXTILE:
            content_html = textile.textile(content)
        elif selected_markup == self.ReST:
            content_html = self.convert_to_ReST(content)

        setattr(model_instance, self.fill_to, content_html)

        return super().pre_save(model_instance, add)

    @staticmethod
    def convert_to_ReST(content):
        """ """

        return publish_parts(source=content, writer_name='html')['fragment']


class AutoOneToOneField(models.OneToOneField):
    """ """

    related_accessor_class = ReverseOneToOneDescriptorWithAutoCreate


class ColorField(models.CharField):
    """
    Three widgets:
        HTML5 input color - OK
        jQuery Color Picker
        http://jscolor.com/
    Types=['rgb', 'hex', 'name']
    """

    description = _('ColorField for the Django')

    def __init__(self, *args, **kwargs):

        kwargs['max_length'] = 30

        super(ColorField, self).__init__(*args, **kwargs)

    def deconstruct(self):

        name, path, args, kwargs = super(ColorField, self).deconstruct()

        del kwargs['max_length']

        return name, path, args, kwargs

    def formfield(self, form_class=None, choices_form_class=None, **kwargs):

        kwargs['widget'] = ColorInput()

        return super().formfield(form_class=None, choices_form_class=None, **kwargs)

    def clean(self, value, model_instance):
        """
        Convert the value's type and run validation. Validation errors
        from to_python and validate are propagated. The correct value is
        returned if no error is raised.
        """
        value = self.to_python(value)

        if self.unique:
            value = value.upper()

        self.validate(value, model_instance)
        self.run_validators(value)
        # import ipdb; ipdb.set_trace()
        return value


class FixedCharField(models.CharField):

    description = 'CharField with fixed text'

    def __init__(self, *args, **kwargs):
        self.startswith = kwargs.pop('startswith', '')
        super(FixedCharField, self).__init__(*args, **kwargs)

    def check(self, **kwargs):
        errors = super(FixedCharField, self).check(**kwargs)
        errors.extend(self._check_startswith_attribute(**kwargs))
        return errors

    def _check_startswith_attribute(self, **kwargs):
        if self.startswith is None or self.startswith == '':
            return [
                checks.Error(
                    "FixedCharField must define a 'startswith' attribute.",
                    obj=self,
                    id='fields.E120',
                )
            ]
        else:
            return []

    def deconstruct(self):

        name, path, args, kwargs = super(FixedCharField, self).deconstruct()
        kwargs.pop('startswith', None)
        return name, path, args, kwargs

    def formfield(self, **kwargs):

        defaults = {
            'form_class': CharFieldFixed,
            'modelfield': self,
        }
        defaults.update(kwargs)
        return super(FixedCharField, self).formfield(**defaults)
