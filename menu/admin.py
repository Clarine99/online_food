from django.contrib import admin
from .models import Category, FoodItem
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('category_name','vendor',)}
    list_display = ('category_name', 'vendor', 'updated_at')
    search_fields = ('category_name', 'vendor__vendor_name')

class FoodItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('food_title','vendor',)}
    list_display = ('food_title', 'category', 'vendor', 'price', 'is_available', 'modified_at')
    list_editable = ('is_available',)
    list_filter = ('is_available', 'category', 'vendor')
    search_fields = ('food_title', 'category__category_name', 'vendor__vendor_name')

admin.site.register(Category, CategoryAdmin)
admin.site.register(FoodItem, FoodItemAdmin)