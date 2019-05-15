# banrep: Analítica de Texto en el [Banco de la República][web_banrep].

[web_banrep]: http://www.banrep.gov.co/

**banrep** es una librería para analizar conjuntos de documentos textuales.

----

## 📖Cómo usar

Visite la [documentación][web_docs] para información detallada de uso.

[web_docs]: https://www.ejemplo.com

| Guía                       |                                  |
|----------------------------|----------------------------------|
| [Introducción][intro]      | Motivación de la librería        |
| [Instalación][instalacion] | Cómo instalar en su equipo       |
| [Modo de uso][uso]         | Cómo usar la librería            |
| [Código][api]              | Detalle de cada módulo y función |

[intro]: https://www.intro.com
[instalacion]: https://www.intro.com
[uso]: https://www.intro.com
[api]: https://www.intro.com

----

## Instalación

Se recomienda instalar en un entorno virtual para no interferir con otras instalaciones de python.

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

### pip

Una vez activado el entorno, instalar usando `pip`. Esto instalará automáticamente las librerías que **banrep** requiere.

```bash
pip install banrep
```

### Modelo de Lenguaje Natural

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

----

### TODO: modelos

----

[web_repo]: https://github.com/munozbravo/banrep
