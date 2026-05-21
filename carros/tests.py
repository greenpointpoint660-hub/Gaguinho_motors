from django.test import TestCase
from django.urls import reverse

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
