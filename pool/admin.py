import shortuuid
from django.contrib import admin, messages
from django.shortcuts import render
from django_object_actions import DjangoObjectActions

from pool.form import GenerateVoucherForm
from pool.models import Voucher, Customer, SpecialOffer


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email',)


class SpecialOfferAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount',)


class VoucherAdmin(DjangoObjectActions, admin.ModelAdmin):
    list_display = ['code', 'customer_name', 'customer_email', 'special_offer', 'expiration_date', 'is_code_used', ]
    search_fields = ['customer__email', ]
    changelist_actions = ['set_generate_voucher_action']

    def customer_name(self, obj):
        return f"{obj.customer.name}"

    def customer_email(self, obj):
        return f"{obj.customer.email}"

    def set_generate_voucher_action(self, request, queryset):
        if 'do_action' in request.POST:
            form = GenerateVoucherForm(request.POST)
            if form.is_valid():
                special_offer = form.cleaned_data['offers']
                expiry_date = form.cleaned_data['expiry_date']
                customers = Customer.objects.all()
                bulk_list = list()
                for instance in range(len(customers)):
                    bulk_list.append(Voucher(
                        code=shortuuid.ShortUUID().random(length=8).upper(),
                        customer=customers[instance],
                        special_offer=special_offer,
                        expiration_date=expiry_date,
                    ))
                items = Voucher.objects.bulk_create(bulk_list)
                messages.success(request, '{0} vouchers were added'.format(len(items)))
                return
        else:
            form = GenerateVoucherForm()

        return render(request, 'admin/form_generate_vouchers.html',
                      {
                          'title': u'Select Special Offer',
                          'objects': queryset,
                          'form': form
                      })

    set_generate_voucher_action.label = u'Generate Vouchers'
    set_generate_voucher_action.short_description = u'Generate Vouchers'


admin.site.register(Voucher, VoucherAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(SpecialOffer, SpecialOfferAdmin)
