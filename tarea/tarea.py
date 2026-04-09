"""
tarea.py — Laboratorio 4: Probabilidad y Estadística con Spotify
Universidad Rafael Landívar · Curso de Inteligencia Artificial
Erick Rivas — 1116323
"""

import pandas as pd
import numpy as np
from datasets import load_dataset


# ---------------------------------------------------------------------------
# 1. CARGA Y PREPROCESAMIENTO
# ---------------------------------------------------------------------------

def cargar_datos() -> pd.DataFrame:
    """
    Carga el dataset de Spotify Tracks desde Hugging Face (114,000 canciones).

    Retorna
    -------
    pd.DataFrame
        DataFrame original sin modificaciones.
    """
    ds = load_dataset("maharshipandya/spotify-tracks-dataset", split="train")
    df = ds.to_pandas()
    return df


def preprocesar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Realiza el preprocesamiento básico del dataset:
      - Elimina filas duplicadas.
      - Elimina filas con valores nulos en columnas críticas.
      - Convierte la columna 'explicit' a tipo bool si no lo es.
      - Agrega la columna 'duration_min' (duración en minutos).

    Parámetros
    ----------
    df : pd.DataFrame
        DataFrame original cargado con cargar_datos().

    Retorna
    -------
    pd.DataFrame
        DataFrame limpio y enriquecido.
    """
    df = df.copy()
    df = df.drop_duplicates()
    df = df.dropna()
    df["explicit"] = df["explicit"].astype(bool)
    df["duration_min"] = df["duration_ms"] / 60000
    return df


# ---------------------------------------------------------------------------
# 2. PROBABILIDADES
# ---------------------------------------------------------------------------

def calcular_probabilidad_total(df: pd.DataFrame, columna: str, valor) -> float:
    """
    Calcula P(columna = valor) sobre todo el DataFrame.

    Parámetros
    ----------
    df : pd.DataFrame
    columna : str
        Nombre de la columna a evaluar.
    valor :
        Valor a buscar en la columna.

    Retorna
    -------
    float
        Probabilidad entre 0 y 1.
    """
    return (df[columna] == valor).mean()


def calcular_probabilidad_condicional(
    df: pd.DataFrame,
    condicion_col: str,
    condicion_valor,
    target_col: str,
    target_valor
) -> float:
    """
    Calcula P(target_col = target_valor | condicion_col = condicion_valor).

    Parámetros
    ----------
    df : pd.DataFrame
    condicion_col : str
        Columna de la condición.
    condicion_valor :
        Valor de la condición.
    target_col : str
        Columna objetivo.
    target_valor :
        Valor objetivo.

    Retorna
    -------
    float
        Probabilidad condicional entre 0 y 1.
    """
    subconjunto = df[df[condicion_col] == condicion_valor]
    if len(subconjunto) == 0:
        return 0.0
    return (subconjunto[target_col] == target_valor).mean()


# ---------------------------------------------------------------------------
# 3. MEDIDAS DE TENDENCIA CENTRAL Y DISPERSIÓN
# ---------------------------------------------------------------------------

def calcular_medidas_tendencia_central(df: pd.DataFrame, columna: str) -> dict:
    """
    Calcula media, mediana y moda de una columna numérica,
    ignorando valores nulos.

    Parámetros
    ----------
    df : pd.DataFrame
    columna : str

    Retorna
    -------
    dict
        Claves: 'media', 'mediana', 'moda'.
    """
    serie = df[columna].dropna()
    return {
        "media": serie.mean(),
        "mediana": serie.median(),
        "moda": serie.mode().iloc[0]
    }


def calcular_medidas_dispersion(df: pd.DataFrame, columna: str) -> dict:
    """
    Calcula varianza poblacional y desviación estándar poblacional (ddof=0).

    Parámetros
    ----------
    df : pd.DataFrame
    columna : str

    Retorna
    -------
    dict
        Claves: 'varianza', 'desviacion_estandar'.
    """
    serie = df[columna].dropna()
    return {
        "varianza": serie.var(ddof=0),
        "desviacion_estandar": serie.std(ddof=0)
    }


# ---------------------------------------------------------------------------
# 4. ANÁLISIS POR CATEGORÍA
# ---------------------------------------------------------------------------

def distribucion_por_categoria(df: pd.DataFrame, columna: str) -> pd.DataFrame:
    """
    Calcula la distribución de frecuencias (relativa) de una columna categórica.

    Parámetros
    ----------
    df : pd.DataFrame
    columna : str

    Retorna
    -------
    pd.DataFrame
        Columnas: [columna, 'proporcion'], ordenadas de mayor a menor.
    """
    proporciones = df[columna].value_counts(normalize=True)
    resultado = pd.DataFrame({
        columna: proporciones.index,
        "proporcion": proporciones.values
    })
    return resultado


def top_n_por_metrica(
    df: pd.DataFrame,
    columna_grupo: str,
    columna_metrica: str,
    n: int = 10,
    funcion_agregacion: str = "mean"
) -> pd.DataFrame:
    """
    Devuelve los N grupos con mayor valor de una métrica agregada.

    Parámetros
    ----------
    df : pd.DataFrame
    columna_grupo : str
        Columna por la que agrupar (ej. 'track_genre').
    columna_metrica : str
        Columna numérica a agregar (ej. 'popularity').
    n : int
        Cantidad de grupos a retornar.
    funcion_agregacion : str
        'mean', 'median', 'sum' o 'max'.

    Retorna
    -------
    pd.DataFrame
        Columnas: [columna_grupo, columna_metrica], ordenado descendente.
    """
    agrupado = df.groupby(columna_grupo)[columna_metrica].agg(funcion_agregacion)
    agrupado = agrupado.sort_values(ascending=False).head(n)
    resultado = agrupado.reset_index()
    resultado.columns = [columna_grupo, columna_metrica]
    return resultado


# ---------------------------------------------------------------------------
# 5. CORRELACIÓN Y POPULARIDAD
# ---------------------------------------------------------------------------

def calcular_correlacion(
    df: pd.DataFrame,
    col_x: str,
    col_y: str
) -> float:
    """
    Calcula el coeficiente de correlación de Pearson entre dos columnas numéricas.

    Parámetros
    ----------
    df : pd.DataFrame
    col_x : str
    col_y : str

    Retorna
    -------
    float
        Valor entre -1 y 1.
    """
    return df[col_x].corr(df[col_y])


def clasificar_popularidad(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega la columna 'categoria_popularidad' al DataFrame según los cuartiles
    de la columna 'popularity':
      - 'Baja'    : Q1 o menor
      - 'Media'   : entre Q1 y Q3
      - 'Alta'    : Q3 o mayor

    Parámetros
    ----------
    df : pd.DataFrame
        Debe contener la columna 'popularity'.

    Retorna
    -------
    pd.DataFrame
        DataFrame con la columna 'categoria_popularidad' agregada.
    """
    df = df.copy()
    q1 = df["popularity"].quantile(0.25)
    q3 = df["popularity"].quantile(0.75)

    condiciones = [
        df["popularity"] <= q1,
        df["popularity"] >= q3
    ]
    categorias = ["Baja", "Alta"]
    df["categoria_popularidad"] = np.select(condiciones, categorias, default="Media")
    return df
