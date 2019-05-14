# coding: utf-8
"""Modulo para pruebas de comunes."""
from banrep.comunes import crear_directorio

import pytest


def test_comunes_crear_directorio_error():
    with pytest.raises(TypeError):
        crear_directorio()


def test_comunes_crear_directorio_default(tmp_path):
    existente = tmp_path.joinpath("output")
    nombre = 'default'
    nuevo = crear_directorio(existente, nombre)

    assert nuevo.parent == tmp_path
