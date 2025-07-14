from rest_framework import serializers
from reports.models import Report
from tasks.models import Task

class TaskSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'description', 'status']


class ReportSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()
    completed_tasks = TaskSimpleSerializer(many=True, read_only=True)
    pending_tasks = TaskSimpleSerializer(many=True, read_only=True)

    class Meta:
        model = Report
        fields = ['id', 'employee', 'employee_name', 'date', 'completed_tasks', 'pending_tasks', 'observations']

    def get_employee_name(self, obj):
        return f"{obj.employee}"


    def create(self, validated_data):
        employee = validated_data['employee']
        date = validated_data['date']
        observations = validated_data.get('observations', '')

        tasks = Task.objects.filter(employee=employee, created_at__date=date)
        completed = tasks.filter(status='concluida')
        pending = tasks.exclude(status='concluida')

        report = Report.objects.create(
            employee=employee,
            date=date,
            observations=observations
        )
        report.completed_tasks.set(completed)
        report.pending_tasks.set(pending)

        return report
