from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

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


class CadastroUsuarioForm(UserCreationForm):
    email = forms.EmailField(
        required=False,
        label="E-mail",
        widget=forms.EmailInput(attrs={"placeholder": "seuemail@exemplo.com"}),
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        labels = {
            "username": "Usuário",
            "password1": "Senha",
            "password2": "Confirmar senha",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].help_text = ""
        self.fields["password1"].help_text = ""
        self.fields["password2"].help_text = ""


class LoginUsuarioForm(AuthenticationForm):
    username = forms.CharField(label="Usuário")
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)
