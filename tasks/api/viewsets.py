# tasks/api/viewsets.py (Seu TaskViewSet corrigido)

from django.utils import timezone
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied, ValidationError 
from tasks.api.serializers import TaskSerializer
from tasks.models import Task
from tasks.permissions import IsTeamMember
from users.models import Employee


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_permissions(self):
        user = self.request.user
        if user.is_superuser:
            return [permissions.IsAuthenticated()]
        else:
            # Para list, retrieve, e partial_update, use IsTeamMember
            if self.action in ['list', 'retrieve', 'partial_update']:
                return [permissions.IsAuthenticated(), IsTeamMember()]
            else:
                return [permissions.IsAdminUser()]

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return Task.objects.all().select_related('team', 'work').prefetch_related('employee').order_by('-created_at')

        # --- CORREÇÃO AQUI ---
        # Usa o related_name 'funcionario' para acessar os Employees do User
        employee_qs = user.funcionario.all() 
        if not employee_qs.exists():
            return Task.objects.none() # Se o User não tem Employee, não vê tarefas

        employee = employee_qs.first() 

        if employee and employee.team:

            return Task.objects.filter(team=employee.team).select_related('team', 'work').prefetch_related('employee').order_by('-created_at')
        
        return Task.objects.none() 

    def perform_create(self, serializer):
        if not self.request.user.is_superuser:
            raise PermissionDenied("Você não tem permissão para criar tarefas.")
        serializer.save()

    def perform_update(self, serializer):
        user = self.request.user
        task = serializer.instance

        if user.is_superuser:
            serializer.save()
            return

        employee = Employee.objects.filter(employe=user).first()
        if not employee or employee.team != task.team:
            raise PermissionDenied("Você não tem permissão para alterar esta tarefa.")

        # Permitir somente alteração de status e observações
        allowed_fields = {"status", "observations"}
        incoming_fields = set(serializer.validated_data.keys())

        if not incoming_fields.issubset(allowed_fields):
            raise PermissionDenied("Você só pode alterar o status e as observações da tarefa.")

        # Atualização do completed_at com base no status
        old_status = task.status
        new_status = serializer.validated_data.get("status", old_status)

        if new_status == "concluida" and old_status != "concluida":
            serializer.save(completed_at=timezone.now())
        elif old_status == "concluida" and new_status != "concluida":
            serializer.save(completed_at=None)
        else:
            serializer.save()
            
    def perform_destroy(self, instance):
        if not self.request.user.is_superuser:
            raise PermissionDenied("Você não tem permissão para deletar tarefas.")
        instance.delete()
