from django.db import models


# Create your models here.


class Vehicle(models.Model):

    STATUS_CHOICES = (
        ('disponivel', 'Disponível'),
        ('em_manutencao', 'Em Manutenção'),
        ('em_uso', 'Em Uso'),
        ('indisponivel', 'Indisponível'),
    )
     
    brand = models.CharField(max_length=100, verbose_name='Marca')
    model = models.CharField(max_length=100, verbose_name='Modelo')
    license_plate = models.CharField(max_length=20, unique=True, verbose_name='Placa')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='disponivel',
        verbose_name='Status do Veículo'
    )

    def __str__(self):
        return f'{self.model}'
    
    class Meta:
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'

