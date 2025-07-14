from django.db.models.signals import post_save
from django.dispatch import receiver

from tasks.models import Task

from services.callmebot import CallmeBot


whatsapp_bot = CallmeBot()


@receiver(post_save, sender=Task)
def notify_when_task_is_completed(sender, instance, created, **kwargs):
    if instance.status == "concluida":
        employee_names = ', '.join([
            emp.employe.get_full_name() or emp.employe.username
            for emp in instance.employee.all()
        ])

        whatsapp_bot.send_message(
            "✅ *Tarefa Concluída!*\n\n"
            f"📌 *Obra:* {instance.work}\n"
            f"📝 *Descrição:* {instance.description}\n"
            f"👥 *Equipe:* {instance.team}\n"
            f"👷 *Funcionários:* {employee_names}"
        )
