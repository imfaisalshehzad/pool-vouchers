from rest_framework import serializers

from pool.models import Voucher, Customer


class VoucherSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(read_only=True, source='customer.name')
    customer_email = serializers.CharField(read_only=True, source='customer.email')
    special_offer_name = serializers.CharField(read_only=True, source='special_offer.name')
    special_offer_discount = serializers.CharField(read_only=True, source='special_offer.discount')

    class Meta:
        model = Voucher
        fields = (
            'code',
            'customer',
            'customer_email',
            'expiration_date',
            'is_code_used',
            'special_offer_name',
            'special_offer_discount',
            'created_at',
            'updated_at',
        )


class ValidCustomerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = Customer
        fields = ('email',)


class ValidVoucherSerializer(serializers.ModelSerializer):
    code = serializers.CharField(min_length=8)
    email = serializers.EmailField()

    class Meta:
        model = Voucher
        fields = ('code', 'email',)


class VoucherDiscountSerializer(serializers.ModelSerializer):
    offer_name = serializers.CharField(source='special_offer.name')
    percentage_discount = serializers.CharField(source='special_offer.discount')

    class Meta:
        model = Voucher
        fields = ('percentage_discount', 'offer_name',)


class GenerateVoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = (
            'expiration_date',
            'special_offer',
        )
