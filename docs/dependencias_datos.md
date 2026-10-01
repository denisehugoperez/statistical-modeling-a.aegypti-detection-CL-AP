# Dependencias de datos

Inventario estático de los notebooks conservados. No se ejecutó código ni se validó el contenido analítico de los archivos.

| Notebook | Entradas | Tipo de entrada | Outputs | Ruta nueva | Consumidor posterior | Estado |
|---|---|---|---|---|---|---|
| check_ndvi_tiff_integrity.ipynb | TESIS_NDVI_ROOT/{minimo_bisemanal,maximo_bisemanal,media_bisemanal,desvest_bisemanal}/*_BI??_{min,max,mean,std}.tif | GeoTIFF externos mediante glob | ndvi_pending_tiff_integrity_results.csv; ndvi_pending_tiff_files_to_redownload.csv | GeoTIFF: TESIS_NDVI_ROOT; CSV: data/diagnostics/ | repair_ndvi_bisemanal_from_diagnostics.ipynb consume el CSV de pendientes | DEPENDENCIA EXTERNA / NO GENERA PARQUET |
| download_ndvi_arica_y_parinacota_bisemanal.ipynb | Google Earth Engine (COPERNICUS/S2_SR_HARMONIZED) | Fuente remota | ndvi_arica_y_parinacota_2024_BI??_{min,max,mean,std}.tif | TESIS_NDVI_ROOT/{minimo_bisemanal,maximo_bisemanal,media_bisemanal,desvest_bisemanal}/ | check_ndvi_tiff_integrity.ipynb; environmental/data_aggregation.ipynb | DEPENDENCIA EXTERNA / SE GENERA AL EJECUTAR |
| download_ndvi_arica_y_parinacota_mensual.ipynb | Google Earth Engine (COPERNICUS/S2_SR_HARMONIZED) | Fuente remota | ndvi_arica_y_parinacota_2024_M??_{min,max,mean,std}.tif | TESIS_NDVI_ROOT/ndvi_mensual/... | Ninguno entre los notebooks conservados | DEPENDENCIA EXTERNA / SE GENERA AL EJECUTAR |
| download_ndvi_arica_y_parinacota_SE.ipynb | Google Earth Engine (COPERNICUS/S2_SR_HARMONIZED) | Fuente remota | ndvi_arica_y_parinacota_2024_SE??_{min,max,mean,std}.tif | TESIS_NDVI_ROOT/ndvi_semanal/... | Ninguno entre los notebooks conservados | DEPENDENCIA EXTERNA / SE GENERA AL EJECUTAR |
| repair_ndvi_bisemanal_from_diagnostics.ipynb | data/diagnostics/ndvi_pending_tiff_files_to_redownload.csv; GeoTIFF externos dañados; Google Earth Engine | CSV regenerable, GeoTIFF externo y fuente remota | GeoTIFF bisemanales reemplazados; copias *.damaged_&lt;timestamp&gt;.tif | TESIS_NDVI_ROOT/; TESIS_NDVI_ROOT/damaged_backup/ | check_ndvi_tiff_integrity.ipynb; environmental/data_aggregation.ipynb | DEPENDENCIA EXTERNA / SE GENERA AL EJECUTAR |
| environmental/data_aggregation.ipynb | era5_weather_altitude_epiweek_2024_population.parquet; GeoTIFF bisemanales externos | Parquet inicial y GeoTIFF | quality_check_environment_grid_week_2024_raw.parquet; environment_grid_week_2024_raw.parquet; grid_geometry.parquet | data/interim/environment/; data/processed/environment/grid_geometry.parquet | El panel de calidad alimenta `02`; el panel reducido alimenta `03` | PUNTO DE PARTIDA / SE GENERA AL EJECUTAR; exclusivamente por grilla |
| environmental/data_null_exploration.ipynb | quality_check_environment_grid_week_2024_raw.parquet; Parquet ambiental inicial; grid_geometry.parquet | Parquet | Tablas y figuras diagnósticas de nulos y cobertura | data/diagnostics/; outputs/figures/ | No aplica | DIAGNÓSTICO; NO MODIFICA LOS PANELES |
| environmental/data_cleaning.ipynb | environment_grid_week_2024_raw.parquet; grid_geometry.parquet | Parquet intermedio | environment_grid_week_2024_clean.parquet; diagnostico_vecinos_knn_altura.parquet; diagnostico_vecinos_knn_ndvi.parquet; figuras PNG KNN | data/processed/environment/; data/diagnostics/; outputs/figures/knn_experiments/ | Futuro EDA y modelamiento | SE GENERA AL EJECUTAR |
| entomology/entomology.ipynb | HALLAZGOS_AEDES_AEGYPTI.{shp,shx,dbf,prj,cpg} | Shapefile original | entomology_2024_clean.parquet | data/processed/entomology/entomology_2024_clean.parquet | Futuro EDA | COPIAR RAW / SE GENERA AL EJECUTAR |
| epidemiology/epidemiology.ipynb | TRANSPARENCIA_final Arica.xlsx; grid_geometry.parquet | Excel original y geometría canónica de grilla | epidemiology_2024_clean.parquet; epidemiology_2024_grid_week.parquet | data/processed/epidemiology/ | Futuro EDA exclusivamente por grilla | COPIAR RAW / SE GENERA AL EJECUTAR; ubicación por centro notificador como proxy |
| integration/build_analytical_grid_week.ipynb | Productos limpios ambiental, entomológico y epidemiológico | Pendiente de definir | Ninguno: notebook vacío | — | Futuro producto analítico integrado por grilla y semana | RESERVADO / NO IMPLEMENTADO |

## Punto de partida ambiental

data/raw/environment/era5_weather_altitude_epiweek_2024_population.parquet es un insumo inmutable. Se lee, no se regenera ni se sobrescribe.

El calendario común está en `src/epidemiological_calendar.py`: define EPI_YEAR=2024, el intervalo 31-12-2023–28-12-2024 y exactamente 52 semanas domingo–sábado. `environmental/data_aggregation.ipynb` no utiliza semanas ISO.

## Orden de ejecución propuesto

1. Conectar el disco externo o definir TESIS_NDVI_ROOT y retirar/refactorizar la lógica distrital señalada.
2. Opcionalmente, ejecutar check_ndvi_tiff_integrity.ipynb con el disco disponible. Su CSV de pendientes alimenta repair_ndvi_bisemanal_from_diagnostics.ipynb.
3. environmental/data_aggregation.ipynb: Parquet ambiental inicial + NDVI → panel de control de calidad, panel raw reducido y grid_geometry.parquet.
4. environmental/data_null_exploration.ipynb: diagnóstico del panel de control de calidad.
5. environmental/data_cleaning.ipynb: panel raw reducido → panel limpio y diagnósticos KNN.
6. entomology/entomology.ipynb: shapefile original → entomology_2024_clean.parquet.
7. epidemiology/epidemiology.ipynb: Excel original + grid_geometry.parquet → epidemiology_2024_clean.parquet y epidemiology_2024_grid_week.parquet. La asignación usa el centro notificador como proxy.
8. integration/build_analytical_grid_week.ipynb: reservado para la futura integración por grilla y semana; actualmente está vacío.
9. Futuro EDA exclusivamente a nivel de grilla.

## Diferencias frente a las cadenas esperadas

- La cadena ambiental canónica queda definida como: Parquet ambiental inicial + NDVI externo → `01` → panel de control de calidad para `02` y panel raw reducido para `03`; el producto limpio de `03` alimenta EDA y modelamiento.
- environmental/data_aggregation.ipynb ya no lee carto-chile.gpkg ni genera overlaps territoriales; el GeoPackage puede seguir siendo una dependencia cartográfica potencial para futuros límites regionales o comunales, pero no participa en este panel.
- environmental/data_null_exploration.ipynb usa sólo la grilla canónica para sus visualizaciones espaciales; no consume overlaps distritales.
- environmental/data_cleaning.ipynb genera `environment_grid_week_2024_clean.parquet`, que es el producto ambiental destinado al EDA y modelamiento.
- entomology/entomology.ipynb define nombres para un panel y reporte distritales, pero no los lee ni escribe en el código actual. Se consideran OBSOLETO DISTRITAL.
- epidemiology/epidemiology.ipynb quedó refactorizado para leer sólo grid_geometry.parquet, asignar cada centro notificador a un grid_id y producir únicamente los dos Parquet epidemiológicos canónicos. El lugar de residencia se conserva con fines descriptivos y no participa en la asignación espacial.
- El TSV denv_chile_transparencia.tsv sólo aparece en versiones heredadas; el notebook epidemiológico reorganizado no lo utiliza.

## Dependencia externa NDVI

- La fuente canónica de todos los GeoTIFF es NDVI_EXTERNAL_DIR, definida en src/paths.py desde TESIS_NDVI_ROOT y con D:\GeoTIFF NDVI como valor predeterminado.
- require_ndvi_external_dir() detiene la ejecución con FileNotFoundError si el disco o la carpeta no están disponibles. No existe fallback a data/raw/ndvi ni redescarga automática.
- Leen esta dependencia: environmental/data_aggregation.ipynb y check_ndvi_tiff_integrity.ipynb.
- Escriben en esta dependencia: los tres notebooks de descarga y repair_ndvi_bisemanal_from_diagnostics.ipynb.
- Los CSV de integridad y pendientes permanecen dentro del proyecto en data/diagnostics.
- data/raw/ndvi se mantiene vacío salvo por su README.md y no almacena GeoTIFF.

## Dependencias faltantes, ambiguas u obsoletas

- EXTERNA, NO VERIFICADA: los GeoTIFF permanecen en el disco externo. Su ausencia durante una sesión indica que el disco puede estar desconectado, no que la dependencia sea obsoleta.
- REGENERABLE, NO COPIADO: data/ndvi_quality/ndvi_pending_tiff_integrity_results.csv y ndvi_pending_tiff_files_to_redownload.csv.
- DEPENDENCIA CARTOGRÁFICA POTENCIAL, NO COPIADA: data/raw/geo/carto-chile.gpkg. No debe considerarse completamente obsoleto; revisar sus capas regionales o comunales cuando se implemente el recorte de grilla o la cartografía.
- OBSOLETO DISTRITAL, NO COPIADO: data/processed/geo/district_geometries_eda.parquet.
- OBSOLETO DISTRITAL: data/processed/geo/district_week_eda_area.parquet, declarado pero no usado por el notebook entomológico conservado.
- OBSOLETO DISTRITAL: grid_distrito_overlap.parquet, generado por agregación y consumido por exploración de nulos.
- FALTA DEFINIR: no existe generación de grid_and_data_nonull_features.parquet en el notebook de limpieza actual.

## Scripts requeridos

- src/paths.py: única dependencia importada desde src por los notebooks conservados. Además de las rutas internas, centraliza NDVI_EXTERNAL_DIR, TESIS_NDVI_ROOT y require_ndvi_external_dir().
- No se copiaron generadores, reparadores, ejecutores históricos ni scripts distritales.
