# Instalación

Se recomienda instalar [banrep][pypi_banrep] en un entorno virtual para no interferir con otras instalaciones de python.

[pypi_banrep]: https://pypi.org/project/banrep/

Una opción es descargar [Miniconda3][web_conda], para crear y activar un entorno básico con `conda` que instale `pip`.

[web_conda]: https://conda.io/miniconda.html

```bash
# crear un entorno...
conda create --name entorno python=3.7 pip

# confirmar que quiere descargar lo solicitado...
Proceed ([y]/n)? y

# activar el entorno creado...
conda activate entorno
```

## pip

Una vez activado el entorno, instalar usando `pip`. Esto instalará automáticamente las librerías que [banrep][pypi_banrep] requiere.

```bash
pip install banrep
```

## Modelo de Lenguaje Natural

Se requiere un modelo pre-entrenado de [Spacy][spacy_models], que depende del idioma del texto que se quiera procesar.

[spacy_models]: https://spacy.io/models

Existen diversas formas de instalar, la más fácil es usando `download`.

```bash
python -m spacy download es_core_news_md
```

Cuando se piensa usar el mismo modelo para diferentes proyectos, una alternativa es hacer una [instalación manual][spacy_manual]: descargar el [archivo del modelo][spacy_esmd], guardarlo en el directorio deseado, y crear un [vínculo simbólico][spacy_link] a dicho modelo.

[spacy_manual]: https://spacy.io/usage/models#download-manual
[spacy_esmd]: https://github.com/explosion/spacy-models/releases/download/es_core_news_md-2.1.0/es_core_news_md-2.1.0.tar.gz
[spacy_link]: https://spacy.io/usage/models#usage-link
