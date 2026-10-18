from dataclasses import dataclass

VALOR_MINIMO = 0
VALOR_MAXIMO = 65535
BASES_VALIDAS = (2, 8, 10, 16)
MAX_CARACTERES = 20

NOMBRES_BASE = {2: "binaria", 8: "octal", 10: "decimal", 16: "hexadecimal"}
DIGITOS_BASE = {
    2: "01",
    8: "01234567",
    10: "0123456789",
    16: "0123456789ABCDEF",
}


class ErrorDeEntrada(ValueError):
    """Error de validación con un mensaje claro para el usuario."""


@dataclass(frozen=True)
class ResultadoNumero:
    decimal: int
    binario: str
    binario_agrupado: str
    octal: str
    hexadecimal: str
    bits_significativos: int
    bytes_necesarios: int
    bits_totales: int


@dataclass(frozen=True)
class FilaCaracter:
    caracter: str
    decimal: int
    punto_codigo: str
    hexadecimal: str
    bytes_utf8: str
    cantidad_bytes: int


def convertir_numero(texto: str, base: int) -> ResultadoNumero:
    if base not in BASES_VALIDAS:
        raise ErrorDeEntrada("La base seleccionada no es válida. Elija 2, 8, 10 o 16.")

    texto = (texto or "").strip()
    if not texto:
        raise ErrorDeEntrada("Ingrese un número: el campo está vacío.")

    if texto.startswith("-"):
        raise ErrorDeEntrada(
            "No se permiten valores negativos: el rango válido es de 0 a 65 535."
        )

    permitidos = DIGITOS_BASE[base]
    invalidos = []
    for c in texto.upper():
        if c not in permitidos and c not in invalidos:
            invalidos.append(c)
    if invalidos:
        raise ErrorDeEntrada(
            f"Dígito(s) inválido(s) para la base {base} ({NOMBRES_BASE[base]}): "
            f"{', '.join(repr(c) for c in invalidos)}. "
            f"Dígitos permitidos: {', '.join(permitidos)}."
        )

    valor = int(texto, base)
    if not VALOR_MINIMO <= valor <= VALOR_MAXIMO:
        raise ErrorDeEntrada(
            f"El valor {valor} en decimal está fuera de rango. "
            f"Debe estar entre {VALOR_MINIMO} y 65 535."
        )

    bits_significativos = max(1, valor.bit_length())
    bytes_necesarios = (bits_significativos + 7) // 8
    bits_totales = bytes_necesarios * 8
    binario = format(valor, f"0{bits_totales}b")
    binario_agrupado = " ".join(binario[i:i + 4] for i in range(0, bits_totales, 4))

    return ResultadoNumero(
        decimal=valor,
        binario=binario,
        binario_agrupado=binario_agrupado,
        octal=format(valor, "o"),
        hexadecimal=format(valor, "X").zfill(bytes_necesarios * 2),
        bits_significativos=bits_significativos,
        bytes_necesarios=bytes_necesarios,
        bits_totales=bits_totales,
    )


def analizar_texto(texto: str) -> list[FilaCaracter]:
    if texto is None or texto.strip() == "":
        raise ErrorDeEntrada("Ingrese un texto: el campo está vacío.")
    if len(texto) > MAX_CARACTERES:
        raise ErrorDeEntrada(
            f"El texto tiene {len(texto)} caracteres; el máximo permitido es {MAX_CARACTERES}."
        )

    filas = []
    for c in texto:
        punto = ord(c)
        codificado = c.encode("utf-8")
        filas.append(
            FilaCaracter(
                caracter=c,
                decimal=punto,
                punto_codigo=f"U+{punto:04X}",
                hexadecimal=f"0x{punto:X}",
                bytes_utf8=" ".join(f"{b:02X}" for b in codificado),
                cantidad_bytes=len(codificado),
            )
        )
    return filas