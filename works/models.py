from django.db import models

# Create your models here.


class Address(models.Model):
    street = models.CharField(max_length=255, verbose_name='Rua')
    number = models.CharField(max_length=20, verbose_name='Número')
    city = models.CharField(max_length=100, verbose_name='Cidade')
    state = models.CharField(max_length=100,  null=True, blank=True, verbose_name='Estado')
    zip_code = models.CharField(max_length=20, null=True, blank=True, verbose_name='CEP')

    def __str__(self):
        return self.street

    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'


class Work(models.Model):

    STATUS_CHOICES = [
        ('planejada', 'Planejada'),
        ('em_andamento', 'Em Andamento'),
        ('paralisada', 'Paralisada'),
        ('concluida', 'Concluída'),
        ('cancelada', 'Cancelada'),
        # Adicione outros status conforme a necessidade do seu projeto
    ]

    name = models.CharField(max_length=100, verbose_name='Obra')
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='work', verbose_name='Endereço')
    client = models.CharField(max_length=100, verbose_name='Cliente')
    phone = models.CharField(max_length=20, verbose_name='Telefone')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='planejada',
        verbose_name='Status da Obra'
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Obra'
        verbose_name_plural = 'Obras'
