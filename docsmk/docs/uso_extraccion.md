# Extraer texto de documentos

Una necesidad común para analizar texto es poder extraerlo de archivos pdf, word, powerpoint o similares, que usualmente están almacenados en una carpeta en disco.

!!! note "Uso de entorno virtual"
    Para usar [banrep][pypi_banrep] se recomienda hacerlo dentro de un entorno virtual.

    Puede ver la sección de [instalación][install] para instrucciones sobre cómo crearlo y activarlo.

[pypi_banrep]: https://pypi.org/project/banrep/
[install]: instalacion.md

!!! note "Uso de Apache Tika"
    La extracción de texto hace uso de [Apache Tika Server][web_tika], una reconocida librería de Java. El uso de los comandos de extracción que se muestran en esta página asume que se cuenta con una copia de dicha librería. Si no se tiene, automáticamente se descargará una [copia][tika_server], y por tanto se requiere acceso a internet y la posibilidad de descargar ejecutables.

[web_tika]: http://tika.apache.org/download.html
[tika_server]: https://www.apache.org/dyn/closer.cgi/tika/tika-server-1.21.jar

## Línea de comandos

Con su [entorno virtual activado][install], desde la línea de comandos puede extraer el texto de cada archivo que tenga guardado en una carpeta, y almacenarlo en un nuevo archivo *.txt* que será guardado en una nueva carpeta.

```bash
# En este ejemplo tiene documentos en carpeta ~/Downloads/pubs/
# Textos serán almacenado en ~Downloads/corpus/
# Ejemplo asume directorio de trabajo será ~Downloads/

~$ cd Downloads/
~/Downloads$ python -m banrep.extraccion pubs corpus --recursivo --exts pdf --chars 5 --basura '_<>#!' --basura '\*' --basura �
```

Directorios de entrada y salida son requeridos (`pubs` y `corpus` en este ejemplo).

Si se incluye el flag `--recursivo`se extrae texto de subdirectorios.

La opción `--exts` permite especificar extensiones de archivos a procesar. Esta no es obligatoria, pero sirve para cuando tiene otro tipo de archivos en la misma carpeta que no quiere procesar.

La opción `--chars` permite determinar un número mínimo de caracteres que debe tener una línea de texto.

La opción `--basura` permite especificar caracteres que se quiere eliminar del texto. Esto usa *regular expressions*, así que caracteres especiales como *asterisco (\*)* deben escribirse con *backslash (\\)*.

## Librería

Para importar en python y usar las funciones individualmente:

```python
from banrep.io import guardar_texto
from banrep.extraccion import extraer_info, extraer_todos, procesar_xhtml

# Extrae el texto y metadata de pdf.
contenido, metadata = extraer_info('mi-super-archivo.pdf')

# Procesa el texto para limpiarlo
# Puede incluir caracteres `basura` a eliminar, y mínima longitud `chars`.
texto = procesar_xhtml(contenido, basura=None, chars=0)

# Guarda el texto extraído.
guardar_texto(texto, 'mi-super-archivo.txt')

# Extrae texto de archivos en un directorio
# y almacena nuevos archivos en carpeta textos.
# Devuelve el número de archivos procesados.
n = extraer_todos('~Downloads/pubs/', 'corpus', recursivo=True, exts=None, basura=None, chars=0)

print(f'{n} archivos procesados')
```

## Ayuda

Para ayuda sobre las funciones disponibles, desde python puede usar `help`.

```bash
~$ python
>>> from banrep import extraccion
>>> help(extraccion)
```
