from django.contrib import admin

from .models import Team

# Register your models here.


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'employees_names', 'description')
    search_fields = ('name',)
    

    def employees_names(self, obj):
        return ', '.join([employee.employe.get_full_name() or employee.employe.username for employee in obj.employee.all()])

    employees_names.short_description = 'Funcionários'
