from django.contrib import admin

from .models import Task

# Register your models here.


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('description', 'vehicle', 'team', 'work', 'team_members', 'status', 'created_at', 'updated_at')
    list_filter = ('team', 'work', 'status')
    search_fields = (
        'description',
        'team__name',
        'work__name',
        'employee__user__first_name',
        'employee__user__last_name',
        'vehicle__brand',
        'vehicle__model',
        'vehicle__license_plate',
    )

    def team_members(self, obj):
        return ', '.join([
            f"{emp.employe.first_name} {emp.employe.last_name}".strip() or emp.employe.username
            for emp in obj.employee.all()
        ])
    team_members.short_description = 'Funcionários'