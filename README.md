# ElasticSearch-IR

A) Sistema de recuperación ad-hoc
El objetivo es crear un sistema de recuperación de información empleando la API de Apache
Lucene (https://lucene.apache.org/), la de ElasticSearch (https://www.elastic.co) o la de Solr
(https://solr.apache.org/), con el objetivo último de implementar diferentes modos de análisis e
indización del contenido de documentos y consultas. En concreto, se desea contrastar la eficacia de
varios enfoques mediante un sistema de evaluación ad-hoc en español, similar al utilizado como
ejemplo en el apartado 3 de la asignatura. El alumno debe implementar al menos los siguientes
enfoques:

• Enfoque base. Implementación del analizador por defecto para el español. Sería
SpanishAnalyzer para Lucene/ElasticSearch/Solr; este analizador incluye por defecto la
conversión a minúsculas, la eliminación de palabras vacías (lista procedente de Snowball) y
empleo de un s-stemmer simple (procedente de la página de recursos de Jacques Savoy).

• Palabras vacías. Cambiar, respecto del enfoque base, la lista de palabras vacías para que
sean las contenidas en el fichero vacias.txt (ver más adelante). Este fichero contiene los
términos que aparecen en más del 20% de los documentos.

• Lematizador Snowball. Cambiar el enfoque base para utilizar el lematizador Snowball para
el español.

• Cambio de modelo de recuperación. Cambiar el modelo de recuperación. Las últimas
versiones de Lucene/ElasticSearch utilizan por defecto el modelo BM25, superior al clásico
TF-IDF de versiones previas, si bien, hay modelos que pueden obtener mejores resultados
todavía: uno es DFR (divergence from randomness). El modelo DFR requiere tres
componentes, en general, los valores utilizados por defecto son adecuados.

La colección de pruebas en español se ha extraído de las correspondientes a las conferencias CLEF,
consiste en 15.000 documentos, 25 consultas y los juicios de relevancia asociados. Los documentos
y consultas se encuentran en ficheros XML (efe01.xml a efe10.xml y topics.xml). Los juicios de
relevancia están en formato TREC en los ficheros qrels.txt y qrels_rel.txt (solo relevantes).

Se sugiere que cree varios índices, uno por cada enfoque, a los que debe añadir los documentos y
luego lanzar las búsquedas sobre ellos para poder obtener los ficheros de similitud en formato
TREC.

Para los documentos debe utilizar la concatenación de los campos TITLE y TEXT; para las
consultas debe utilizar la concatenación de los campos ES-title y ES-desc. El número máximo de
documentos por consulta que deben ser devueltos es 1000.

Se comprueba que algunas preguntas se comportan de manera muy diferente con algunos enfoques.
¿Podría explicar por qué?
