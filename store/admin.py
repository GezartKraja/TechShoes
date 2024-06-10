from django.contrib import admin
from .models import Category, Customer, Product, Order,About
from django.http import HttpResponseRedirect
from django.urls import reverse


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at')

@admin.register(About)
class AboutsAdmin(admin.ModelAdmin):
    def response_add(self, request, obj, post_url_continue=None):
        return HttpResponseRedirect(reverse('about'))


admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)

