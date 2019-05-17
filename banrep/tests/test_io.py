# coding: utf-8
"""Modulo para pruebas de io."""

from banrep.io import guardar_texto, leer_texto

import pytest


def test_guardar_texto(tmp_path):
    texto = "Hello"
    archivo = tmp_path.joinpath("filas.txt")

    guardar_texto(texto, archivo)
    assert archivo.read_text(encoding="utf-8") == "Hello\n"


def test_guardar_texto_arg1(tmp_path):
    with pytest.raises(TypeError):
        archivo = tmp_path.joinpath("filas.txt")
        guardar_texto(archivo)


def test_leer_texto(tmp_path):
        texto = leer_texto(tmp_path)
        assert texto == ""


def test_leer_texto_arg0():
        with pytest.raises(TypeError):
                texto = leer_texto()
