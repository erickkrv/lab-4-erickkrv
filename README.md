# Laboratorio 4 — Probabilidad y Estadística con Spotify

Curso: **Inteligencia Artificial**  
Institución: **Universidad Rafael Landívar**  
Semestre: **Primer Semestre 2026**  
Modalidad: **Individual / GitHub Classroom**

Este repositorio está preparado para que implementes y verifiques el laboratorio siguiendo el enunciado original.

---

## 1) Objetivo del laboratorio

Aplicar técnicas de probabilidad y estadística sobre el dataset de Spotify para analizar factores asociados a la popularidad de canciones, implementando funciones en `tarea/tarea.py` y validándolas con `pytest`.

> Importante: debe trabajar en la carpeta `tarea/`.

---

## 2) Estructura esperada del repositorio

- `tarea/tarea.py`: implementación de las funciones solicitadas.
- `tarea/enunciado.ipynb`: notebook con EDA, gráficos, análisis guiado y conclusiones.
- `test/test_tarea.py`: pruebas automáticas (no modificar).
- `notebook_lab4.pdf`: exportación del notebook completamente ejecutado.

---

## 3) Entorno y dependencias

Instala dependencias:

```bash
pip install -r requirements.txt
```

> Recomendación: usa un entorno virtual de Python para aislar paquetes.

---

## 4) Flujo recomendado (paso a paso)

1. Implementa todas las funciones requeridas en `tarea/tarea.py`.
2. En el notebook `tarea/enunciado.ipynb`:
   - Completa todas las secciones.
   - Incluye **al menos 5 gráficos** bien etiquetados (título, ejes, leyenda cuando aplique).
   - Responde las **4 preguntas guiadas** de la Sección 7 con código y análisis en Markdown.
   - Escribe conclusiones en la Sección 8.
3. Ejecuta pruebas unitarias:

```bash
pytest test/test_tarea.py -v
```

4. Verifica ejecución completa del notebook:
   - Jupyter: **Kernel → Restart & Run All**.
5. Exporta PDF:
   - `notebook_lab4.pdf` con todas las celdas ejecutadas.
6. Haz commit y push antes de la fecha límite en GitHub Classroom.

---

## 5) Funciones requeridas en `tarea.py`

Debes implementar estas funciones:

- `cargar_datos()`
- `preprocesar_datos(df)`
- `calcular_probabilidad_total(df, col, val)`
- `calcular_probabilidad_condicional(df, cc, cv, tc, tv)`
- `calcular_medidas_tendencia_central(df, col)`
- `calcular_medidas_dispersion(df, col)`
- `distribucion_por_categoria(df, col)`
- `top_n_por_metrica(df, grupo, metrica, n, fn)`
- `calcular_correlacion(df, col_x, col_y)`
- `clasificar_popularidad(df)`

---

## 6) Criterios de evaluación (resumen)

- Pruebas unitarias (`pytest`) correctas.
- Implementación de funciones completa y generalizable.
- Notebook con EDA, gráficos y análisis interpretativo.
- Respuestas completas en Sección 7.
- Conclusiones sólidas en Sección 8.

---

## 7) Tips importantes

- Usa `ddof=0` para varianza y desviación estándar poblacional.
- Llama `preprocesar_datos(df)` antes de cualquier análisis.
- `categoria_popularidad` solo existe después de ejecutar `clasificar_popularidad(df)`.
- Si necesitas condicionales como `popularidad > 70`, crea primero una columna binaria auxiliar.
- Verifica timezone UTC del repositorio para no fallar con la fecha de entrega.

---

## 8) Comandos útiles

```bash
# correr pruebas
pytest test/test_tarea.py -v

# (opcional) ver resumen rápido de tests
pytest -q
```

---

## 9) Recordatorio final de entrega

Antes de entregar, confirma que tu repositorio tenga:

- `tarea/tarea.py`
- `tarea/enunciado.ipynb`
- `notebook_lab4.pdf`

Si todo lo anterior está completo y el notebook corre de principio a fin, estarás alineado con el enunciado original.
