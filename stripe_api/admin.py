from django.contrib import admin
from django.contrib.auth.models import Group, User  # pylint: disable=E5142

from .models import Discount, Item, Order, Tax


class ItemAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Item._meta.fields]
    list_display_links = ('name',)


class OrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields] + ['get_num_of_items']


class DiscountAdmin(admin.ModelAdmin):
    list_display = ('coupon_id',)

    def has_add_permission(self, *_):
        return False


admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(Tax)

admin.site.unregister((Group, User))
