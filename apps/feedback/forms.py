
from django import forms


class Feedback(forms.Form):
    """

    """

    user_email = forms.EmailField(_('Your email'))
    user_name = forms.CharField(_('Your name'), max_length=100)
    title = forms.CharField(_('Title'))
    message = forms.CharField(_('Message'))

