# Banrep

Analítica de Texto en el [Banco de la República | Colombia][web_banrep].

El código fuente está disponible [en este repositorio][web_repo]

*En construcción: se irá agregando funcionalidad*

----

## Instalación

Se recomienda instalar en un entorno virtual para no interferir con otras instalaciones de python.

Una opción es descargar [Miniconda3][web_conda], para crear y activar un entorno básico con `conda`.

```bash
# crear un entorno...
conda create --name entorno python=3.7 pip

# confirmar que quiere descargar lo solicitado...
Proceed ([y]/n)? y

# activar el entorno creado...
conda activate entorno
```

 El archivo [environment.yml](environment.yml) detalla las diferentes librerías requeridas que se instararán.

### pip

El entorno debe tener instalado **pip**.

```bash
pip install banrep
```

## Modelo de Procesamiento de Lenguaje Natural

Se requiere un modelo pre-entrenado de [Spacy][spacy_models], que depende del idioma del texto que se quiera procesar.

Existen diversas formas de instalar, la más fácil es usando *download*.

```bash
python -m spacy download es_core_news_md
```

Cuando se piensa usar el mismo modelo para diferentes proyectos, una alternativa es hacer una [instalación manual][spacy_manual]: descargar el [archivo del modelo][spacy_esmd], guardarlo en el directorio deseado, y crear un [vínculo simbólico][spacy_link] a dicho modelo.

----

## Modo de uso

### [Extraer texto de documentos][repo_extraccion]
Asume que el usuario quiere extraer texto de archivos binarios como pdf, word, powerpoint, y que están almacenados en una carpeta en disco.

El uso desde la línea de comandos crea directorio de salida paralelo a directorio original.

```bash
# En este ejemplo tiene documentos en carpeta ~/Downloads/docs/
# Resultado será almacenado en ~Downloads/corpus

python -m banrep.extraccion ~/Downloads/docs/ --salida corpus
```

Si se omite directorio de salida crea uno llamado `textos`.

```bash
# Resultado será almacenado en ~Downloads/textos

python -m banrep.extraccion ~/Downloads/docs/
```

Para importar en python y usar las funciones individualmente:

```python
from banrep.extraccion import extraer_texto, guardar_texto, procesar_todos

texto = extraer_texto('mi-super-archivo.pdf')

guardar_texto(texto, 'mi-super-archivo.txt', filas=True)

n = procesar_todos('algun/directorio/', 'textos', filas=True)

print(f'{n} archivos procesados')
```

Para ayuda sobre las funciones disponibles, desde python usar `help`

```bash
python
>>> from banrep import extraccion
>>> help(extraccion)
````

### TODO: modelos

----

[web_banrep]: http://www.banrep.gov.co/
[web_repo]: https://github.com/munozbravo/banrep
[web_conda]: https://conda.io/miniconda.html
[spacy_models]: https://spacy.io/models
[spacy_manual]: https://spacy.io/usage/models#download-manual
[spacy_esmd]: https://github.com/explosion/spacy-models/releases/download/es_core_news_md-2.1.0/es_core_news_md-2.1.0.tar.gz
[spacy_link]: https://spacy.io/usage/models#usage-link

[repo_extraccion]: banrep/extraccion.py
