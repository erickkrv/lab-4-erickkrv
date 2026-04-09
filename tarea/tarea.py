"""
tarea.py — Laboratorio 4: Probabilidad y Estadística con Spotify
Universidad Rafael Landívar · Curso de Inteligencia Artificial

Completa cada función según el enunciado.
"""

import pandas as pd


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
    # TODO: Cargar el CSV desde la URL del enunciado y retornar el DataFrame.
    raise NotImplementedError("Implementa cargar_datos()")


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
    # TODO: Aplicar limpieza y crear duration_min = duration_ms / 60000.
    raise NotImplementedError("Implementa preprocesar_datos(df)")


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
    # TODO: Calcular frecuencia relativa de (df[columna] == valor).
    raise NotImplementedError("Implementa calcular_probabilidad_total(df, columna, valor)")


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
    # TODO: Filtrar por condición y calcular la proporción del target.
    raise NotImplementedError(
        "Implementa calcular_probabilidad_condicional(df, condicion_col, condicion_valor, target_col, target_valor)"
    )


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
    # TODO: Retornar un dict con media, mediana y moda.
    raise NotImplementedError("Implementa calcular_medidas_tendencia_central(df, columna)")


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
    # TODO: Usar ddof=0 para varianza y desviación estándar poblacional.
    raise NotImplementedError("Implementa calcular_medidas_dispersion(df, columna)")


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
    # TODO: Calcular value_counts(normalize=True) y devolver DataFrame.
    raise NotImplementedError("Implementa distribucion_por_categoria(df, columna)")


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
    # TODO: Agrupar, agregar con la función indicada, ordenar desc y tomar top n.
    raise NotImplementedError(
        "Implementa top_n_por_metrica(df, columna_grupo, columna_metrica, n, funcion_agregacion)"
    )


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
    # TODO: Calcular correlación de Pearson entre col_x y col_y.
    raise NotImplementedError("Implementa calcular_correlacion(df, col_x, col_y)")


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
    # TODO: Calcular Q1 y Q3 y clasificar en Baja/Media/Alta.
    raise NotImplementedError("Implementa clasificar_popularidad(df)")
