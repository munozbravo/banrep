# coding: utf-8
"""Módulo de interacción con el sistema, lectura y escritura."""
from pathlib import Path
import json
import random

import pandas as pd

from banrep.preprocesos import filtrar_cortas


def crear_carpeta(nombre):
    """Crea nueva carpeta en disco si no existe.

    Si no es ruta absoluta será creada relativo a carpeta de trabajo.

    Parameters
    -------------
    nombre : str | Path
        Nombre de carpeta a crear.

    Returns
    ---------
    Path
        Ruta absoluta de carpeta.
    """
    ruta = Path(nombre).resolve()

    if not ruta.is_dir():
        ruta.mkdir(parents=True, exist_ok=True)

    return ruta


def iterar_rutas(carpeta, recursivo=False, aleatorio=False, exts=None):
    """Itera rutas de archivos en carpeta.

    Puede ser o no recursivo, en orden o aleatorio, limitando extensiones.

    Parameters
    ----------
    carpeta : str | Path
        Directorio a iterar.
    recursivo: bool
        Iterar recursivamente.
    aleatorio : bool
        Iterar aleatoriamente.
    exts: Iterable[str]
        Solo considerar estas extensiones.

    Yields
    ------
    Path
        Ruta de archivo.
    """
    absoluto = Path(carpeta).resolve()

    if recursivo:
        rutas = (r for r in absoluto.glob("**/*"))
    else:
        rutas = (r for r in absoluto.iterdir())

    rutas = (r for r in rutas if r.is_file() and not r.name.startswith("."))

    if exts:
        rutas = (r for r in rutas if any(r.suffix.endswith(e) for e in exts))

    todas = sorted(rutas)

    if aleatorio:
        random.shuffle(todas)

    yield from todas


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
    nombre = ruta.name
    carpeta = ruta.parent.name

    try:
        with open(ruta, encoding="utf-8") as f:
            texto = f.read()

    except OSError:
        print(f"No puede abrirse archivo {nombre} en {carpeta}.")
        texto = ""
    except UnicodeDecodeError:
        print(f"No puede leerse archivo {nombre} en {carpeta}.")
        texto = ""
    except Exception:
        print(f"Error inesperado leyendo {nombre} en {carpeta}")
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
            ruta.write("\n")


def leer_jsonl(archivo):
    """Lee objetos json de archivo.

    Parameters
    ----------
    archivo : str | Path
        Ruta del archivo del cual se quiere leer objetos json.

    Yields
    ------
    dict
       Contenido de cada objeto json.
    """
    ruta = Path(archivo).resolve()
    nombre = ruta.name
    carpeta = ruta.parent.name

    try:
        with open(ruta, encoding="utf-8") as f:
            for line in f:
                try:
                    yield json.loads(line.strip())
                except ValueError:
                    print(f"Ignorando registro de archivo {nombre} en {carpeta}.")

    except OSError:
        print(f"No puede abrirse archivo {nombre} en {carpeta}.")
    except UnicodeDecodeError:
        print(f"No puede leerse archivo {nombre} en {carpeta}.")
    except Exception:
        print(f"Error inesperado leyendo {nombre} en {carpeta}")


def guardar_jsonl(archivo, objs):
    """Guarda objetos json en archivo.

    Parameters
    ----------
    archivo : str | Path
        Ruta del archivo en el cual se quiere guardar objetos json.
    objs : Iterable[dict]
        Contenido de cada objeto json a guardar.

    Returns
    -------
    None
    """
    ruta = Path(archivo).resolve()
    nombre = ruta.name
    with open(ruta, "w", newline="\n", encoding="utf-8") as f:
        n = 0
        for objeto in objs:
            json.dump(objeto, f, ensure_ascii=False)
            f.write("\n")
            n += 1

    print(f"Guardados {n} registros en {nombre}")


def leer_palabras(archivo, hoja, c_grupo, c_palabras):
    """Extrae grupos de palabras de un archivo Excel.

    Parameters
    ----------
    archivo : str | Path
        Ruta del archivo Excel en disco.
    hoja : str
        Hoja de cálculo de archivo Excel.
    c_grupo : str
        Nombre de columna para determinar grupos.
    c_palabras : str
        Nombre de columna que contiene palabras de cada grupo.

    Returns
    -------
    dict (str:set)
       Grupos de palabras en cada grupo.
    """
    df = pd.read_excel(archivo, sheet_name=hoja)
    grupos = {k: set(v) for k, v in df.groupby(c_grupo)[c_palabras]}

    return grupos


def crear_txts(df, col_id, textcol, carpeta):
    """Crea archivo de texto en carpeta para cada record de dataframe.

    Parameters
    ----------
    df : pd.DataFrame
        En alguna de sus columnas tiene texto en cada fila.
    col_id : str
        Nombre de columna con valores únicos para usar en nombre archivo.
    textcol: str
        Nombre de columna que contiene texto en sus filas.
    carpeta: str | Path
        Directorio en donde se quiere guardar los archivos de texto.

    Returns
    ---------
    None
    """
    salida = Path(carpeta).resolve()
    df["nombres"] = df[col_id].apply(lambda x: salida.joinpath(f"{x}.txt"))
    df.apply(lambda x: guardar_texto(x[textcol], x["nombres"]), axis=1)

    return


class Textos:
    """Colección de textos almacenados en archivos planos en carpeta.

    Itera archivos y extrae texto y metadata a considerar como documento.
    """

    def __init__(
        self,
        carpeta,
        recursivo=False,
        aleatorio=False,
        exts=None,
        chars=0,
        parrafos=False,
    ):
        """Requiere: carpeta. Opcional: recursivo, aleatorio, exts, chars, párrafos.

        Parameters
        ----------
        carpeta : str | Path
            Directorio a iterar.
        recursivo: bool
            Iterar recursivamente.
        aleatorio : bool
            Iterar aleatoriamente.
        exts: Iterable[str]
            Solo considerar estas extensiones de archivo.
        chars : int
            Mínimo número de caracteres en una línea de texto.
        parrafos : bool
            Considerar cada párrafo como documento.
        """
        self.absoluto = Path(carpeta).resolve()
        self.recursivo = recursivo
        self.aleatorio = aleatorio
        self.exts = exts
        self.chars = chars
        self.parrafos = parrafos

        self.n = 0

    def __len__(self):
        return self.n

    def __repr__(self):
        return f"{self.__len__()} archivos leídos de carpeta {self.absoluto.name}."

    def __iter__(self):
        """Itera archivos y extrae texto y metadata de cada archivo.

        Yields
        ------
        tuple (str, dict)
            Texto y metadata de cada documento.
        """
        self.n = 0
        ndoc = 1

        for archivo in iterar_rutas(
            self.absoluto,
            aleatorio=self.aleatorio,
            recursivo=self.recursivo,
            exts=self.exts,
        ):
            texto = leer_texto(archivo)
            if texto:
                self.n += 1
                if self.chars:
                    texto = filtrar_cortas(texto, chars=self.chars)

                comun = {"archivo": archivo.name, "fuente": archivo.parent.name}

                if self.parrafos:
                    for p in texto.splitlines():
                        if p:
                            info = {"id_doc": f"{ndoc:0>7}", **comun}
                            ndoc += 1

                            yield p, info

                else:
                    meta = {"id_doc": f"{ndoc:0>7}", **comun}
                    ndoc += 1

                    yield texto, meta


class Datos:
    """Colección de textos en DataFrame.

    Itera registros y extrae texto y metadata a considerar como documento.
    """

    def __init__(self, df, textcol, metacols, chars=0):
        """Requiere: df, textcol, metacols. Opcional: chars.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame que contiene los textos.
        textcol : str
            Nombre de columna que contiene texto en sus filas.
        metacols : list
            Nombre de columnas a incluir como metadata.
        chars : int
            Mínimo número de caracteres en una línea de texto.
        """
        self.df = df
        self.textcol = textcol
        self.metacols = metacols
        self.chars = chars

    def __repr__(self):
        return f"{self.__len__()} registros en DataFrame."

    def __len__(self):
        return len(self.df.index)

    def __iter__(self):
        """Itera registros de DataFrame y extrae texto y metadata.

        Yields
        ------
        tuple (str, dict)
            Texto y metadata de cada registro.
        """
        for row in self.df.itertuples():
            texto = getattr(row, self.textcol)
            meta = {k: getattr(row, k) for k in self.metacols}

            if self.chars:
                texto = filtrar_cortas(texto, chars=self.chars)

            yield texto, meta


class Registros:
    """Colección de textos almacenados en archivos csv o Excel.

    Itera archivos y extrae texto y metadata de cada DataFrame resultante.
    """

    def __init__(
        self,
        carpeta,
        textcol,
        metacols,
        recursivo=False,
        exts=None,
        chars=0,
        hoja=None,
    ):
        """Requiere: carpeta, textcol, metacols. Opcional: recursivo, exts, chars, hoja.

        Parameters
        ----------
        carpeta : str | Path
            Ruta de carpeta que se quiere iterar.
        textcol : str
            Nombre de columna que contiene texto en sus filas.
        metacols : list
            Nombre de columnas a incluir como metadata.
        recursivo: bool
            Iterar recursivamente.
        exts: Iterable
            Solo considerar estas extensiones de archivo.
        chars : int
            Mínimo número de caracteres en una línea de texto.
        hoja : str
            Nombre de hoja en archivo excel.
        """
        self.absoluto = Path(carpeta).resolve()
        self.textcol = textcol
        self.metacols = metacols
        self.chars = chars
        self.hoja = hoja
        self.recursivo = recursivo
        self.exts = exts

        self.n = 0

    def __repr__(self):
        return f"{self.__len__()} archivos en carpeta {self.absoluto.name}."

    def __len__(self):
        return self.n

    def __iter__(self):
        """Itera archivos y extrae texto y metadata de cada registro.

        Yields
        ------
        tuple (str, dict)
            Texto y metadata de cada registro.
        """
        self.n = 0

        for archivo in iterar_rutas(
            self.absoluto, recursivo=self.recursivo, exts=self.exts
        ):
            if self.hoja:
                df = pd.read_excel(archivo, sheet_name=self.hoja)
            else:
                df = pd.read_csv(archivo)

            df = df.dropna(subset=[self.textcol])

            self.n += 1

            yield from Datos(df, self.textcol, self.metacols, chars=self.chars)
