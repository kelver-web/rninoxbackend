from rest_framework import serializers
from django.db.models import Count
from collections import defaultdict

from users.models import Employee
from tasks.models import Task
from teams.models import Team


class MemberSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    bio = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ['id', 'name', 'role', 'avatar', 'bio']

    def get_name(self, obj):
        return obj.employe.get_full_name() or obj.employe.username

    def get_role(self, obj):
        return obj.position.name if obj.position else ''

    def get_avatar(self, obj):
        full_name = self.get_name(obj)
        initials = ''.join([n[0] for n in full_name.split()][:2]).upper()
        return initials

    def get_bio(self, obj):
        cargos = obj.position.name if obj.position else "Sem cargo"
        equipes = ", ".join([team.name for team in obj.teams.all()])
        return f'{cargos} nas equipes {equipes if equipes else "Sem equipe"}'


class TeamSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    monthly = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'members', 'status', 'monthly']

    def get_members(self, obj):
        employees = obj.employee.all()
        return MemberSerializer(employees, many=True).data

    def get_status(self, obj):
        counts = Task.objects.filter(team=obj).values('status').annotate(total=Count('id'))
        status_counts = {'a_fazer': 0, 'concluidas': 0, 'em_andamento': 0, 'canceladas': 0}
        for item in counts:
            if item['status'] == 'a_fazer':
                status_counts['a_fazer'] = item['total']
            elif item['status'] == 'concluida':
                status_counts['concluidas'] = item['total']
            elif item['status'] == 'em_andamento':
                status_counts['em_andamento'] = item['total']
            elif item['status'] == 'cancelada':
                status_counts['canceladas'] = item['total']
        return status_counts

    def get_monthly(self, obj):
        tasks = Task.objects.filter(team=obj)
        data = defaultdict(lambda: {'a_fazer': 0, 'concluidas': 0, 'em_andamento': 0, 'canceladas': 0})

        for task in tasks:
            month = task.created_at.strftime('%Y-%m')
            if task.status == 'a_fazer':
                data[month]['a_fazer'] += 1
            elif task.status == 'concluida':
                data[month]['concluidas'] += 1
            elif task.status == 'em_andamento':
                data[month]['em_andamento'] += 1
            elif task.status == 'cancelada':
                data[month]['canceladas'] += 1

        result = []
        for month in sorted(data.keys()):
            result.append({
                'mes': month,
                'a_fazer': data[month]['a_fazer'],
                'concluidas': data[month]['concluidas'],
                'em_andamento': data[month]['em_andamento'],
                'canceladas': data[month]['canceladas'],
            })

        return result
