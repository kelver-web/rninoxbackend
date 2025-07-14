from rest_framework import serializers
from logistics.api.serializers import VehicleSerializer
from logistics.models import Vehicle
from tasks.models import Task
from teams.models import Team
from works.models import Work
from users.models import Employee


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name']

class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = ['id', 'name']

class EmployeeSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['id', 'name']

    def get_name(self, obj):
        return obj.employe.get_full_name() or obj.employe.username


class TaskSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)
    work = WorkSerializer(read_only=True)

    team_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(),
        source='team',
        write_only=True
    )
    work_id = serializers.PrimaryKeyRelatedField(
        queryset=Work.objects.all(),
        source='work',
        write_only=True
    )

    employee_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Employee.objects.all(),
        source='employee',
        write_only=True
    )

    employees = serializers.SerializerMethodField()
    vehicle = serializers.StringRelatedField(read_only=True)
    vehicle_id = serializers.PrimaryKeyRelatedField(
        queryset=Vehicle.objects.all(),
        source='vehicle',
        write_only=True,
        allow_null=True,
        required=False
    )

    class Meta:
        model = Task
        fields = [
            'id', 'description', 'estimated_deadline',
            'team',
            'work',
            'team_id',
            'work_id',
            'vehicle',
            'vehicle_id',
            'employee_ids',
            'employees',
            'status', 
            'observations', 
            'created_at',
            'updated_at',
            'completed_at'
        ]
        read_only_fields = ['employees', 'created_at', 'updated_at', 'completed_at']

    def get_employees(self, obj):
        employees_related = obj.employee.all()
        return [emp.employe.get_full_name() or emp.employe.username for emp in employees_related]
    