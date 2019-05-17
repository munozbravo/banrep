# coding: utf-8
"""Modulo para pruebas de utils."""
from banrep.utils import crear_directorio

import pytest


def test_crear_directorio_default(tmp_path):
    nombre = tmp_path.joinpath("output")
    nuevo = crear_directorio(nombre)

    assert nuevo.parent == tmp_path
