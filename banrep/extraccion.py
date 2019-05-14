# coding: utf-8
"""Modulo para extraer texto de archivos binarios."""
from pathlib import Path

from tika import parser
from banrep.comunes import crear_directorio


def extraer_texto(archivo):
    """Extrae texto de archivo.

    Parámetros
    ----------
    archivo : str | Path
        Ruta del archivo del cual se quiere extraer texto.

    Devuelve
    --------
    str
        Texto extraído.
    """
    ruta = Path(archivo)
    if ruta.is_file():
        try:
            info = parser.from_file(str(ruta))

        except Exception:
            print(f"Archivo {ruta.name} no pudo extraerse.")
            info = dict()
    else:
        print(f"{ruta.name} no es un archivo")
        info = dict()

    return info.get("content")


def guardar_texto(texto, archivo, filas=True):
    """Guarda texto en un archivo.

    Parámetros
    ----------
    texto : str
        Texto que se quiere guardar.
    archivo : str | Path
        Ruta del archivo en el cual se quiere guardar texto.
    filas : bool
        Escribe por filas si verdadero.

    Devuelve
    --------
    None
    """
    with open(archivo, "w", newline="\n", encoding="utf-8") as ruta:
        if filas:
            for fila in texto.splitlines():
                ruta.write(fila)
                ruta.write("\n")
        else:
            ruta.write(texto)


def procesar_todos(existente, nombre, filas=True):
    """Extrae y guarda texto de cada archivo al que no se le ha extraído.

    Parámetros
    ----------
    existente : str | Path
        Directorio inicial existente donde están los documentos.
    nombre : str
        Nombre de directorio en donde se quiere almacenar texto.
    filas : bool
        Escribe por filas si verdadero.

    Devuelve
    --------
    int
        Número de documentos procesados
    """
    dirdocs = Path(existente)
    dirtextos = crear_directorio(existente, nombre)

    n = 0
    for ruta in dirdocs.iterdir():
        if ruta.is_file():
            archivo = dirtextos.joinpath(f"{ruta.stem}.txt")
            if not archivo.exists():
                texto = extraer_texto(ruta)
                if texto:
                    guardar_texto(texto, archivo, filas=filas)

                    n += 1

    return n


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="""Extrae texto de cada documento ubicado en dirdocs y, si no existe ya, lo almacena en salida"""
    )

    parser.add_argument("dirdocs", help="Directorio en el que están los documentos")
    parser.add_argument(
        "--salida",
        default="textos",
        help="Nombre de directorio para guardar lo extraído (si no se especifica: %(default)s)",
    )
    args = parser.parse_args()

    dirdocs = args.dirdocs
    salida = args.salida

    n = procesar_todos(dirdocs, salida, filas=True)
    print(f"{n} nuevos archivos de la carpeta {Path(dirdocs).name} procesados")


if __name__ == "__main__":
    main()
