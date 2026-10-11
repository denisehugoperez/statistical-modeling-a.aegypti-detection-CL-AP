"""Paleta vigente: referencias adjuntas más recientes; docs/paleta_colores.md."""

COLORS = {'dark_purple': '#01012C', 'aeon_dark': '#225453', 'bright_purple': '#B3C0FB', 'aeon_light': '#8CC63F', 'nature_white': '#FAFCC7', 'white': '#FFFFFF', 'teal': '#207D80', 'pale_cyan': '#A3D3DE', 'deep_teal': '#006174', 'ice_white': '#F2F7FA', 'soft_gray': '#F4F4F4', 'gray': '#D9DADB', 'charcoal': '#4C4F50', 'petrol': '#193D4E', 'black': '#000000'}

ENVIRONMENT_COLORS = {base: COLORS[name] for base, name in {'tmean_c': 'aeon_dark', 'rh_mean': 'deep_teal', 'tp_sum': 'dark_purple', 'ndvi_mean_biweekly': 'aeon_light', 'ndvi_max_biweekly': 'petrol'}.items()}

SEASON_COLORS = {season: COLORS[name] for season, name in {'Verano': 'nature_white', 'Otoño': 'bright_purple', 'Invierno': 'pale_cyan', 'Primavera': 'aeon_light'}.items()}

EVENT_COLORS = {"hallazgos": COLORS["teal"], "casos": COLORS["black"]}

STAGE_COLORS = dict(zip(['eggs','larvae','pupae','adults'],
    [COLORS[k] for k in ['aeon_light','deep_teal','bright_purple','dark_purple']]))

LINE_STYLES = {"media": "-", "minimo": "-", "maximo": "-", "desviacion": "-"}


import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
from cycler import cycler

# Escalas continuas y categóricas derivadas de la paleta vigente.
MAP_CMAP = LinearSegmentedColormap.from_list('project_sequential',
    [COLORS[k] for k in ['ice_white','pale_cyan','teal','dark_purple']])
CORRELATION_CMAP = LinearSegmentedColormap.from_list('project_correlation',
    [COLORS[k] for k in ['dark_purple','bright_purple','white','pale_cyan','deep_teal']])
MAP_CMAP.set_bad(COLORS['gray'])
CORRELATION_CMAP.set_bad(COLORS['gray'])
CATEGORY_CMAP = ListedColormap([COLORS[k] for k in
    ['teal','aeon_light','bright_purple','dark_purple','pale_cyan','aeon_dark','nature_white','petrol']])


COLOR_CYCLE = [COLORS[k] for k in
    ['teal','dark_purple','aeon_light','bright_purple','petrol','aeon_dark','pale_cyan']]


def apply_plot_palette():
    """Apply shared colors while preserving each notebook's plot layout and sizes."""
    if MAP_CMAP.name not in mpl.colormaps:
        mpl.colormaps.register(MAP_CMAP)
    plt.rcParams.update({
        'figure.facecolor':COLORS['white'], 'axes.facecolor':COLORS['ice_white'],
        'text.color':COLORS['dark_purple'], 'axes.labelcolor':COLORS['dark_purple'],
        'axes.edgecolor':COLORS['gray'], 'grid.color':COLORS['gray'],
        'xtick.color':COLORS['charcoal'], 'ytick.color':COLORS['charcoal'],
        'legend.facecolor':COLORS['white'], 'legend.edgecolor':COLORS['gray'],
        'axes.prop_cycle':cycler(color=COLOR_CYCLE), 'image.cmap':MAP_CMAP.name,
        'patch.facecolor':COLORS['teal'], 'patch.edgecolor':COLORS['white'],
        'scatter.edgecolors':COLORS['white'], 'savefig.facecolor':COLORS['white'],
    })
