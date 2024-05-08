from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from reservadjango.models import CustomUser

#Register model on admin page
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

#create order item inline
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0

#extend order model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["fecha"]
    inlines = [OrderItemInline]

admin.site.unregister(Order)
admin.site.register(Order, OrderAdmin)