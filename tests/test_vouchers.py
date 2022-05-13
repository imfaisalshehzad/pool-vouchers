import random
from datetime import timedelta

import shortuuid
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from pool.models import Customer, SpecialOffer, Voucher


class Tests(APITestCase):
    def setUp(self) -> None:
        super().setUp()
        self.customer = Customer.objects.create(name='faisal', email='faisal@example.com')
        self.offer = SpecialOffer.objects.create(name='MEGASALE50', discount=50)
        self.voucher = Voucher.objects.create(
            code=shortuuid.ShortUUID().random(length=8).upper(),
            customer=self.customer,
            special_offer=self.offer,
            expiration_date=timezone.now() + timedelta(1),
        )
        self.customer.save()
        self.offer.save()

    def test_special_offer(self):
        my_list = [1, 2, 3, 4, 5, 6]
        rand_num = random.choice(my_list)
        data = {
            'name': shortuuid.ShortUUID().random(length=8).upper(),
            'discount': rand_num,
        }
        response = self.client.post(reverse('pool_api:generate-offers'), data=data)
        # import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_email_return_all_valid_voucher_codes(self):
        data = {
            'email': self.customer.email,
        }
        response = self.client.post(reverse('pool_api:email-return-voucher-codes'), data=data)
        # import pdb; pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_generate_voucher_code_foreach_customer(self):
        data = {
            'expiration_date': timezone.now() + timedelta(1),
            'special_offer': self.offer.pk,
        }
        response = self.client.post(reverse('pool_api:generate-voucher'), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_validates_the_voucher_code(self):
        data = {
            'code': self.offer.name,
            'email': 'mix_'+self.customer.email,
        }
        response = self.client.post(reverse('pool_api:verify-voucher'), data=data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
