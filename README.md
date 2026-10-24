# Laboratorio N° 15 — Instalación y configuración de Apache Hadoop

Cluster Hadoop (HDFS + YARN + MapReduce) en modo pseudo-distribuido, desplegado con Docker Compose
(imágenes `bde2020/hadoop-*`, Hadoop 3.2.1). Se eligió Docker en vez de instalación nativa en Windows
porque Hadoop 3.x requiere oficialmente Java 8/11 (la máquina de desarrollo tiene Java 21) y porque
Docker hace el entorno reproducible en cualquier equipo del grupo con un solo comando.

## Estructura

```
hadoop-docker/
├── docker-compose.yml    # Define los 5 servicios del cluster
├── hadoop.env             # Configuración de HDFS/YARN/MapReduce (core-site, hdfs-site, yarn-site, mapred-site)
├── data/
│   └── don_quijote.txt    # Dataset real (2.2 MB, Project Gutenberg, dominio público) usado en el job wordcount
└── evidence/
    ├── render_terminal.py # Script que renderiza capturas de terminal (código+salida) a PNG para el PDF
    ├── spec_*.json         # Contenido (comando + salida real) de cada captura
    ├── img_*.png            # Capturas generadas, embebidas en el documento final
    └── build_doc.py        # Genera el Word completo (GLAB-S15-INTG-5-DESARROLLO.docx) con todas las secciones
```

## Componentes del cluster (docker-compose.yml)

| Servicio | Rol en la arquitectura |
|---|---|
| `namenode` | HDFS — metadata del sistema de archivos (qué bloques existen y dónde) |
| `datanode` | HDFS — almacenamiento físico de los bloques de datos |
| `resourcemanager` | YARN — asigna recursos (CPU/memoria) del cluster a las aplicaciones |
| `nodemanager` | YARN — ejecuta los contenedores de cómputo en el nodo |
| `historyserver` | Guarda el historial de jobs MapReduce ya ejecutados |

## Cómo correrlo

```bash
cd hadoop-docker
docker compose up -d
docker compose ps                 # esperar a que los 5 estén "healthy"
docker exec namenode jps          # ver el daemon NameNode activo
```

Cargar el dataset y correr el job de ejemplo (wordcount) sobre HDFS vía YARN:

```bash
docker exec namenode hdfs dfs -mkdir -p /user/root/input-quijote
docker exec namenode hdfs dfs -put /data/don_quijote.txt /user/root/input-quijote/
docker exec namenode hadoop jar /opt/hadoop-3.2.1/share/hadoop/mapreduce/hadoop-mapreduce-examples-3.2.1.jar \
    wordcount /user/root/input-quijote /user/root/output-quijote
docker exec namenode hdfs dfs -cat /user/root/output-quijote/part-r-00000
```

Resultado esperado (deterministico, mismo archivo): 38,059 líneas de entrada, 389,656 palabras totales,
39,755 palabras únicas. Top 3: `que` (19546), `de` (18133), `y` (15976).

## Incidente real durante el desarrollo (documentado en el PDF, sección 4.5)

La primera corrida del job se quedó congelada en `map 100% / reduce 0%` indefinidamente. Causa: `hadoop.env`
pedía `mapreduce.reduce.memory.mb=8192`, el 100% de la capacidad del único NodeManager (`Memory-Capacity:
8192MB` según `yarn node -status`), sin dejar espacio para el ApplicationMaster — YARN nunca podía asignar
ese contenedor. Se corrigió bajando `map` a 1024 MB y `reduce` a 1536 MB en `hadoop.env`, se recrearon
`resourcemanager` y `nodemanager` (`docker compose up -d --force-recreate resourcemanager nodemanager`), y
el job completó en segundos.

## Generación de evidencia para el PDF

`evidence/render_terminal.py` toma un JSON (`spec_*.json` con comando + salida real copiada de la terminal)
y genera un PNG estilo terminal. `evidence/build_doc.py` arma el `.docx` final insertando esas imágenes y
el texto de cada sección del laboratorio (SEMMA, arquitectura, aplicabilidad Big Data, reflexión de
desarrollo sostenible). Para regenerar todo:

```bash
cd hadoop-docker/evidence
for f in spec_*.json; do python render_terminal.py "$f" "${f/spec_/img_}.png"; done
python build_doc.py
```
