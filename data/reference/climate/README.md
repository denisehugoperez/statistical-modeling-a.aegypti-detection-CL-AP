# Referencias climáticas externas

Este directorio conserva tablas de contraste para evaluar la plausibilidad de las variables climáticas del proyecto. Son referencias contextuales: no reemplazan los datos de 2024 ni deben tratarse como verdad puntual para cada celda de la grilla.

## `ciren_station_climatology.csv`

Transcripción de estaciones presentada en *Antecedentes climáticos: XV Región de Arica y Parinacota*, documento publicado por CIREN en 2013 dentro del proyecto de caracterización de humedales altoandinos. Según la documentación del análisis original, la cartografía climática procede de CIREN (1992) y las estaciones DGA utilizan series de distinta longitud, aproximadamente entre 1961 y 2008.

Columnas:

- `estacion`: nombre de la estación.
- `altitud_m`: altitud en metros sobre el nivel del mar.
- `precipitacion_anual_media_mm`: precipitación anual media en milímetros.
- `zona_altitud`: clasificación operativa usada en la auditoría; no corresponde necesariamente a una categoría oficial de CIREN.

El documento primario no está almacenado actualmente en este repositorio. Antes de citar cifras en la tesis se debe cotejar esta transcripción con la tabla y página originales e incorporar la referencia bibliográfica completa.

## `inia_december_2021_stations.csv`

Transcripción del boletín agroclimático de INIA publicado en enero de 2022, con observaciones informadas para diciembre de 2021:

<http://riesgoclimatico.inia.cl/public/boletines/eyJpdiI6IlNjN1ZVc05Qd2FmWDBPNUdHZjE1b0E9PSIsInZhbHVlIjoiZzlqSGRNYkpaRVNuMUFmSTl6YXR2dz09IiwibWFjIjoiYjBmY2NlNDg2NmNhODQzYmJjZGRlMTc2ZWFlYWI0NjU1MDg2ODMwM2ExMDliZTlmNjE1MmQ1MTg5OGEzZmM5YSJ9>

Columnas:

- `estacion`: nombre de la estación o sector.
- `nombre_en_informe` y `zona_inia`: nombre y clasificación territorial conservados desde el informe de INIA.
- `latitud`, `longitud`, `altitud_m` y `codigo_dmc_saclim`: identificación y ubicación de la estación en el registro oficial DMC-SACLIM.
- `precision_ubicacion`, `fuente_coordenadas`, `fuente_altitud` y `estado_verificacion`: trazabilidad de la verificación externa. Las siete estaciones se verificaron el 18 de septiembre de 2026 en fichas DMC-SACLIM pertenecientes a RedINIA.
- `pagina_pdf`: páginas del informe en las que se documentan la zona y la descripción de la estación; el PDF no publica sus coordenadas ni altitud.
- `zona_altitud`: categoría analítica estandarizada a partir de `altitud_m`: litoral y valles `<1000 m`, desierto interior `1000–1999 m`, marginal de altura `2000–3499 m` y altiplano `≥3500 m`.
- `observaciones`: decisiones de identificación, advertencias y exclusiones relevantes.
- `temperatura_min_c`, `temperatura_media_c` y `temperatura_max_c`: temperaturas informadas en grados Celsius.
- `humedad_relativa_pct`: humedad relativa en porcentaje.
- `inconsistencia_interna_fuente`: marca una relación mínima–media–máxima que requiere comprobación contra el documento original.

La fila de Socoroma conserva la transcripción disponible, pero está marcada porque la temperatura mínima (`12.2 °C`) supera la media (`9.8 °C`). Su temperatura media se muestra en el contraste gráfico con un tono y una etiqueta especiales; no debe interpretarse como un valor validado mientras no se confirme en la fuente. Su humedad relativa no presenta esa contradicción.

En Putre y Visviri se eligieron expresamente las fichas **Putre INIA 180029** y **Visviri INIA 170007**, pertenecientes a RedINIA. Las categorías originales de INIA se conservan sin alteración; `zona_altitud` es una variable separada y reproducible que permite comparar todas las estaciones con los mismos intervalos usados para ERA5 y CIREN.

## Procedencia dentro del proyecto

Estas tablas se trasladaron desde los productos generados por `C:\Code tesis\notebooks\EDA\auxiliares\auditoria_calidad_plausibilidad_datos_2024.ipynb`:

- `C:\Code tesis\outputs\tables\data_quality_audit\02_referencia_ciren_estaciones.csv`
- `C:\Code tesis\outputs\tables\data_quality_audit\02_referencia_inia_diciembre_2021.csv`

Los archivos originales de `C:\Code tesis` no fueron modificados. Los CSV de este directorio son ahora las copias de referencia del proyecto `tesis_aedes_grilla_2024`.

## Uso previsto

- Contrastar órdenes de magnitud y gradientes altitudinales.
- Detectar posibles errores de unidad, escala o agregación en ERA5.
- Documentar diferencias que requieran investigación adicional.

No se debe exigir coincidencia exacta con ERA5 2024: CIREN resume periodos históricos e INIA corresponde a diciembre de 2021.
