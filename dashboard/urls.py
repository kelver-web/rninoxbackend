from django.urls import path

from .views import DashboardSummaryAPIView, TeamTaskRankingAPIView 


urlpatterns = [
    path('summary/', DashboardSummaryAPIView.as_view(), name='dashboard_summary'),
    path('teams/ranking/tasks_completed/', TeamTaskRankingAPIView.as_view(), name='team_ranking'),
]
