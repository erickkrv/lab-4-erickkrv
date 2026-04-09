import subprocess
import os
import json
import sys
import re
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from autograder.semantic_validator import main as semantic_main


# =========================
# 1. EJECUTAR NOTEBOOK
# =========================
def ejecutar_notebook(path):
    try:
        with open(path) as f:
            nb = nbformat.read(f, as_version=4)

        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

        # 👇 CLAVE
        ep.preprocess(nb, {'metadata': {'path': 'tarea'}})

        return True, "Notebook ejecutado correctamente"

    except Exception as e:
        return False, str(e)


# =========================
# 2. ANALIZAR NOTEBOOK
# =========================
def analizar_notebook(path):
    with open(path) as f:
        nb = nbformat.read(f, as_version=4)

    codigo = 0
    markdown = 0
    graficos = 0
    usa_funciones = False
    conclusiones = False

    funciones = ["def ", "lambda "]

    for cell in nb.cells:
        if cell.cell_type == "code":
            codigo += 1

            if "plt." in cell.source or "matplotlib" in cell.source:
                graficos += 1

            if any(f in cell.source for f in funciones):
                usa_funciones = True

        elif cell.cell_type == "markdown":
            markdown += 1

            if "conclusiones" in cell.source.lower():
                conclusiones = True

    return {
        "codigo": codigo,
        "markdown": markdown,
        "graficos": graficos,
        "usa_funciones": usa_funciones,
        "conclusiones": conclusiones,
        "nb": nb
    }


# =========================
# 3. EVALUAR PREGUNTAS
# =========================
def evaluar_preguntas(nb):
    score = 0

    for cell in nb.cells:
        if cell.cell_type == "markdown":
            texto = cell.source.lower()

            if "respuesta" in texto:
                score += 3

    return min(score, 15)


# =========================
# 4. PYTEST SCORE
# =========================
def evaluar_pytest():
    result = subprocess.run(
        ["pytest", "test/test_tarea.py", "-q"],
        capture_output=True,
        text=True
    )

    output = f"{result.stdout}\n{result.stderr}"

    passed_match = re.search(r"(\d+)\s+passed", output)
    failed_match = re.search(r"(\d+)\s+failed", output)
    error_match = re.search(r"(\d+)\s+error", output)

    passed = int(passed_match.group(1)) if passed_match else 0
    failed = int(failed_match.group(1)) if failed_match else 0
    errors = int(error_match.group(1)) if error_match else 0

    total = passed + failed + errors

    if total == 0:
        return 0

    ratio = passed / total

    if ratio == 1:
        return 30
    elif ratio >= 0.8:
        return 25
    elif ratio >= 0.6:
        return 20
    else:
        return 0


def hay_not_implemented():
    tarea_path = "tarea/tarea.py"

    if not os.path.exists(tarea_path):
        return True

    with open(tarea_path, "r", encoding="utf-8") as f:
        contenido = f.read()

    return "NotImplementedError" in contenido


def extraer_error_clave(error_str):
    lineas = error_str.split("\n")

    for linea in lineas:
        if "Error" in linea or "Exception" in linea:
            return linea.strip()

    return "Error no identificado"


def imprimir_resultados(resultado):
    print("\n" + "=" * 30)
    print("      RESULTADO FINAL")
    print("=" * 30 + "\n")

    print(f"🧪 Tests (código):        {resultado['pytest']:>3} / 30")
    print(f"🧩 Implementación:        {resultado['implementacion']:>3} / 25")
    print(f"📓 Notebook:              {resultado['notebook']:>3} / 20")
    print(f"🧠 Preguntas:             {resultado['preguntas']:>3} / 15")
    print(f"📝 Conclusiones:          {resultado['conclusiones']:>3} / 10")
    print("-" * 30)
    print(f"🎯 NOTA FINAL:            {resultado['final']:>3} / 100\n")

    if resultado["feedback"]:
        print("⚠️ Observaciones:")
        for f in resultado["feedback"]:
            print(f" - {f}")


# =========================
# MAIN
# =========================
def main():
    notebook_path = "tarea/enunciado.ipynb"

    ejecuta, mensaje = ejecutar_notebook(notebook_path)
    analisis = analizar_notebook(notebook_path)
    nb = analisis["nb"]

    pytest_score = evaluar_pytest()

    feedback = []

    # =========================
    # NOTEBOOK SCORE (20 pts)
    # =========================
    score_nb = 0

    if analisis["codigo"] >= 5:
        score_nb += 5
    else:
        feedback.append("Pocas celdas de código")

    if analisis["markdown"] >= 5:
        score_nb += 5
    else:
        feedback.append("Pocas explicaciones en markdown")

    if analisis["graficos"] >= 1:
        score_nb += 5
    else:
        feedback.append("Faltan gráficos")

    if analisis["usa_funciones"]:
        score_nb += 3
    else:
        feedback.append("No se usan funciones")

    if analisis["conclusiones"]:
        score_nb += 2
    else:
        feedback.append("Faltan conclusiones")

    # preguntas
    score_preguntas = evaluar_preguntas(nb)

    # penalización si no ejecuta
    if not ejecuta:
        score_nb = max(score_nb - 10, 0)
        feedback.append(f"Error al ejecutar notebook: {extraer_error_clave(mensaje)}")

    # =========================
    # SEMANTIC VALIDATION
    # =========================
    semantic_result = semantic_main()
    feedback_semantic = semantic_result["calidad"]["comentarios"]

    # =========================
    # IMPLEMENTACIÓN (25 pts)
    # =========================
    score_implementacion = round((pytest_score / 30) * 25, 2)

    # detección plantilla
    plantilla_sin_implementar = hay_not_implemented()

    # =========================
    # CONCLUSIONES (10 pts)
    # =========================
    texto_semantic = " ".join(feedback_semantic).lower()

    if "conclusiones demasiado cortas" in texto_semantic:
        score_conclusiones = 5
    elif "conclusiones" in texto_semantic:
        score_conclusiones = 8
    else:
        score_conclusiones = 10

    # 🔥 penalización total
    if plantilla_sin_implementar:
        pytest_score = 0
        score_implementacion = 0
        score_nb = 0
        score_preguntas = 0
        score_conclusiones = 0
        feedback.append("Se detectó NotImplementedError en tarea.py")

    # unir feedback
    feedback_total = feedback + feedback_semantic

    # nota final
    final = (
        pytest_score +
        score_implementacion +
        score_nb +
        score_preguntas +
        score_conclusiones
    )

    # =========================
    # EXPORTAR RESULTADOS
    # =========================
    resultado = {
        "pytest": pytest_score,
        "implementacion": score_implementacion,
        "notebook": score_nb,
        "preguntas": score_preguntas,
        "conclusiones": score_conclusiones,
        "final": final,
        "feedback": feedback_total,
        "ejecucion": mensaje
    }

    with open("resultado_autograder.json", "w") as f:
        json.dump(resultado, f, indent=4)

    imprimir_resultados(resultado)

    # =========================
    # GITHUB ACTIONS OUTPUT
    # =========================
    print(f"::notice title=Nota Final::{final}/100")

    if final >= 90:
        print("::notice title=Feedback::Excelente trabajo")
    elif final >= 70:
        print("::notice title=Feedback::Buen trabajo, pero puede mejorar")
    else:
        print("::warning title=Feedback::Revisar implementación y notebook")

    print(f"::notice title=Detalle::Tests: {pytest_score}/30 | Notebook: {score_nb}/40 | Preguntas: {score_preguntas}/20")
    print("\033[92m✔ Finalizaron los TEST, revise...\033[0m")


if __name__ == "__main__":
    main()