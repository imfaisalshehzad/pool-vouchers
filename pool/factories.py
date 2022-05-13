import datetime

import factory
from dateutil.tz import UTC
from factory.django import DjangoModelFactory

from .models import Customer, SpecialOffer, Voucher


class CustomerFactory(DjangoModelFactory):
    class Meta:
        model = Customer

    name = factory.Faker('name')
    email = factory.Faker('email')


class SpecialOfferFactory(DjangoModelFactory):
    class Meta:
        model = SpecialOffer

    name = factory.Faker('password', length=6, special_chars=False, digits=True, upper_case=True, lower_case=False)
    discount = factory.Faker('random_int', min=10, max=90)


class VoucherFactory(DjangoModelFactory):
    class Meta:
        model = Voucher

    code = factory.Faker('password', length=8, special_chars=False, digits=True, upper_case=True, lower_case=False)
    customer = factory.SubFactory(CustomerFactory)
    special_offer = factory.SubFactory(SpecialOfferFactory)
    expiration_date = factory.Faker('date_time_between', start_date=datetime.datetime(2022, 5, 1, tzinfo=UTC),
                                    end_date=datetime.datetime(2022, 12, 30, tzinfo=UTC), tzinfo=UTC)
