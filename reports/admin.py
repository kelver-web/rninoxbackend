from django.contrib import admin
from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('employee_name', 'date', 'list_completed_tasks', 'list_pending_tasks', 'short_observations')
    list_filter = ('date', 'employee')
    search_fields = ('employee__user__first_name', 'employee__user__last_name')
    filter_horizontal = ('completed_tasks', 'pending_tasks')  # Interface amigável no admin

    def employee_name(self, obj):
        return obj.employee.employe
    employee_name.short_description = 'Funcionário'

    def list_completed_tasks(self, obj):
        return ', '.join([t.description[:30] for t in obj.completed_tasks.all()])
    list_completed_tasks.short_description = 'Tarefas Concluídas'

    def list_pending_tasks(self, obj):
        return ', '.join([t.description[:30] for t in obj.pending_tasks.all()])
    list_pending_tasks.short_description = 'Tarefas Pendentes'

    def short_observations(self, obj):
        return (obj.observations[:40] + '...') if len(obj.observations) > 40 else obj.observations
    short_observations.short_description = 'Observações'
