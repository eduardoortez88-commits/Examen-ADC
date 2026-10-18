from django.shortcuts import render

from .forms import FormularioNumero, FormularioTexto


def index(request):
    form_numero = FormularioNumero(prefix="n")
    form_texto = FormularioTexto(prefix="t")
    resultado = None
    filas = None

    if request.method == "POST":
        if "convertir" in request.POST:
            form_numero = FormularioNumero(request.POST, prefix="n")
            if form_numero.is_valid():
                resultado = form_numero.resultado
        elif "analizar" in request.POST:
            form_texto = FormularioTexto(request.POST, prefix="t")
            if form_texto.is_valid():
                filas = form_texto.filas

    return render(
        request,
        "analizador/index.html",
        {
            "form_numero": form_numero,
            "form_texto": form_texto,
            "resultado": resultado,
            "filas": filas,
        },
    )