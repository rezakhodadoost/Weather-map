from django.db import models

# Create your models here.
#identity country
class Country(models.Model):
    name = models.CharField(max_length=100)
    official_name = models.CharField(max_length=200, blank=True)
    iso2 = models.CharField(max_length=2, unique=True)
    iso3 = models.CharField(max_length=3, unique=True)

    capital = models.CharField(max_length=100, blank=True)
    continent = models.CharField(max_length=50)

    population = models.BigIntegerField(default=0)
    area = models.FloatField()

    currency = models.CharField(max_length=100, blank=True)
    language = models.CharField(max_length=200, blank=True)

    latitude = models.FloatField()
    longitude = models.FloatField()

    flag = models.CharField(max_length=10)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
#weater   
class Weather(models.Model):
    country = models.OneToOneField(
        Country,
        on_delete=models.CASCADE,
        related_name='weather'
    )

    temperature = models.FloatField()
    feels_like = models.FloatField()

    humidity = models.IntegerField()

    wind_speed = models.FloatField()

    pressure = models.IntegerField()

    description = models.CharField(max_length=200)

    icon = models.CharField(max_length=20)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.country.name} Weather"