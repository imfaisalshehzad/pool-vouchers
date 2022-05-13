import random

from django.core.management.base import BaseCommand
from django.db import transaction

from pool.factories import CustomerFactory, SpecialOfferFactory, VoucherFactory
from pool.models import Customer, SpecialOffer, Voucher

NUM_CUSTOMERS = 2
NUM_OFFERS = 2
NUM_VOUCHERS = NUM_CUSTOMERS * NUM_OFFERS


class Command(BaseCommand):
    help = 'generate test data'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Deleting old data...")
        models = [Customer, SpecialOffer, Voucher]
        for m in models:
            m.objects.all().delete()

        self.stdout.write("Creating new data...")

        # Create all the users
        people = []
        for _ in range(NUM_CUSTOMERS):
            person = CustomerFactory()
            people.append(person)

        # Add some users to clubs
        offers = []
        for _ in range(NUM_OFFERS):
            offer = SpecialOfferFactory()
            offers.append(offer)

        vouchers = []
        for _ in range(NUM_CUSTOMERS):
            customer = random.choice(people)
            offer = random.choice(offers)
            voucher = VoucherFactory(customer=customer, special_offer=offer)
            vouchers.append(voucher)
