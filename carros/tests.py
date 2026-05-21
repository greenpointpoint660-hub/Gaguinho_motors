from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Carro


class CarroViewsTests(TestCase):
    def setUp(self):
        self.carro = Carro.objects.create(
            marca="Ford",
            modelo="Mustang",
            ano=2024,
            preco="240000.00",
            descricao="Carro esportivo em excelente estado.",
        )

    def test_lista_carros_exibe_estoque(self):
        response = self.client.get(reverse("lista_carros"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ford Mustang")
        self.assertContains(response, "R$ 240.000,00")

    def test_home_exibe_pagina_inicial(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Seu próximo carro")

    def test_criar_carro_salva_no_banco(self):
        response = self.client.post(
            reverse("criar_carro"),
            {
                "marca": "Toyota",
                "modelo": "Corolla",
                "ano": 2023,
                "preco": "135000.00",
                "descricao": "Sedan completo e economico.",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Carro.objects.filter(modelo="Corolla").exists())

    def test_editar_carro_atualiza_no_banco(self):
        response = self.client.post(
            reverse("editar_carro", args=[self.carro.pk]),
            {
                "marca": "Ford",
                "modelo": "Mustang GT",
                "ano": 2024,
                "preco": "255000.00",
                "descricao": "Versao GT revisada.",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.carro.refresh_from_db()
        self.assertEqual(self.carro.modelo, "Mustang GT")

    def test_excluir_carro_remove_do_banco(self):
        response = self.client.post(reverse("excluir_carro", args=[self.carro.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Carro.objects.filter(pk=self.carro.pk).exists())

    def test_carrinho_adiciona_carro(self):
        response = self.client.post(reverse("adicionar_carrinho", args=[self.carro.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertIn(str(self.carro.pk), self.client.session["carrinho"])

    def test_cadastro_cria_usuario(self):
        response = self.client.post(
            reverse("cadastro"),
            {
                "username": "aluno",
                "email": "aluno@example.com",
                "password1": "senha-forte-123",
                "password2": "senha-forte-123",
            },
        )

        self.assertEqual(response.status_code, 302)

    def test_painel_admin_exige_usuario_admin(self):
        response = self.client.get(reverse("painel_admin"))

        self.assertEqual(response.status_code, 302)

    def test_painel_admin_abre_para_staff(self):
        usuario = User.objects.create_user(
            username="admin_teste",
            password="senha-forte-123",
            is_staff=True,
        )
        self.client.force_login(usuario)

        response = self.client.get(reverse("painel_admin"))

        self.assertEqual(response.status_code, 200)
