from django.contrib import admin
from .models import ProductGroup, Product

@admin.register(ProductGroup)
class ProductGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
    list_filter = ('parent',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('brand', 'article', 'cross_brand', 'cross_article', 'product_group', 'product_status')
    list_display_links = ('brand', 'article')
    search_fields = ('brand', 'article', 'cross_brand', 'cross_article', 'trading_numbers', 'description')
    list_filter = ('brand', 'product_group', 'product_status')
    raw_id_fields = ('product_group',)
    raw_id_fields = ('product_group',)
    list_editable = ('product_status',)
    list_per_page = 50
    fieldsets = (
        ('Основная информация', {
            'fields': ('brand', 'article', 'product_group', 'product_status')
        }),
        ('Кросс-ссылки', {
            'fields': ('cross_brand', 'cross_article', 'trading_numbers')
        }),
        ('Описания', {
            'fields': ('description', 'additional_name', 'specifications'),
            'classes': ('collapse',)
        }),
    )