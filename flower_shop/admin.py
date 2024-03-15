from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
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


class PriceRangeFilter(admin.SimpleListFilter):
    title = _('Ценовой диапазон')
    parameter_name = 'price_range'

    def lookups(self, request, model_admin):
        return (
            ('0-1000', _('от 0 до 1000')),
            ('1000-3000', _('от 1000 до 3000')),
            ('3000-5000', _('от 3000 до 5000')),
            ('5000+', _('более 5000')),
        )

    def queryset(self, request, queryset):
        if self.value() == '0-1000':
            return queryset.filter(price__gte=0, price__lte=1000)
        elif self.value() == '1000-3000':
            return queryset.filter(price__gte=1000, price__lte=3000)
        elif self.value() == '3000-5000':
            return queryset.filter(price__gte=3000, price__lte=5000)
        elif self.value() == '5000+':
            return queryset.filter(price__gt=5000)
        return queryset


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


@admin.register(Bouquet)
class BouquetAdmin(admin.ModelAdmin):
    list_display = [
        'preview',
        'name',
        'description',
        'content',
        'price',
        'is_recommended',
        'get_orders_count',
    ]
    list_filter = ('occasion', PriceRangeFilter)
    readonly_fields = ['preview',]

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" style="max-height: 200px;">')

    @admin.display(description='Заказов')
    def get_orders_count(self, obj):
        return obj.get_orders()


admin.site.register(Occasion)
admin.site.register(ConsultingStatus)
admin.site.register(Order)
admin.site.register(PaymentType)
admin.site.register(DeliveryInterval)
