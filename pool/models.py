from django.core.validators import MinLengthValidator
from django.db import models


# Create your models here.

class Customer(models.Model):
    name = models.CharField(blank=False, null=False, max_length=255)
    email = models.EmailField(unique=True, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"


class SpecialOffer(models.Model):
    name = models.CharField(blank=False, null=False, max_length=255)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"


class Voucher(models.Model):
    code = models.CharField(unique=True, max_length=10, null=False, blank=False, validators=[MinLengthValidator(8)])
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    special_offer = models.ForeignKey(SpecialOffer, on_delete=models.CASCADE)
    expiration_date = models.DateTimeField(null=False, blank=False)
    is_code_used = models.DateTimeField(null=True, blank=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code}"
