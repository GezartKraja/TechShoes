from django.contrib import admin

from store.models import Customer
from .models import ShippingAddress, Order, OrderItem

# Register the model on the admin section thing
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

