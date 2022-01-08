from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText


from django.contrib.auth.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = FuzzyText(prefix='user')
    is_superuser = False
    is_staff = False
    is_active = True


class SuperUser(UserFactory):
    is_superuser = True


class StaffUser(UserFactory):
    is_staff = True


class AdminUser(SuperUser, StaffUser):
    pass
