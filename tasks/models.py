from django.db import models
from django.utils import timezone
from logistics.models import Vehicle
from teams.models import Team
from users.models import Employee
from works.models import Work

# Create your models here.


class Task(models.Model):

    STATUS_CHOICES = (
        ('a_fazer', 'A fazer'),
        ('em_andamento', 'Em andamento'),
        ('concluida', 'Concluída'),
        ('cancelada', 'Cancelada'),
    )

    description = models.TextField(verbose_name='Descrição')
    estimated_deadline = models.DateField(verbose_name='Prazo Estimado')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='tasks', verbose_name='Equipe')
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='tasks', verbose_name='Obra')
    employee = models.ManyToManyField(Employee, related_name='tasks', verbose_name='Funcionário', blank=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, related_name='tasks', verbose_name='Veículo', blank=True, null=True)
    status = models.CharField( max_length=20, choices=STATUS_CHOICES, verbose_name='Status', default='planejada')
    observations = models.TextField(verbose_name='Observações', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    completed_at = models.DateTimeField(
        verbose_name='Concluída em',
        null=True,
        blank=True
    )

    def __str__(self):
        return f'Tarefa: {self.description[:50]}... [ {self.team} ]'
    
    def save(self, *args, **kwargs):
        # Preencher `completed_at` quando status virar concluída
        if self.status == 'concluida' and not self.completed_at:
            self.completed_at = timezone.now()

        # Se status NÃO for 'concluida', zera completed_at
        if self.status != 'concluida':
            self.completed_at = None

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Tarefa'
        verbose_name_plural = 'Tarefas'
