from django.contrib import admin
from django import forms
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from flower_shop.models import (
    Bouquet,
    Occasion,
    ConsultingStatus,
    Consulting,
    Order,
    PaymentType,
    DeliveryInterval, ConsultingStatusHistory,
)


class ConsultingForm(forms.ModelForm):
    class Meta:
        widgets = {
            'contact_phone': PhoneNumberPrefixWidget(initial='RU'),
        }


class ConsultingStatusInline(admin.TabularInline):
    model = ConsultingStatusHistory
    extra = 1
    readonly_fields = ('status_created_at',)


@admin.register(Consulting)
class ConsultingAdmin(admin.ModelAdmin):
    inlines = (ConsultingStatusInline,)
    form = ConsultingForm


admin.site.register(Bouquet)
admin.site.register(Occasion)
admin.site.register(ConsultingStatus)
admin.site.register(Order)
admin.site.register(PaymentType)
admin.site.register(DeliveryInterval)
