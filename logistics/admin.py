from django.contrib import admin

from .models import Vehicle

# Register your models here.


admin.site.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'license_plate')
    search_fields = ('brand', 'model', 'license_plate')

