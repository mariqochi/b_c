from django.contrib import admin

from .models import Car, Type, User




# class CarAdmin(admin.ModelAdmin):
#     list_display = ('make', 'model', 'price')  # Correctly defined list_display attributes

admin.site.register(Car)

# class TypeAdmin(admin.ModelAdmin):
#     list_display = ('name',)  # Correctly defined list_display attribute

admin.site.register(Type)


admin.site.register(User)

