
from django.db.models.fields.related import ReverseOneToOneDescriptor


class ReverseOneToOneDescriptorWithAutoCreate(ReverseOneToOneDescriptor):
    """
    The descriptor that handles the object creation for an AutoOneToOneField.
    """

    def __get__(self, instance, instance_type=None):

        model = getattr(self.related, 'related_model', self.related.model)

        try:
            return super().__get__(instance, instance_type)
        except model.DoesNotExist:
            # Using get_or_create instead() of save() or create() as it better handles race conditions
            model.objects.get_or_create(**{self.related.field.name: instance})

            # Don't return obj directly, otherwise it won't be added
            # to Django's cache, and the first 2 calls to obj.relobj
            # will return 2 different in-memory objects
            return super().__get__(instance, instance_type)
