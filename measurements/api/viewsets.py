from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from measurements.models import ItemMeasurement, Measurement
from .serializers import MeasurementSerializer


class MeasurementViewSet(viewsets.ModelViewSet):
    queryset = Measurement.objects.all().prefetch_related('items_measurement')
    serializer_class = MeasurementSerializer
    permission_classes = [IsAuthenticated]  # Certifique-se de que a autenticação está configurada corretamente

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemChoicesAPIView(APIView):
    """
    View para retornar as opções de choices para Tipo e Localização de ItemMeasurement.
    """
    def get(self, request, *args, **kwargs):
        types_choices = [{'value': choice[0], 'label': choice[1]} for choice in ItemMeasurement.CHOICES_TIPES]
        localization_choices = [{'value': choice[0], 'label': choice[1]} for choice in ItemMeasurement.CHOICES_LOCALIZATION]
        
        return Response({
            'types': types_choices,
            'localizations': localization_choices
        }, status=status.HTTP_200_OK)
