
import datetime

from autoslug import AutoSlugField

from django import forms
from django.utils.text import capfirst
from django.core.exceptions import ValidationError
from django.core.validators import validate_unicode_slug
from django.db.models import NullBooleanField
from django.utils.translation import ugettext as _
from django.db import models

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
        kwargs['max_length'] = kwargs.get('max_length', 200)
        kwargs['editable'] = True
        kwargs['blank'] = True
        kwargs['always_update'] = True
        kwargs['db_index'] = True
        kwargs['allow_unicode'] = True
        super(ConfiguredAutoSlugField, self).__init__(*args, **kwargs)
        # replace SlugValidator and SlugUnicodeValidator
        self.validators[0] = validate_unicode_slug


class YearField(models.IntegerField):
    description = _("Year ")

    def get_internal_type(self):
        return "SmallIntegerField"

    def formfield(self, **kwargs):
        defaults = {'min_value': datetime.datetime.now().year}
        defaults = {'max_value': datetime.datetime.now().year}
        defaults.update(kwargs)
        # defaults = {'min_value': 1900}
        # defaults = {'min_value': 2000}
        # defaults.update(kwargs)
        return super(YearField, self).formfield(**defaults)


class NullTrueField(NullBooleanField):
    pass
    # empty_strings_allowed = False
    # default_error_messages = {
    #     'invalid': _("'%(value)s' value must be either None, True or False."),
    # }
    # description = _("Boolean (Either True, False or None)")

    # def __init__(self, *args, **kwargs):
    #     kwargs['null'] = True
    #     kwargs['blank'] = True
    #     super(NullTrueField, self).__init__(*args, **kwargs)

    # def deconstruct(self):
    #     name, path, args, kwargs = super(NullTrueField, self).deconstruct()
    #     del kwargs['null']
    #     del kwargs['blank']
    #     return name, path, args, kwargs

    # def get_internal_type(self):
    #     return "NullTrueField"

    # def to_python(self, value):
    #     if value is None:
    #         return None
    #     if value in (True, False):
    #         return bool(value)
    #     if value in ('None',):
    #         return None
    #     if value in ('t', 'True', '1'):
    #         return True
    #     if value in ('f', 'False', '0'):
    #         return False
    #     raise ValidationError(
    #         self.error_messages['invalid'],
    #         code='invalid',
    #         params={'value': value},
    #     )

    # def get_prep_lookup(self, lookup_type, value):
    #     # Special-case handling for filters coming from a Web request (e.g. the
    #     # admin interface). Only works for scalar values (not lists). If you're
    #     # passing in a list, you might as well make things the right type when
    #     # constructing the list.
    #     if value in ('1', '0'):
    #         value = bool(int(value))
    #     return super(NullTrueField, self).get_prep_lookup(lookup_type, value)

    # def get_prep_value(self, value):
    #     value = super(NullTrueField, self).get_prep_value(value)
    #     if value is None:
    #         return None
    #     return bool(value)

    # def formfield(self, **kwargs):
    #     defaults = {
    #         'form_class': forms.NullTrueField,
    #         'required': not self.blank,
    #         'label': capfirst(self.verbose_name),
    #         'help_text': self.help_text}
    #     defaults.update(kwargs)
    #     return super(NullTrueField, self).formfield(**defaults)
