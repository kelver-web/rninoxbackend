# Generated by Django 5.2.2 on 2025-06-26 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('works', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='status',
            field=models.CharField(choices=[('planejada', 'Planejada'), ('em_andamento', 'Em Andamento'), ('paralisada', 'Paralisada'), ('concluida', 'Concluída'), ('cancelada', 'Cancelada')], default='planejada', max_length=20, verbose_name='Status da Obra'),
        ),
    ]
