from django.contrib import admin
from .models import Category, Customer, Product, Order, About, Profile
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User


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
admin.site.register(Profile)

# Mix profile info and user info
class ProfileInline(admin.StackedInline):
    model = Profile

#Extend User Model
class UserAmin(admin.ModelAdmin):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    inlines = [ProfileInline ]


# Unregister the old way
admin.site.unregister(User)

# Register the new way
admin.site.register(User, UserAmin)