# coding: utf-8
"""Módulo para funciones de lectura y escritura."""
from pathlib import Path

from banrep.utils import iterar_rutas


def leer_texto(archivo):
    """Lee texto de un archivo.

    Parameters
    ----------
    archivo : str | Path
        Ruta del archivo del cual se quiere leer texto.

    Returns
    -------
    str
       Texto de archivo.
    """
    ruta = Path(archivo)

    if ruta.is_file():
        try:
            with open(ruta, encoding="utf-8") as f:
                texto = f.read()

        except Exception:
            print(f"No pudo extraerse información de {ruta.name}.")
            texto = ""

    else:
        print(f"{ruta.name} no es un archivo.")
        texto = ""

    return texto


def iterar_textos(directorio, aleatorio=False):
    """Itera sobre cada ruta en directorio y extrae el texto.

    Parameters
    ----------
    directorio: str | Path
        Directorio a iterar.
    aleatorio : bool
        Iterar aleatoriamente.

    Yields
    ------
    str
        Texto de archivo en ruta.
    """
    for archivo in iterar_rutas(directorio, aleatorio=aleatorio):
        yield leer_texto(archivo)


def guardar_texto(texto, archivo):
    """Guarda texto en un archivo.

    Parameters
    -------------
    texto : str
        Texto que se quiere guardar.
    archivo : str | Path
        Ruta del archivo en el cual se quiere guardar texto.

    Returns
    ---------
    None
    """
    with open(archivo, "w", newline="\n", encoding="utf-8") as ruta:
        for fila in texto.splitlines():
            ruta.write(fila)
            ruta.write("\n")
