from rest_framework import serializers
from . import models

base_fields = ['id', 'headline', 'thumbnail', 'get_transaction_type_display',
               'price', 'get_currency_display', 'area', 'get_area_units_display']


class ApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Apartment
        fields = base_fields + ['floor_number',
                                'number_of_floors', 'number_of_rooms']


class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.House
        fields = base_fields + ['number_of_rooms', 'number_of_floors']


class LandSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Land
        fields = base_fields


class GarageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Garage
        fields = base_fields


class CommercialtSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Commercial
        fields = base_fields + ['commercial_type']
