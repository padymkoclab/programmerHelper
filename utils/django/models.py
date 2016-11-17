
import collections
import uuid

# from django.utils import timezone
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class UUIDable(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Timestampable(models.Model):
    """
    Abstract base models with two fields: created and updated. And too supported localization.
    """

    updated = models.DateTimeField(_('date modified'), auto_now=True, db_index=True)
    created = models.DateTimeField(_('date added'), auto_now_add=True, db_index=True)

    class Meta:
        abstract = True

    # def is_new(self):
    #     return self.created > \
    #         timezone.now() - timezone.timedelta(
    #             days=settings.COUNT_DAYS_FOR_NEW_ELEMENTS
    #         )
    # is_new.admin_order_field = 'created'
    # is_new.short_description = _('is new?')
    # is_new.boolean = True


class GenericRelatable(models.Model):

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name=_('type object'))
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True


class Moderatable(models.Model):
    """

    """

    approved = models.BooleanField(_('approved'), default=False)

    class Meta:
        abstract = True


class Orderable(models.Model):
    """

    """

    position = models.PositiveSmallIntegerField(_('position'), unique=True)

    class Meta:
        abstract = True


class Scheduleable(models.Model):
    """

    """

    started = models.DateTimeField(_('started'))
    ended = models.DateTimeField(_('ended'))

    class Meta:
        abstract = True


class Permalinkable(models.Model):
    """

    """

    slug = models.SlugField(_('slug'))

    class Meta:
        abstract = True


class Userable(models.Model):
    """

    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, verbose_name=_('user'))

    class Meta:
        abstract = True


class Publishable(models.Model):
    """

    """

    PUBLISHED = 'published'
    DRAFT = 'draft'
    STATUS_CHOICES = (
        (PUBLISHED, _('Published')),
        (DRAFT, _('Draft')),
    )

    status = models.CharField(_('status'), choices=STATUS_CHOICES, max_length=10)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, verbose_name=_('user'))

    class Meta:
        abstract = True


class Viewable(models.Model):
    """

    """

    count_views = models.PositiveIntegerField(_('count views'), default=0, editable=False, db_index=True)

    class Meta:
        abstract = True


class Commentable(models.Model):
    """

    """

    comments_is_allowed = models.BooleanField(_('comments is allowed'), default=True)

    class Meta:
        abstract = True


class Creatable(models.Model):
    """

    """

    created = models.DateTimeField(_('created'), auto_now_add=True, db_index=True)

    class Meta:
        abstract = True


class Updateable(models.Model):
    """

    """

    updated = models.DateTimeField(_('updated'), auto_now=True)

    class Meta:
        abstract = True


class TimeFrameable(models.Model):
    """

    """

    start = models.DateTimeField(_('start'), null=True, blank=True)
    end = models.DateTimeField(_('end'), null=True, blank=True)


class OverrrideUniqueTogetherErrorMessages(object):
    """
    Always must first inheriotanced meta-class:
        class Opinion(OverrrideUniqueTogetherErrorMessages, GenericRelatable, Timestampable, UUIDable):
    """

    UNIQUE_TOGETHER_ERROR_MESSAGES = None

    def __init__(self, *args, **kwargs):
        super(OverrrideUniqueTogetherErrorMessages, self).__init__(*args, **kwargs)

        if self.UNIQUE_TOGETHER_ERROR_MESSAGES is None:
            raise ValueError('Override UNIQUE_TOGETHER_ERROR_MESSAGES')

        count_restrictions = len(self._meta.unique_together)
        if count_restrictions == 0:
            raise AttributeError('Meta-attribute "unique_together" is empty')

        if not isinstance(self.UNIQUE_TOGETHER_ERROR_MESSAGES, dict):
            if isinstance(self._meta.unique_together[0], (list, tuple)):
                if count_restrictions > 1:
                    raise ValueError(
                        "Overrided UNIQUE_TOGETHER_ERROR_MESSAGES for single restriction,"
                        " but 'unique_together' contains several restrictions"
                    )
                first_restriction = self._meta.unique_together[0]
            else:
                first_restriction = self._meta.unique_together

            self.UNIQUE_TOGETHER_ERROR_MESSAGES = {
                first_restriction: self.UNIQUE_TOGETHER_ERROR_MESSAGES
            }

    class Meta:
        abstract = True

    def unique_error_message(self, model_class, unique_check):

        if type(self) == model_class and unique_check:
            return self.UNIQUE_TOGETHER_ERROR_MESSAGES[unique_check]
        return super(OverrrideUniqueTogetherErrorMessages, self).unique_error_message(model_class, unique_check)


class IsChangedInstanceModelMixin(models.Model):
    """
    Mixin to a model for tracing changes from previous status on determined or all fields.
    Ignore date/datetime fields with attribute auto_now=True, since it field will be changed in any case.
    Does not support for M2M fields and fields to the ContentType`s model.
    """

    FIELDS_FOR_TRACING = ()

    class Meta:
        abstract = True

    @classmethod
    def from_db(cls, db, field_names, values):
        """ """

        # check up a type of attribute
        if not isinstance(cls.FIELDS_FOR_TRACING, (tuple, list)):
            raise ValueError('Attribute "FIELDS_FOR_TRACING" must list or tuple')

        # check up fieldnames passed to tracing
        concrete_fieldnames = [field.name for field in cls._meta.concrete_fields]
        non_exists_fieldnames = list()
        for fieldname in cls.FIELDS_FOR_TRACING:
            if fieldname not in concrete_fieldnames:
                non_exists_fieldnames.append(fieldname)
        if non_exists_fieldnames:
            raise ValueError('Unknown fields for trace: {}'.format(','.join(non_exists_fieldnames)))

        # get a instance from a db
        instance = super(IsChangedInstanceModelMixin, cls).from_db(db, field_names, values)

        # get values of fields of the instance
        fields_values = dict(zip(field_names, values))

        # drop unnecessary fields if need tracing for concrete fields
        if cls.FIELDS_FOR_TRACING:
            instance._original_values_fields = {
                k: v for k, v in fields_values.items() if k in cls.FIELDS_FOR_TRACING
            }
        else:
            instance._original_values_fields = fields_values

        return instance

    def is_changed(self) -> bool:
        """Check up if values of fields for tracing was changed."""

        for fieldname, value in self._original_values_fields.items():

            # ignore a field with auto_now=True
            field = self._meta.get_field(fieldname)
            if isinstance(field, (models.DateField, models.DateTimeField)):
                if field.auto_now is True:
                    continue

            if getattr(self, fieldname) != value:
                return True
        return False

    def get_changed_fields(self) -> dict:
        """Get fields where was changes with an original value and current."""

        changed_fields = dict()
        for fieldname, original_value in self._original_values_fields.items():

            # ignore a field with auto_now=True
            field = self._meta.get_field(fieldname)
            if isinstance(field, (models.DateField, models.DateTimeField)):
                if field.auto_now is True:
                    continue

            current_value = getattr(self, fieldname)
            if current_value != original_value:
                changed_fields[fieldname] = (original_value, current_value)

        return changed_fields

    def save(self, *args, **kwargs):

        i = super(IsChangedInstanceModelMixin, self).save(*args, **kwargs)
        import ipdb; ipdb.set_trace()
        self._original_values_fields = 1
