from django.urls import path

from . import  views


urlpatterns = [
    path("", views.IndexView.as_view(), name="home"),
    path("countries/",views.CountryListView.as_view()),
    path("countries/<str:iso3>/", views.CountryDetailView.as_view()),
    path("weather/<str:iso3>/", views.CountryWeatherView.as_view()),
]