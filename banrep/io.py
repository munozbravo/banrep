# coding: utf-8
"""Módulo para funciones de lectura y escritura."""
from pathlib import Path


def leer_texto(archivo):
    """Lee texto de un archivo.

    Parameters
    ----------
    archivo: str|Path
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
                text = f.read()

        except Exception:
            print(f"No pudo extraerse información de {ruta.name}.")

    else:
        print(f"{ruta.name} no es un archivo.")
        text = ""

    return text


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
