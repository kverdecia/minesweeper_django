import factory
import factory.fuzzy

from django.contrib.auth import get_user_model


User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.fuzzy.FuzzyText()

    class Meta:
        model = User
