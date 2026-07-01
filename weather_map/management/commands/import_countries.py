import json
from pathlib import Path
from django.core.management.base import BaseCommand
from weather_map.models import Country

# Custom management command to import country data from a JSON file.
class Command(BaseCommand):
    help = "Import countries from countries.json"

    def handle(self, *args, **kwargs):

        file_path = Path("data/countries.json")
 
        with open(file_path, "r", encoding="utf-8") as file:
            countries = json.load(file)

        for country in countries:

            languages = ", ".join(country.get("languages", {}).values())

            currencies = country.get("currencies", {})
            currency = ""
            if currencies:
                currency = list(currencies.values())[0].get("name", "")

            capital_list = country.get("capital", [])
            capital = capital_list[0] if capital_list else ""

            latlng = country.get("latlng", [])
            latitude = latlng[0] if len(latlng) > 0 else 0
            longitude = latlng[1] if len(latlng) > 1 else 0

            Country.objects.update_or_create(
                iso2=country.get("cca2", ""),
                defaults={
                    "name": country.get("name", {}).get("common", ""),
                    "official_name": country.get("name", {}).get("official", ""),
                    "iso3": country.get("cca3", ""),
                    "capital": capital,
                    "continent": country.get("region", ""),
                    "population": country.get("population", 0),
                    "area": country.get("area", 0),
                    "currency": currency,
                    "language": languages,
                    "latitude": latitude,
                    "longitude": longitude,
                    "flag": country.get("flag", ""),
                },
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"{len(countries)} countries imported successfully."
            )
        )