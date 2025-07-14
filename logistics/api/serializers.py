from rest_framework import serializers

from logistics.models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'brand', 'model', 'license_plate']


