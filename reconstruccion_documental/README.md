# Reconstruccion documental

Este proyecto concentra, dentro de `Laboratorio metodos mixtos`, todo el trabajo de reconstruccion limpia del PDF presupuestal, la explotacion a Excel y la documentacion tecnica para que cualquier programador o IA pueda retomar el flujo sin depender del historial del chat.

## Objetivos

1. Reconstruir el PDF original en una version limpia, pagina por pagina.
2. Exportar la informacion a Excel de forma util para auditoria y analisis.
3. Demostrar una reconstruccion puntual de la pagina 3 sin usar JSON de Document AI.
4. Dejar trazabilidad completa de codigo, librerias, rutas, salidas y decisiones tecnicas.
5. Dejar evidencia clara del estado real de `git` y `GitHub`.

## Estructura

- `inputs/Sin_titulo.pdf`: copia local del PDF original.
- `../Nueva carpeta/`: JSON de Google Cloud Document AI entregados por el usuario.
- `resources/tessdata/`: modelos OCR `spa`, `eng` y `osd`.
- `scripts/docai_pdf_pipeline.py`: pipeline hibrido Document AI + OCR.
- `scripts/reconstruct_clean_document.py`: reconstruccion limpia pagina por pagina.
- `scripts/reconstruct_without_json_hybrid.py`: pipeline alterno sin JSON usando texto incrustado del PDF + OCR + deteccion de rejilla.
- `scripts/reconstruct_page3_without_json.py`: wrapper de benchmark para reconstruir solo la pagina 3 con el pipeline alterno sin JSON.
- `scripts/project_paths.py`: rutas canonicas del proyecto.
- `outputs/sin_titulo_extraction_full/`: extraccion estructurada.
- `outputs/sin_titulo_reconstructed_uniform_v2/`: PDF limpio completo y Excel de layout.
- `outputs/page3_without_json_hybrid/`: reconstruccion aislada de la pagina 3 sin JSON con el pipeline alterno.
- `outputs/no_json_hybrid_full/`: salida del pipeline alterno para pruebas futuras sobre multiples paginas o el documento completo.
- `docs/`: documentacion tecnica y de diagnostico.

## Flujo recomendado

### Reconstruccion limpia completa

```powershell
.\run_reconstruct_clean.ps1
```

Salida principal:

- `outputs/sin_titulo_reconstructed_uniform_v2/document_reconstructed_clean.pdf`
- `outputs/sin_titulo_reconstructed_uniform_v2/document_reconstructed_layout.xlsx`

### Extraccion estructurada completa

```powershell
& "C:\Users\ZN-\Documents\Antigravity\.venv\Scripts\python.exe" `
  ".\scripts\docai_pdf_pipeline.py"
```

Salida principal:

- `outputs/sin_titulo_extraction_full/document_extraction.xlsx`
- `outputs/sin_titulo_extraction_full/document_extraction_report.pdf`
- `outputs/sin_titulo_extraction_full/document_extraction_report.docx`

### Pagina 3 sin JSON

```powershell
.\run_page3_without_json.ps1
```

Salida principal:

- `outputs/page3_without_json_hybrid/page3_reconstructed_without_json_hybrid.pdf`
- `outputs/page3_without_json_hybrid/page3_reconstructed_without_json_hybrid.xlsx`
- `outputs/page3_without_json_hybrid/page3_reconstructed_without_json_hybrid.json`

### Pipeline alterno sin JSON para comparar con el anterior

```powershell
.\run_no_json_hybrid.ps1
```

Uso directo con paginas especificas:

```powershell
& "C:\Users\ZN-\Documents\Antigravity\.venv\Scripts\python.exe" `
  ".\scripts\reconstruct_without_json_hybrid.py" `
  --pages 3,15,35,49,69
```

## Resultado alcanzado

- PDF reconstruido limpio de `69` paginas.
- Excel con una hoja por pagina mas hoja `summary`.
- Extraccion estructurada con `34` tablas recuperadas.
- Reconstruccion sin JSON para la pagina 3 usando un pipeline alterno separado.
- Validacion de `git pull` y `git push --dry-run` exitosa por SSH.

## Documentacion clave

- `docs/ARCHITECTURE.md`
- `docs/DEPENDENCIES.md`
- `docs/GIT_GITHUB_DIAGNOSIS.md`
- `docs/PAGE3_NO_JSON.md`
- `docs/NO_JSON_HYBRID.md`
- `docs/docai_pipeline_guide.md`

## Nota sobre GitHub

El remoto del repo es `git@github.com:zerausn/Note9.git`.

La autenticacion SSH funciona. `pull` y `push --dry-run` responden bien desde este repo. Adicionalmente, varios JSON de `Nueva carpeta` superan `100 MB`, asi que para subir todo a GitHub se requiere `git-lfs`; esa es una causa real de fallo si Antigravity intenta empujar esos archivos con `git` normal.
