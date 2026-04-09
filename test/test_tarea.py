import pytest
import pandas as pd
import numpy as np

from tarea import *


# =========================
# FIXTURE PRINCIPAL
# =========================
@pytest.fixture(scope="module")
def df():
    df = cargar_datos()
    df = preprocesar_datos(df)
    return df


# =========================
# FIXTURE SINTÉTICO
# =========================
@pytest.fixture
def df_fake():
    data = {
        "col": ["A", "A", "B", "B", "B"],
        "val": [1, 2, 3, 4, 5],
        "flag": [True, False, True, True, False]
    }
    return pd.DataFrame(data)


# =========================
# 1. PROBABILIDAD TOTAL (ANTI-HARDCODE)
# =========================
class TestProbabilidadTotalAntiTrampa:

    def test_dataset_sintetico(self, df_fake):
        p = calcular_probabilidad_total(df_fake, "col", "A")
        assert pytest.approx(p, 0.001) == 2/5

    def test_subset_random(self, df):
        sample = df.sample(500, random_state=42)

        p1 = calcular_probabilidad_total(sample, "explicit", True)
        manual = (sample["explicit"] == True).mean()

        assert pytest.approx(p1, 0.001) == manual

    def test_no_hardcode(self, df):
        # cambia el dataset dinámicamente
        sample = df.sample(1000, random_state=1)

        p1 = calcular_probabilidad_total(sample, "explicit", True)
        p2 = calcular_probabilidad_total(sample, "explicit", False)

        assert pytest.approx(p1 + p2, 0.01) == 1


# =========================
# 2. PROBABILIDAD CONDICIONAL (ANTI-TRAMPA)
# =========================
class TestProbabilidadCondicionalAntiTrampa:

    def test_sintetico(self, df_fake):
        p = calcular_probabilidad_condicional(df_fake, "col", "B", "flag", True)

        # manual: B = [3,4,5] → flag True = [True, True, False] → 2/3
        assert pytest.approx(p, 0.001) == 2/3

    def test_random(self, df):
        sample = df.sample(800, random_state=42)

        condicion = sample[sample["explicit"] == True]
        if len(condicion) == 0:
            return

        manual = (condicion["explicit"] == True).mean()

        p = calcular_probabilidad_condicional(sample, "explicit", True, "explicit", True)

        assert pytest.approx(p, 0.001) == manual


# =========================
# 3. MEDIDAS ESTADÍSTICAS (ANTI-TRAMPA)
# =========================
class TestMedidasAntiTrampa:

    def test_media_correcta(self, df_fake):
        res = calcular_medidas_tendencia_central(df_fake, "val")
        assert pytest.approx(res["media"], 0.001) == np.mean([1,2,3,4,5])

    def test_varianza_correcta(self, df_fake):
        res = calcular_medidas_dispersion(df_fake, "val")
        assert pytest.approx(res["varianza"], 0.001) == np.var([1,2,3,4,5], ddof=0)

    def test_random_dataset(self, df):
        sample = df.sample(500, random_state=10)

        res = calcular_medidas_tendencia_central(sample, "duration_min")

        assert pytest.approx(res["media"], 0.01) == sample["duration_min"].mean()


# =========================
# 4. TOP N (ANTI-HARDCODE)
# =========================
class TestTopNAntiTrampa:

    def test_sintetico(self):
        df = pd.DataFrame({
            "grupo": ["A", "A", "B", "B", "C"],
            "val": [10, 20, 30, 40, 5]
        })

        res = top_n_por_metrica(df, "grupo", "val", 1, "mean")

        # B tiene promedio más alto
        assert res.iloc[0]["grupo"] == "B"

    def test_random(self, df):
        sample = df.sample(1000, random_state=5)

        res = top_n_por_metrica(sample, "track_genre", "popularity", 3, "mean")

        assert len(res) == 3


# =========================
# 5. CORRELACIÓN (ANTI-TRAMPA)
# =========================
class TestCorrelacionAntiTrampa:

    def test_sintetico_perfecto(self):
        df = pd.DataFrame({
            "x": [1,2,3,4,5],
            "y": [2,4,6,8,10]
        })

        corr = calcular_correlacion(df, "x", "y")
        assert pytest.approx(corr, 0.001) == 1.0

    def test_random(self, df):
        sample = df.sample(500, random_state=3)

        corr = calcular_correlacion(sample, "energy", "popularity")

        assert -1 <= corr <= 1


# =========================
# 6. CLASIFICACIÓN (ANTI-TRAMPA)
# =========================
class TestClasificacionAntiTrampa:

    def test_crea_columna(self, df):
        df2 = clasificar_popularidad(df)
        assert "categoria_popularidad" in df2.columns

    def test_categorias(self, df):
        df2 = clasificar_popularidad(df)
        cats = set(df2["categoria_popularidad"].unique())

        assert cats.issubset({"Baja", "Media", "Alta"})

    def test_balance_aproximado(self, df):
        df2 = clasificar_popularidad(df)

        counts = df2["categoria_popularidad"].value_counts(normalize=True)

        # Cuartiles → distribución más o menos balanceada
        assert all(c > 0.2 for c in counts)