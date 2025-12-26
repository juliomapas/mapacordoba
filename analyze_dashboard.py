"""
Script para analizar el dashboard usando las herramientas del MCP Server
Genera un reporte completo con recomendaciones de UI/UX
"""

import json
import asyncio
from pathlib import Path
import sys
import io

# Configurar stdout para manejar encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Importar las funciones de análisis del MCP server
sys.path.insert(0, str(Path(__file__).parent))

from src.mcp_server.server import (
    analyze_responsive_design,
    validate_party_colors,
    check_accessibility,
    suggest_ui_improvements,
    get_design_recommendations
)


async def main():
    """Ejecutar análisis completo del dashboard"""

    # Leer el código del dashboard
    with open('app.py', 'r', encoding='utf-8') as f:
        dashboard_code = f.read()

    print("=" * 80)
    print("ANÁLISIS COMPLETO DEL DASHBOARD ELECTORAL")
    print("=" * 80)
    print()

    # 1. Análisis de Diseño Responsivo
    print("1. ANÁLISIS DE DISEÑO RESPONSIVO")
    print("-" * 80)
    responsive_result = await analyze_responsive_design(dashboard_code)
    responsive_data = json.loads(responsive_result[0].text)
    print(f"Score: {responsive_data['score']}/100 - Estado: {responsive_data['status']}")
    print(f"Resumen: {responsive_data['summary']}")

    if responsive_data['issues']:
        print("\nProblemas encontrados:")
        for issue in responsive_data['issues']:
            print(f"  [{issue['severity'].upper()}] {issue['message']}")
            print(f"    - {issue['recommendation']}")

    if responsive_data['recommendations']:
        print("\nRecomendaciones:")
        for rec in responsive_data['recommendations']:
            print(f"  * {rec['message']}")
    print()

    # 2. Validación de Colores de Partidos
    print("2. VALIDACIÓN DE COLORES DE PARTIDOS POLÍTICOS")
    print("-" * 80)
    colors_result = await validate_party_colors(dashboard_code)
    colors_data = json.loads(colors_result[0].text)
    print(f"Valido: {'SI' if colors_data['valid'] else 'NO'}")
    print(f"Score: {colors_data['validation_score']:.1f}%")
    print(f"Resumen: {colors_data['summary']}")

    if colors_data['violations']:
        print("\nVIOLACIONES CRITICAS:")
        for v in colors_data['violations']:
            print(f"  * Partido: {v['party']}")
            print(f"    Color actual: {v['current_color']}")
            print(f"    Color esperado: {v['expected_color']}")
            print(f"    Fix: {v['fix']}")

    if colors_data['warnings']:
        print("\nAdvertencias:")
        for w in colors_data['warnings']:
            if 'party' in w:
                print(f"  * {w['message']}: {w['party']} ({w['color']})")
    print()

    # 3. Verificación de Accesibilidad
    print("3. VERIFICACIÓN DE ACCESIBILIDAD (WCAG 2.1 AA)")
    print("-" * 80)
    a11y_result = await check_accessibility(dashboard_code)
    a11y_data = json.loads(a11y_result[0].text)
    print(f"Score de Accesibilidad: {a11y_data['accessibility_score']}/100")
    print(f"Nivel de Cumplimiento: {a11y_data['compliance_level']}")
    print(f"Total de problemas: {a11y_data['total_issues']}")
    print(f"  - Alta severidad: {a11y_data['high_severity']}")
    print(f"  - Media severidad: {a11y_data['medium_severity']}")
    print(f"  - Baja severidad: {a11y_data['low_severity']}")

    if a11y_data['issues']:
        print("\nProblemas de Accesibilidad:")
        for issue in a11y_data['issues']:
            print(f"\n  [{issue['severity'].upper()}] {issue['wcag_criterion']}")
            print(f"  {issue['message']}")
            print(f"  - {issue['recommendation']}")
            if 'example' in issue:
                print(f"    Ejemplo: {issue['example']}")
    print()

    # 4. Sugerencias de Mejora UI/UX
    print("4. SUGERENCIAS DE MEJORA UI/UX")
    print("-" * 80)
    ui_result = await suggest_ui_improvements(dashboard_code, "all")
    ui_data = json.loads(ui_result[0].text)
    print(f"Total de sugerencias: {ui_data['total_suggestions']}")
    print(f"Área de enfoque: {ui_data['focus_area']}")

    # Agrupar por categoría
    categories = {}
    for sug in ui_data['suggestions']:
        cat = sug['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(sug)

    for category, suggestions in categories.items():
        print(f"\n  {category.upper()}: {len(suggestions)} sugerencias")
        for sug in suggestions:
            priority_symbol = "[HIGH]" if sug['priority'] == 'high' else "[MED]" if sug['priority'] == 'medium' else "[LOW]"
            print(f"    {priority_symbol} {sug['message']}")
            print(f"      - {sug['recommendation']}")
            if 'example' in sug:
                print(f"        Ejemplo: {sug['example']}")

    if ui_data['priority_actions']:
        print("\n  ACCIONES PRIORITARIAS (Alta prioridad):")
        for action in ui_data['priority_actions']:
            print(f"    * {action['message']}")
            print(f"      - {action['recommendation']}")
    print()

    # 5. Recomendaciones Específicas de Diseño
    print("5. RECOMENDACIONES ESPECÍFICAS DE DISEÑO")
    print("-" * 80)

    categories_to_check = ['responsive', 'colors', 'typography', 'charts', 'maps']

    for category in categories_to_check:
        rec_result = await get_design_recommendations(category)
        rec_data = json.loads(rec_result[0].text)

        print(f"\n  {rec_data.get('category', category).upper()}")
        print("  " + "-" * 76)

        if 'best_practices' in rec_data:
            print("  Mejores Practicas:")
            for practice in rec_data['best_practices'][:3]:  # Mostrar solo 3
                print(f"    * {practice}")

        if 'code_examples' in rec_data and isinstance(rec_data['code_examples'], dict):
            print("  Ejemplos de Código:")
            for name, code in list(rec_data['code_examples'].items())[:2]:  # Mostrar solo 2
                print(f"    {name}: {code}")

    print("\n" + "=" * 80)
    print("RESUMEN EJECUTIVO")
    print("=" * 80)

    print(f"""
Diseno Responsivo:        {responsive_data['score']}/100 ({responsive_data['status']})
Colores Partidos:         {'VALIDO' if colors_data['valid'] else 'REQUIERE CORRECCION'}
Accesibilidad:            {a11y_data['accessibility_score']}/100 ({a11y_data['compliance_level']})
Sugerencias UI/UX:        {ui_data['total_suggestions']} mejoras identificadas

PRIORIDADES INMEDIATAS:
1. Actualizar choroplethmapbox a choroplethmap (deprecated en Plotly)
2. Actualizar scattermapbox a scattermap (deprecated en Plotly)
3. Mejorar accesibilidad: agregar ARIA labels a graficos interactivos
4. Revisar jerarquia de headings para SEO y accesibilidad
5. Considerar diseno responsivo para xs/sm breakpoints (moviles)

DOCUMENTACION GENERADA: Este reporte incluye toda la informacion necesaria para
mejorar el dashboard siguiendo las mejores practicas de UI/UX actuales (2025).
    """)

    # Guardar reporte completo en JSON
    report = {
        "fecha_analisis": "2025-12-25",
        "dashboard": "Electoral Córdoba Capital 2021-2025",
        "responsive_design": responsive_data,
        "party_colors": colors_data,
        "accessibility": a11y_data,
        "ui_suggestions": ui_data
    }

    with open('outputs/analysis/dashboard_ui_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print("\nOK - Reporte completo guardado en: outputs/analysis/dashboard_ui_analysis.json")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
