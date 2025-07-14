from django.db import models

from users.models import Employee

# Create your models here.


class Team(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nome')
    description = models.TextField(blank=True, null=True, verbose_name='Descrição')
    employee = models.ManyToManyField(Employee, related_name='teams', verbose_name='Funcionários', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Equipe'
        verbose_name_plural = 'Equipes'
