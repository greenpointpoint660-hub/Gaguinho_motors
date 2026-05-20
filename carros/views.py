from django.shortcuts import render
from .models import Carro

def lista_carros(request):

    carros = Carro.objects.all()

    return render(request, 'lista_carros.html', {
        'carros': carros
    })