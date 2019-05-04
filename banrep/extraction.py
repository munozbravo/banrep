"""Modulo para extraer texto de archivos binarios."""
from pathlib import Path
import json
import time

from tika import parser


def create_sibling_dir(dirpath, newdir):
    """
    Crea directorio `newdir` al mismo nivel de `dirpath`.

    Parameters
    ----------
    :param dirpath: str
    :param newdir: str

    Returns
    -------
    :return: Path (Nuevo directorio)
    """
    initial = Path(dirpath)
    parent = initial.parent

    newpath = parent.joinpath(newdir)
    newpath.mkdir(parents=True, exist_ok=True)

    return newpath


def extract(filepath):
    """
    Extrae texto y metadata de archivo en `filepath`.

    Parameters
    ----------
    :param filepath: str|Path

    Returns
    -------
    :return: tuple (Texto, Metadata)
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
    """
    Almacena `text` en `filepath`.

    Parameters
    ----------
    :param text: str
    :param filepath: str|Path
    """
    with open(filepath, "w", newline="\n", encoding="utf-8") as out:
        for line in text.splitlines():
            out.write(line)
            out.write("\n")


def save_metadata(metadata, filepath):
    """
    Almacena `metadata` en `filepath`.

    Parameters
    ----------
    :param metadata: dict
    :param filepath: str|Path
    """
    with open(filepath, mode="w", encoding="utf-8") as out:
        json.dump(metadata, out, ensure_ascii=False)


def extract_all(docspath, textspath, metapath):
    """
    Extrae texto y metadata de cada archivo en `docspath`.

    Almacena texto y metadata en directorios `textspath` y `metapath`.

    Parameters
    ----------
    :param docspath: str
    :param textspath: str
    :param metapath: str
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
