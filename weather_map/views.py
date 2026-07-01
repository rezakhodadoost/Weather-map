from django.shortcuts import render
from django.http import JsonResponse
from .serializers import CountrySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status , generics
from .models import Country, Weather
from .services import get_weather
from django.views import View


# Create your views here.
# Render the application's homepage.
class IndexView(View):
    def get(self, request):
        return render(request, "weather_map/index.html")
# Return a list of all countries.    
class CountryListView(generics.ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

# Return details of a single country using its ISO2 code.
class CountryDetailView(generics.RetrieveAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    lookup_field = "iso2"



# Retrieve current weather for a country and update the local database.
class CountryWeatherView(APIView):

    def get(self, request, iso3):
        # Find the requested country by its ISO3 code.
        try:
            country = Country.objects.get(
                iso3=iso3.upper()
            )
        # Return 404 if the country does not exist.
        except Country.DoesNotExist:

            return Response(
                {"error": "Country not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Fetch live weather data from the weather service.
        weather_data = get_weather(
            country.latitude,
            country.longitude
        )

        # Create or update the weather record for the country.
        Weather.objects.update_or_create(
            country=country,
            defaults={

                "temperature": weather_data["temperature"],
                "feels_like": weather_data["feels_like"],
                "humidity": weather_data["humidity"],
                "pressure": weather_data["pressure"],
                "wind_speed": weather_data["wind_speed"],
                "description": weather_data["description"],
                "icon": weather_data["icon"],

            }
        )



        return JsonResponse({


            "country": country.name,

            "official_name": country.official_name,

            "capital": country.capital,

            "continent": country.continent,

            "area": country.area,

            "currency": country.currency,

            "language": country.language,

            "latitude": country.latitude,

            "longitude": country.longitude,

            "flag": country.flag,




            "temperature": weather_data["temperature"],

            "feels_like": weather_data["feels_like"],

            "humidity": weather_data["humidity"],

            "wind_speed": weather_data["wind_speed"],

            "pressure": weather_data["pressure"],

            "description": weather_data["description"],

            "icon": weather_data["icon"],

        })