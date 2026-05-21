from django import forms

from .models import Carro


class CarroForm(forms.ModelForm):
    class Meta:
        model = Carro
        fields = ["marca", "modelo", "ano", "preco", "descricao"]
        labels = {
            "marca": "Marca",
            "modelo": "Modelo",
            "ano": "Ano",
            "preco": "Preço",
            "descricao": "Descrição",
        }
        widgets = {
            "marca": forms.TextInput(attrs={"placeholder": "Ex.: Ford"}),
            "modelo": forms.TextInput(attrs={"placeholder": "Ex.: Mustang"}),
            "ano": forms.NumberInput(attrs={"min": 1900, "max": 2100}),
            "preco": forms.NumberInput(attrs={"min": 0, "step": "0.01"}),
            "descricao": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Resumo do veículo, estado de conservação e diferenciais.",
                }
            ),
        }
