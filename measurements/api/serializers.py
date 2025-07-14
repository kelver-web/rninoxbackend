from rest_framework import serializers

from measurements.models import Measurement, ItemMeasurement
from users.models import Employee
from works.models import Work


class ItemMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemMeasurement
        fields = (
            'id',
            'identifier',
            'type',
            'height_cm',
            'width_cm',
            'localization',
            'observations',
        )


class MeasurementSerializer(serializers.ModelSerializer):
    items = ItemMeasurementSerializer(source='items_measurement', many=True)
    work = serializers.PrimaryKeyRelatedField(queryset=Work.objects.all(), required=True)
    work_name = serializers.StringRelatedField(source='work.name', read_only=True)
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), required=True)
    employee_name = serializers.CharField(source='employee.employe', read_only=True)

    class Meta:
        model = Measurement
        fields = ['id', 'employee', 'employee_name', 'work', 'work_name', 'date_measurement', 'observations', 'items']
        read_only_fields = ['id', 'employee_name']


    def create(self, validated_data):
        items_data = validated_data.pop('items', None)

        if items_data is None:
            items_data = validated_data.pop('items_measurement', [])

        measurement = Measurement.objects.create(
            employee=validated_data['employee'],
            work=validated_data['work'],
            date_measurement=validated_data['date_measurement'],
            observations=validated_data.get('observations', ''),
        )
        
        for item_data in items_data:
            try:
                ItemMeasurement.objects.create(measurement=measurement, **item_data)
            except Exception as e:
                measurement.delete()
                raise

        return measurement

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        if items_data is None:
            items_data = validated_data.pop('items_measurement', [])

        instance.employee = validated_data.get('employee', instance.employee)
        instance.work = validated_data.get('work', instance.work)
        instance.date_measurement = validated_data.get('date_measurement', instance.date_measurement)
        instance.observations = validated_data.get('observations', instance.observations)
        instance.save()

        existing_item_ids = set(item.id for item in instance.items_measurement.all())
        incoming_item_ids = set(item.get('id') for item in items_data if item.get('id'))

        items_to_delete_ids = existing_item_ids - incoming_item_ids
        if items_to_delete_ids:
            ItemMeasurement.objects.filter(id__in=items_to_delete_ids).delete()

        for item_data in items_data:
            item_id = item_data.get('id')
            if item_id:
                try:
                    item_instance = ItemMeasurement.objects.get(id=item_id, measurement=instance)
                    for key, value in item_data.items():
                        setattr(item_instance, key, value)
                    item_instance.save()
                except ItemMeasurement.DoesNotExist:
                    ItemMeasurement.objects.create(measurement=instance, **item_data)

            else:
                ItemMeasurement.objects.create(measurement=instance, **item_data)

        return instance
