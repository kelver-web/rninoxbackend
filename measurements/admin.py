from django.contrib import admin
from .models import Measurement, ItemMeasurement


class ItemMeasurementsInline(admin.StackedInline):
    model = ItemMeasurement
    extra = 1
    fields = ('identifier', 'type', 'width_cm', 'height_cm', 'localization', 'observations')
    autocomplete_fields = []
    show_change_link = False


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('work', 'employee', 'date_measurement', 'observations')
    list_filter = ('date_measurement', 'work')
    search_fields = ('work__name', 'empployee__user__first_name', 'empployee__user__last_name')
    inlines = [ItemMeasurementsInline]


    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True


@admin.register(ItemMeasurement)
class ItemMeasurementAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'type', 'width_cm', 'height_cm', 'localization', 'measurement')
    list_filter = ('type',)
    search_fields = ('identifier', 'measurement__work__name')
