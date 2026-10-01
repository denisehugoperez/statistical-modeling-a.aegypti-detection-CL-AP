"""Calendario epidemiológico oficial de Chile para 2024.

Las semanas comienzan el domingo y terminan el sábado. La SE1 comienza el
31-12-2023 y la SE52 termina el 28-12-2024.
"""

from __future__ import annotations

import pandas as pd


EPI_YEAR = 2024
EPI_START = pd.Timestamp("2023-12-31")
EPI_END = pd.Timestamp("2024-12-28")
N_EPIWEEKS = 52


def build_epidemiological_calendar() -> pd.DataFrame:
    """Construye la tabla oficial de las 52 semanas epidemiológicas."""
    starts = pd.date_range(EPI_START, periods=N_EPIWEEKS, freq="7D")
    return pd.DataFrame(
        {
            "epiweek": range(1, N_EPIWEEKS + 1),
            "start_date": starts,
            "end_date": starts + pd.Timedelta(days=6),
        }
    )


def assign_epiweek_2024(dates) -> pd.Series:
    """Asigna vectorizadamente la SE 2024; fechas fuera del rango quedan NA."""
    if isinstance(dates, pd.Series):
        index = dates.index
        values = pd.to_datetime(dates, errors="coerce")
    else:
        values = pd.Series(pd.to_datetime(dates, errors="coerce"))
        index = values.index

    result = pd.Series(pd.array([pd.NA] * len(values), dtype="Int64"), index=index)
    valid = values.between(EPI_START, EPI_END, inclusive="both")
    if valid.any():
        offsets = (values.loc[valid] - EPI_START).dt.days // 7
        result.loc[valid] = (offsets + 1).astype("Int64")
    return result


def validate_epidemiological_range(
    frame: pd.DataFrame,
    year_column: str = "year",
    epiweek_column: str = "epiweek",
) -> None:
    """Valida que las llaves temporales correspondan exclusivamente a SE1..SE52."""
    required = {year_column, epiweek_column}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Faltan columnas temporales requeridas: {sorted(missing)}")

    years = set(frame[year_column].dropna().astype(int))
    if years != {EPI_YEAR}:
        raise ValueError(
            f"El año epidemiológico debe ser {EPI_YEAR}; se encontraron {sorted(years)}."
        )

    weeks = set(frame[epiweek_column].dropna().astype(int))
    invalid = sorted(weeks.difference(range(1, N_EPIWEEKS + 1)))
    if invalid:
        raise ValueError(f"SE fuera del rango oficial 1..{N_EPIWEEKS}: {invalid}")

