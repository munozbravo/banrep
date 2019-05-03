"""Modulo para extraer texto de archivos binarios."""
from pathlib import Path
import argparse
import json
import time

from tika import parser


if __name__ == "__main__":
    description = """Extrae texto y metadata de docs ubicados en dirdocs"""
    parser = argparse.ArgumentParser(description=description)
    desc_dirdocs = "Ubicación de los documentos"
    parser.add_argument("dirdocs", help=desc_dirdocs)
    args = parser.parse_args()

    dirin = args.dirdocs

    dirdocs = Path(dirin)
    dirparent = dirdocs.parent

    dirtexts = dirparent.joinpath("text_raw")
    dirtexts.mkdir(parents=True, exist_ok=True)

    dirmeta = dirparent.joinpath("text_meta")
    dirmeta.mkdir(parents=True, exist_ok=True)

    files = 0
    start = time.time()

    for fp in dirdocs.iterdir():
        if fp.is_file():
            textfile = dirtexts.joinpath(f"{fp.stem}.txt")
            if not textfile.exists():
                try:
                    parsed = parser.from_file(str(fp))

                except Exception as e:
                    print(f"Error Tika en {fp.name} : {e}")
                    parsed = dict()

                text = parsed.get("content")
                meta = parsed.get("metadata")

                if text and meta:
                    with open(textfile, "w", newline="\n", encoding="utf-8") as out:
                        for line in text.splitlines():
                            out.write(line)
                            out.write("\n")

                    metafile = dirmeta.joinpath(f"{fp.stem}.json")
                    with open(metafile, mode="w", encoding="utf-8") as out:
                        json.dump(meta, out, ensure_ascii=False)

                    files += 1

    finish = time.time()
    print(f"{files} nuevos archivos procesados en {(finish - start) / 60} minutos")
