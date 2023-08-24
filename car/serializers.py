from rest_framework import serializers
from .models import *

class CarSerializer(serializers.ModelSerializer):   
    class Meta:
        model=Car
        fields=('plate_number',
                'brand',
                'model',
                'year',
                'gear',
                'rent_per_day',
                'availability',)
    def get_fields(self):
        fields=super().get_fields()
        request=self.context.get('request')
        if request.user and not request.user.is_staff:
            fields.pop('plate_number')
            fields.pop('rent_per_day')
            fields.pop('availability')


class ReservationSerializer(serializers.ModelSerializer):
    car=serializers.StringRelatedField()
    car_id=serializers.IntegerField()

    user=serializers.StringRelatedField()
    user_id=serializers.IntegerField()

    class Meta:
        model=Reservation
        fields=('customer',
                'car',
                'start_date',
                'and_date',)

