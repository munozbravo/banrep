# coding: utf-8
"""Módulo para funciones de preprocesamiento de texto."""
import re


def filtrar_cortas(texto, chars=0):
    """Filtra líneas en texto de longitud chars o inferior.

    Parameters
    ----------
    texto : str
        Texto que se quiere filtrar.
    chars : int
        Mínimo número de caracteres en una línea de texto.

    Returns
    -------
    str
       Texto filtrado.
    """
    filtrado = ""
    for linea in texto.splitlines():
        if len(linea) > chars:
            filtrado += linea + "\n"

    return filtrado


def unir_fragmentos(texto):
    """Une fragmentos de palabras partidas por final de línea.

    Parameters
    ----------
    texto : str

    Returns
    -------
    str
        Texto con palabras de fin de línea unidas si estaban partidas.
    """
    # Asume ord('-') == 45
    return texto.replace('-\n', '').replace('-\r\n', '')


def eliminar_newlines(texto):
    """Elimina caracteres de fin de línea.

    Parameters
    ----------
    texto : str

    Returns
    -------
    str
        Texto sin caracteres de fin de línea.
    """
    return ' '.join(texto.split())


def separar_guiones(texto):
    """Separa guiones de primera y última palabra de fragmentos de texto.

    Parameters
    ----------
    texto : str

    Returns
    -------
    str
        Texto con guiones de fragmentos separados de las palabras.
    """
    # Asume ord('–') == 8211
    nuevo = re.sub(r'(\W)–([A-Za-z]+)', r'\1– \2', texto)
    nuevo = re.sub(r'([A-Za-z]+)–(\W)', r'\1 –\2', nuevo)

    return nuevo


def separar_numeros(texto):
    """Separa números de palabras que los tienen.

    Parameters
    ----------
    texto : str

    Returns
    -------
    str
        Texto con números separados de palabras.
    """
    return re.sub(r'([A-Za-z]{2,}?)(\d+)', r'\1 \2', texto)
