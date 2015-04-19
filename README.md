# WSDumbo

## Requerimientos
* hadoop-1.2, se recomienda configuracion single node para testeo.
* Python>=2.7
* C++
* Freeling (para preprocesamiento del corpus)
* Dumbo
* [redsvd](http://code.google.com/p/redsvd/wiki/English) para calcular SVD.
##Estructura general
* transform_corpus.cpp es un programa sencillo usado para el preprocesamiento de datos, es necesario correrlo sobre los corpus sobre los que se quiera trabajar, pues transforma las palabras a sus formas normales (lemas). De esa forma se puede trabajar con Hadoop sin tener que usar de por medio Freeling.

* Para ver los archivos generados por una rutina hadoop:
```
dumbo cat /user/eze/count/part* -hadoop /usr/local/hadoop | sort -k2,2nr > coocurrences
```

* Para correr el coocur1
```
/*Reemplazar input por *spanish* para leer de todos los archivos del corpus*/
dumbo start coocur1.py -hadoop /usr/local/hadoop -input corpus/spanishText_480000_485000.lemma.txt -output count -memlimit 1073741824 -file count_20000_wiki.dat
```
* Si no puede leer el archivo de palabras (words), este comando lo modifica para
poder definirlo como una lista en python directamente (bastante pedestre, pero evita cargar un archivo externo):
```
cat count_20000_wiki.dat | awk '{print "\""$1"\"" ","}'  > hola
```
* Para transformar la matriz de coocurrencias a una matriz de solo numeros (es decir, sacarle las palabras que caracteriza), hacer:
```
cat coocurrences | cut -f2- > coocurrences_nowords
```
* Para hacer SVD sobre la matriz de coocurrencias (disminicion de dimensiones a 1/20 del original):
```
redsvd -i coocurrences_nowords -o coocurrences_svd -r 100  -m SVD
```
* Para correr la rutina que busca los contexts de cada palabra:
```
dumbo start context.py -hadoop /usr/local/hadoop -input corpus/algo -output count -file coocurrences_svd.V -file count_20000_wiki.dat
```
* Para correr la rutina que arma los clusters
```
dumbo start cluster_original.py -hadoop /usr/local/hadoop -input /user/eze/clusters/contexts_noletters.dat -output count -file init_clusters_noletters.dat  -memlimit 2073741824
```

* Para correr el context_cluster:
```
dumbo start context_cluster.py -hadoop /usr/local/hadoop -input /user/eze/corpus/spanishText_10000_15000.lemma.txt -output clusters -file coocurrences_svd.V -file coocurrences_word_order -file count_20000_wiki.dat  -memlimit 2073741824
```
##TIPS
* Acordarse de correr start-dfs.sh y luego start-mapred.sh.
* Si el datanode no inició correctamente, probar con:
    - cambiar los permisos de la carpeta /user/nombre_de_usuario: chmod -R 755 ~/user/nombre_de_usuario/
    - borrar la carpeta y formatear el nodo:rm -Rf ~/user/nombre_de_usuario/* && hadoop namenode -format
    - Detener todo, borrar el directorio de datos (se encuentra en dfs.data.dir en conf/hdfs-site.xml), formatear el namenode y reiniciar todo.
    - Reiniciar la computadora, lanzar primero el dfs y después el mapred
* Una vez que este el nodo vivo. copiar archivo así: 
```
hadoop dfs -copyFromLocal ruta_al_archivo hdfs://localhost:54310/user/nombre_de_usuario/carpeta_de_destino/nombre_archivo
```
* Para borrar un archivo del hdsf: hadoop dfs -rmr /user/eze/carpeta
* Recomiendo definir alias en el bash para que sea mas rapido manejar comandos de hadooop:
```
alias startdfs='/usr/local/hadoop/bin/start-dfs.sh'
alias startmapred='/usr/local/hadoop/bin/start-mapred.sh'
alias dls='hadoop fs -ls'
alias drmr='hadoop fs -rmr'
alias dcfl='hadoop fs -copyFromLocal'
alias dctl='hadoop fs -copyToLocal'
alias jps='/usr/java/jdk1.6.0_45/bin/jps'
```

## A la hora de instalar/usar hadoop:
* Bajarse el java de Oracle y agregar su ruta de instalacion a JAVA_HOME en basrc
* Bajarse la version >=0.21 de la [pagina](http://archive.apache.org/dist/hadoop/core/hadoop-0.21.0/)
* Descomprimirla en algun lado, y hacer el usuario dueño de esa carpeta: 
```
chown usuario /ruta/a/hadoop_descomprimido
```
* Agregar a hadoop_env.sh el JAVA_HOME Y desactivar el ipv6.
* Se puede seguir el tuto de esta [pagina](http://pushpalankajaya.blogspot.com.ar/2012/11/hadoop-single-node-set-up.html).
* Instalar dumbo como dice en la [pagina oficial](https://github.com/klbostee/dumbo/wiki/Building-and-installing).
* Una vez que se tiene todo configurado de acuerdo al tutorial, correr Dumbo con algo así (especial atencion al memlimit, a veces conviene poner algo irreal para que no haya errores de memoria):
```
/*La opcion hadooplib puede no ser necesaria dependiendo de la version de haddop que se esté usando*/
dumbo start test.py -input texto_a_procesar -output carpeta_de_salida -hadoop /usr/local/hadoop -hadooplib /usr/local/hadoop/contrib/streaming/ -memlimit 1073741824
```
* Cambiar las rutas de arriba por las carpetas donde se tengan instaladas las cosas.
* Para repetir algun trabajo, se tiene que borrar la carpeta de salida de datos que se creo en el trabajo anterior. Fijarse en TIPS.
