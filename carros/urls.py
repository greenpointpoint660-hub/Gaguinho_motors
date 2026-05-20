from django.urls import path
from .views import lista_carros

urlpatterns = [
    path('', lista_carros),
]
