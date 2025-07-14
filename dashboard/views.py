# dashboard/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Sum, Q
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

from tasks.models import Task
from logistics.models import Vehicle # Certifique-se de que Vehicle está importado
from works.models import Work       # Certifique-se de que Work está importado
from users.models import Employee
from teams.models import Team



class DashboardSummaryAPIView(APIView):
    def get(self, request, format=None):
        today = date.today()
        first_day_of_current_month = today.replace(day=1)
        first_day_of_last_month = (first_day_of_current_month - relativedelta(months=1))
        
        # --- Métricas de Tarefas ---
        total_tasks = Task.objects.count()
        
        tasks_by_status = Task.objects.values('status').annotate(count=Count('status'))
        tasks_status_dict = {item['status']: item['count'] for item in tasks_by_status}

        completed_tasks_this_month = Task.objects.filter(
            status='concluida',
            completed_at__gte=first_day_of_current_month
        ).count()

        completed_tasks_last_month = Task.objects.filter(
            status='concluida',
            completed_at__gte=first_day_of_last_month,
            completed_at__lt=first_day_of_current_month
        ).count()

        completed_tasks_month_change = 0
        if completed_tasks_last_month > 0:
            completed_tasks_month_change = ((completed_tasks_this_month - completed_tasks_last_month) / completed_tasks_last_month) * 100
        elif completed_tasks_this_month > 0:
            completed_tasks_month_change = 100

        new_tasks_this_month = Task.objects.filter(
            created_at__gte=first_day_of_current_month
        ).count()

        monthly_tasks_data = []
        num_months_history = 6 
        
        for i in range(num_months_history - 1, -1, -1):
            month_start = (first_day_of_current_month - relativedelta(months=i))
            
            tasks_in_month_count = Task.objects.filter(
                status='concluida',
                completed_at__year=month_start.year,
                completed_at__month=month_start.month
            ).count()
            
            monthly_tasks_data.append({
                "mes": month_start.strftime("%Y-%m-%d"),
                "count": tasks_in_month_count
            })

        # --- RE-INCLUINDO AS MÉTRICAS DE VEÍCULOS E OBRAS ---
        # Certifique-se que estas linhas estão no seu código
        total_vehicles = Vehicle.objects.count()
        available_vehicles = Vehicle.objects.filter(status='disponivel').count()

        total_works = Work.objects.count()
        active_works = Work.objects.filter(status='em_andamento').count()
        # --- FIM DA RE-INCLUSÃO ---

        response_data = {
            "total_tasks": total_tasks,
            "completed_tasks_month": completed_tasks_this_month,
            "completed_tasks_month_change": round(completed_tasks_month_change, 2),
            "new_tasks_this_month": new_tasks_this_month,
            "tasks_by_status": tasks_status_dict,
            "monthly_tasks": monthly_tasks_data,
            "total_vehicles": total_vehicles,
            "available_vehicles": available_vehicles,
            "total_works": total_works,
            "active_works": active_works,
        }

        return Response(response_data, status=status.HTTP_200_OK)


class TeamTaskRankingAPIView(APIView):
    def get(self, request, format=None):
        all_teams = Team.objects.all()
        ranking_data = []

        for team in all_teams:
            completed_tasks_count = Task.objects.filter(
                team=team,
                status='concluida'
            ).count()

            ranking_data.append({
                'team_name': team.name,
                'tasks_completed': completed_tasks_count
            })

        ranking_data.sort(key=lambda x: x['tasks_completed'], reverse=True)

        return Response(ranking_data, status=status.HTTP_200_OK)
