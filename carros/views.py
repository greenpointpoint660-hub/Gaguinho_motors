from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import CadastroUsuarioForm, CarroForm, LoginUsuarioForm
from .models import Carro


def home(request):
    carros = Carro.objects.order_by("-id")[:3]
    return render(request, "home.html", {"carros": carros})


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


def cadastro_usuario(request):
    if request.method == "POST":
        form = CadastroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            messages.success(request, "Cadastro feito com sucesso.")
            return redirect("home")
    else:
        form = CadastroUsuarioForm()

    return render(
        request,
        "cadastro.html",
        {"form": form, "titulo": "Criar conta", "botao": "Cadastrar"},
    )


def login_usuario(request):
    if request.method == "POST":
        form = LoginUsuarioForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "Você entrou na sua conta.")
            return redirect("home")
    else:
        form = LoginUsuarioForm(request)

    return render(
        request,
        "login.html",
        {"form": form, "titulo": "Entrar", "botao": "Entrar"},
    )


def logout_usuario(request):
    logout(request)
    messages.success(request, "Você saiu da sua conta.")
    return redirect("home")


def _ids_do_carrinho(request):
    return request.session.get("carrinho", [])


@require_POST
def adicionar_carrinho(request, pk):
    get_object_or_404(Carro, pk=pk)
    carrinho = _ids_do_carrinho(request)
    carro_id = str(pk)

    if carro_id not in carrinho:
        carrinho.append(carro_id)
        request.session["carrinho"] = carrinho
        messages.success(request, "Carro adicionado ao carrinho.")
    else:
        messages.success(request, "Esse carro já está no carrinho.")

    return redirect("carrinho")


@require_POST
def remover_carrinho(request, pk):
    carrinho = [carro_id for carro_id in _ids_do_carrinho(request) if carro_id != str(pk)]
    request.session["carrinho"] = carrinho
    messages.success(request, "Carro removido do carrinho.")
    return redirect("carrinho")


def carrinho(request):
    ids = _ids_do_carrinho(request)
    carros = Carro.objects.filter(pk__in=ids)
    total = sum(carro.preco for carro in carros)
    total_formatado = f"{total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return render(
        request,
        "carrinho.html",
        {"carros": carros, "total": total, "total_formatado": total_formatado},
    )


@require_POST
def finalizar_compra(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Entre na sua conta para finalizar a compra.")
        return redirect("login")

    request.session["carrinho"] = []
    messages.success(request, "Pedido recebido. A loja vai entrar em contato.")
    return redirect("home")


@user_passes_test(lambda user: user.is_staff, login_url="login")
def painel_admin(request):
    return render(request, "painel_admin.html")
