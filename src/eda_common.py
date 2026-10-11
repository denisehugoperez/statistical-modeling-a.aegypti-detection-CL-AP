"""Definiciones, calendario y funciones compartidas del notebook EDA."""
import re
import numpy as np
import unicodedata
import pandas as pd
import matplotlib.pyplot as plt
from src.epidemiological_calendar import build_epidemiological_calendar
from src.plot_palette import COLORS, SEASON_COLORS, STAGE_COLORS, MAP_CMAP, CATEGORY_CMAP, CORRELATION_CMAP

SEASONS = ['Verano','Otoño','Invierno','Primavera']


STAGES = ['eggs','larvae','pupae','adults']

STAGE_LABELS = dict(zip(STAGES,['HUEVO','LARVA','PUPA','ADULTO']))

RESPONSE = 'vector_findings'

COUNTS = {RESPONSE,*STAGES,'total_records','confirmed_cases','reporting_centers'}

STATIC = {'elevation_min','elevation_mean','elevation_max','population','population_weight','koppen_class'}

LABELS = {'tmean_c':'Temperatura media','tmin_c':'Temperatura mínima','tmax_c':'Temperatura máxima',
          'rh_mean':'Humedad relativa media','rh_min':'Humedad mínima','rh_max':'Humedad máxima',
          'tp_sum':'Precipitación acumulada','ndvi_mean_biweekly':'NDVI medio',
          'ndvi_max_biweekly':'NDVI máximo','ndvi_min_biweekly':'NDVI mínimo','ndvi_std_biweekly':'NDVI desviación',
          'elevation_min':'Altitud mínima','elevation_mean':'Altitud media','elevation_max':'Altitud máxima',
          'population':'Población','population_weight':'Peso poblacional','koppen_class':'Köppen',
          RESPONSE:'total_vectores','total_records':'Registros entomológicos',
          'confirmed_cases':'Casos confirmados','reporting_centers':'Centros notificadores',**STAGE_LABELS}


def split_column(c):
    weighted = c.endswith('_popw')
    stem = c[:-5] if weighted else c
    lag = re.search(r'_lag_?(\d+)$', stem)
    roll = re.search(r'_(?:rolling_mean_|roll_?)(\d+)$', stem)
    match = lag or roll
    base = stem[:match.start()] if match else stem
    return base, 'lag' if lag else 'roll' if roll else 'original', int(lag[1]) if lag else None, int(roll[1]) if roll else None, weighted

def classify(c):
    b, t, lag, win, w = split_column(c)
    if b in {'grid_id','geometry'} or any(x in b for x in ['district','distrito']): f='identificadores'
    elif b in {'year','epiweek','epiweek_sin','epiweek_cos'}: f='calendario'
    elif any(x in b for x in ['coverage','imputed','pixel','quality','cobertura']): f='calidad, cobertura e imputación'
    elif b in {RESPONSE,*STAGES,'total_records'}: f='entomología'
    elif b in {'confirmed_cases','reporting_centers'}: f='epidemiología'
    elif b.startswith(('tmean','tmin','tmax')): f='temperatura'
    elif b.startswith('rh_'): f='humedad'
    elif b.startswith('tp_'): f='precipitación'
    elif b.startswith('ndvi_'): f='NDVI'
    elif b.startswith('elevation_'): f='altitud'
    elif b.startswith('population'): f='población'
    elif b.startswith('koppen'): f='Köppen'
    else: f='otras transformaciones temporales'
    return b,t,lag,win,w,f

def unit(c):
    b,_,_,_,w,f = classify(c)
    u = ('°C' if f=='temperatura' else '%' if f=='humedad' else 'm' if f=='precipitación'
         else 'adimensional' if f=='NDVI' or b=='population_weight' else 'm' if f=='altitud'
         else 'personas' if b=='population' else 'conteo' if b in COUNTS else 'categoría' if f=='Köppen' else 'no aplica')
    return u+' × peso de celda' if w else u

def label(c):
    b,t,k,v,w = split_column(c)
    return LABELS.get(b,b) + (f' · lag {k}' if t=='lag' else f' · media móvil {v}' if t=='roll' else '') + (' · popw' if w else '')

def aggregate(c):
    b,*_ = split_column(c)
    return 'suma' if b in COUNTS or b=='tp_sum' else 'media'

def summary_by(frame, c, by):
    group = frame.groupby(by, observed=True)[c]
    return group.sum(min_count=1) if aggregate(c)=='suma' else group.mean()

def safe_name(s):
    s = unicodedata.normalize('NFKD',str(s)).encode('ascii','ignore').decode()
    return re.sub(r'[^A-Za-z0-9_-]+','_',s).strip('_')

def plot_scatter(x,y,ax,panel,trend=False):
    z=panel[[x,y]].dropna()
    ax.scatter(z[x],z[y],s=8,alpha=.15 if len(z)>1000 else .65,rasterized=True,color=COLORS['teal'])
    ax.set(xlabel=label(x)+' ['+unit(x)+']',ylabel=label(y)+' ['+unit(y)+']',title=f'n = {len(z):,} pares válidos')
    if trend and z[x].nunique() > 1:
        xv = z[x].to_numpy(dtype=float)
        yv = z[y].to_numpy(dtype=float)
        if trend == 'lowess':
            from statsmodels.nonparametric.smoothers_lowess import lowess
            line_x = np.linspace(xv.min(), xv.max(), 150)
            line_y = lowess(yv, xv, frac=2/3, it=0, xvals=line_x)
            trend_label = 'Tendencia LOWESS'
        else:
            centered = xv - xv.mean()
            slope = np.sum(centered * (yv-yv.mean())) / np.sum(centered**2)
            line_x = np.array([xv.min(), xv.max()])
            line_y = yv.mean() + slope * (line_x-xv.mean())
            trend_label = 'Tendencia lineal'
        ax.plot(line_x, line_y, color=COLORS['bright_purple'], linewidth=1.8,
                linestyle='-', label=trend_label)
        ax.legend(fontsize=9)
    if z.empty:
        ax.text(.5,.5,'Sin pares disponibles',transform=ax.transAxes,ha='center')
    return len(z)

def plot_matrix(matrix,title):
    n=len(matrix)
    fig,ax=plt.subplots(figsize=(max(6,.31*n+2),max(5,.31*n+1)),layout='constrained')
    cmap=CORRELATION_CMAP
    artist=ax.imshow(matrix.to_numpy(),cmap=cmap,vmin=-1,vmax=1,aspect='equal')
    ax.set_xticks(range(n),matrix.columns,rotation=90,fontsize=7)
    ax.set_yticks(range(n),matrix.index,fontsize=7)
    ax.set_title(title)
    if n<=12:
        for i in range(n):
            for j in range(n):
                if pd.notna(matrix.iloc[i,j]): ax.text(j,i,f'{matrix.iloc[i,j]:.2f}',ha='center',va='center',fontsize=7)
    fig.colorbar(artist,ax=ax,shrink=.75,label='Spearman (gris: no estimable)')
    return fig

def eda_calendar():
    calendar = build_epidemiological_calendar()
    calendar["week_start"] = pd.to_datetime(calendar["start_date"])
    calendar["week_end"] = calendar["week_start"] + pd.Timedelta(days=6)

    season_ranges = {
        "Verano": (pd.Timestamp("2023-12-21"), pd.Timestamp("2024-03-19")),
        "Otoño": (pd.Timestamp("2024-03-20"), pd.Timestamp("2024-06-20")),
        "Invierno": (pd.Timestamp("2024-06-21"), pd.Timestamp("2024-09-21")),
        "Primavera": (pd.Timestamp("2024-09-22"), pd.Timestamp("2024-12-20")),
    }

    def assign_season(week_start, week_end):
        overlaps = {}

        for season, (season_start, season_end) in season_ranges.items():
            overlap_start = max(week_start, season_start)
            overlap_end = min(week_end, season_end)

            overlaps[season] = max(
                0,
                (overlap_end - overlap_start).days + 1
            )

        # Completa el verano siguiente para las semanas finales de 2024.
        overlaps["Verano"] += max(
            0,
            (min(week_end, pd.Timestamp("2025-03-19"))
             - max(week_start, pd.Timestamp("2024-12-21"))).days + 1
        )
        if not any(overlaps.values()):
            raise ValueError(f"Semana fuera de los rangos estacionales: {week_start} - {week_end}")
        return max(overlaps, key=overlaps.get)

    calendar["season"] = calendar.apply(
        lambda row: assign_season(row["week_start"], row["week_end"]),
        axis=1
    )

    season_lookup = calendar.set_index("epiweek")["season"]
    return calendar, season_lookup


def prepare_eda(master_path, geometry_path, season_lookup):
    """Carga las fuentes y prepara las columnas utilizadas por el EDA."""
    import geopandas as gpd

    source = pd.read_parquet(master_path)
    panel = source.copy(deep=True)
    geo = gpd.read_parquet(geometry_path)
    geo['grid_id'] = pd.to_numeric(geo.grid_id).astype('Int64').astype('string')
    analysis = panel.assign(season=panel.epiweek.map(season_lookup),
                            zona_altitud=altitude_zone(panel.elevation_mean))
    KEY = ['grid_id', 'year', 'epiweek']
    rows = []
    for c in panel:
        base, transform, lag, window, weighted, family = classify(c)
        rows.append(dict(columna=c, variable_base=base, familia=family,
                         serie_base=base+('_popw' if weighted else ''), unidad=unit(c),
                         tipo='numérica' if pd.api.types.is_numeric_dtype(panel[c]) else 'categórica',
                         temporalidad='estática' if base in STATIC else 'temporal',
                         transformacion=transform, lag=lag, ventana_movil=window,
                         ponderada=weighted, no_nulos=int(panel[c].notna().sum()),
                         valores_unicos=int(panel[c].nunique())))
    inventory = pd.DataFrame(rows)
    meta = inventory.set_index('columna')
    substantive = inventory.loc[~inventory.familia.isin(['identificadores', 'calendario']), 'columna'].tolist()
    temporal = [c for c in substantive if meta.at[c,'temporalidad']=='temporal' and meta.at[c,'tipo']=='numérica']
    map_columns = [c for c in substantive if meta.at[c,'transformacion']=='original']
    numeric_originals = [c for c in map_columns if meta.at[c,'tipo']=='numérica']
    ndvi_mean, ndvi_max = 'ndvi_mean_biweekly', 'ndvi_max_biweekly'
    exact_duplicates = {}
    for i,c in enumerate(substantive):
        if meta.at[c,'tipo'] != 'numérica':
            continue
        for previous in substantive[:i]:
            if meta.at[previous,'tipo']=='numérica' and panel[c].equals(panel[previous]):
                exact_duplicates[c] = previous
                break
    scatter_vars = [c for c in numeric_originals if c not in {RESPONSE,*STAGES,ndvi_mean,ndvi_max} and c not in exact_duplicates]
    ndvi_vars = [c for c in numeric_originals if meta.at[c,'temporalidad']=='temporal' and c not in {ndvi_mean,ndvi_max} and c not in exact_duplicates]
    plans = []
    for c in panel:
        m = meta.loc[c]
        eligibility = {
            'series_temporales': c in temporal,
            'mapas': c in map_columns,
            'dispersion_total_vectores': c in scatter_vars or c in {RESPONSE,ndvi_mean,ndvi_max},
            'dispersion_ndvi': c in ndvi_vars or c in {ndvi_mean,ndvi_max},
            'correlaciones': c in substantive and m['tipo']=='numérica' and m.valores_unicos>1 and c not in exact_duplicates and c not in STAGES,
        }
        for kind,included in eligibility.items():
            reason = '' if included else (
                'lag/roll: se reservan para series y correlaciones' if kind=='mapas' and m.transformacion!='original'
                else 'clave o calendario auxiliar' if c not in substantive
                else 'duplicado exacto' if c in exact_duplicates
                else 'estadio integrante de la respuesta' if c in STAGES else 'no elegible para este grupo')
            plans.append(dict(columna=c, familia=m.familia, transformacion=m.transformacion,
                              tipo_figura=kind, incluida=included, justificacion_exclusion=reason))
    figure_plan = pd.DataFrame(plans)
    counts = {t: int(inventory.transformacion.eq(t).sum()) for t in ['original','lag','roll']}
    return (source, panel, geo, analysis, inventory, meta, temporal, map_columns,
            scatter_vars, ndvi_vars, figure_plan, counts, KEY, ndvi_mean, ndvi_max)


# Misma clasificación operativa de 00_source_quality_and_plausibility.
ZONE_ORDER = [
    "Litoral y valles (<1000 m)",
    "Desierto interior (1000–1999 m)",
    "Marginal de altura (2000–3499 m)",
    "Altiplano (≥3500 m)",
]

ZONE_BINS = [-np.inf, 1000, 2000, 3500, np.inf]

def altitude_zone(values):
    return pd.cut(
        values,
        bins=ZONE_BINS,
        labels=ZONE_ORDER,
        right=False,
        ordered=True,
    )


def animated_maps(panel, geo, column, calendar, output_dir):
    """Weekly maps with a shared color scale and two fixed views."""
    from matplotlib.animation import FuncAnimation, PillowWriter
    from matplotlib.patches import Patch

    output_dir.mkdir(parents=True, exist_ok=True)
    layer = geo.explode(index_parts=False).reset_index(drop=True)
    weekly = panel.pivot(index='epiweek', columns='grid_id', values=column).reindex(calendar.epiweek)
    values = weekly.reindex(columns=layer.grid_id).to_numpy(dtype=float, na_value=np.nan)
    lo, hi = np.nanmin(values), np.nanmax(values)
    if lo == hi:
        hi = lo + 1
    norm = plt.Normalize(lo, hi)
    finding_ids = panel.loc[panel[RESPONSE].gt(0), 'grid_id'].unique()
    findings = geo.loc[geo.grid_id.isin(finding_ids)]
    xmin, ymin, xmax, ymax = findings.total_bounds
    margin = max(xmax-xmin, ymax-ymin) * .35
    dates = calendar.set_index('epiweek')
    totals = panel.groupby('epiweek')[RESPONSE].sum(min_count=1)
    paths=[]
    for view in ['region', 'zoom_hallazgos']:
        fig, ax = plt.subplots(figsize=(7, 9), layout='constrained')
        layer.plot(ax=ax, color=COLORS['gray'], linewidth=0)
        collection = ax.collections[0]
        collection.set_cmap(MAP_CMAP)
        collection.set_norm(norm)
        findings.boundary.plot(ax=ax, color=COLORS['charcoal'], linewidth=.9)
        if view == 'zoom_hallazgos':
            ax.set_xlim(xmin-margin, xmax+margin)
            ax.set_ylim(ymin-margin, ymax+margin)
        ax.set_axis_off()
        stamp = ax.set_title('', fontsize=11)
        fig.suptitle(label(column)+' : '+('Región completa' if view == 'region' else 'Zoom moderado en zona con hallazgos'), fontsize=12)
        fig.colorbar(collection, ax=ax, shrink=.65, label=unit(column))
        ax.legend(handles=[Patch(facecolor='none', edgecolor=COLORS['charcoal'], label='Celdas con hallazgos durante 2024')],
                  loc='lower left', fontsize=8, frameon=False)

        def update(frame):
            week = weekly.index[frame]
            collection.set_array(np.ma.masked_invalid(values[frame]))
            start = dates.at[week, 'week_start'].strftime('%d/%m')
            end = dates.at[week, 'week_end'].strftime('%d/%m')
            season = dates.at[week, 'season']
            total = totals.get(week, np.nan)
            count = f'{total:,.0f}'.replace(',', '.') if pd.notna(total) else 'sin registro'
            stamp.set_text(f'SE {week:02d} : {start} - {end} ({season})\n'
                           f'Vectores registrados en la semana: {count}')
            return collection, stamp

        animation = FuncAnimation(fig, update, frames=len(weekly), interval=250,
                                  blit=False, cache_frame_data=False)
        path = output_dir / f'mapa_{column}_{view}_2024.gif'
        animation.save(path, writer=PillowWriter(fps=4), dpi=90)
        plt.close(fig)
        paths.append(path)
    return paths
