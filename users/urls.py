from django.urls import path
from .views import RegisterUserAPIView, UserProfileAPIView, LogoutAPIView, PositionListCreateAPIView, PositionRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('register/', RegisterUserAPIView.as_view(), name='register_user'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    
    # Rotas para Cargos (Positions)
    path('positions/', PositionListCreateAPIView.as_view(), name='position_list_create'),
    path('positions/<int:pk>/', PositionRetrieveUpdateDestroyAPIView.as_view(), name='position_detail_update_delete'),
]