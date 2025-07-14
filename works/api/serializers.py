from rest_framework import serializers

from works.models import Work
from works.models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'street', 'number', 'city', 'state', 'zip_code']


class WorkSerializer(serializers.ModelSerializer):
    address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all(), required=True)
    address_name = serializers.SerializerMethodField()
    zip_code = serializers.CharField(source='address.zip_code', read_only=True)

    class Meta:
        model = Work
        fields = ['id', 'name', 'address', 'client', 'phone', 'address_name', 'zip_code']

    def get_address(self, obj):
        return obj.address.street
    
    def get_address_name(self, obj):
        return obj.address.street
