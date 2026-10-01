import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
DATA_RAW = DATA_DIR / "raw"
DATA_INTERIM = DATA_DIR / "interim"
DATA_PROCESSED = DATA_DIR / "processed"
DATA_DIAGNOSTICS = DATA_DIR / "diagnostics"

RAW_GEO = DATA_RAW / "geography"
RAW_CLIMATE = DATA_RAW / "environment"
RAW_NDVI = DATA_RAW / "ndvi"
RAW_EPIDEMIOLOGY = DATA_RAW / "epidemiology"

EPIDEMIOLOGY_RAW_PATH = RAW_EPIDEMIOLOGY / "TRANSPARENCIA_final Arica.xlsx"
REPORTING_CENTERS_COORDINATES_PATH = (
    RAW_EPIDEMIOLOGY / "reporting_centers_coordinates.csv"
)

NDVI_EXTERNAL_DIR = Path(
    os.environ.get("TESIS_NDVI_ROOT", r"D:\GeoTIFF NDVI")
)


def require_ndvi_external_dir() -> Path:
    """Return the canonical external NDVI directory or fail clearly."""
    if not NDVI_EXTERNAL_DIR.is_dir():
        raise FileNotFoundError(
            "No se encontró la carpeta externa de GeoTIFF NDVI en "
            f"'{NDVI_EXTERNAL_DIR}'. Conecta el disco externo o define "
            "TESIS_NDVI_ROOT con la ruta correcta. No se usará "
            "data/raw/ndvi como alternativa ni se iniciará una redescarga."
        )
    return NDVI_EXTERNAL_DIR

INTERIM_GEO = DATA_INTERIM / "environment"
INTERIM_CLIMATE = DATA_INTERIM / "environment"
INTERIM_NDVI = DATA_INTERIM / "ndvi"

PROCESSED_GEO = DATA_PROCESSED / "environment"
PROCESSED_CLIMATE = DATA_PROCESSED / "environment"
PROCESSED_NDVI = DATA_PROCESSED / "ndvi"
PROCESSED_EPIDEMIOLOGY = DATA_PROCESSED / "epidemiology"
PROCESSED_ENTOMOLOGY = DATA_PROCESSED / "entomology"
PROCESSED_INTEGRATED = DATA_PROCESSED / "integrated"

RAW_ENTOMOLOGY_FINDINGS_PATH = (
    DATA_RAW / "entomology" / "Hallazgos" / "HALLAZGOS_AEDES_AEGYPTI.shp"
)
RAW_ENTOMOLOGY_OVITRAP_CSV_PATH = (
    DATA_RAW / "entomology" / "Ovitrampas location" / "ovitrampas_latlon.csv"
)
RAW_ENTOMOLOGY_OVITRAP_SHP_PATH = (
    DATA_RAW / "entomology" / "Ovitrampas location" / "OVITRAMPAS.shp"
)
ENTOMOLOGY_CLEAN_PATH = PROCESSED_ENTOMOLOGY / "entomology_2024_clean.parquet"
ENTOMOLOGY_GRID_WEEK_PATH = (
    PROCESSED_ENTOMOLOGY / "entomology_2024_grid_week.parquet"
)

EPIDEMIOLOGY_CLEAN_PATH = PROCESSED_EPIDEMIOLOGY / "epidemiology_2024_clean.parquet"
EPIDEMIOLOGY_GRID_WEEK_PATH = PROCESSED_EPIDEMIOLOGY / "epidemiology_2024_grid_week.parquet"
ANALYTICAL_GRID_WEEK_PATH = (
    PROCESSED_INTEGRATED / "analytical_grid_week_2024.parquet"
)

ENVIRONMENT_GRID_WEEK_RAW_PATH = INTERIM_GEO / "environment_grid_week_2024_raw.parquet"
ENVIRONMENT_GRID_WEEK_QUALITY_CHECK_PATH = (
    INTERIM_GEO / "quality_check_environment_grid_week_2024_raw.parquet"
)
ENVIRONMENT_GRID_WEEK_CLEAN_PATH = PROCESSED_GEO / "environment_grid_week_2024_clean.parquet"
GRID_GEOMETRY_PATH = PROCESSED_GEO / "grid_geometry.parquet"

DIAGNOSTICS_KNN_ALTITUDE_PATH = DATA_DIAGNOSTICS / "diagnostico_vecinos_knn_altura.parquet"
DIAGNOSTICS_KNN_NDVI_PATH = DATA_DIAGNOSTICS / "diagnostico_vecinos_knn_ndvi.parquet"

DIAGNOSTICS_NULLS = DATA_DIAGNOSTICS / "nulls"
DIAGNOSTICS_KNN = DATA_DIAGNOSTICS
DIAGNOSTICS_POPW = DATA_DIAGNOSTICS / "popw"

OUTPUTS_DIR = PROJECT_ROOT / "outputs"
FIGURES_DIR = OUTPUTS_DIR / "figures"
TABLES_DIR = OUTPUTS_DIR / "tables"
MAPS_INTERACTIVE_DIR = OUTPUTS_DIR / "maps_interactive"
ENTOMOLOGY_FIGURES_DIR = FIGURES_DIR / "entomology"

EDA_FIGURES = FIGURES_DIR / "eda_preliminar"
EDA_TABLES = TABLES_DIR / "eda_preliminar"

EDA_FIGURES_REGIONAL = EDA_FIGURES / "regional"
EDA_FIGURES_GRID = EDA_FIGURES / "grid"
EDA_FIGURES_DISTRICT = EDA_FIGURES / "district"
EDA_FIGURES_CORRELATIONS = EDA_FIGURES / "correlations"
EDA_FIGURES_INTERACTIVE = EDA_FIGURES / "interactive"
EDA_FIGURES_LAGS_ROLLINGS = EDA_FIGURES / "lags_rollings"
EDA_FIGURES_POPW_COMPARISON = EDA_FIGURES / "popw_comparison"

EDA_TABLES_REGIONAL = EDA_TABLES / "regional"
EDA_TABLES_GRID = EDA_TABLES / "grid"
EDA_TABLES_DISTRICT = EDA_TABLES / "district"
EDA_TABLES_CORRELATIONS = EDA_TABLES / "correlations"
EDA_TABLES_RANKINGS = EDA_TABLES / "rankings"
EDA_TABLES_POPW_COMPARISON = EDA_TABLES / "popw_comparison"

NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
NOTEBOOKS_DATA_WRANGLING = NOTEBOOKS_DIR / "02_data_preparation"
NOTEBOOKS_ENVIRONMENTAL = NOTEBOOKS_DATA_WRANGLING / "environmental"
NOTEBOOKS_NDVI_DOWNLOAD = NOTEBOOKS_DIR / "01_ndvi_download"
NOTEBOOKS_STATISTICS = NOTEBOOKS_DIR / "statistics"

DOCS_DIR = PROJECT_ROOT / "docs"
DOCS_METODOLOGIA = DOCS_DIR / "metodologia"
DOCS_ANTEPROYECTO = DOCS_DIR / "anteproyecto"
DOCS_FIGURAS_INFORME = DOCS_DIR / "figuras_informe"

ALL_DIRS = [
    RAW_GEO,
    RAW_CLIMATE,
    RAW_NDVI,
    RAW_EPIDEMIOLOGY,
    INTERIM_GEO,
    INTERIM_CLIMATE,
    INTERIM_NDVI,
    PROCESSED_GEO,
    PROCESSED_CLIMATE,
    PROCESSED_NDVI,
    PROCESSED_EPIDEMIOLOGY,
    PROCESSED_ENTOMOLOGY,
    PROCESSED_INTEGRATED,
    DIAGNOSTICS_NULLS,
    DIAGNOSTICS_KNN,
    DIAGNOSTICS_POPW,
    EDA_FIGURES_REGIONAL,
    EDA_FIGURES_GRID,
    EDA_FIGURES_DISTRICT,
    EDA_FIGURES_CORRELATIONS,
    EDA_FIGURES_INTERACTIVE,
    EDA_FIGURES_LAGS_ROLLINGS,
    EDA_FIGURES_POPW_COMPARISON,
    EDA_TABLES_REGIONAL,
    EDA_TABLES_GRID,
    EDA_TABLES_DISTRICT,
    EDA_TABLES_CORRELATIONS,
    EDA_TABLES_RANKINGS,
    EDA_TABLES_POPW_COMPARISON,
    MAPS_INTERACTIVE_DIR,
    ENTOMOLOGY_FIGURES_DIR,
    NOTEBOOKS_DATA_WRANGLING,
    NOTEBOOKS_ENVIRONMENTAL,
    NOTEBOOKS_NDVI_DOWNLOAD,
    NOTEBOOKS_STATISTICS,
    DOCS_METODOLOGIA,
    DOCS_ANTEPROYECTO,
    DOCS_FIGURAS_INFORME,
]


def ensure_directories():
    for directory in ALL_DIRS:
        directory.mkdir(parents=True, exist_ok=True)
