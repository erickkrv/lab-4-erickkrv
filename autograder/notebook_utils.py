import nbformat

def evaluar_notebook(path):
    nb = nbformat.read(path, as_version=4)

    codigo = 0
    markdown = 0
    graficos = 0
    usa_funciones = False
    conclusiones = False

    funciones_clave = [
        "calcular_probabilidad_total",
        "calcular_probabilidad_condicional",
        "calcular_correlacion",
        "top_n_por_metrica"
    ]

    for cell in nb.cells:
        if cell.cell_type == "code":
            codigo += 1
            src = cell.source

            if "plt." in src or "sns." in src:
                graficos += 1

            if any(fn in src for fn in funciones_clave):
                usa_funciones = True

        elif cell.cell_type == "markdown":
            markdown += 1

            if "Conclusiones" in cell.source:
                conclusiones = True

    return {
        "codigo": codigo,
        "markdown": markdown,
        "graficos": graficos,
        "usa_funciones": usa_funciones,
        "conclusiones": conclusiones
    }