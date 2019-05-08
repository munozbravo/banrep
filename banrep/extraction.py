"""Modulo para extraer texto de archivos binarios."""
from pathlib import Path
import json
import time

from tika import parser


def create_sibling_dir(dirpath, newdir):
    """Crea nuevo directorio al mismo nivel de uno existente.

    Crea `newdir` al mismo nivel de `dirpath`.

    Parameters
    ----------
    dirpath : str
        Directorio inicial existente.
    newdir : str
        Nombre de nuevo directorio a crear.

    Returns
    -------
    Path
        Nuevo directorio.
    """
    initial = Path(dirpath)
    parent = initial.parent

    newpath = parent.joinpath(newdir)
    newpath.mkdir(parents=True, exist_ok=True)

    return newpath


def extract(filepath):
    """Extrae texto y metadata de archivo.

    Archivo ubicado en `filepath`.

    Parameters
    ----------
    filepath : str or Path
        Ruta del archivo del cual se quiere extraer info.

    Returns
    -------
    tuple (str, dict)
        Texto y Metadata extraídos.
    """
    try:
        parsed = parser.from_file(str(filepath))

    except Exception as e:
        print(f"Error Tika en {Path(filepath).name} : {e}")
        parsed = dict()

    text = parsed.get("content")
    meta = parsed.get("metadata")

    return text, meta


def save_text(text, filepath):
    """Guarda texto en un archivo.

    Guarda `text` en `filepath`.

    Parameters
    ----------
    text : str
        Texto que se quiere guardar.
    filepath : str or Path
        Ruta del archivo en el cual se quiere guardar texto.

    Returns
    -------
    None
    """
    with open(filepath, "w", newline="\n", encoding="utf-8") as out:
        for line in text.splitlines():
            out.write(line)
            out.write("\n")


def save_metadata(metadata, filepath):
    """Guarda metadata en un archivo.

    Guarda `metadata` en `filepath`.

    Parameters
    ----------
    metadata : dict
        Metadata que se quiere guardar.
    filepath : str or Path
        Ruta de archivo en el cual se quiere guardar metadata.

    Returns
    -------
    None
    """
    with open(filepath, mode="w", encoding="utf-8") as out:
        json.dump(metadata, out, ensure_ascii=False)


def extract_all(docspath, textspath, metapath):
    """Extrae y guarda texto y metadata de archivos en un directorio.

    Extrae de cada archivo en `docspath`, y guarda texto y metadata en directorios `textspath` y `metapath` respectivamente.

    Parameters
    ----------
    docspath : str
        Directorio inicial existente donde están los documentos.
    textspath : str
        Nombre de directorio en donde se quiere almacenar texto.
    metapath: str
        Nombre de directorio en donde se quiere almacenar metadata.

    Returns
    -------
    None
    """
    dirdocs = Path(docspath)
    dirtexts = create_sibling_dir(docspath, textspath)
    dirmeta = create_sibling_dir(docspath, metapath)

    files = 0

    for fp in dirdocs.iterdir():
        if fp.is_file():
            textfile = dirtexts.joinpath(f"{fp.stem}.txt")
            if not textfile.exists():
                text, meta = extract(fp)

                if text and meta:
                    save_text(text, textfile)

                    metafile = dirmeta.joinpath(f"{fp.stem}.json")
                    save_metadata(meta, metafile)

                    files += 1

    print(f"{files} nuevos archivos de la carpeta {dirdocs.name} procesados")


if __name__ == "__main__":
    import argparse

    description = """Extrae texto y metadata de docs ubicados en dirdocs"""
    parser = argparse.ArgumentParser(description=description)
    desc_dirdocs = "Ubicación de los documentos"
    parser.add_argument("dirdocs", help=desc_dirdocs)
    args = parser.parse_args()

    dirin = args.dirdocs

    extract_all(dirin, "text_raw", "text_meta")
