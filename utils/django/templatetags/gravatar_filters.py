
import hashlib
import urllib
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def gravatar_url(email, size=40):
    """
    return only the URL of the gravatar
    TEMPLATE USE:  {{ email|gravatar_url:150 }}
    """

    # if problems with display image
    # use image in "identicon" style
    default = "identicon"

    # size image
    size = size

    # rating is 'g.' (suitable for display on all websites with any audience type)
    # By default, only 'G' rated images are displayed unless you indicate that you would like to see higher ratings
    rating = 'g'

    # get hash by email
    email = email.lower().encode()
    hash_email = hashlib.md5(email).hexdigest()

    # set up size, default image and rating
    attrs = urllib.parse.urlencode({
        'd': default,
        's': str(size),
        'r': rating,
    })

    # return full URL
    return 'https://www.gravatar.com/avatar/{}?{}'.format(hash_email, attrs)


@register.filter
def gravatar(email, size=40):
    """
    return an image tag with the gravatar
    TEMPLATE USE:  {{ email|gravatar:150 }}
    """

    full_url = gravatar_url(email, size)
    return mark_safe('<img src="{}" height="{}" width="{}">'.format(full_url, size, size))
