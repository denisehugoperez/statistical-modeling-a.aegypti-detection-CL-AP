- Panel de 177,268 filas y 3,409 celdas, SE1–SE52, sin duplicados ni geometrías inválidas.

- Solo 24 filas en 7 celdas tienen respuesta; faltan 99.9865% de los conteos y hay 0 ceros observados.

- Total observado 3,613 vectores. Verano: 1,933; Otoño: 1,604; Invierno: 1; Primavera: 75. Máximo semanal: SE11, 1,792.

- Huevos: 2,276; larvas: 1,104; pupas: 116; adultos: 117. 0 discrepancias entre estadios disponibles y respuesta.

- La celda con mayor acumulación observada es grid_id 102 (3,259 vectores); los mapas de conteos dejan las celdas no observadas en gris.

- Los 66 lags y 22 rolls ambientales construidos en 02 se conservan en el panel; sus nulos documentados y versiones popw se mantienen separadas.

- NDVI medio y máximo: Spearman 0.563 con 177,268 pares; temperatura media semanal entre celdas: 7.20–13.40 °C.

- Mayor asociación con total_vectores: total_records, Spearman 0.646, n=24; todas las correlaciones de la respuesta tienen pocos pares.

Las dispersiones muestran registros de vigilancia escasos y concentrados; no permiten inferir causalidad ni ausencia de vectores. Las celdas de mayor acumulación observada son 102 (3,259), 100 (190), 354 (72). Hay 4 casos confirmados asignados, en 4 filas; sus ubicaciones son centros notificadores. La matriz detecta 1507 pares con |Spearman| ≥ 0,95 y 4 cambios de signo frente a la métrica contemporánea. Los rolls suavizan el comportamiento temporal; sus asociaciones con originales y rezagos se detallan en diagnostico_dependencia_lags_rolls.csv. Antes de modelar se debe resolver la selección de observaciones vigiladas, el esfuerzo desconocido, los proxies espaciales, la dependencia por celda y semana, la colinealidad y la influencia de la imputación climática del NDVI. `tp_sum` se interpreta en metros; no se convierte a otra unidad. No existen lags o rolls de la respuesta en esta fuente; todos los derivados detectados son ambientales. No se puede recuperar del panel qué valores ambientales fueron imputados ni separar ubicaciones entomológicas exactas de proxies.