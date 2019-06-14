# Instalación

Se requiere tener instalado [Python 3.7][web_python].

Si es la primera vez que va a instalar este lenguaje de programación, se recomienda instalarlo usando [Anaconda3][web_anaconda] o [Miniconda3][web_conda]. Siga las instrucciones de instalación para su sistema.

!!! note "Uso de entorno virtual"
    Se recomienda instalar [banrep][pypi_banrep] en un entorno virtual para no interferir con otras instalaciones de python.

[web_python]: https://www.python.org/downloads/
[web_anaconda]: https://www.anaconda.com/distribution/
[web_conda]: https://conda.io/miniconda.html
[pypi_banrep]: https://pypi.org/project/banrep/

Tanto Anaconda como Miniconda instalan un programa llamado `conda`, para crear y activar un entorno virtual que instale `pip`.

Desde la *línea de comandos* ([Terminal][terminal] en macOS, [Anaconda Prompt][anacondocs] en windows):

[terminal]: https://support.apple.com/guide/terminal/welcome/mac
[anacondocs]: https://docs.anaconda.com/anaconda/install/verify-install/


```bash
# crear un entorno...
~$ conda create --name entorno python=3.7 pip jupyterlab
```

```bash
# confirmar que quiere descargar lo solicitado...
Proceed ([y]/n)? y
```

```bash
# activar el entorno creado...
~$ conda activate entorno
```

## pip

Una vez activado el entorno, instalar [banrep][pypi_banrep] usando `pip`. Esto instalará automáticamente las librerías que se requieren.

```bash
~$ pip install --upgrade banrep
```

## Modelo de Lenguaje Natural

Se requiere un modelo pre-entrenado de [Spacy][spacy_models], que depende del idioma del texto que se quiera procesar.

[spacy_models]: https://spacy.io/models

Existen diversas formas de instalar, la más fácil es usando `download`.

```bash
~$ python -m spacy download es_core_news_md
```

Cuando se piensa usar el mismo modelo para diferentes proyectos, una alternativa es hacer una [instalación manual][spacy_manual]: descargar el [archivo del modelo][spacy_esmd], guardarlo en el directorio deseado, y crear un [vínculo simbólico][spacy_link] a dicho modelo.

[spacy_manual]: https://spacy.io/usage/models#download-manual
[spacy_esmd]: https://github.com/explosion/spacy-models/releases/download/es_core_news_md-2.1.0/es_core_news_md-2.1.0.tar.gz
[spacy_link]: https://spacy.io/usage/models#usage-link

## Verificar instalación
Puede verificar si [banrep][pypi_banrep] instaló correctamente usando `python` o `jupyter lab` desde la línea de comandos:

```bash
~$ python
>>> from banrep.corpus import MiCorpus
>>>
```

Si no aparece ningún error quiere decir que la instalación fue exitosa.

!!! info "Sobre JupyterLab"
    Si quiere obtener mayor información sobre el uso de JupyterLab puede consultar su [documentación][jupyter]

[jupyter]: https://jupyterlab.readthedocs.io/en/stable/
