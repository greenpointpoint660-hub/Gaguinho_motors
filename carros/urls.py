from django.urls import path

from . import views

urlpatterns = [
    path('', views.lista_carros, name='lista_carros'),
    path('carros/novo/', views.criar_carro, name='criar_carro'),
    path('carros/<int:pk>/', views.detalhe_carro, name='detalhe_carro'),
    path('carros/<int:pk>/editar/', views.editar_carro, name='editar_carro'),
    path('carros/<int:pk>/excluir/', views.excluir_carro, name='excluir_carro'),
]
