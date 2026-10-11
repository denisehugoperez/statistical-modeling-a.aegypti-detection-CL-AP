# Paleta vigente del proyecto

Reemplaza las paletas anteriores. Los HEX de la primera referencia se transcriben de la imagen. La segunda imagen no indica HEX: sus tonos se aproximan visualmente.

| Color | HEX | Uso | Origen |
| --- | --- | --- | --- |
| Dark Purple | `#01012C` | Precipitación acumulada y texto principal | HEX de primera imagen |
| Aeon Dark | `#225453` | Temperatura media y texto secundario | HEX de primera imagen |
| Bright Purple | `#B3C0FB` | Fondo de otoño | HEX de primera imagen |
| Aeon Light | `#8CC63F` | NDVI medio y fondo de primavera | HEX de primera imagen |
| Nature White | `#FAFCC7` | Fondo de verano | HEX de primera imagen |
| White | `#FFFFFF` | Fondo de figuras | HEX de primera imagen |
| Teal | `#207D80` | Marcas verticales de hallazgos | Aproximación visual de segunda imagen |
| Pale Cyan | `#A3D3DE` | Fondo de invierno | Aproximación visual de segunda imagen |
| Deep Teal | `#006174` | Humedad relativa media | Aproximación visual de segunda imagen |
| Ice White | `#F2F7FA` | Fondo del área de trazado | Aproximación visual de segunda imagen |
| Soft Gray | `#F4F4F4` | Rellenos neutros | Aproximación visual de segunda imagen |
| Gray | `#D9DADB` | Cuadrícula, bordes y datos ausentes | Aproximación visual de segunda imagen |
| Charcoal | `#4C4F50` | Texto auxiliar | Aproximación visual de segunda imagen |
| Petrol | `#193D4E` | NDVI máximo | Aproximación visual de segunda imagen |
| Black | `#000000` | Marcas verticales de casos confirmados | Segunda imagen |

Las cuatro series ambientales son continuas y priorizan popw. Solo las marcas verticales son discontinuas. Las estaciones usan fondos al 30 % y bandas etiquetadas al 85 %. El color se mantiene para una misma variable en futuras figuras.

Fuente compartida: `src/plot_palette.py`. Catálogo: `docs/paleta_colores.json`.

## Uso en los notebooks

La paleta se importa en el primer bloque de código de los notebooks desde `02_data_preparation` en adelante, después de agregar la raíz del proyecto a `sys.path`:

```python
from src.plot_palette import COLORS, MAP_CMAP, apply_plot_palette
apply_plot_palette()
```

La llamada se realiza después de la configuración de estilo de Matplotlib o Seaborn. Modifica los colores por defecto y conserva los tamaños, distribuciones y parámetros propios de cada notebook. Los colores explícitos se referencian como `COLORS["teal"]`, y las escalas continuas como `MAP_CMAP`.

El mismo módulo define `CORRELATION_CMAP`, `CATEGORY_CMAP`, `STAGE_COLORS`, `ENVIRONMENT_COLORS`, `SEASON_COLORS` y `EVENT_COLORS`. El EDA importa estas definiciones compartidas; `eda_common.py` mantiene las funciones de análisis. Los mapas usan blanco hielo, cian, verde azulado y púrpura oscuro; las correlaciones usan una escala divergente con blanco en cero. Los valores ausentes se representan en gris.

Las figuras ya guardadas conservan su apariencia hasta que se ejecuten sus celdas de gráficos. Los notebooks de `01_ndvi_download` quedan fuera del alcance de esta integración.
