from django.contrib import admin

from .models import Employee, Position

# Register your models here.


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'team__name')


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employe', 'position')
    list_filter = ('position',)
    search_fields = ('name', 'team__name', 'position__name')
    ordering = ('employe',)
