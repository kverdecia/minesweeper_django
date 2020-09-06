import factory
import factory.fuzzy

from django.contrib.auth import get_user_model

from .. import models


User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.fuzzy.FuzzyText()

    class Meta:
        model = User


class BoardModelFactory(factory.django.DjangoModelFactory):
    rows = factory.fuzzy.FuzzyInteger(20, 40)
    columns = factory.fuzzy.FuzzyInteger(20, 40)
    mines = factory.fuzzy.FuzzyInteger(40, 60)
    user = factory.lazy_attribute(lambda obj: UserFactory())

    class Meta:
        model = models.Board
