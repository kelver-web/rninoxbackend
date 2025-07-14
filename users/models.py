from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Position(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nome')
    description = models.TextField(blank=True, null=True, verbose_name='Descrição')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'


class Employee(models.Model):
    employe = models.ForeignKey(User, on_delete=models.CASCADE, related_name='funcionario', verbose_name='Funcionário')
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='cargo', verbose_name='Cargo')
    team = models.ForeignKey(
        'teams.Team',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employees',
        verbose_name='Equipe'
    )

    def __str__(self):
        return self.employe.get_full_name() or self.employe.username
    
    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
