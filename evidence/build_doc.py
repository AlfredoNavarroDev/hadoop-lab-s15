# -*- coding: utf-8 -*-
"""Build the full Lab S15-D Word report (Hadoop/Big Data)."""
from docx import Document
from docx.shared import Pt, Inches, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = "GLAB-S15-INTG-5-DESARROLLO.docx"
EV = "."  # evidence images live alongside this script

BLUE = RGBColor(0x2E, 0x75, 0xB5)
DARK = RGBColor(0x22, 0x22, 0x22)


def set_cell_shading(cell, color_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:fill'), color_hex)
    tcPr.append(shd)


def h1(doc, text):
    p = doc.add_heading(level=1)
    run = p.add_run(text)
    run.font.color.rgb = BLUE
    run.font.size = Pt(16)
    return p


def h2(doc, text):
    p = doc.add_heading(level=2)
    run = p.add_run(text)
    run.font.color.rgb = DARK
    run.font.size = Pt(13)
    return p


def body(doc, text, bold=False, italic=False, size=11):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.size = Pt(size)
    p.paragraph_format.space_after = Pt(8)
    return p


def bullet(doc, text):
    p = doc.add_paragraph(style="List Bullet")
    run = p.add_run(text)
    run.font.size = Pt(11)
    return p


def code_line(doc, text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = "Consolas"
    run.font.size = Pt(9.5)
    p.paragraph_format.space_after = Pt(0)
    return p


def add_image(doc, path, caption, width_in=6.3):
    doc.add_picture(path, width=Inches(width_in))
    last = doc.paragraphs[-1]
    last.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = cap.add_run(caption)
    run.italic = True
    run.font.size = Pt(9.5)
    run.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
    cap.paragraph_format.space_after = Pt(14)


doc = Document()

# Base style
normal = doc.styles["Normal"]
normal.font.name = "Calibri"
normal.font.size = Pt(11)

# ---------- Portada ----------
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = title.add_run("LABORATORIO N° 15")
r.bold = True
r.font.size = Pt(26)
r.font.color.rgb = BLUE

sub = doc.add_paragraph()
sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = sub.add_run("Instalación y Configuración de Apache Hadoop\nHDFS · YARN · MapReduce")
r.font.size = Pt(14)

doc.add_paragraph()
body(doc, "Integrantes:", bold=True)
bullet(doc, "________________________________")
bullet(doc, "________________________________")
bullet(doc, "________________________________")
bullet(doc, "________________________________")

doc.add_paragraph()
h2(doc, "Indicaciones")
bullet(doc, "Subir el documento en PDF (imágenes de los códigos y salidas del resultado) a la plataforma.")
bullet(doc, "Subir el archivo de códigos (docker-compose.yml, hadoop.env, dataset) a la plataforma.")
bullet(doc, "Considerar la rúbrica de evaluación para el desarrollo del documento PDF.")

doc.add_page_break()

# ---------- Objetivo ----------
h1(doc, "1. Objetivo de la actividad")
body(doc,
     "Aplicar la metodología SEMMA (Sample, Explore, Modify, Model, Assess) para organizar y gestionar "
     "eficientemente los recursos materiales y humanos en un proyecto de Inteligencia de Negocios, "
     "implementando técnicas de gestión de proyectos de software que optimicen el proceso de instalación, "
     "configuración y análisis de datos sobre el framework Apache Hadoop.")

h1(doc, "2. Descripción")
body(doc,
     "En esta actividad se explora el proceso de instalación y configuración de herramientas clave del "
     "ecosistema Big Data, centrándose en Apache Hadoop. Se identifican sus componentes principales "
     "(HDFS, YARN, MapReduce), se comprende su arquitectura distribuida y su importancia en entornos de "
     "análisis de datos masivos, y se reflexiona sobre el impacto de estas tecnologías en la transformación "
     "digital de las organizaciones y en el desarrollo sostenible.")

# ---------- SEMMA ----------
h1(doc, "3. Metodología SEMMA aplicada a este proyecto")
body(doc,
     "SEMMA es la metodología de SAS para mineria de datos y proyectos de BI, estructurada en 5 fases. "
     "Se usó como marco de gestión para ordenar los pasos de instalación, configuración y validación del "
     "cluster Hadoop, en lugar de instalar componentes al azar:")

table = doc.add_table(rows=1, cols=3)
table.style = "Light Grid Accent 1"
hdr = table.rows[0].cells
hdr[0].text = "Fase"
hdr[1].text = "Qué significa"
hdr[2].text = "Aplicación en este laboratorio"
for c in hdr:
    set_cell_shading(c, "2E75B5")
    for p in c.paragraphs:
        for r in p.runs:
            r.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

rows = [
    ("Sample", "Definir la muestra de datos a usar", "Se probó primero con un dataset sintético pequeño (ventas por ciudad/producto) para validar el pipeline, y luego se reemplazó por una muestra real de volumen significativo: el texto completo de Don Quijote de la Mancha (Project Gutenberg, dominio público), 2.2 MB / 38,059 líneas."),
    ("Explore", "Explorar estructura y disponibilidad de los datos/recursos", "Verificación de que los 5 servicios del cluster (NameNode, DataNode, ResourceManager, NodeManager, HistoryServer) estuvieran activos (docker compose ps, jps) antes de cargar datos."),
    ("Modify", "Preparar/transformar datos y entorno para el análisis", "Ajuste de la configuración de recursos (hadoop.env): la primera corrida quedó colgada en reduce 0% porque se pidieron 8192 MB para el reducer en un nodo de 8192 MB de capacidad total; se corrigió a 1024/1536 MB para que YARN pudiera asignar el contenedor."),
    ("Model", "Aplicar el modelo/algoritmo de procesamiento", "Ejecución del job MapReduce wordcount sobre HDFS vía YARN (hadoop jar ... wordcount) sobre las 38,059 líneas del texto."),
    ("Assess", "Evaluar el resultado obtenido", "Lectura del resultado final en HDFS (part-r-00000) y validación de los contadores del job (Map input records=38,059, Reduce output records=39,755 palabras únicas, Job completed successfully)."),
]
for a, b_, c_ in rows:
    row = table.add_row().cells
    row[0].text = a
    row[1].text = b_
    row[2].text = c_
    for cell in row:
        for p in cell.paragraphs:
            for r in p.runs:
                r.font.size = Pt(9.5)
doc.add_paragraph()

# ---------- Instalacion ----------
h1(doc, "4. Instalación y configuración de Hadoop (evidencia)")
body(doc,
     "Se optó por desplegar Hadoop en modo pseudo-distribuido usando contenedores Docker (imágenes "
     "bde2020/hadoop-*, Hadoop 3.2.1) en lugar de una instalación nativa en Windows, por dos razones: "
     "(1) Hadoop 3.x requiere oficialmente Java 8/11 y la máquina de desarrollo tenía Java 21 instalado, lo "
     "que genera incompatibilidades; (2) Docker Compose hace el entorno reproducible en cualquier equipo del "
     "grupo con un solo comando (docker compose up -d), sin tocar la configuración del sistema operativo host.")

h2(doc, "4.1 Definición del cluster (docker-compose.yml)")
body(doc, "Servicios definidos: namenode, datanode, resourcemanager, nodemanager, historyserver — un nodo "
          "lógico para cada rol principal de la arquitectura distribuida.")
for line in [
    "services:",
    "  namenode:        # HDFS - metadata del sistema de archivos",
    "  datanode:        # HDFS - almacenamiento real de bloques",
    "  resourcemanager: # YARN - asignación de recursos del cluster",
    "  nodemanager:     # YARN - ejecución de contenedores/tareas",
    "  historyserver:   # Historial de jobs MapReduce",
]:
    code_line(doc, line)
doc.add_paragraph()

h2(doc, "4.2 Levantamiento del cluster y verificación de servicios")
add_image(doc, f"{EV}/img_01_compose.png",
          "Figura 1. Los 5 contenedores del cluster en estado healthy.")

h2(doc, "4.3 Verificación de daemons Java activos por nodo")
body(doc, "Cada contenedor corre exactamente el daemon que le corresponde según su rol en la arquitectura "
          "(un proceso Java por servicio), confirmado con jps:")
add_image(doc, f"{EV}/img_02_jps.png",
          "Figura 2. NameNode, DataNode, ResourceManager y NodeManager activos.")

h2(doc, "4.4 Carga de datos en HDFS")
body(doc, "Se crea el directorio de trabajo en HDFS y se sube un dataset de volumen real: el texto completo "
          "de 'Don Quijote de la Mancha' (edición en español de Project Gutenberg, dominio público), "
          "2,225,803 bytes (2.2 MB) en 38,059 líneas, para ser procesado por el job MapReduce.")
add_image(doc, f"{EV}/img_03_hdfs.png",
          "Figura 3. Dataset don_quijote.txt (2.2 MB) replicado y disponible en HDFS.")

h2(doc, "4.5 Incidente de configuración y corrección")
body(doc,
     "Al primer intento, el job quedó estancado en map 100% / reduce 0% de forma indefinida. Diagnóstico "
     "con yarn node -status: el NodeManager reportaba Memory-Capacity: 8192MB, pero hadoop.env solicitaba "
     "mapreduce.reduce.memory.mb=8192, es decir, el 100% de la capacidad del nodo solo para el reducer, sin "
     "dejar espacio para el ApplicationMaster. YARN nunca podía satisfacer esa reserva y el contenedor del "
     "reducer quedaba en espera eterna. Se corrigió bajando map a 1024 MB y reduce a 1536 MB, se recrearon "
     "resourcemanager y nodemanager, y el job se volvió a lanzar.")

h2(doc, "4.6 Ejecución del job MapReduce (wordcount) vía YARN")
add_image(doc, f"{EV}/img_04_job.png",
          "Figura 4. Job sobre las 38,059 líneas del texto: map 100% / reduce 100%, completado exitosamente.")
body(doc,
     "El job procesó 38,059 registros de entrada (líneas) y emitió 389,656 pares clave-valor en la fase "
     "Map (una por cada palabra encontrada). La fase Combine redujo eso a 39,755 claves únicas antes de "
     "enviarlas por la red al reducer (Reduce shuffle bytes=601,995, frente a Map output bytes=3,740,265 "
     "sin combinar) — evidencia directa de por qué el combiner importa en Hadoop: reduce el tráfico de red "
     "entre las fases Map y Reduce.")

h2(doc, "4.7 Resultado final")
add_image(doc, f"{EV}/img_05_result.png",
          "Figura 5. Top 15 palabras más frecuentes, de un total de 39,755 palabras únicas, leído desde HDFS.")
body(doc,
     "Las palabras más frecuentes son artículos, preposiciones y conjunciones ('que', 'de', 'y', 'la', 'a', "
     "'el'...), lo esperable en cualquier texto largo en español (stopwords). En un caso de negocio real, "
     "este mismo job —sin cambiar una línea de código— se aplicaría para contar términos relevantes "
     "(productos, quejas, menciones de marca) sobre millones de reseñas o tickets de soporte en vez de un "
     "libro.")

doc.add_page_break()

# ---------- Arquitectura ----------
h1(doc, "5. Arquitectura distribuida de Hadoop")
body(doc, "Hadoop se apoya en tres componentes que cubren roles distintos y se coordinan entre sí:")

h2(doc, "5.1 HDFS (Hadoop Distributed File System)")
bullet(doc, "NameNode: guarda el metadato (qué bloques existen y en qué DataNode viven); es el único punto "
            "que sabe la estructura del sistema de archivos, no almacena los datos en sí.")
bullet(doc, "DataNode: almacena físicamente los bloques de datos (por defecto 128 MB por bloque) y los "
            "replica (factor de replicación 3 en producción) para tolerar la caída de un nodo.")
bullet(doc, "En este laboratorio: ventas.txt se partió y almacenó como bloques en el DataNode, con el "
            "NameNode llevando el registro de su ubicación (visible en la UI web del puerto 9870).")

h2(doc, "5.2 YARN (Yet Another Resource Negotiator)")
bullet(doc, "ResourceManager: dueño global de los recursos del cluster (CPU/memoria); decide qué "
            "aplicación recibe qué contenedor y cuándo.")
bullet(doc, "NodeManager: agente local en cada nodo que reporta su capacidad disponible y ejecuta los "
            "contenedores que el ResourceManager le asigna.")
bullet(doc, "En este laboratorio: el ResourceManager asignó primero un contenedor para el "
            "ApplicationMaster del job, luego uno para el mapper y uno para el reducer, todo dentro de los "
            "8192 MB que el NodeManager reportaba como capacidad (evidencia directa del incidente de la "
            "sección 4.5).")

h2(doc, "5.3 MapReduce")
bullet(doc, "Fase Map: procesa cada bloque de entrada en paralelo y emite pares clave-valor (en wordcount: "
            "cada palabra → 1).")
bullet(doc, "Fase Shuffle & Sort: agrupa automáticamente todos los valores que comparten la misma clave.")
bullet(doc, "Fase Reduce: agrega los valores por clave (en wordcount: suma las ocurrencias) y escribe el "
            "resultado final en HDFS.")
bullet(doc, "En este laboratorio: Map input records=5 (las 5 líneas del archivo), Map output records=50 "
            "(cada palabra emitida), Reduce output records=9 (las 9 palabras únicas con su conteo final).")

h2(doc, "5.4 Cómo interactúan los tres componentes")
body(doc,
     "El flujo real observado fue: (1) el cliente sube el archivo a HDFS, que lo trocea en bloques vía "
     "NameNode/DataNode; (2) al lanzar el job, YARN (ResourceManager) negocia con el NodeManager los "
     "contenedores de cómputo necesarios; (3) MapReduce ejecuta las tareas Map y Reduce dentro de esos "
     "contenedores, leyendo los bloques directamente del DataNode (procesamiento cerca del dato, no al "
     "revés); (4) el resultado final se escribe de vuelta en HDFS. HDFS resuelve el ÓNDE están los datos, "
     "YARN resuelve el QUIÉN y CUÁNTO recurso se usa, y MapReduce resuelve el QUÉ cálculo se hace — "
     "ninguno de los tres reemplaza a los otros dos.")

doc.add_page_break()

# ---------- Aplicabilidad ----------
h1(doc, "6. Aplicabilidad de Hadoop en procesamiento de datos masivos")
body(doc,
     "Hadoop resuelve un problema que las bases de datos relacionales tradicionales no resuelven bien: "
     "procesar volúmenes de datos que no caben ni se procesan en tiempo razonable en una sola máquina. Su "
     "ventaja no es que sea 'más rápido' por nodo, sino que escala horizontalmente (agregar más máquinas "
     "baratas) en lugar de verticalmente (una máquina cada vez más cara).")

h2(doc, "6.1 Casos de uso reales")
bullet(doc, "Retail/e-commerce: análisis de clickstream y logs de transacciones para detectar patrones de "
            "compra a escala de todo el catálogo y toda la base de clientes (el mismo tipo de conteo que "
            "hicimos por ciudad/producto, pero sobre millones de registros).")
bullet(doc, "Telecomunicaciones: procesamiento de registros de llamadas (CDR) para detección de fraude y "
            "optimización de red.")
bullet(doc, "Salud/genómica: procesamiento distribuido de secuencias genómicas, demasiado grandes para "
            "memoria de un solo servidor.")
bullet(doc, "Finanzas: análisis de riesgo y detección de fraude sobre historiales transaccionales masivos.")

h2(doc, "6.2 Por qué Hadoop y no solo una base de datos más grande")
body(doc,
     "Una base de datos relacional escala verticalmente y asume que los datos caben en un esquema fijo con "
     "consistencia fuerte; eso la vuelve costosa y limitada frente a petabytes de datos semi/no "
     "estructurados (logs, texto, sensores). Hadoop acepta datos en su formato crudo (schema-on-read), "
     "reparte el costo de cómputo entre muchos nodos baratos y tolera la caída de nodos individuales sin "
     "perder el trabajo completo — algo que el laboratorio evidenció a escala pequeña con la replicación "
     "de bloques en HDFS y la reasignación de contenedores por YARN.")

doc.add_page_break()

# ---------- Sostenibilidad ----------
h1(doc, "7. Reflexión: impacto de Big Data / Hadoop en el desarrollo sostenible")

h2(doc, "7.1 Beneficios")
bullet(doc, "Eficiencia energética: análisis de datos de sensores IoT en redes eléctricas inteligentes "
            "(smart grids) permite predecir demanda y reducir desperdicio de energía; esto solo es viable "
            "procesando volúmenes masivos de lecturas en tiempo casi real, exactamente el tipo de carga para "
            "la que HDFS+YARN+MapReduce fueron diseñados.")
bullet(doc, "Gestión de recursos naturales: agricultura de precisión (sensores de humedad, clima, "
            "imágenes satelitales) procesada a escala Big Data reduce el uso de agua y fertilizantes.")
bullet(doc, "Salud pública: cruce de datos epidemiológicos masivos para detección temprana de brotes y "
            "optimización de la distribución de recursos médicos.")
bullet(doc, "Escalar con hardware básico (commodity hardware) en lugar de servidores especializados "
            "costosos reduce la barrera de entrada para que organizaciones pequeñas accedan a análisis de "
            "datos avanzado.")

h2(doc, "7.2 Desafíos éticos y de sostenibilidad")
bullet(doc, "Consumo energético de los propios centros de datos: un cluster Hadoop a escala real son "
            "cientos o miles de servidores corriendo 24/7; el beneficio ambiental de optimizar un proceso "
            "externo puede verse contrarrestado por el costo energético de la infraestructura que lo "
            "calcula, si no se usa hardware eficiente ni energía renovable en el datacenter.")
bullet(doc, "Huella de almacenamiento: HDFS replica cada bloque (típicamente 3 veces) para tolerar fallos; "
            "esa redundancia multiplica el espacio físico y el consumo eléctrico asociado a guardar los "
            "mismos datos tres veces.")
bullet(doc, "Privacidad y sesgo: procesar datos masivos de personas (ubicación, consumo, salud) sin "
            "gobierno de datos adecuado puede derivar en vigilancia o decisiones automáticas sesgadas que "
            "afectan de forma desigual a distintos grupos.")

h2(doc, "7.3 Postura y compromiso personal")
p = body(doc,
     "[Espacio para completar con la voz del equipo — ejemplo de punto de partida a parafrasear:] "
     "Como futuros profesionales de Inteligencia de Negocios, el compromiso no es solo saber instalar y "
     "operar herramientas como Hadoop, sino decidir CUÁNDO usarlas: un cluster distribuido sobredimensionado "
     "para un problema que cabe en una sola máquina desperdicia energía sin necesidad. Aplicar Big Data de "
     "forma responsable implica dimensionar la infraestructura al problema real (como se tuvo que corregir "
     "en este mismo laboratorio al ajustar la memoria del cluster), preferir proveedores de nube con energía "
     "renovable, y tratar los datos personales dentro de esos sistemas masivos con los mismos estándares "
     "éticos que se exigirían en una base de datos pequeña.")
for r in p.runs:
    r.italic = True

doc.add_page_break()

# ---------- Rubrica ----------
h1(doc, "8. Anexo — Rúbrica de evaluación considerada")
rtable = doc.add_table(rows=1, cols=2)
rtable.style = "Light Grid Accent 1"
hdr = rtable.rows[0].cells
hdr[0].text = "Criterio"
hdr[1].text = "Sección de este documento que lo cubre"
for c in hdr:
    set_cell_shading(c, "2E75B5")
    for p in c.paragraphs:
        for r in p.runs:
            r.bold = True
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
rub = [
    ("Instalación y configuración de Hadoop", "Sección 4 (instalación + incidente de memoria diagnosticado y resuelto)"),
    ("Comprensión de la arquitectura distribuida", "Sección 5 (HDFS / YARN / MapReduce y su interacción)"),
    ("Aplicabilidad en procesamiento de datos masivos", "Sección 6 (casos de uso + por qué Hadoop)"),
    ("Reflexión crítica sobre desarrollo sostenible", "Sección 7 (beneficios, desafíos y compromiso personal)"),
]
for a, b_ in rub:
    row = rtable.add_row().cells
    row[0].text = a
    row[1].text = b_

doc.save(OUT)
print("saved", OUT)
