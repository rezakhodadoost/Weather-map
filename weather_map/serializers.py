from rest_framework import serializers
from .models import Country, Weather

# Serializer for the Country model
# Converts Country model instances to JSON and validates incoming data.
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class WeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weather
        fields = "__all__"