from factory import SubFactory
from factory.django import DjangoModelFactory, ImageField
from factory.fuzzy import FuzzyChoice, FuzzyText

from factories.user import UserFactory


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = 'profiles.Profile'
        django_get_or_create = ('user',)

    user = SubFactory(UserFactory)
    avatar = ImageField(color='blue')


class ProfileSettingFactory(DjangoModelFactory):
    class Meta:
        model = 'profiles.ProfileSetting'
        django_get_or_create = ('profile',)

    todoist = FuzzyChoice(choices=(False, True))
    gmail = FuzzyChoice(choices=(False, True))
    gcalendar = FuzzyChoice(choices=(False, True))
    gh_pr = FuzzyChoice(choices=(False, True))
    uptime_robot = FuzzyChoice(choices=(False, True))
    profile = SubFactory(ProfileFactory)


class NotificationFactory(DjangoModelFactory):
    class Meta:
        model = 'profiles.Notification'
        django_get_or_create = ('text',)

    profile = SubFactory(ProfileFactory)
    text = FuzzyText(length=50)

    # Read is not included so that it can its default value can be tested.
    # These will be changed to choices when mode kinds are introduced.
    kind = 'default'
    link = '/prod/defaults'
