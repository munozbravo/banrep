# coding: utf-8
"""Módulo para variables y funciones de uso comun."""
from pathlib import Path


def crear_directorio(existente, nombre):
    """Crea nuevo directorio al mismo nivel de uno existente.

    Parámetros
    ----------
    existente : str | Path
        Directorio inicial existente.
    nombre : str
        Nombre de nuevo directorio a crear.

    Devuelve
    --------
    Path
        Nuevo directorio.
    """
    inicial = Path(existente)
    padre = inicial.parent

    nuevo = padre.joinpath(nombre)
    nuevo.mkdir(parents=True, exist_ok=True)

    return nuevo
