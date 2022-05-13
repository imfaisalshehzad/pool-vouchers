import shortuuid

from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone

from pool.models import Voucher, Customer
from .serializers import VoucherSerializer, ValidCustomerSerializer, ValidVoucherSerializer, VoucherDiscountSerializer, \
    GenerateVoucherSerializer


class VoucherAPIView(APIView):
    serializer_class = ValidCustomerSerializer

    @extend_schema(
        methods=['GET'],
        summary="Get all Vouchers",
        description="Get all Vouchers",
    )
    def get(self, request, *args, **kwargs):
        queryset = Voucher.objects.all()
        serializer = VoucherSerializer(queryset, many=True)
        return Response({"vouchers": serializer.data})

    @extend_schema(
        methods=['POST'],
        summary="For a given Email return all its valid Voucher Codes with the Name of the Special Offer",
        description="For a given Email return all its valid Voucher Codes with the Name of the Special Offer",
    )
    def post(self, request):
        serializer = ValidCustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        get_object_or_404(Customer, email=email)

        queryset = Voucher.objects.filter(
            customer__email=email,
            # expiration_date__gte=timezone.now(),
            is_code_used__isnull=True
        )

        serializer = VoucherSerializer(queryset, many=True)
        return Response({'vouchers': serializer.data}, status=status.HTTP_200_OK)


class VoucherValidationAPIView(APIView):
    serializer_class = ValidVoucherSerializer

    @extend_schema(
        methods=['POST'],
        summary="Verify Voucher Code",
        description="Provide an endpoint, reachable via HTTP,"
                    " which receives a Voucher Code and Email and validates the Voucher Code."
                    " In Case it is valid, return the Percentage Discount and set the date of usage",
    )
    def post(self, request):
        body = ValidVoucherSerializer(data=request.data)
        body.is_valid(raise_exception=True)
        instance = get_object_or_404(Voucher,
                                     code=body.validated_data['code'],
                                     customer__email=body.validated_data['email']
                                     )

        if instance.expiration_date < timezone.now():
            return Response({
                'message': 'Voucher Code is Expired'
            }, status=status.HTTP_400_BAD_REQUEST)

        if instance.is_code_used is None:
            instance.is_code_used = timezone.now()
            instance.save()
        else:
            return Response({
                'message': 'Voucher Code has been consumed already.'
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = VoucherDiscountSerializer(instance=instance)

        return Response({
            'vouchers': serializer.data
        }, status=status.HTTP_200_OK)


class GenerateVoucherAPIView(APIView):
    serializer_class = GenerateVoucherSerializer

    @extend_schema(
        methods=['POST'],
        summary="Generate Voucher Code for each customer",
        description="Generate Voucher Code for each customer for a given Special Offer and expiration data",
    )
    def post(self, request):
        body = GenerateVoucherSerializer(data=request.data)
        body.is_valid(raise_exception=True)
        expiry_date = body.validated_data['expiration_date']
        special_offer = body.validated_data['special_offer']
        customers = Customer.objects.all()
        bulk_list = list()
        for instance in range(len(customers)):
            bulk_list.append(Voucher(
                code=shortuuid.ShortUUID().random(length=8).upper(),
                customer=customers[instance],
                special_offer=special_offer,
                expiration_date=expiry_date,
            ))

        if bulk_list is None:
            return Response({
                'message': 'no email found'
            }, status=status.HTTP_404_NOT_FOUND)

        items = Voucher.objects.bulk_create(bulk_list)
        serializer = VoucherSerializer(items, many=True)
        return Response({
            'vouchers': serializer.data
        }, status=status.HTTP_201_CREATED)
