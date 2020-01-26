# coding: utf-8
"""Módulo de interacción con el sistema, lectura y escritura."""
from pathlib import Path
import random

import pandas as pd

from banrep.preprocesos import filtrar_cortas


def crear_directorio(nombre):
    """Crea nuevo directorio si no existe.

    Si no es ruta absoluta será creado relativo al directorio de trabajo.

    Parameters
    -------------
    nombre : str | Path
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


def iterar_rutas(directorio, recursivo=False, aleatorio=False, exts=None):
    """Itera rutas de archivos en directorio.

    Puede ser o no recursivo, en orden o aleatorio, limitando extensiones.

    Parameters
    ----------
    directorio : str | Path
        Directorio a iterar.
    recursivo: bool
        Iterar recursivamente.
    aleatorio : bool
        Iterar aleatoriamente.
    exts: Iterable
        Solo considerar estas extensiones.

    Yields
    ------
    Path
        Ruta de archivo.
    """
    absoluto = Path(directorio).resolve()

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


def leer_palabras(archivo, hoja, col_grupo="type", col_palabras="word"):
    """Extrae grupos de palabras de un archivo Excel.

    Agrupa `col_palabras` por columna `col_grupo` de hoja `hoja` de archivo Excel.

    Parameters
    ----------
    archivo : str | Path
    hoja : str
    col_grupo : str
    col_palabras : str

    Returns
    -------
    dict (str:set)
       Grupos de palabras en cada grupo.
    """
    df = pd.read_excel(archivo, sheet_name=hoja)
    grupos = {k: set(v) for k, v in df.groupby(col_grupo)[col_palabras]}

    return grupos


def crear_txts(df, col_id, textcol, directorio):
    """Crea archivo de texto en directorio para cada record de dataframe.

    Parameters
    ----------
    df : pd.DataFrame
        En alguna de sus columnas tiene texto en cada fila.
    col_id : str
        Nombre de columna con valores únicos para usar en nombre archivo.
    textcol: str
        Nombre de columna que contiene texto en sus filas.
    directorio: str | Path
        Directorio en donde se quiere guardar los archivos de texto.

    Returns
    ---------
    None
    """
    salida = Path(directorio).resolve()
    df["nombres"] = df[col_id].apply(lambda x: salida.joinpath(f"{x}.txt"))
    df.apply(lambda x: guardar_texto(x[textcol], x["nombres"]), axis=1)

    return


class Textos:
    """Colección de textos almacenados en archivos planos en directorio."""

    def __init__(
        self,
        directorio,
        aleatorio=False,
        chars=0,
        parrafos=False,
        recursivo=False,
        exts=None,
    ):
        """Define el directorio, iteración, y filtro de longitud de líneas.

        Iteración puede ser el texto de un archivo o cada párrafo en él, filtrando líneas según longitud, recursivo o no, limitando extensiones.

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
        recursivo: bool
            Iterar recursivamente.
        exts: Iterable
            Solo considerar estas extensiones.
        """
        self.directorio = Path(directorio).resolve()
        self.aleatorio = aleatorio
        self.chars = chars
        self.parrafos = parrafos
        self.recursivo = recursivo
        self.exts = exts

    def __repr__(self):
        return f"{self.__len__()} archivos en directorio {self.directorio.name}."

    def __len__(self):
        return len(
            list(
                iterar_rutas(self.directorio, recursivo=self.recursivo, exts=self.exts,)
            )
        )

    def __iter__(self):
        """Itera archivos y extrae detalles (texto, meta) de cada archivo.

        Yields
        ------
        tuple (str, dict)
            Información de cada documento (texto, metadata).
        """
        ndoc = 1

        for archivo in iterar_rutas(
            self.directorio,
            aleatorio=self.aleatorio,
            recursivo=self.recursivo,
            exts=self.exts,
        ):
            texto = leer_texto(archivo)
            if texto:
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
    """Colección de textos en DataFrame."""

    def __init__(self, df, textcol, metacols, chars=0):
        """Define parametros.

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
        """Itera registros de DataFrame y extrae detalles (texto, meta).

        Yields
        ------
        tuple (str, dict)
            Información de cada registro (texto, metadata).
        """
        for row in self.df.itertuples():
            texto = getattr(row, self.textcol)
            meta = {k: getattr(row, k) for k in self.metacols}

            if self.chars:
                texto = filtrar_cortas(texto, chars=self.chars)

            yield texto, meta


class Registros:
    """Colección de textos almacenados en archivos csv o Excel."""

    def __init__(
        self,
        directorio,
        textcol,
        metacols,
        chars=0,
        hoja=None,
        recursivo=False,
        exts=None,
    ):
        """Define el directorio, columnas para texto y metadata, y tipo archivo.

        Parameters
        ----------
        directorio : str | Path
            Ruta del directorio que se quiere iterar.
        textcol : str
            Nombre de columna que contiene texto en sus filas.
        metacols : list
            Nombre de columnas a incluir como metadata.
        chars : int
            Mínimo número de caracteres en una línea de texto.
        hoja : str
            Nombre de hoja en archivo, si excel.
        recursivo: bool
            Iterar recursivamente.
        exts: Iterable
            Solo considerar estas extensiones.
        """
        self.directorio = Path(directorio).resolve()
        self.textcol = textcol
        self.metacols = metacols
        self.chars = chars
        self.hoja = hoja
        self.recursivo = recursivo
        self.exts = exts

    def __repr__(self):
        return f"{self.__len__()} archivos en directorio {self.directorio.name}."

    def __len__(self):
        return len(
            list(
                iterar_rutas(self.directorio, recursivo=self.recursivo, exts=self.exts)
            )
        )

    def __iter__(self):
        """Itera archivos y extrae detalles (texto, meta) de cada registro.

        Yields
        ------
        tuple (str, dict)
            Información de cada registro (texto, metadata).
        """
        for archivo in iterar_rutas(
            self.directorio, recursivo=self.recursivo, exts=self.exts
        ):
            if self.hoja:
                df = pd.read_excel(archivo, sheet_name=self.hoja)
            else:
                df = pd.read_csv(archivo)

            df = df.dropna(subset=[self.textcol])

            yield from Datos(df, self.textcol, self.metacols, chars=self.chars)
