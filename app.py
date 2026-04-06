import streamlit as st
import pandas as pd
import tempfile
import os
import io
import folium
from streamlit_folium import st_folium
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components

# Importar el backend (con manejo de errores por si fallan librerías no instaladas)
try:
    from backend.nlp_module import NLPProcessor
    nlp_proc = NLPProcessor()
except Exception as e:
    nlp_proc = None
    st.error(f"Error crítico cargando módulo NLP: {str(e)}")

try:
    from backend.document_parser import DocumentParser
except ImportError as e:
    DocumentParser = None
    st.error(f"Error cargando el parser de documentos: {e}")

try:
    from backend.spatial_module import SpatialProcessor
    spa_proc = SpatialProcessor()
except Exception as e:
    spa_proc = None
    st.error(f"Error cargando módulo Espacial: {e}")

try:
    from backend.stats_module import StatsProcessor
    stat_proc = StatsProcessor()
except Exception as e:
    stat_proc = None

try:
    from backend.ocr_engine import OCREngine
    from backend.export_module import DataExporter
    ocr_engine = OCREngine()
except Exception as e:
    ocr_engine = None
    st.warning(f"Motor OCR no disponible (instala dependencias OCR): {e}")

# Configuración inicial de la página (estética del laboratorio)
st.set_page_config(page_title="SocEnv Lab | Métodos Mixtos", page_icon="🔬", layout="wide")

# CSS personalizado para mejorar estética
st.markdown("""
    <style>
    .main {background-color: #f7fbff;}
    h1 {color: #1a365d; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;}
    .stButton>button {background-color: #2c5282; color: white; border-radius: 8px;}
    .stButton>button:hover {background-color: #2a4365; border-color: #2a4365;}
    </style>
""", unsafe_allow_html=True)

import json

# Barra lateral para navegación
st.sidebar.title("🔬 SocEnv Lab")
st.sidebar.markdown("Plataforma Open-Source para Investigación Social y Ambiental.")

# Gestión de Workspaces (Directorio base)
WORKSPACES_DIR = "workspaces"
if not os.path.exists(WORKSPACES_DIR):
    os.makedirs(WORKSPACES_DIR)

st.sidebar.markdown("---")
st.sidebar.subheader("📂 Espacio de Trabajo (Proyecto)")
workspaces_disponibles = [d for d in os.listdir(WORKSPACES_DIR) if os.path.isdir(os.path.join(WORKSPACES_DIR, d))]
if not workspaces_disponibles:
    workspaces_disponibles = ["Default"]
    os.makedirs(os.path.join(WORKSPACES_DIR, "Default"))

workspace_actual = st.sidebar.selectbox("Proyecto Actual:", workspaces_disponibles, index=0)

nuevo_ws = st.sidebar.text_input("Crear Nuevo Proyecto:")
if st.sidebar.button("Crear Proyecto"):
    if nuevo_ws and nuevo_ws not in workspaces_disponibles:
        os.makedirs(os.path.join(WORKSPACES_DIR, nuevo_ws))
        st.sidebar.success(f"Creado: {nuevo_ws}")
        st.rerun()

st.session_state["workspace"] = workspace_actual
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Selecciona una herramienta:",
    [
        "🏠 Inicio",
        "📝 Procesamiento NLP (Automático)",
        "🧠 Codificación Avanzada (Manual/NVivo)",
        "🌍 Análisis Espacial (QGIS)",
        "📊 Métodos Mixtos (R)",
        "🔍 OCR Multi-Motor (Documentos Degradados)",
    ]
)

if menu == "🏠 Inicio":
    st.title("Bienvenido al Laboratorio de Investigación")
    st.markdown("""
    Este laboratorio integra tres motores de procesamiento bajo una única interfaz amigable:
    * **Spacy/NLTK (Python)** para el procesamiento de lenguaje natural cualitativo.
    * **GeoPandas/PyQGIS** para la representación del territorio.
    * **R Project** cruzando los datos para pruebas estadísticas complejas.
    
    Selecciona un módulo en la barra de la izquierda para comenzar a investigar.
    """)

elif menu == "📝 Procesamiento NLP (Automático)":
    st.title("Análisis Cualitativo (NLP)")
    st.write("Sube múltiples documentos (PDFs, Word, PPTX, Excel, CSV, TXT) o archivos de Audio/Video (MP3, WAV, MP4) para transformarlos en texto analizable y extraer información semántica (Transcribe automáticamente con Whisper).")
    
    # Campo para subir múltiples archivos
    archivos_subidos = st.file_uploader(
        "Selecciona uno o más archivos de tu investigación:", 
        accept_multiple_files=True,
        type=['pdf', 'docx', 'pptx', 'xlsx', 'xls', 'csv', 'txt', 'mp3', 'wav', 'm4a', 'mp4']
    )
    
    texto_usuario = st.text_area("Opcional: Añade texto libre adicional aquí:", height=100)
    
    if st.button("Procesar Corpus Documental"):
        if not nlp_proc:
            st.error("El modelo de lenguaje (NLP) no está disponible.")
            st.stop()
            
        corpus_completo = texto_usuario # Empezamos con el texto manual si lo hay
        
        # Procesar todos los archivos subidos si existen
        Textos_Individuales = [] # Guardaremos textos por documento para Topic Modeling
        
        if archivos_subidos and DocumentParser:
            with st.spinner("Moliendo y convirtiendo documentos/audios a texto puro..."):
                textos_extraidos = []
                for archivo in archivos_subidos:
                    # Parsear cada documento
                    texto = DocumentParser.extract_text(archivo, filename=archivo.name)
                    textos_extraidos.append(f"--- Documento: {archivo.name} ---\n{texto}\n")
                    if texto and len(texto.strip()) > 50:
                        Textos_Individuales.append(texto)
                
                # Unir todos para el análisis NLP
                corpus_completo += "\n" + "\n".join(textos_extraidos)
                st.success(f"Se fusionaron y/o transcribieron {len(archivos_subidos)} elementos con éxito.")
                
        if len(corpus_completo.strip()) > 0:
            st.info("Iniciando análisis de procesamiento del lenguaje natural (NLP) profundo...")
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Entidades Clave Encontradas")
                # Spacy tiene un límite razonable; para corpus inmensos se debe truncar, 
                # pero para este contexto podemos pasar el max_length:
                nlp_proc.nlp.max_length = len(corpus_completo) + 10000 
                try:
                    df_ent = nlp_proc.extract_entities(corpus_completo)
                    if not df_ent.empty:
                        st.dataframe(df_ent, use_container_width=True)
                    else:
                        st.info("No se encontraron entidades nombradas.")
                except Exception as e:
                    st.error(f"Error extrayendo entidades: {e}")
                    
            with col2:
                st.subheader("Frecuencia de Palabras")
                try:
                    df_freq = nlp_proc.word_frequencies(corpus_completo)
                    if not df_freq.empty:
                        st.dataframe(df_freq.head(100), use_container_width=True)
                    else:
                        st.info("Sin palabras suficientes tras limpiar.")
                except Exception as e:
                    st.error(f"Error analizando frecuencias: {e}")
                    
            st.markdown("---")
            col3, col4 = st.columns(2)
            with col3:
                st.subheader("☁️ Nube de Palabras")
                try:
                    fig_wc = nlp_proc.generate_wordcloud(corpus_completo)
                    st.pyplot(fig_wc)
                except Exception as e:
                    st.warning(f"No se pudo generar Nube de Palabras: {e}")
                    
            with col4:
                st.subheader("🎭 Análisis de Sentimiento Global")
                try:
                    sent = nlp_proc.analyze_sentiment(corpus_completo)
                    st.metric(label="Polaridad (Negativo -1 a 1 Positivo)", value=round(sent["Polaridad"], 3))
                    st.metric(label="Subjetividad (0 Objetivo a 1 Subjetivo)", value=round(sent["Subjetividad"], 3))
                    st.progress(max(0, min(100, int((sent["Polaridad"] + 1) * 50)))) # Barra visual 0-100% (Neutral en 50)
                except Exception as e:
                    st.warning(f"No se pudo analizar sentimiento: {e}")
                    
            st.markdown("---")
            st.subheader("🧠 Modelado Asistido de Temas (BERTopic)")
            if len(Textos_Individuales) >= 5:
                # Si el usuario subió varios pedazos podemos hacer topic modeling
                try:
                    with st.spinner("Entrenando Modelo de Tópicos (Puede Tardar)..."):
                        df_topics = nlp_proc.topic_modeling(Textos_Individuales)
                        st.dataframe(df_topics, use_container_width=True)
                except Exception as e:
                    st.error(f"Error en Topic Modeling: {e}")
            else:
                st.info("Se requieren al menos 5 documentos cargados por separado para realizar el modelado estadístico y extracción de Temas subyacentes.")
                    
            with st.expander("Ver Corpus de Texto Completo Generado / Transcrito"):
                st.text(corpus_completo)
                
        else:
            st.warning("Por favor, sube archivos o escribe texto para analizar.")

elif menu == "🧠 Codificación Avanzada (Manual/NVivo)":
    st.title("🧠 Módulo Cualitativo Avanzado")
    st.write("Emulación de NVivo / ATLAS.ti: Crea tu Libro de Códigos, asocia fragmentos de texto y recupera tus citas.")

    # 1. Gestión de Persistencia en Disco según Workspace actual
    ws_path = os.path.join("workspaces", st.session_state["workspace"])
    codebook_path = os.path.join(ws_path, "codebook.json")
    quotes_path = os.path.join(ws_path, "quotes.csv")

    # Si cambiamos de workspace o es la primera vez en la sesión actual, cargar desde disco
    if "current_ws_loaded" not in st.session_state or st.session_state["current_ws_loaded"] != st.session_state["workspace"]:
        if os.path.exists(codebook_path):
            with open(codebook_path, "r", encoding="utf-8") as f:
                st.session_state["codebook"] = json.load(f)
        else:
            st.session_state["codebook"] = []
            
        if os.path.exists(quotes_path):
            st.session_state["quotes"] = pd.read_csv(quotes_path)
        else:
            st.session_state["quotes"] = pd.DataFrame(columns=["Documento", "Fragmento", "Codigo", "Comentario"])
            
        st.session_state["doc_actual"] = ""
        st.session_state["nombre_doc"] = "Sin_Cargar"
        st.session_state["current_ws_loaded"] = st.session_state["workspace"]

    # Controles Globales para guardar
    col_g1, col_g2 = st.columns([8, 2])
    with col_g2:
        if st.button("💾 Guardar Proyecto en Disco", help="Fuerza el guardado del Codebook y las Citas construidas."):
            with open(codebook_path, "w", encoding="utf-8") as f:
                json.dump(st.session_state["codebook"], f, ensure_ascii=False, indent=4)
            st.session_state["quotes"].to_csv(quotes_path, index=False, encoding="utf-8")
            st.success("Guardado en Disco Exitosamente.")
    st.write("---")

    # 2. Divide la pantalla: Izquierda (Documento y Codificación) | Derecha (Libro de códigos y Citas)
    col_izq, col_der = st.columns([6, 4])

    with col_izq:
        st.subheader("1. Carga de Documento a Codificar")
        arch_upload = st.file_uploader("Sube un documento (PDF, Word, TXT, etc.)", type=['pdf', 'docx', 'txt'])
        
        if st.button("Cargar Documento al Entorno"):
            if arch_upload and DocumentParser:
                with st.spinner("Parseando..."):
                    texto_leido = DocumentParser.extract_text(arch_upload, arch_upload.name)
                    st.session_state["doc_actual"] = texto_leido
                    st.session_state["nombre_doc"] = arch_upload.name
                st.success(f"Documento '{arch_upload.name}' cargado para codificación.")
            else:
                st.warning("No hay documento o parser.")

        st.markdown("---")
        st.subheader("2. Texto y Asignación de Códigos")
        if st.session_state["doc_actual"]:
            st.info(f"📄 Trabajando en: **{st.session_state['nombre_doc']}**")
            
            # Formulario para codificar un fragmento
            with st.form("form_codificacion"):
                fragmento_seleccionado = st.text_area("Copia y pega aquí el fragmento a codificar (Quote):", height=150)
                codigos_seleccionados = st.multiselect("Asigna Códigos (Elige del Codebook):", st.session_state["codebook"])
                comentario = st.text_input("Comentario/Memo analítico (opcional):")
                
                submitted = st.form_submit_button("Guardar Cita (Codificar)")
                if submitted:
                    if not fragmento_seleccionado.strip():
                        st.error("Debes pegar un fragmento.")
                    elif not codigos_seleccionados:
                        st.error("Debes seleccionar al menos un código.")
                    else:
                        # Guardar la cita para cada código asociado
                        nuevas_citas = []
                        for code in codigos_seleccionados:
                            nuevas_citas.append({
                                "Documento": st.session_state["nombre_doc"],
                                "Fragmento": fragmento_seleccionado,
                                "Codigo": code,
                                "Comentario": comentario
                            })
                        
                        df_nuevas = pd.DataFrame(nuevas_citas)
                        st.session_state["quotes"] = pd.concat([st.session_state["quotes"], df_nuevas], ignore_index=True)
                        st.success("¡Fragmento codificado correctamente!")
            
            with st.expander("Ver Documento Completo", expanded=False):
                st.text(st.session_state["doc_actual"])
        else:
            st.write("Carga un documento arriba para comenzar a leer.")

    with col_der:
        st.subheader("Libro de Códigos (Codebook)")
        nuevo_codigo = st.text_input("Crear Nuevo Código:")
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("Añadir Código Manual"):
                if nuevo_codigo and nuevo_codigo not in st.session_state["codebook"]:
                    st.session_state["codebook"].append(nuevo_codigo)
                    st.success(f"Código '{nuevo_codigo}' añadido.")
                else:
                    st.warning("El código ya existe o está vacío.")
                    
        with col_btn2:
            if st.button("✨ Autogenerar (IA)"):
                if st.session_state["doc_actual"] and nlp_proc:
                    with st.spinner("Analizando texto para sugerencias..."):
                        try:
                            # Autogenerar basado en las 10 entidades/palabras más frecuentes
                            df_freq = nlp_proc.word_frequencies(st.session_state["doc_actual"])
                            if not df_freq.empty:
                                top_words = df_freq.head(10)['Word'].tolist()
                                agregados = 0
                                for w in top_words:
                                    codigo_sug = w.capitalize()
                                    if codigo_sug not in st.session_state["codebook"]:
                                        st.session_state["codebook"].append(codigo_sug)
                                        agregados += 1
                                if agregados > 0:
                                    st.success(f"{agregados} códigos sugeridos añadidos.")
                                else:
                                    st.info("Sin códigos nuevos sugeridos.")
                            else:
                                st.warning("No hay suficiente texto para sugerir.")
                        except Exception as e:
                            st.error(f"Error en IA: {e}")
                else:
                    st.warning("Carga un documento primero.")
        
        st.write("---")
        st.write("**Lista de Códigos Activos:**")
        if st.session_state["codebook"]:
            for c in st.session_state["codebook"]:
                # Calcular frecuencias
                freq = len(st.session_state["quotes"][st.session_state["quotes"]["Codigo"] == c])
                st.markdown(f"- 🏷️ {c} *(Citas: {freq})*")
        else:
            st.info("Aún no tienes códigos.")

        st.markdown("---")
        st.subheader("Citas Recuperadas (Quotes)")
        filtro_codigo = st.selectbox("Filtrar por Código:", ["Todos"] + st.session_state["codebook"])
        
        df_quotes = st.session_state["quotes"]
        if not df_quotes.empty:
            if filtro_codigo != "Todos":
                df_mostrar = df_quotes[df_quotes["Codigo"] == filtro_codigo]
            else:
                df_mostrar = df_quotes
                
            st.dataframe(df_mostrar[["Fragmento", "Codigo", "Documento", "Comentario"]], use_container_width=True)
            
            # Exportar proyecto
            csv = df_quotes.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Exportar Proyecto Cualitativo (CSV)",
                data=csv,
                file_name='proyecto_cualitativo_export.csv',
                mime='text/csv',
            )

            # Exportar a Excel (codebook + citas + matriz)
            from backend.export_module import DataExporter
            excel_bytes = DataExporter.codebook_to_excel_bytes(
                st.session_state.get("codebook", []),
                df_quotes
            )
            if excel_bytes:
                st.download_button(
                    label="📥 Exportar Proyecto Cualitativo (Excel multi-hoja)",
                    data=excel_bytes,
                    file_name='proyecto_cualitativo_export.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                )
        else:
            st.info("Aún no has codificado ningún fragmento.")
            
        st.markdown("---")
        st.subheader("🕸️ Red Semántica de Co-ocurrencia")
        st.write("Visualiza cómo se relacionan los códigos (ocurrencia en el mismo documento).")
        if st.button("Generar Red Semántica"):
            if len(df_quotes) > 0:
                with st.spinner("Construyendo grafo..."):
                    # Crear Grafo
                    G = nx.Graph()
                    # Añadir Nodos
                    for c in st.session_state["codebook"]:
                        G.add_node(c, label=c, title=f"Código: {c}", size=20)
                        
                    # Agrupar por Documento para encontrar co-ocurrencias
                    docs_group = df_quotes.groupby("Documento")["Codigo"].apply(list)
                    for codes_in_doc in docs_group:
                        unique_codes = list(set(codes_in_doc))
                        for i in range(len(unique_codes)):
                            for j in range(i+1, len(unique_codes)):
                                c1, c2 = unique_codes[i], unique_codes[j]
                                if G.has_edge(c1, c2):
                                    G[c1][c2]['weight'] += 1
                                else:
                                    G.add_edge(c1, c2, weight=1)
                    
                    # Usar PyVis para interactividad
                    net = Network(height="400px", width="100%", bgcolor="#ffffff", font_color="black")
                    net.from_nx(G)
                    
                    # Generar HTML en archivo temporal
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpHtml:
                        net.save_graph(tmpHtml.name)
                        HtmlFile = open(tmpHtml.name, 'r', encoding='utf-8')
                        source_code = HtmlFile.read() 
                        components.html(source_code, height=420)
                        
            else:
                st.warning("Se requieren citas codificadas para construir la red.")

        st.markdown("---")
        st.subheader("📊 Matriz de Métodos Mixtos")
        st.write("Frecuencia de códigos cruzados por documento.")
        if len(df_quotes) > 0:
            matriz = pd.crosstab(df_quotes['Documento'], df_quotes['Codigo'])
            st.dataframe(matriz, use_container_width=True)
            # Mapa de calor simple en texto o con pandas
            st.info("Pista: Esta matriz puede ser enviada al Módulo R para análisis de correspondencia o componentes principales.")


elif menu == "🌍 Análisis Espacial (QGIS)":
    st.title("Análisis Espacial")
    st.write("Geoprocesamientos automatizados en tus archivos shape o geojson.")
    
    upload_gdf = st.file_uploader("Sube un archivo GeoJSON", type=['geojson'])
    if upload_gdf and spa_proc:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".geojson") as tmp:
            tmp.write(upload_gdf.getvalue())
            tmp_path = tmp.name
        
        try:
            gdf = spa_proc.load_vector_data(tmp_path)
            st.success("Archivo cargado con éxito.")
            stats = spa_proc.get_summary_stats(gdf)
            st.json(stats)
            
            # Simple render
            st.subheader("Vista en Mapa")
            if not gdf.crs or gdf.crs.is_geographic:
                m = folium.Map(location=[0, 0], zoom_start=2)
                folium.GeoJson(gdf).add_to(m)
                st_folium(m, width=700, height=500)
            else:
                st.write("Proyecta tu capa a lat/lon para verla en el mapa web, o haz un plot estático.")
                st.pyplot(gdf.plot().figure)
                
            distancia_buffer = st.slider("Crear Buffer (Distancia)", 0, 1000, 50)
            if st.button("Ejecutar Buffer"):
                buf_gdf = spa_proc.calculate_buffer(gdf, distancia_buffer)
                st.success("Buffer creado exitosamente.")
                st.pyplot(buf_gdf.plot().figure)
        except Exception as e:
            st.error(f"Error procesando el archivo espacial: {e}")
        finally:
            os.remove(tmp_path)

elif menu == "📊 Métodos Mixtos (R)":
    st.title("Motor Estadístico Bivariado (R)")
    if stat_proc:
        st.success("El Motor R está conectado (rpy2 funcionando).")
        st.write("Genera una tabla de datos combinada (ej. CSV de encuestas territoriales).")
        
        # DataFrame de Prueba integrado por simplicidad en la UI
        st.write("Usando Dataset Demográfico de prueba...")
        df_test = pd.DataFrame({
            'Satisfaccion': [5, 4, 3, 5, 2, 4, 5, 2, 1, 3],
            'Grupo': ['Urbano', 'Urbano', 'Rural', 'Urbano', 'Rural', 'Urbano', 'Rural', 'Rural', 'Rural', 'Urbano'],
            'Edad': [25, 30, 22, 40, 35, 28, 50, 42, 60, 29]
        })
        st.dataframe(df_test.head(3))
        
        formula = st.text_input("Ingresa la fórmula para el modelo Lineal (lm en R)", "Satisfaccion ~ Grupo + Edad")
        if st.button("Correr Modelo de R"):
            try:
                resultados = stat_proc.run_linear_model(df_test, formula)
                st.text_area("Resultados de la Regresión (R Summary)", resultados, height=300)
            except Exception as e:
                st.error(f"Error de R: {e}")
    else:
        st.error("No se pudo iniciar el conector R. Verifica que R esté instalado correctamente en Windows.")


# =====================================================================
# SECCIÓN: OCR MULTI-MOTOR
# =====================================================================
elif menu == "🔍 OCR Multi-Motor (Documentos Degradados)":
    st.title("🔍 Reconstrucción Documental OCR")
    st.markdown("""
    Procesa PDFs degradados o escaneados con **tres motores OCR en paralelo**, elige el mejor
    resultado automáticamente y permite exportar a Word/Excel.

    **Motores disponibles:**
    | Motor | Descripción | Requiere |
    |-------|-------------|----------|
    | PyMuPDF nativo | Extraccion de texto incrustado (instantáneo) | `pymupdf` |
    | Tesseract | OCR clásico, muy estable | `tesseract` + `pytesseract` |
    | EasyOCR | Deep learning, mejor en degradados | `easyocr` + `torch` |
    """)

    # Diagnistico de motores
    if ocr_engine:
        with st.expander("⚙️ Estado de los motores OCR", expanded=False):
            diagnostics = ocr_engine.run_diagnostics()
            for line in diagnostics:
                st.write(line)

        # Upload de PDF
        uploaded_pdf = st.file_uploader(
            "Sube tu PDF (puede ser degradado, escaneado, o con ruido de fotocopia):",
            type=["pdf"]
        )

        if uploaded_pdf:
            col_a, col_b = st.columns(2)
            with col_a:
                total_hint = st.number_input("Total de páginas del PDF (aproximado)", min_value=1, value=10, step=1)
            with col_b:
                page_range_str = st.text_input(
                    "Páginas a procesar (ej. 1,2,5 o 1-3):",
                    value="1,2,3"
                )

            # Parsear rango de páginas
            def _parse_pages(s):
                pages = set()
                for part in s.split(","):
                    part = part.strip()
                    if "-" in part:
                        a, _, b = part.partition("-")
                        try:
                            pages.update(range(int(a.strip()), int(b.strip()) + 1))
                        except ValueError:
                            pass
                    elif part.isdigit():
                        pages.add(int(part))
                return sorted(pages)

            page_range = _parse_pages(page_range_str)
            st.caption(f"Páginas seleccionadas: {page_range}")

            if st.button("🔍 Procesar PDF", type="primary"):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                    tmp_pdf.write(uploaded_pdf.getvalue())
                    tmp_pdf_path = tmp_pdf.name

                try:
                    with st.spinner("Procesando páginas con los motores OCR disponibles..."):
                        results = ocr_engine.process_pdf(tmp_pdf_path, page_range=page_range)
                    st.session_state["ocr_results"] = results
                    st.success(f"Se procesaron {len(results)} páginas.")
                except Exception as exc:
                    st.error(f"Error durante el OCR: {exc}")
                finally:
                    os.remove(tmp_pdf_path)

        # Mostrar resultados
        if "ocr_results" in st.session_state and st.session_state["ocr_results"]:
            results = st.session_state["ocr_results"]

            st.markdown("---")
            st.subheader("📊 Resumen de calidad por página")

            # Tabla resumen de scores
            score_rows = []
            for r in results:
                row = {"Página": r["page"], "Mejor Motor": r["best_engine"],
                       "Score": round(r["best_score"], 3), "Combinado": r.get("combined", False)}
                row.update({f"score_{k}": round(v, 3) for k, v in r.get("score_summary", {}).items()})
                score_rows.append(row)
            st.dataframe(pd.DataFrame(score_rows), use_container_width=True)

            # Advertencias de baja calidad
            low_quality = [r for r in results if r["best_score"] < 0.15]
            if low_quality:
                st.warning(
                    f"⚠️ {len(low_quality)} página(s) con calidad baja (score < 0.15): "
                    f"{[r['page'] for r in low_quality]}. "
                    "Puede que sean imágenes, páginas en blanco o documentos muy degradados."
                )

            # Ver texto por página
            st.markdown("---")
            st.subheader("📄 Texto extraído por página")
            for r in results:
                label = (f"Página {r['page']} — motor: {r['best_engine']} — "
                         f"score: {r['best_score']:.3f}"
                         + (" — [COMBINADO]") if r.get("combined") else "")
                with st.expander(label):
                    if r.get("warning"):
                        st.warning(r["warning"])

                    st.text_area("Texto extraído:", value=r.get("best_text", ""),
                                 height=200, key=f"ocr_txt_{r['page']}")

                    # Comparativa de motores
                    st.markdown("**Comparativa de motores:**")
                    for eng_name, eng_result in r.get("results_by_engine", {}).items():
                        sc = eng_result.get("score", 0)
                        avail = eng_result.get("available", False)
                        err = eng_result.get("error")
                        if not avail:
                            st.write(f"  - `{eng_name}`: **no disponible** — {err or ''}")
                        elif err:
                            st.write(f"  - `{eng_name}`: **error** — {err}")
                        else:
                            preview = str(eng_result.get("text", ""))[:150].replace("\n", " ")
                            st.write(f"  - `{eng_name}` (score {sc:.3f}): {preview}...")

            # Exportaciones
            st.markdown("---")
            st.subheader("📥 Exportar resultados")
            from backend.export_module import DataExporter

            col_exp1, col_exp2, col_exp3 = st.columns(3)

            with col_exp1:
                excel_bytes = DataExporter.ocr_results_to_excel_bytes(results)
                if excel_bytes:
                    st.download_button(
                        label="📊 Excel (Resumen + Scores)",
                        data=excel_bytes,
                        file_name="ocr_resultados.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )

            with col_exp2:
                word_bytes = DataExporter.to_word_bytes(
                    results, title=f"Resultados OCR — {uploaded_pdf.name if 'uploaded_pdf' in dir() else 'documento'}"
                )
                if word_bytes:
                    st.download_button(
                        label="📄 Word (Informe narrativo)",
                        data=word_bytes,
                        file_name="ocr_informe.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    )

            with col_exp3:
                csv_bytes = DataExporter.to_csv_bytes(
                    [{"pagina": r["page"], "motor": r["best_engine"],
                      "score": r["best_score"], "texto": r["best_text"]} for r in results]
                )
                st.download_button(
                    label="📄 CSV (Texto plano)",
                    data=csv_bytes,
                    file_name="ocr_texto.csv",
                    mime="text/csv",
                )

    else:
        st.error("El motor OCR no pudo inicializarse. Instala las dependencias con: `pip install pymupdf pytesseract easyocr`")
        st.code("pip install pymupdf pytesseract easyocr pillow opencv-python")
