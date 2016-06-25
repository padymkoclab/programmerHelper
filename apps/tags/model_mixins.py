

class RelatedObjectsByTags(object):
    """
    Model mixin adding addional method for each instance model.
    """

    def _get_pks_related_objects_by_tags(self):
        """Private method, for getting all a primary keys by each tag passwed object."""

        #
        pks_related_snippets_by_tags = list()
        model = self._meta.model
        #
        for tag in self.tags.iterator():
            pks_snippets = model.objects.exclude(pk=self.pk).filter(tags=tag).values_list('pk', flat=True)
            pks_related_snippets_by_tags.extend(pks_snippets)
        return pks_related_snippets_by_tags
