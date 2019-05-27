# Introducción

En el [Banco de la República][web_banrep] se han adelantado diferentes proyectos de analítica de texto. Los proyectos se han enfocado principalmente en identificar el sentimiento expresado en diferentes conjuntos de documentos, así como los tópicos o temáticas que se tratan en ellos.

Cada vez que se ha analizado un nuevo conjunto de documentos se ha generado código específico para procesar el texto, aún cuando el tipo de análisis requiere generalmente las mismas rutinas. A medida que se han presentado resultados de analítica de texto, otras personas quieren aplicar el mismo tipo de técnicas a otros conjuntos de documentos.

Cuando recurrentemente se utiliza la misma serie de pasos para el análisis, y cuando más de una persona tiene interés en replicar esa serie de pasos para analizar un conjunto de documentos, resulta adecuado empaquetarlos en una librería que cualquiera pueda reusar.

La librería [banrep][pypi_banrep] recoge las funciones usadas recurrentemente para el análisis de un conjunto de documentos textuales.

[web_banrep]: http://www.banrep.gov.co/
[pypi_banrep]: https://pypi.org/project/banrep/
