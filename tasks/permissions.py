# tasks/permissions.py
from rest_framework import permissions
from django.contrib.auth import get_user_model

from users.models import Employee

User = get_user_model()


class IsTeamMember(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # obj é a instância da Task
        
        # --- CORREÇÃO AQUI ---
        # Tenta obter os objetos Employee associados ao usuário logado
        employee_qs = request.user.funcionario.all() # Usa o related_name 'funcionario'
        if not employee_qs.exists():
            return False # Se o User não tem Employee, nega acesso
        
        # Pega o primeiro Employee. Se um User pode ter vários Employees,
        # você pode precisar de uma lógica mais complexa aqui para decidir qual Employee usar.
        employee = employee_qs.first()
        # --- FIM DA CORREÇÃO ---

        # A tarefa tem que ter uma equipe associada
        if not obj.team:
            return False 
        
        # O funcionário logado deve pertencer à equipe da tarefa
        # Assumindo que Employee tem um campo 'team' que é ForeignKey para Team:
        return employee.team == obj.team
        
        # Se o Employee pode estar em várias equipes (ManyToManyField 'teams' no Employee):
        # return obj.team in employee.teams.all() # Essa linha é para ManyToMany




class IsTeamMemberForListCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_superuser:
            return True

        employee = Employee.objects.filter(employe=request.user).first()
        return bool(employee and employee.team)
