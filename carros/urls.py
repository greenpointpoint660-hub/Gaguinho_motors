from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('carros/', views.lista_carros, name='lista_carros'),
    path('carros/novo/', views.criar_carro, name='criar_carro'),
    path('carros/<int:pk>/', views.detalhe_carro, name='detalhe_carro'),
    path('carros/<int:pk>/editar/', views.editar_carro, name='editar_carro'),
    path('carros/<int:pk>/excluir/', views.excluir_carro, name='excluir_carro'),
    path('carrinho/', views.carrinho, name='carrinho'),
    path('carrinho/adicionar/<int:pk>/', views.adicionar_carrinho, name='adicionar_carrinho'),
    path('carrinho/remover/<int:pk>/', views.remover_carrinho, name='remover_carrinho'),
    path('carrinho/finalizar/', views.finalizar_compra, name='finalizar_compra'),
    path('cadastro/', views.cadastro_usuario, name='cadastro'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    path('painel/', views.painel_admin, name='painel_admin'),
]
