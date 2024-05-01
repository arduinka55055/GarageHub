from django.contrib import admin
from .models import *


    
class ProductImageInline(admin.TabularInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "manufacturer":
            manufacturer_id = request.resolver_match.kwargs.get('object_id')
            if manufacturer_id:
                kwargs["queryset"] = Model_car.objects.filter(manufacturer_id=manufacturer_id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    


    class Media:
        js = ('js/admin.js',)

admin.site.register(Category)
admin.site.register(Manufacturer)
admin.site.register(Model_car)
admin.site.register(Order)
admin.site.register(ShippingAddress)
admin.site.register(OrderItem)
