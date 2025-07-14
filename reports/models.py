from django.db import models
from users.models import Employee
from tasks.models import Task

class Report(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='reports', verbose_name='Funcionário')
    date = models.DateField(verbose_name='Data do Relatório')

    completed_tasks = models.ManyToManyField(Task, related_name='completed_reports', blank=True, verbose_name='Tarefas Concluídas')
    pending_tasks = models.ManyToManyField(Task, related_name='pending_reports', blank=True, verbose_name='Tarefas Pendentes')

    observations = models.TextField(verbose_name='Observações', null=True, blank=True)

    class Meta:
        verbose_name = 'Relatório'
        verbose_name_plural = 'Relatórios'
        unique_together = ('employee', 'date')

    def __str__(self):
        return f'Relatório de {self.employee.employe} - {self.date.strftime("%d/%m/%Y")}'
