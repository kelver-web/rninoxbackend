from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from logistics.models import Vehicle
from logistics.api.serializers import VehicleSerializer


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]
    
