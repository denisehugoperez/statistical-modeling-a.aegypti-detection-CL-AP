"""Figuras temporales del EDA: constructores compartidos y grupos de figuras."""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from src.plot_palette import COLORS, ENVIRONMENT_COLORS, EVENT_COLORS, SEASON_COLORS


def population_mean(frame, column):
    """Promedio regional: valores ya ponderados / pesos de celdas válidas."""
    if not column.endswith('_popw'):
        return frame.groupby('epiweek')[column].mean()
    valid = frame[column].notna() & frame.population_weight.notna()
    groups = frame.loc[valid].groupby('epiweek')
    weights = groups.population_weight.sum(min_count=1)
    return groups[column].sum(min_count=1) / weights.where(weights.gt(0))


def normalized_figure(normalized, labels, colors, title, subtitle, name, columns,
                      calendar, seasons, finding_weeks, case_weeks, plan_output,
                      save_show, ncols=2, points=None):
    fig, ax = plt.subplots(figsize=(19, 8.4))
    fig.subplots_adjust(left=.065, right=.98, bottom=.22, top=.75)
    fig.patch.set_facecolor(COLORS['white'])
    ax.set_facecolor(COLORS['ice_white'])
    SEASON_BACKGROUND_ALPHA = .30
    SEASON_STRIP_ALPHA = .85
    for _, run in calendar.groupby(calendar.season.ne(calendar.season.shift()).cumsum()):
        season = run.season.iloc[0]
        left, right = run.epiweek.min() - .5, run.epiweek.max() + .5
        color = SEASON_COLORS[season]
        ax.axvspan(left, right, color=color, alpha=SEASON_BACKGROUND_ALPHA, zorder=0)
        # Banda superior más intensa, con etiquetas fuera de las curvas.
        ax.axvspan(left, right, ymin=1.015, ymax=1.075,
                               color=color, alpha=SEASON_STRIP_ALPHA, clip_on=False, zorder=4)
        if len(run) >= 3:
            ax.text((left + right) / 2, 1.045, season,
                                transform=ax.get_xaxis_transform(),
                                ha='center', va='center', color=COLORS['dark_purple'], fontsize=13,
                                fontweight='bold', clip_on=False, zorder=5)
        if left > .5:
            ax.axvline(left, color=COLORS['white'], linewidth=1.3, linestyle=(0, (5, 3)), zorder=.5)
    for week in finding_weeks:
        ax.axvline(week, color=EVENT_COLORS['hallazgos'], linewidth=2.4, linestyle=(0, (5, 3)), alpha=.85, zorder=1)
    for week in case_weeks:
        ax.axvline(week, color=EVENT_COLORS['casos'], linewidth=1.4, linestyle=(0, (4, 3)), alpha=.8, zorder=2)
    for c in columns:
        legend_label = labels[c]
        ax.plot(normalized.index,
                            normalized[c].to_numpy(dtype=float, na_value=np.nan),
                            color=colors[c], linestyle='-',
                            linewidth=2.3, marker='o' if c == points else None, markersize=4, label=legend_label, zorder=3)
    ax.set(xlim=(.5, 52.5), ylim=(-.03, 1.03), xticks=[1, *range(4, 53, 4)],
                       xlabel='Semana epidemiológica 2024 (domingo a sábado)',
                       ylabel='Valor normalizado (0–1)')
    ax.grid(axis='x', visible=False)
    ax.grid(axis='y', color=COLORS['gray'], linewidth=.6, alpha=.65)
    ax.tick_params(colors=COLORS['dark_purple'], labelsize=12)
    ax.xaxis.label.set_size(13)
    ax.yaxis.label.set_size(13)
    for spine in ax.spines.values(): spine.set_color(COLORS['gray'])
    fig.suptitle(title,
                             x=.065, y=.98, ha='left', fontsize=19, color=COLORS['dark_purple'], fontweight='bold')
    fig.text(.065, .935, subtitle,
                         fontsize=12, color=COLORS['charcoal'])
    variable_legend = ax.legend(loc='lower left', bbox_to_anchor=(0, 1.12),
                                           ncols=ncols, frameon=False, fontsize=12, title='Variables ambientales (unidad original)',
                                           title_fontsize=13, handlelength=2.5, columnspacing=1.2)
    ax.add_artist(variable_legend)
    event_handles = [Line2D([0], [0], color=EVENT_COLORS['hallazgos'], linewidth=3, linestyle=(0, (5, 3)), label='SE con hallazgos de vectores'),
                     Line2D([0], [0], color=EVENT_COLORS['casos'], linewidth=1.6, linestyle='--', label='SE con casos confirmados')]
    ax.legend(handles=event_handles, loc='upper left', bbox_to_anchor=(0, -.15),
                          ncols=2, frameon=False, fontsize=12)
    fig.legend(handles=[Patch(facecolor=SEASON_COLORS[s], alpha=SEASON_BACKGROUND_ALPHA, label=s) for s in seasons],
                           loc='lower center', bbox_to_anchor=(.5, .03), ncols=4, frameon=False,
                           title='Estaciones (fondo)', fontsize=12, title_fontsize=13)
    plan_output('series_temporales', name, columns)
    save_show(fig, 'series_temporales', name, columns)
    return event_handles

def environment_overview(LABELS, RESPONSE, SEASONS, calendar, inventory, panel, plan_output, save_show, split_column, summary_by, table, temporal, unit):

    # Conserva todas las series y sus nulos para tablas y análisis posteriores.
    environmental = inventory.loc[inventory.familia.isin(['temperatura', 'humedad', 'precipitación', 'NDVI']), 'columna']
    weekly = pd.DataFrame({c: population_mean(panel, c) if c in environmental.values
                           else summary_by(panel, c, 'epiweek') for c in temporal})
    weekly_n = panel.groupby('epiweek')[temporal].count()
    table(weekly, 'series_semanales', index=True)
    table(weekly_n, 'series_numero_celdas_validas', index=True)
    constant_series = weekly.columns[weekly.nunique(dropna=True) < 2].tolist()
    table(pd.DataFrame({'serie_constante': constant_series}), 'series_constantes')

    # Una columna por variable base; solo originales y preferencia por popw.
    environment_families = {'temperatura', 'humedad', 'precipitación', 'NDVI'}
    selected_variables = {'tmean_c', 'rh_mean', 'ndvi_mean_biweekly', 'tp_sum'}
    environment_inventory = inventory.loc[
        inventory.familia.isin(environment_families)
        & inventory.variable_base.isin(selected_variables)
        & inventory.transformacion.eq('original')
        & inventory.temporalidad.eq('temporal')
        & inventory.tipo.eq('numérica')
    ]
    environment_columns = []
    for base, rows in environment_inventory.groupby('variable_base', sort=False):
        preferred = rows.loc[rows.ponderada]
        environment_columns.append((preferred if not preferred.empty else rows).columna.iloc[0])
    assert environment_columns, 'No hay variables ambientales temporales originales.'

    environment_weekly = weekly[environment_columns].reindex(calendar.epiweek)
    minimum = environment_weekly.min()
    span = environment_weekly.max() - minimum
    normalized_environment = (environment_weekly - minimum) / span.replace(0, np.nan)
    for c in span.index[span.eq(0)]:
        normalized_environment[c] = environment_weekly[c].where(environment_weekly[c].isna(), 0.0)

    # La presencia de un registro por sí sola no se interpreta como un hallazgo o caso.
    weekly_events = panel.groupby('epiweek')[[RESPONSE, 'confirmed_cases']].sum(min_count=1).reindex(calendar.epiweek)
    weekly_events['con_hallazgos'] = weekly_events[RESPONSE].gt(0).fillna(False)
    weekly_events['con_casos'] = weekly_events.confirmed_cases.gt(0).fillna(False)
    finding_weeks = weekly_events.index[weekly_events.con_hallazgos]
    case_weeks = weekly_events.index[weekly_events.con_casos]
    table(environment_weekly, 'ambiente_semanal_seleccionado', index=True)
    table(normalized_environment, 'ambiente_semanal_normalizado', index=True)
    table(weekly_events, 'semanas_hallazgos_y_casos', index=True)
    table(pd.DataFrame({'columna': environment_columns, 'minimo_semanal': minimum,
                        'rango_semanal': span, 'semanas_validas': environment_weekly.count()}),
          'normalizacion_ambiente', index=True)

    labels = {c: f'{LABELS[split_column(c)[0]]} ({unit(split_column(c)[0])})'
              + (' (constante)' if span[c] == 0 else '') for c in environment_columns}
    event_handles = normalized_figure(
        normalized_environment, labels,
        {c: ENVIRONMENT_COLORS[split_column(c)[0]] for c in environment_columns},
        'Ambiente, hallazgos de vectores y casos confirmados',
        'Variables ponderadas por población · normalización 0–1 por variable',
        'ambiente_normalizado_hallazgos_casos_2024', environment_columns,
        calendar, SEASONS, finding_weeks, case_weeks, plan_output, save_show)
    return weekly, weekly_n, constant_series, environment_columns, weekly_events, finding_weeks, case_weeks, event_handles


def population_panels(LABELS, RESPONSE, calendar, finding_weeks, panel, plan_output, save_show, table, unit):
    # Figura complementaria: cinco paneles ambientales en unidades originales.
    climate_bases = ['tmean_c', 'rh_mean', 'tp_sum', 'ndvi_mean_biweekly', 'ndvi_max_biweekly']
    climate_columns = [base + '_popw' if base + '_popw' in panel else base
                       for base in climate_bases]
    climate_population_weekly = pd.DataFrame(index=pd.Index(calendar.epiweek, name='epiweek'))
    climate_valid_weights = pd.DataFrame(index=climate_population_weekly.index)
    for base, column in zip(climate_bases, climate_columns):
        climate_population_weekly[base] = population_mean(panel, column)
        valid = panel[column].notna() & panel.population_weight.notna()
        climate_valid_weights[base] = panel.loc[valid].groupby('epiweek').population_weight.sum(min_count=1)

    table(climate_population_weekly, 'clima_promedio_poblacional_semanal', index=True)
    table(climate_valid_weights, 'clima_pesos_validos_semanales', index=True)
    fig_climate, axes_climate = plt.subplots(5, 1, figsize=(19, 17), sharex=True)
    fig_climate.subplots_adjust(left=.09, right=.98, bottom=.09, top=.92, hspace=.16)
    fig_climate.patch.set_facecolor(COLORS['white'])
    for ax, base in zip(axes_climate, climate_bases):
        values = climate_population_weekly[base].to_numpy(dtype=float, na_value=np.nan)
        color = ENVIRONMENT_COLORS[base]
        series_label = LABELS[base] + ' (ponderada por población)'
        ax.set_facecolor(COLORS['ice_white'])
        for week in finding_weeks:
            ax.axvline(week, color=EVENT_COLORS['hallazgos'], linestyle=(0, (5, 3)),
                       linewidth=1.4, alpha=.6, zorder=1)
        if base == 'tp_sum':
            ax.bar(climate_population_weekly.index, values, width=.65,
                   color=color, alpha=.8, label=series_label, zorder=3)
            ax.set_ylim(bottom=0)
            ax.ticklabel_format(axis='y', style='sci', scilimits=(-3, 3), useMathText=True)
        else:
            ax.plot(climate_population_weekly.index, values, color=color,
                    linestyle='-', linewidth=2.3, label=series_label, zorder=3)
        ax.set_ylabel(f'{LABELS[base]} ({unit(base)})', fontsize=13)
        ax.set_xlim(.5, 52.5)
        ax.grid(axis='x', visible=False)
        ax.grid(axis='y', color=COLORS['gray'], linewidth=.6, alpha=.65)
        ax.tick_params(colors=COLORS['dark_purple'], labelsize=12)
        for spine in ax.spines.values(): spine.set_color(COLORS['gray'])
        ax.legend(loc='upper right', frameon=True, facecolor=COLORS['white'],
                  edgecolor=COLORS['gray'], framealpha=.9, fontsize=12)
    axes_climate[-1].set(xticks=[1, *range(4, 53, 4)],
                         xlabel='Semana epidemiológica 2024 (domingo a sábado)')
    axes_climate[-1].xaxis.label.set_size(13)
    fig_climate.suptitle('Semanas con hallazgos, clima y NDVI ponderados por población',
                         x=.09, y=.97, ha='left', fontsize=19,
                         fontweight='bold', color=COLORS['dark_purple'])
    fig_climate.text(.09, .945, 'Temperatura, humedad y NDVI: curvas continuas · precipitación: barras · unidades originales',
                     fontsize=12, color=COLORS['charcoal'])
    fig_climate.legend(handles=[Line2D([0], [0], color=EVENT_COLORS['hallazgos'],
                                      linewidth=2, linestyle=(0, (5, 3)),
                                      label='SE con hallazgos de vectores')],
                       loc='lower center', bbox_to_anchor=(.5, .02), frameon=False, fontsize=12)
    climate_name = 'ambiente_poblacional_cinco_paneles_hallazgos_2024'
    plan_output('series_temporales', climate_name, [*climate_columns, RESPONSE])
    save_show(fig_climate, 'series_temporales', climate_name, [*climate_columns, RESPONSE])


def environmental_lags(LABELS, RESPONSE, calendar, inventory, panel, plan_output, save_show, table, unit):
    """Hallazgos y cada variable con todos sus rezagos existentes."""
    from matplotlib.colors import to_rgb
    bases = ['rh_mean', 'tmean_c', 'tp_sum', 'ndvi_mean_biweekly', 'ndvi_max_biweekly']
    for base in bases:
        candidates = inventory.loc[inventory.variable_base.eq(base)
                                   & inventory.transformacion.isin(['original', 'lag'])].copy()
        candidates['orden_lag'] = candidates.lag.fillna(0)
        columns = [RESPONSE]
        labels = {RESPONSE: 'Hallazgos totales (conteo)'}
        for lag, rows in candidates.groupby('orden_lag', sort=True):
            preferred = rows.loc[rows.ponderada]
            column = (preferred if not preferred.empty else rows).columna.iloc[0]
            columns.append(column)
            labels[column] = f'{LABELS[base]} ({unit(base)})' + ('' if lag == 0 else f' · lag {int(lag)} SE')
        data = pd.DataFrame(index=pd.Index(calendar.epiweek, name='epiweek'))
        data[RESPONSE] = panel.groupby('epiweek')[RESPONSE].sum(min_count=1)
        for column in columns[1:]:
            data[column] = population_mean(panel, column)
        ranges = data.max() - data.min()
        normalized = (data-data.min()) / ranges.replace(0, np.nan)
        for column in ranges.index[ranges.eq(0)]:
            normalized[column] = data[column].where(data[column].isna(), 0.)
        name = ('hallazgos_totales_humedad_relativa_lags_2024' if base == 'rh_mean'
                else 'hallazgos_'+base+'_lags_2024')
        table(data, name+'_series', index=True)
        table(normalized, name+'_normalizados', index=True)
        fig, ax = plt.subplots(figsize=(19, 8.4))
        fig.subplots_adjust(left=.065, right=.98, bottom=.12, top=.72)
        fig.patch.set_facecolor(COLORS['white'])
        ax.set_facecolor(COLORS['ice_white'])
        for _, run in calendar.groupby(calendar.season.ne(calendar.season.shift()).cumsum()):
            week = run.epiweek.min()
            ax.axvline(week, color=COLORS['charcoal'], linestyle=':',
                       linewidth=1.2, alpha=.35, zorder=0)
            ax.text(week, 1.01, run.season.iloc[0], transform=ax.get_xaxis_transform(),
                    ha='left' if week == 1 else 'right' if week == 52 else 'center',
                    va='bottom', fontsize=11, color=COLORS['charcoal'], alpha=.65)
        color = ENVIRONMENT_COLORS[base] if base != 'tp_sum' else COLORS['teal']
        rgb = np.array(to_rgb(color))
        tones = [tuple(rgb*(1-light)+light) for light in np.linspace(0, .55, len(columns)-1)]
        for column, color in zip(columns, [COLORS['dark_purple'], *tones]):
            ax.plot(normalized.index, normalized[column].to_numpy(dtype=float, na_value=np.nan),
                    color=color, linewidth=2.3, linestyle='-', label=labels[column],
                    marker='o' if column == RESPONSE else None, markersize=4)
        ax.set(xlim=(.5, 52.5), ylim=(-.03, 1.03), xticks=[1, *range(4, 53, 4)],
               xlabel='Semana epidemiológica 2024 (domingo a sábado)',
               ylabel='Valor normalizado (0–1)')
        ax.xaxis.label.set_size(13)
        ax.yaxis.label.set_size(13)
        ax.tick_params(colors=COLORS['dark_purple'], labelsize=12)
        ax.grid(axis='x', visible=False)
        ax.grid(axis='y', color=COLORS['gray'], linewidth=.6, alpha=.65)
        for spine in ax.spines.values(): spine.set_color(COLORS['gray'])
        ax.legend(loc='lower left', bbox_to_anchor=(0, 1.04), ncols=(len(columns)+1)//2,
                  frameon=False, fontsize=12, handlelength=2.5)
        fig.suptitle('Hallazgos totales y '+LABELS[base].lower()+' con lags',
                     x=.065, y=.97, ha='left', fontsize=19, fontweight='bold', color=COLORS['dark_purple'])
        fig.text(.065, .92, 'Promedios ambientales ponderados por población · normalización 0–1 por serie',
                 fontsize=12, color=COLORS['charcoal'])
        plan_output('series_temporales', name, columns)
        save_show(fig, 'series_temporales', name, columns)


def temporal_axes(ax, calendar, finding_weeks=(), case_weeks=(), events=True):
    for _, run in calendar.groupby(calendar.season.ne(calendar.season.shift()).cumsum()):
        ax.axvspan(run.epiweek.min()-.5, run.epiweek.max()+.5,
                   color=SEASON_COLORS[run.season.iloc[0]], alpha=.30, zorder=0)
    if events:
        for week in finding_weeks:
            ax.axvline(week, color=EVENT_COLORS['hallazgos'], linestyle='--', alpha=.5, zorder=1)
        for week in case_weeks:
            ax.axvline(week, color=EVENT_COLORS['casos'], linestyle='--', alpha=.5, zorder=1)
    ax.set(xlim=(.5,52.5), xticks=[1,*range(4,53,4)])
    ax.grid(axis='x', visible=False)
    ax.grid(axis='y', color=COLORS['gray'], alpha=.6)
    ax.tick_params(labelsize=12, colors=COLORS['dark_purple'])



def local_cell_figures(LABELS, RESPONSE, calendar, panel, geo, plan_output, save_show, table, unit):
    # 6: una figura por celda con hallazgos; clima local sin ponderación espacial.
    local_bases=['tmean_c','rh_mean','tp_sum','ndvi_mean_biweekly']
    for grid in panel.loc[panel[RESPONSE].gt(0),'grid_id'].drop_duplicates():
        local=panel.loc[panel.grid_id.eq(grid)].set_index('epiweek').reindex(calendar.epiweek)
        fig,axes=plt.subplots(5,1,figsize=(19,15),sharex=True,layout='constrained')
        for ax in axes: temporal_axes(ax,calendar,events=False)
        local_weeks=local.index[local[RESPONSE].gt(0)]
        for ax in axes:
            for week in local_weeks:
                ax.axvline(week,color=EVENT_COLORS['hallazgos'],linestyle='--',alpha=.6)
        axes[0].plot(local.index,local[RESPONSE],color=COLORS['dark_purple'],marker='o',linestyle='-')
        axes[0].set_ylabel('Hallazgos totales (conteo)',fontsize=12)
        for ax,base in zip(axes[1:],local_bases):
            if base=='tp_sum': ax.bar(local.index,local[base],color=ENVIRONMENT_COLORS[base],width=.65)
            else: ax.plot(local.index,local[base],color=ENVIRONMENT_COLORS[base],linewidth=2.3,linestyle='-')
            ax.set_ylabel(f'{LABELS[base]} ({unit(base)})',fontsize=12)
        axes[-1].set_xlabel('Semana epidemiológica 2024',fontsize=13)
        fig.suptitle(f'Hallazgos y ambiente local · celda {grid}',fontsize=18)
        name=f'celda_{grid}_hallazgos_ambiente_2024'
        table(local[[RESPONSE,*local_bases]],name+'_series',index=True)
        plan_output('series_temporales',name,[RESPONSE,*local_bases])
        save_show(fig,'series_temporales',name,[RESPONSE,*local_bases])

        selected = geo.loc[geo.grid_id.eq(grid)]
        fig_map, ax_map = plt.subplots(figsize=(9, 11), layout='constrained')
        fig_map.patch.set_facecolor(COLORS['white'])
        geo.plot(ax=ax_map, color=COLORS['pale_cyan'], edgecolor=COLORS['white'], linewidth=.15)
        selected.plot(ax=ax_map, color=COLORS['dark_purple'],
                      edgecolor=COLORS['dark_purple'], linewidth=1.2, zorder=3)
        center = selected.geometry.iloc[0].representative_point()
        ax_map.annotate(f'Celda {grid}', xy=(center.x, center.y), xytext=(35, 25),
                        textcoords='offset points', fontsize=12, color=COLORS['dark_purple'],
                        arrowprops=dict(arrowstyle='->', color=COLORS['dark_purple'], linewidth=1.2),
                        bbox=dict(facecolor=COLORS['white'], edgecolor='none', alpha=.9))
        ax_map.set_title(f'Ubicación de la celda {grid} en la región',
                         fontsize=16, color=COLORS['dark_purple'])
        ax_map.set_axis_off()
        ax_map.legend(handles=[Patch(facecolor=COLORS['dark_purple'], label='Celda analizada'),
                               Patch(facecolor=COLORS['pale_cyan'], label='Resto de la grilla regional')],
                      loc='lower left', frameon=False, fontsize=11)
        map_name = f'celda_{grid}_ubicacion_regional_2024'
        plan_output('series_temporales', map_name, ['grid_id'])
        save_show(fig_map, 'series_temporales', map_name, ['grid_id'])



def rolling_figures(LABELS, calendar, finding_weeks, case_weeks, panel, plan_output, save_show, unit):
    def temporal_column(base, suffix=''):
        stem = base + suffix
        return stem + '_popw' if stem + '_popw' in panel else stem


    def temporal_mean(base, suffix='', frame=panel):
        column = temporal_column(base, suffix)
        return population_mean(frame, column).reindex(calendar.epiweek)


    # 7: originales y medias móviles de 4 SE ya existentes, en unidades originales.
    roll_bases=['tmean_c','rh_mean','tp_sum','ndvi_mean_biweekly','ndvi_max_biweekly']
    fig,axes=plt.subplots(5,1,figsize=(19,15),sharex=True,layout='constrained')
    roll_columns=[]
    for ax,base in zip(axes,roll_bases):
        temporal_axes(ax,calendar,finding_weeks,case_weeks)
        ax.plot(calendar.epiweek,temporal_mean(base),color=ENVIRONMENT_COLORS[base],
                linewidth=1.8,linestyle='-',label='Original')
        ax.plot(calendar.epiweek,temporal_mean(base,'_rolling_mean_4'),color=COLORS['charcoal'],
                linewidth=2.4,linestyle='-',label='Media móvil existente · 4 SE')
        ax.set_ylabel(f'{LABELS[base]} ({unit(base)})',fontsize=12)
        ax.legend(ncols=2,fontsize=12)
        roll_columns.extend([temporal_column(base),temporal_column(base,'_rolling_mean_4')])
    axes[-1].set_xlabel('Semana epidemiológica 2024',fontsize=13)
    fig.suptitle('Series ambientales y medias móviles ponderadas por población',fontsize=18)
    name='ambiente_originales_medias_moviles_2024'
    plan_output('series_temporales',name,roll_columns)
    save_show(fig,'series_temporales',name,roll_columns)






def altitude_zone_figures(panel, calendar, environment_columns, LABELS, SEASONS,
                          RESPONSE, split_column, unit, table, plan_output, save_show):
    """Una comparación ambiental por zona; ponderación cuando hay población."""
    from src.eda_common import altitude_zone, ZONE_ORDER
    zones = altitude_zone(panel.elevation_mean)
    for number, zone in enumerate(ZONE_ORDER, start=1):
        local = panel.loc[zones.eq(zone)]
        weighted = local.population_weight.sum() > 0
        data = pd.DataFrame(index=pd.Index(calendar.epiweek, name='epiweek'))
        for column in environment_columns:
            base = split_column(column)[0]
            data[column] = (population_mean(local, column) if weighted
                            else local.groupby('epiweek')[base].mean())
        ranges = data.max() - data.min()
        normalized = (data-data.min()) / ranges.replace(0, np.nan)
        for column in ranges.index[ranges.eq(0)]:
            normalized[column] = data[column].where(data[column].isna(), 0.)
        events = local.groupby('epiweek')[[RESPONSE,'confirmed_cases']].sum(min_count=1)
        findings = events.index[events[RESPONSE].gt(0).fillna(False)]
        cases = events.index[events.confirmed_cases.gt(0).fillna(False)]
        name = f'ambiente_zona_altitud_{number}_2024'
        table(data, name+'_series', index=True)
        table(normalized, name+'_normalizado', index=True)
        table(events, name+'_eventos', index=True)
        labels = {c: f'{LABELS[split_column(c)[0]]} ({unit(split_column(c)[0])})'
                  + (' (constante)' if ranges[c] == 0 else '') for c in data}
        subtitle = ('Promedios ponderados por población dentro de la zona' if weighted
                    else 'Medias simples entre celdas: la zona no tiene peso poblacional registrado')
        normalized_figure(normalized, labels,
            {c: ENVIRONMENT_COLORS[split_column(c)[0]] for c in data},
            'Series ambientales · '+zone, subtitle+' · normalización 0–1 por variable',
            name, environment_columns, calendar, SEASONS, findings, cases, plan_output, save_show)
