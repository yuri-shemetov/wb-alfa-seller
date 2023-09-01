from django.contrib import admin

from products.models import Product, Feedback


@admin.register(Product)
class MailingModelAdmin(admin.ModelAdmin):
    list_display = ("sku", "name", "rating")


@admin.register(Feedback)
class MailingModelAdmin(admin.ModelAdmin):
    list_display = ("buyer_name", "buyer_rating")
