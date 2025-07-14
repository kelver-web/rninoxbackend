from django.db import models

from users.models import Employee
from works.models import Work

# Create your models here.


class Measurement(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='measurements', verbose_name='Funcionário')
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='measurements', verbose_name='Obra')
    date_measurement = models.DateField(verbose_name='Data da Medição')
    observations = models.TextField(verbose_name='Observações', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    def __str__(self):
        return f'Medição - {self.work.name} - {self.date_measurement.strftime("%d/%m/%Y")}'
    
    class Meta:
        verbose_name = 'Medição'
        verbose_name_plural = 'Medições'


class ItemMeasurement(models.Model):
    CHOICES_TIPES = (
        ('janela', 'Janela'),
        ('porta', 'Porta'),
        ('box', 'Box'),
        ('sacada', 'Sacada'),
        ('portão', 'Portão'),
        ('fachada', 'Fachada'),
        ('outro', 'Outro'),
    )

    CHOICES_LOCALIZATION = (
        ('entrada', 'Entrada'),
        ('corredor', 'Corredor'),
        ('fachada', 'Fachada'),
        ('sala', 'Sala'),
        ('quarto', 'Quarto'),
        ('banheiro', 'Banheiro'),
        ('cozinha', 'Cozinha'),
        ('escritório', 'Escritório'),
        ('sala_de_estar', 'Sala de Estar'),
        ('sala_de_jantar', 'Sala de Jantar'),
        ('varanda', 'Varanda'),
        ('area_gourmet', 'Área gourmet'),
        ('outro', 'Outro'),
    )

    measurement = models.ForeignKey(Measurement, on_delete=models.CASCADE, related_name='items_measurement', verbose_name='Medição')
    identifier = models.CharField(max_length=100, verbose_name='Identificador', help_text='EX: Janela 1 ou Porta 2')
    type = models.CharField(max_length=20, choices=CHOICES_TIPES, verbose_name='Tipo')
    width_cm = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Largura (cm)')
    localization = models.CharField(max_length=100, choices=CHOICES_LOCALIZATION, verbose_name='Localização')
    height_cm = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Altura (cm)')
    observations = models.TextField(verbose_name='Observações')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    def __str__(self):
        return f'{self.identifier} - ({self.type})'
    
    class Meta:
        verbose_name = 'Item de Medição'
        verbose_name_plural = 'Itens de Medição'
