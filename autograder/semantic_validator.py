import os
import nbformat

# =========================
# CONFIGURACIÓN DE RUTAS
# =========================
TAREA_PATH = "tarea/tarea.py"
NOTEBOOK_PATH = "tarea/enunciado.ipynb"

tarea_path = TAREA_PATH if os.path.exists(TAREA_PATH) else "tarea.py"
notebook_path = NOTEBOOK_PATH if os.path.exists(NOTEBOOK_PATH) else "enunciado.ipynb"


# =========================
# VALIDAR tarea.py
# =========================
def validar_tarea():
    if not os.path.exists(tarea_path):
        return False, ["No se encontró tarea.py"]

    errores = []

    with open(tarea_path, "r", encoding="utf-8") as f:
        codigo = f.read()

    funciones_requeridas = [
        "calcular_probabilidad_total",
        "calcular_probabilidad_condicional",
        "calcular_medidas_tendencia_central",
        "calcular_medidas_dispersion",
        "top_n_por_metrica",
        "calcular_correlacion"
    ]

    for fn in funciones_requeridas:
        if fn not in codigo:
            errores.append(f"Falta la función: {fn}")

    # ✔ VALIDACIÓN MÁS JUSTA
    if "raise ValueError" not in codigo:
        errores.append("No se detecta validación de errores con ValueError")

    return len(errores) == 0, errores


# =========================
# VALIDAR NOTEBOOK
# =========================
def validar_notebook():
    if not os.path.exists(notebook_path):
        return None, {
            "existe": False,
            "graficos": 0,
            "usa_funciones": False,
            "tiene_conclusiones": False,
            "problemas": ["No se encontró enunciado.ipynb"]
        }

    with open(notebook_path, encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    graficos = 0
    usa_funciones = False
    conclusiones = ""
    markdown_total = 0

    for cell in nb.cells:
        if cell.cell_type == "code":
            if "plt." in cell.source or "sns." in cell.source:
                graficos += 1

            if "calcular_" in cell.source or "top_n_" in cell.source:
                usa_funciones = True

        elif cell.cell_type == "markdown":
            markdown_total += 1
            if "conclus" in cell.source.lower():
                conclusiones += cell.source.lower()

    problemas = []

    if graficos < 3:
        problemas.append("Pocos gráficos (menos de 3)")

    if not usa_funciones:
        problemas.append("No se detecta uso de funciones de tarea.py")

    if len(conclusiones.split()) < 15:
        problemas.append("Conclusiones muy breves (poco análisis)")

    return nb, {
        "existe": True,
        "graficos": graficos,
        "usa_funciones": usa_funciones,
        "tiene_conclusiones": len(conclusiones) > 0,
        "problemas": problemas
    }


# =========================
# VALIDAR PREGUNTAS (MEJORADO)
# =========================
def validar_preguntas(nb):
    if nb is None:
        return 0, ["No hay notebook"]

    texto = ""

    for cell in nb.cells:
        if cell.cell_type == "markdown":
            texto += cell.source.lower()

    criterios = {
        "probabilidad total": ["probabilidad total", "p(", "frecuencia"],
        "probabilidad condicional": ["condicional", "|", "dado"],
        "medidas estadísticas": ["media", "mediana", "moda"],
        "correlación": ["correlacion", "relacion", "pearson"]
    }

    completas = 0
    faltantes = []

    for tema, palabras in criterios.items():
        if any(p in texto for p in palabras):
            completas += 1
        else:
            faltantes.append(tema)

    return completas, faltantes


# =========================
# CLASIFICAR CALIDAD
# =========================
def clasificar_calidad(problemas, completas):
    if len(problemas) == 0 and completas >= 3:
        return "alto"
    elif completas >= 2:
        return "medio"
    else:
        return "bajo"


# =========================
# MAIN
# =========================
def main():
    tarea_ok, errores_tarea = validar_tarea()
    nb, notebook_info = validar_notebook()
    completas, faltantes = validar_preguntas(nb)

    problemas = errores_tarea + notebook_info["problemas"]

    calidad = clasificar_calidad(problemas, completas)

    resultado = {
        "tarea_py": {
            "completo": tarea_ok,
            "errores": errores_tarea
        },
        "notebook": notebook_info,
        "preguntas": {
            "completas": completas,
            "faltantes": faltantes
        },
        "calidad": {
            "nivel": calidad,
            "comentarios": problemas
        },
        "resultado_final": {
            "cumple": tarea_ok and notebook_info["existe"],
            "observaciones": problemas
        }
    }

    return resultado


if __name__ == "__main__":
    main()