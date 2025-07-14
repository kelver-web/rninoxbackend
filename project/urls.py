from django.urls import path, include
from django.contrib import admin

from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from logistics.api.viewsets import VehicleViewSet
from measurements.api.viewsets import ItemChoicesAPIView, MeasurementViewSet
from reports.api.viewsets import ReportViewSet
from tasks.api.viewsets import TaskViewSet
from teams.api.viewsets import TeamViewSet
from users.api.viewsets import EmployeeViewSet
from users.views import UserProfileAPIView
from works.api.viewsets import WorkViewSet
from works.api.viewsets import AddressViewSet


# Criação do roteador padrão do Django REST Framework
# que irá registrar os viewsets e gerar as rotas automaticamente
router = DefaultRouter()
router.register('logistics', VehicleViewSet, basename='logistics')
router.register('measurements', MeasurementViewSet, basename='measurements')
router.register('reports', ReportViewSet, basename='reports')
router.register('tasks', TaskViewSet, basename='tasks')
router.register('teams', TeamViewSet, basename='teams')
router.register('users', EmployeeViewSet, basename='users')
router.register('works', WorkViewSet, basename='works')
router.register('addresses', AddressViewSet, basename='addresses')


urlpatterns = [
    # Rota do admin
    path('admin/', admin.site.urls),
    # Rotas de autenticação JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/users/profile/', UserProfileAPIView.as_view(), name='direct_user_profile'),
    # Rotas da API
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('api/item-choices/', ItemChoicesAPIView.as_view(), name='item_choices'),
]
