# users/views.py (ou o arquivo onde seu EmployeeViewSet está definido)

from rest_framework import viewsets, permissions
from users.models import Employee
from users.api.serializers import EmployeeSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.select_related('employe', 'position', 'team').all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        """
        Define permissões diferentes para ações específicas.
        Ex: Admins podem criar/atualizar/deletar. Usuários comuns só podem ver seus próprios dados.
        """
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return []

    def get_queryset(self):
        """
        Permite que superusuários vejam todos os funcionários,
        e usuários comuns vejam apenas o seu próprio perfil de funcionário.
        """
        user = self.request.user
        if user.is_superuser:
            return Employee.objects.select_related('employe', 'position', 'team').all()
        
        if hasattr(user, 'employee_profile'):
            return Employee.objects.filter(pk=user.employee_profile.pk).select_related('employe', 'position', 'team')

        return Employee.objects.select_related('employe', 'position', 'team').all()
        

    def perform_create(self, serializer):
        serializer.save() 
        self.request.user.log_action('created', serializer.instance)

    def perform_update(self, serializer):
        serializer.save()
        self.request.user.log_action('updated', serializer.instance)

    def perform_destroy(self, instance):
        instance.delete()
        self.request.user.log_action('deleted', instance)
