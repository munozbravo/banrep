# coding: utf-8
"""Módulo para funciones de lectura y escritura."""
from pathlib import Path

import pandas as pd

from banrep.preprocesos import filtrar_cortas
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
    ruta = Path(archivo).resolve()

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


def leer_stopwords(archivo, hoja, col="word"):
    """De un archivo excel lee una columna con palabras.

    Columna `col` de la hoja `hoja` de archivo Excel.

    Parameters
    ----------
    archivo : str | Path
    hoja : str
    col : str

    Returns
    -------
    set
       Items únicos en la columna
    """
    df = pd.read_excel(archivo, sheet_name=hoja)

    return set(df[col])


def iterar_registros(directorio, aleatorio=False, chars=0, parrafos=False):
    """Itera rutas en directorio y extrae detalles de cada documento.

    Documento puede ser el texto de un archivo o cada párrafo en él.

    Parameters
    ----------
    directorio : str | Path
        Directorio a iterar.
    aleatorio : bool
        Iterar aleatoriamente.
    chars : int
        Mínimo número de caracteres en una línea de texto.
    parrafos : bool
        Considerar cada párrafo como documento.

    Yields
    ------
    tuple (str, dict)
        Información de cada documento (texto, (archivo, fuente)).
    """
    for archivo in iterar_rutas(directorio, aleatorio=aleatorio):
        comun = {'archivo': archivo.name, 'fuente': archivo.parent.name}
        texto = leer_texto(archivo)

        if chars:
            texto = filtrar_cortas(texto, chars=chars)

        if parrafos:
            i = 1
            for p in texto.splitlines():
                if p:
                    info = {'parrafo': i, **comun}
                    i += 1
                    yield p, info
        else:
            info = {'parrafo': 'no', **comun}
            yield texto, info
