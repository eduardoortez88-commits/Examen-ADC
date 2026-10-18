from django import forms

from .servicios import (
    ErrorDeEntrada,
    ResultadoNumero,
    FilaCaracter,
    analizar_texto,
    convertir_numero,
)

OPCIONES_BASE = [
    (2, "Binaria (base 2)"),
    (8, "Octal (base 8)"),
    (10, "Decimal (base 10)"),
    (16, "Hexadecimal (base 16)"),
]


class FormularioNumero(forms.Form):
    numero = forms.CharField(
        label="Número",
        required=False,
        strip=False,
        widget=forms.TextInput(attrs={"placeholder": "Ej.: 255, 1010, FF", "autocomplete": "off"}),
    )
    base = forms.TypedChoiceField(
        label="Base de origen",
        choices=OPCIONES_BASE,
        coerce=int,
        initial=10,
        error_messages={"invalid_choice": "La base seleccionada no es válida. Elija 2, 8, 10 o 16."},
    )

    resultado: ResultadoNumero | None = None

    def clean(self):
        datos = super().clean()
        if self.errors:
            return datos
        try:
            self.resultado = convertir_numero(datos.get("numero", ""), datos["base"])
        except ErrorDeEntrada as e:
            self.add_error("numero", str(e))
        return datos


class FormularioTexto(forms.Form):
    texto = forms.CharField(
        label="Texto (máx. 20 caracteres)",
        required=False,
        strip=False,
        widget=forms.TextInput(attrs={"placeholder": "Ej.: Año ñandú", "autocomplete": "off"}),
    )

    filas: list[FilaCaracter] | None = None

    def clean(self):
        datos = super().clean()
        try:
            self.filas = analizar_texto(datos.get("texto", ""))
        except ErrorDeEntrada as e:
            self.add_error("texto", str(e))
        return datos