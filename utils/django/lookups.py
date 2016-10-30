
from django.db import models


@models.fields.Field.register_lookup
class NotEqualLookup(models.Lookup):
    """

    Not exact value.
    May used for any type of field.

    Register:
        in file apps.core.apps.CoreConfig.ready() import this object

    Usage:
        User.objects.filter(alias__nexact='Admin')

    """

    lookup_name = 'nexact'

    def as_sql(self, compiler, connection):

        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)

        params = lhs_params + rhs_params
        return '%s <> %s' % (lhs, rhs), params
