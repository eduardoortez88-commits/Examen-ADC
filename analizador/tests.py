from django.test import SimpleTestCase
from django.urls import reverse

from .servicios import ErrorDeEntrada, analizar_texto, convertir_numero


class ConversionNumerosTests(SimpleTestCase):
    def test_decimal_valido_255(self):
        r = convertir_numero("255", 10)
        self.assertEqual(r.decimal, 255)
        self.assertEqual(r.binario, "11111111")
        self.assertEqual(r.octal, "377")
        self.assertEqual(r.hexadecimal, "FF")
        self.assertEqual(r.bits_significativos, 8)
        self.assertEqual(r.bytes_necesarios, 1)

    def test_binario_a_otras_bases(self):
        r = convertir_numero("1010", 2)
        self.assertEqual(r.decimal, 10)
        self.assertEqual(r.octal, "12")
        self.assertEqual(r.hexadecimal, "0A")
        self.assertEqual(r.binario, "00001010")
        self.assertEqual(r.bits_significativos, 4)

    def test_hexadecimal_minusculas_y_relleno_a_16_bits(self):
        r = convertir_numero("1ff", 16)
        self.assertEqual(r.decimal, 511)
        self.assertEqual(r.binario, "0000000111111111")
        self.assertEqual(r.bits_significativos, 9)
        self.assertEqual(r.bytes_necesarios, 2)

    def test_limites_del_rango(self):
        cero = convertir_numero("0", 10)
        self.assertEqual(cero.binario, "00000000")
        self.assertEqual(cero.bits_significativos, 1)
        maximo = convertir_numero("65535", 10)
        self.assertEqual(maximo.hexadecimal, "FFFF")
        self.assertEqual(maximo.bits_significativos, 16)
        self.assertEqual(maximo.bytes_necesarios, 2)

    def test_error_digito_invalido_para_la_base(self):
        with self.assertRaisesMessage(ErrorDeEntrada, "inválido"):
            convertir_numero("102", 2)
        with self.assertRaisesMessage(ErrorDeEntrada, "inválido"):
            convertir_numero("89", 8)
        with self.assertRaisesMessage(ErrorDeEntrada, "inválido"):
            convertir_numero("12G", 16)

    def test_error_fuera_de_rango(self):
        with self.assertRaisesMessage(ErrorDeEntrada, "fuera de rango"):
            convertir_numero("65536", 10)
        with self.assertRaisesMessage(ErrorDeEntrada, "fuera de rango"):
            convertir_numero("10000", 16)

    def test_error_negativo(self):
        with self.assertRaisesMessage(ErrorDeEntrada, "negativos"):
            convertir_numero("-5", 10)

    def test_error_entrada_vacia(self):
        with self.assertRaisesMessage(ErrorDeEntrada, "vacío"):
            convertir_numero("   ", 10)

    def test_error_base_invalida(self):
        with self.assertRaisesMessage(ErrorDeEntrada, "base"):
            convertir_numero("10", 3)


class CodificacionTextoTests(SimpleTestCase):
    def test_caracter_enie_en_utf8(self):
        (fila,) = analizar_texto("ñ")
        self.assertEqual(fila.caracter, "ñ")
        self.assertEqual(fila.decimal, 241)
        self.assertEqual(fila.punto_codigo, "U+00F1")
        self.assertEqual(fila.hexadecimal, "0xF1")
        self.assertEqual(fila.bytes_utf8, "C3 B1")
        self.assertEqual(fila.cantidad_bytes, 2)

    def test_ascii_usa_un_byte(self):
        (fila,) = analizar_texto("A")
        self.assertEqual(fila.decimal, 65)
        self.assertEqual(fila.punto_codigo, "U+0041")
        self.assertEqual(fila.bytes_utf8, "41")

    def test_texto_de_20_caracteres_es_valido_y_21_no(self):
        self.assertEqual(len(analizar_texto("a" * 20)), 20)
        with self.assertRaisesMessage(ErrorDeEntrada, "máximo"):
            analizar_texto("a" * 21)

    def test_texto_vacio(self):
        with self.assertRaisesMessage(ErrorDeEntrada, "vacío"):
            analizar_texto("")


class VistaTests(SimpleTestCase):
    def test_pagina_inicial(self):
        r = self.client.get(reverse("index"))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Analizador de representación de datos")

    def test_post_conversion_valida(self):
        r = self.client.post(reverse("index"), {"n-numero": "FF", "n-base": "16", "convertir": "1"})
        self.assertContains(r, "1111 1111")
        self.assertContains(r, "Bits significativos")

    def test_post_conversion_con_error_muestra_mensaje(self):
        r = self.client.post(reverse("index"), {"n-numero": "2", "n-base": "2", "convertir": "1"})
        self.assertContains(r, "inválido")

    def test_post_texto_con_enie(self):
        r = self.client.post(reverse("index"), {"t-texto": "ñ", "analizar": "1"})
        self.assertContains(r, "U+00F1")
        self.assertContains(r, "C3 B1")