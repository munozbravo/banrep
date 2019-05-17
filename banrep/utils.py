# coding: utf-8
"""Módulo para variables y funciones de uso comun."""
from pathlib import Path


def crear_directorio(nombre):
    """Crea nuevo directorio si no existe.

    Si no es ruta absoluta será creado relativo al directorio de trabajo.

    Parameters
    -------------
    nombre : str
        Nombre de nuevo directorio a crear.

    Returns
    ---------
    Path
        Ruta absoluta del directorio.
    """
    ruta = Path(nombre).resolve()

    if not ruta.is_dir():
        ruta.mkdir(parents=True, exist_ok=True)

    return ruta
