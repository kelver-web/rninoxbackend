# Generated by Django 5.2.2 on 2025-06-25 22:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logistics', '0002_delete_logistics'),
        ('tasks', '0002_task_vehicle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='vehicle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='logistics.vehicle', verbose_name='Veículo'),
        ),
    ]
