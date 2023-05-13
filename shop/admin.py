from django.contrib import admin
from .models import Category, Product, Review, Rating


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['friendly_name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['name',]


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'category',
                    'updated_at', 'in_stock', 'image_tag']
    readonly_fields = ['image_tag']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['name', 'price']
    search_fields = ('category__name',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'review', 'created_at']
    list_filter = ['user', 'created_at']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Rating)
