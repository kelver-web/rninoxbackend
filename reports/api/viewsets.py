from rest_framework import viewsets, filters
from .serializers import ReportSerializer
from reports.models import Report


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all().order_by('-date')
    serializer_class = ReportSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['employee__user__first_name', 'employee__user__last_name']

    def get_queryset(self):
        queryset = super().get_queryset()
        employee_id = self.request.query_params.get('employee')
        date = self.request.query_params.get('date')

        if employee_id is not None:
            queryset = queryset.filter(employee_id=employee_id)

        if date is not None:
            queryset = queryset.filter(date=date)

        return queryset
     