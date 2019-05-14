# coding: utf-8
"""Modulo para pruebas de extraccion."""
from banrep.extraccion import extraer_texto, guardar_texto, procesar_todos

import pytest


def test_extraccion_extraer_texto_error():
        with pytest.raises(TypeError):
                texto = extraer_texto()


def test_extraccion_extraer_texto_inexistente():
        texto = extraer_texto('bla.pdf')
        assert texto == None


def test_extraccion_guardar_texto_filas(tmp_path):
    text = "Hello"
    filepath = tmp_path.joinpath("filas.txt")

    guardar_texto(text, filepath, filas=True)
    assert filepath.read_text(encoding="utf-8") == "Hello\n"


def test_extraccion_guardar_texto_no_filas(tmp_path):
    text = "Hello"
    filepath = tmp_path.joinpath("nofilas.txt")

    guardar_texto(text, filepath, filas=False)
    assert filepath.read_text(encoding="utf-8") == "Hello"


def test_extraccion_procesar_todos_error():
        with pytest.raises(TypeError):
                n = procesar_todos()


def test_extraccion_procesar_todos_0(tmp_path):
        n = procesar_todos(tmp_path, "textos")
        assert n == 0
