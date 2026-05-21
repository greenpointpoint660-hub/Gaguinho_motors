from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import CarroForm
from .models import Carro


def lista_carros(request):
    carros = Carro.objects.order_by("-id")

    return render(request, 'lista_carros.html', {
        'carros': carros
    })


def detalhe_carro(request, pk):
    carro = get_object_or_404(Carro, pk=pk)
    return render(request, "detalhe_carro.html", {"carro": carro})


def criar_carro(request):
    if request.method == "POST":
        form = CarroForm(request.POST)
        if form.is_valid():
            carro = form.save()
            messages.success(request, "Veículo cadastrado com sucesso.")
            return redirect("detalhe_carro", pk=carro.pk)
    else:
        form = CarroForm()

    return render(
        request,
        "form_carro.html",
        {
            "form": form,
            "titulo": "Cadastrar veículo",
            "botao": "Salvar veículo",
        },
    )


def editar_carro(request, pk):
    carro = get_object_or_404(Carro, pk=pk)

    if request.method == "POST":
        form = CarroForm(request.POST, instance=carro)
        if form.is_valid():
            form.save()
            messages.success(request, "Veículo atualizado com sucesso.")
            return redirect("detalhe_carro", pk=carro.pk)
    else:
        form = CarroForm(instance=carro)

    return render(
        request,
        "form_carro.html",
        {
            "form": form,
            "titulo": "Editar veículo",
            "botao": "Atualizar veículo",
            "carro": carro,
        },
    )


@require_POST
def excluir_carro(request, pk):
    carro = get_object_or_404(Carro, pk=pk)
    nome = str(carro)
    carro.delete()
    messages.success(request, f"{nome} removido da vitrine.")
    return redirect("lista_carros")
