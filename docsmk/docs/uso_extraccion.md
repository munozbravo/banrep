# Extraer texto de documentos

Una necesidad común para analizar texto es poder extraerlo de archivos pdf, word, powerpoint o similares, que usualmente están almacenados en una carpeta en disco.

!!! note "Uso de entorno virtual"
    Para usar [banrep][pypi_banrep] se recomienda hacerlo dentro de un entorno virtual. Puede ver la sección de [instalación][install] para instrucciones sobre cómo crearlo y activarlo.

[pypi_banrep]: https://pypi.org/project/banrep/
[install]: instalacion.md

!!! note "Uso de Apache Tika"
    La extracción de texto hace uso de [Apache Tika Server][web_tika], una reconocida librería de Java. El uso de los comandos de extracción que se muestran en esta página asume que se cuenta con una copia de dicha librería. Si no se tiene, automáticamente se descargará una [copia][tika_server], y por tanto se requiere acceso a internet y la posibilidad de descargar ejecutables.

[web_tika]: http://tika.apache.org/download.html
[tika_server]: https://www.apache.org/dyn/closer.cgi/tika/tika-server-1.21.jar

## Línea de comandos

Con su [entorno virtual activado][install], desde la línea de comandos puede extraer el texto de cada archivo que tenga guardado en una carpeta, y almacenarlo en un nuevo archivo *.txt* que será guardado en una nueva carpeta.

```bash
# En este ejemplo tiene documentos en carpeta ~/Downloads/docs/
# Textos serán almacenado en ~Downloads/corpus/
# Asume directorio de trabajo será ~Downloads/

~$ cd Downloads/
~/Downloads$ python -m banrep.extraccion docs/ --salida corpus
```

Si se omite directorio de salida se crea uno llamado `textos`.

```bash
# No se especifica --salida
# Resultado será almacenado en ~Downloads/textos

~/Downloads$ python -m banrep.extraccion docs/
```

## Librería

Para importar en python y usar las funciones individualmente:

```python
from banrep.io import guardar_texto
from banrep.extraccion import extraer_info, extraer_archivos

# Extrae el texto de pdf y lo asigna a una variable.
texto = extraer_info('mi-super-archivo.pdf')

# Guarda el texto extraído.
guardar_texto(texto, 'mi-super-archivo.txt')

# Extrae texto de archivos en un directorio
# y almacena nuevos archivos en carpeta textos.
# Devuelve el número de archivos procesados.
n = extraer_archivos('~Downloads/docs/', 'textos')

print(f'{n} archivos procesados')
```

## Ayuda

Para ayuda sobre las funciones disponibles, desde python puede usar `help`.

```bash
~$ python
>>> from banrep import extraccion
>>> help(extraccion)
```
