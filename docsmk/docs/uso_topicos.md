# Análisis de Tópicos

Ver [este ejemplo][ejemplo_topicos] de cómo usar las funciones para análisis de tópicos. Le mostrará línea por línea el uso de las funciones principales. Cada celda viene precedida por una explicación de lo que hace el código de esa celda.

!!! info "Visualización PyLDAvis"
    GitHub no permite mostrar cierto contenido HTML directamente en su vista de Notebooks.

    Si quiere ver la gráfica ejemplo de modelo de tópicos, usar [nbviewer][ej_nbviewer].


[ejemplo_topicos]: https://github.com/munozbravo/banrep/blob/master/banrep/notebooks/ej_topicos.ipynb

[ej_nbviewer]: https://nbviewer.jupyter.org/github/munozbravo/banrep/blob/master/banrep/notebooks/ej_topicos.ipynb#topic=0&lambda=1&term=


!!! note "Uso de entorno virtual"
    Para usar [banrep][pypi_banrep] se recomienda hacerlo dentro de un entorno virtual.

    Puede ver la sección de [instalación][install] para instrucciones sobre cómo crearlo y activarlo.

[pypi_banrep]: https://pypi.org/project/banrep/
[install]: instalacion.md

## Corpus

Todo proyecto de análisis de texto empieza por definir el corpus, conjunto de documentos, a ser analizado. Esto implica cargar el texto de cada archivo, decidir si todo el texto es relevante o si debe ser pre-procesado para excluir, por ejemplo, filas de corta longitud (títulos, etc.), notas de pie de página (si el texto permite identificarlas de forma estandarizada).

En cada texto hay que identificar frases y palabras, y definir cuales de ellas mantener para analizar y cuales filtrar. Para esto se usan filtros como listas de palabras *stopwords*, que por ser tan usuales no aportan mucho valor al análisis, o definir si solo usar palabras e ignorar números, símbolos, puntuación, etc.

Para calcular sentimiento se suelen usar también listas de palabras predefinidas, que se asocian con diferentes emociones contrarias (positivas vs negativas, por ejemplo), y con base en conteos de presencia de esas palabras en el corpus se puede crear un indicador de sentimiento a lo largo del tiempo.

Con base en estas consideraciones se crea la *Clase* del corpus (llamada `MiCorpus` en esta librería), que permite generar las estadísticas descriptivas y conteos de palabras requeridos en análisis posteriores. Es probablemente la estructura más importante de la librería.

Esta librería se basa principalmente en [spaCy][web_spacy] para la implementación de todo el "pipeline" de procesamiento de texto.

[web_spacy]: https://spacy.io/

## Modelos LDA

Los modelos de tópicos son utilizados para identificar las temáticas implícitas en grandes volúmenes de documentos textuales, para así poder identificar, por ejemplo, la evolución de narrativas a lo largo del tiempo, o simplemente para tener una idea de los temas tratados en el corpus sin tener que leer cado uno de sus documentos.

Esta librería usa LDA, una de múltiples técnicas para generar modelos de tópicos. Ver [este artículo][articulo_lda] para una explicación más detallada de la intuición dentrás de estos modelos.

[articulo_lda]: https://www.machinelearningplus.com/nlp/topic-modeling-gensim-python/

Esta librería usa [Gensim][web_gensim] para la implementación del cálculo de los modelos. En su [documentación][gensim_tuts] encontrará todo lo necesario para correr este tipo de modelos y muchas técnicas adicionales no usadas en esta librería. [banrep][pypi_banrep] simplemente ofrece funciones para correr varios modelos LDA y seleccionar el mejor, todo basado en Gensim.

[web_gensim]: https://radimrehurek.com/gensim/models/ldamodel.html
[gensim_tuts]: https://radimrehurek.com/gensim/tutorial.html
[pypi_banrep]: https://pypi.org/project/banrep/

