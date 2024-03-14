from django.contrib import admin

from flower_shop.models import (
    Bouquet,
    Occasion,
    ConsultingStatus,
    Consulting,
    Order,
    PaymentType,
    DeliveryInterval,
)

admin.site.register(Bouquet)
admin.site.register(Occasion)
admin.site.register(ConsultingStatus)
admin.site.register(Consulting)
admin.site.register(Order)
admin.site.register(PaymentType)
admin.site.register(DeliveryInterval)
