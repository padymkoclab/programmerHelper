
from django.utils.translation import ugettext_lazy as _
from django import forms

from apps.tags.forms import clean_tags

from .models import Article, settings


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ('title', 'account')

    def clean_tags(self):
        super(ArticleForm, self).clean()
        cleaned_tags = clean_tags(self)
        return cleaned_tags

    def clean_links(self):
        links = self.cleaned_data.get('links', tuple())
        if len(links) > settings.MAX_COUNT_WEBLINKS_ON_OBJECT:
            self.add_error('links', _('Count links must be not more than {0}'.format(
                settings.MAX_COUNT_WEBLINKS_ON_OBJECT
            )))
