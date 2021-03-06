# Bootcamp Big Data and Machine Learning 5
# Big Data Architecture

---
# *Apartamentos para turistas en Londres*


## Idea general
Utilizar la informacion de sitios turisticos de londres por ejemplo [london pass](https://www.londonpass.com/london-attractions/) para combinarlo el dataset de Airnb y junto con alguna api de localizacion obtener los apartamentos con más acceso a sitios turisticos de la ciudad y menos coste possible.


### Estrategia del DAaaS
Generar un ranking de los apartamentos de londres que esten más cercanos a los sitios turisticos tradicionales de la ciudad, su relacion con coste por noche y calificacion del host y obtener el listado de las mejores opciones para turistas. 


### Arquitectura

Se utlizaran los components de proveedores cloud como GCP:

- Cluster en Hadoop con DataProc
- Google Storage
- Crawler/Scrappy con python (via Google Function)

Primero seleccionamos la porcion del data set que corresponde a la ciudad de Londres (London), el cual posteriormente sera almacenado en el segment de google storage.

En Segundo lugar se ejecuta el crawler para obtener el listado de sitios turisticos desde https://www.londonpass.com/, almacenando en archivos csv la informacion general del sitio:

- Nombre
- Descripcion
- Direccion
- Puntos de acceso cercanos (Estacion de tren, bus y bus turistico)

El resultado del crawler se sube al segment de google storage.

Una vez se tengan las fuentes en cloud, desde el cluster Hadoop creamos tablas en HIVE e insertamos los datos para cruzarlos y obtener el ranking de los host más cercanos a los puntos turisticos.

![Diagrama](ArquitecturaPracticaBDA.png)
[Diagrama](https://drive.google.com/file/d/1k-SSM-BjNh5QbT1zv2JrVUreTtK-qrxp/view)

[Documento](https://www.lucidchart.com/documents/view/f9281224-1b6b-43c9-b211-db5991582bde/qF6ap.oB9wq-)

`TO DO: Buscar API para convertir las direccion en puntos geograficos`

### Operating Model
El operador va a iniciar el proceso una vez al mes disparando el google function que ejecutara el script end to end:

1. Crawler para obtener el listado actualizado de atracciones y almacenar en el segmento de google storage
2. Script de construccion del cluster
3. En el cluster crear las tablas de HIVE
4. Insertar la data en HIVE leyendo los archivos desde el GS
5. Cruzar la tablas y exportar el resultado al google storage segment
6 Script de eliminacion del cluster

### Crawler
En este caso el crawler se ejecuta en 2 partes:

- [Obtener el listado de atracciones](https://colab.research.google.com/drive/1aI04sSJjQW2HVStpOI22u15XqviS92JL)
- [Obtener los detalles de cada atraccion](https://colab.research.google.com/drive/1isj2iSyWtrT73N8oOpHCT5ofhaKvnzwa)

 


