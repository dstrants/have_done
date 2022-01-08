import faker_microservice
import pendulum

from factory import Faker
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyDateTime, FuzzyText, FuzzyChoice


Faker.add_provider(faker_microservice.Provider)


class BackupFactory(DjangoModelFactory):
    class Meta:
        model = 'logs.Backup'
        django_get_or_create = ('app', 'server', 'created_at')

    app = str(Faker('microservice'))[:19]
    server = 'localhost'
    created_at = FuzzyDateTime(start_dt=pendulum.now().subtract(months=1))
    server = FuzzyText(prefix="server_")
    status = FuzzyChoice((True, False))
    log = Faker('image_url')
