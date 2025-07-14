import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')  # ajuste para o seu settings
django.setup()

from django.contrib.auth import get_user_model
from users.models import Employee
from tasks.models import Task

def main():
    username = 'Cristiano'  # seu usuário

    User = get_user_model()
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        print(f'Usuário "{username}" não encontrado.')
        return

    employees = Employee.objects.filter(employe=user)
    print(f'Total de Employees associados a "{username}": {employees.count()}')
    if not employees.exists():
        print(f'Nenhum Employee associado ao usuário "{username}".')
        return

    for e in employees:
        print(f'- Employee: {e}, Equipe: {e.team}')

    teams = set(e.team for e in employees if e.team is not None)
    print(f'Número de equipes encontradas: {len(teams)}')

    if not teams:
        print('Nenhuma equipe encontrada para os Employees desse usuário.')
        return

    print(f'Usuário "{username}" está nessas equipes:')
    for team in teams:
        print(f'- {team}')

    tasks = Task.objects.filter(team__in=teams)
    print(f'Total de tarefas encontradas: {tasks.count()}')

    if tasks.count() == 0:
        print('Nenhuma tarefa vinculada às equipes do usuário.')
        return

    print('Tarefas visíveis para esse usuário:')
    for task in tasks:
        print(f'- {task.description} (Equipe: {task.team}, Status: {task.status})')

if __name__ == '__main__':
    main()
    