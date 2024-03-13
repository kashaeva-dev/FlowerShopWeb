from django.contrib import admin

from flower_shop.models import Bouquet, Occasion, ConsultingStatus, Consulting, Order

admin.site.register(Bouquet)
admin.site.register(Occasion)
admin.site.register(ConsultingStatus)
admin.site.register(Consulting)
admin.site.register(Order)
