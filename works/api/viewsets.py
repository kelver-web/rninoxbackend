from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from works.models import Work
from works.models import Address
from .serializers import WorkSerializer
from .serializers import AddressSerializer


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]


class WorkViewSet(viewsets.ModelViewSet):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer
    permission_classes = [IsAuthenticated]
