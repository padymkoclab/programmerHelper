
import factory
from factory import fuzzy


class Factory_ScopeGeneric(factory.DjangoModelFactory):

    class Meta:
        model = ScopeGeneric

    @factory.lazy_attribute
    def scope(self):
        return random.randint(ScopeGeneric.MIN_SCOPE, ScopeGeneric.MAX_SCOPE)

    @factory.lazy_attribute
    def user(self):
        instance = ScopeGeneric(content_object=self.content_object, scope=self.scope)
        return get_unique_user(instance)
