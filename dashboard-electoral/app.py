"""
Dashboard Electoral Córdoba Capital 2021-2025
Aplicación web interactiva con Dash y Plotly

Ejecutar:
    python app.py

Luego abrir: http://127.0.0.1:8050/
"""
import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import geopandas as gpd
import json
import folium
from folium import GeoJson
import matplotlib.colors as mcolors

# ============================================================================
# CONFIGURACIÓN Y DATOS
# ============================================================================

# Paleta de colores
PARTY_COLORS = {
    'LA LIBERTAD AVANZA': '#9370DB',
    'ALIANZA LA LIBERTAD AVANZA': '#9370DB',
    'JUNTOS POR EL CAMBIO': '#FFD700',
    'HACEMOS POR CÓRDOBA': '#87CEEB',
    'UNIÓN POR LA PATRIA': '#0047AB',
    'FRENTE DE IZQUIERDA': '#DC143C',
    'FRENTE DE IZQUIERDA  Y DE TRABAJADORES - UNIDAD': '#DC143C',
    'DEFAULT': '#CCCCCC'
}

# Cargar datos
print("Cargando datos...")
gdf_geo = gpd.read_file('data/raw/Seccionales_Circuitos.geojson')
gdf_geo['geometry'] = gdf_geo.geometry.buffer(0)
dissolved = gdf_geo.dissolve(by='Seccional').reset_index()
dissolved['geometry'] = dissolved.geometry.simplify(tolerance=0.001, preserve_topology=True)
dissolved['Seccional'] = dissolved['Seccional'].astype(str)
dissolved['centroid'] = dissolved.geometry.centroid
dissolved['lat'] = dissolved['centroid'].y
dissolved['lon'] = dissolved['centroid'].x

df_electoral = pd.read_csv('data/processed/electoral_data_clean.csv')
df_electoral['seccional'] = df_electoral['seccional'].astype(str)

# Calcular ganadores
ganadores = df_electoral.loc[df_electoral.groupby(['anio', 'seccional'])['votos'].idxmax()]

print(f"Datos cargados: {len(dissolved)} seccionales, {len(df_electoral)} registros")

# Función para crear mapa Folium con colores por partido
def create_folium_map(selected_year):
    """Crea mapa Folium con colores según partido ganador"""

    # Filtrar ganadores del año
    gan_year = ganadores[ganadores['anio'] == selected_year].copy()

    # Merge con geometrías
    gdf_year = dissolved.merge(
        gan_year,
        left_on='Seccional',
        right_on='seccional',
        how='left'
    )

    # Asignar colores por partido
    gdf_year['color'] = gdf_year['agrupacion'].apply(
        lambda x: PARTY_COLORS.get(x, PARTY_COLORS['DEFAULT']) if pd.notna(x) else PARTY_COLORS['DEFAULT']
    )

    # Crear mapa base
    m = folium.Map(
        location=[-31.4201, -64.1888],
        zoom_start=12,
        tiles='CartoDB positron',
        min_zoom=11,
        max_zoom=15
    )

    # Función de estilo normal
    def style_function(feature):
        seccional = feature['properties']['Seccional']
        seccional_data = gdf_year[gdf_year['Seccional'] == seccional]

        if len(seccional_data) > 0:
            color = seccional_data['color'].iloc[0]
        else:
            color = PARTY_COLORS['DEFAULT']

        return {
            'fillColor': color,
            'fillOpacity': 0.65,
            'color': '#2E86AB',
            'weight': 1.8,
            'opacity': 1
        }

    # Función de estilo hover
    def highlight_function(feature):
        seccional = feature['properties']['Seccional']
        seccional_data = gdf_year[gdf_year['Seccional'] == seccional]

        if len(seccional_data) > 0:
            color = seccional_data['color'].iloc[0]
            rgb = mcolors.hex2color(color)
            darker_rgb = tuple(max(0, c * 0.7) for c in rgb)
            darker_color = mcolors.rgb2hex(darker_rgb)
        else:
            darker_color = '#999999'

        return {
            'fillColor': darker_color,
            'fillOpacity': 0.85,
            'color': '#1a5276',
            'weight': 3,
            'opacity': 1
        }

    # Preparar datos para GeoJSON
    gdf_for_geojson = gdf_year[['Seccional', 'agrupacion', 'votos', 'porcentaje', 'geometry']].copy()
    gdf_for_geojson['agrupacion'] = gdf_for_geojson['agrupacion'].fillna('Sin datos')
    gdf_for_geojson['votos'] = gdf_for_geojson['votos'].fillna(0).astype(int)
    gdf_for_geojson['porcentaje'] = gdf_for_geojson['porcentaje'].fillna(0)

    # Agregar GeoJSON con hover
    geojson = GeoJson(
        data=gdf_for_geojson,
        style_function=style_function,
        highlight_function=highlight_function,
        tooltip=folium.GeoJsonTooltip(
            fields=['Seccional', 'agrupacion', 'votos', 'porcentaje'],
            aliases=['Sec:', 'Ganador:', 'Votos:', '%:'],
            style="""
                background-color: white;
                color: #333333;
                font-family: Arial, sans-serif;
                font-size: 11px;
                font-weight: normal;
                padding: 6px 8px;
                border: 1.5px solid #2E86AB;
                border-radius: 4px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.2);
                max-width: 180px;
                line-height: 1.3;
            """,
            sticky=False
        )
    )
    geojson.add_to(m)

    # Agregar etiquetas
    for idx, row in gdf_year.iterrows():
        folium.Marker(
            location=[row['lat'], row['lon']],
            icon=folium.DivIcon(html=f"""
                <div style="
                    font-size: 11px;
                    font-weight: bold;
                    color: #1a1a1a;
                    text-shadow: -1px -1px 0 #fff, 1px -1px 0 #fff, -1px 1px 0 #fff, 1px 1px 0 #fff;
                    text-align: center;
                ">Sec. {row['Seccional']}</div>
            """)
        ).add_to(m)

    return m

# ============================================================================
# INICIALIZAR APP
# ============================================================================

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

app.title = "Dashboard Electoral Córdoba"

# ============================================================================
# LAYOUT
# ============================================================================

app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1("Dashboard Electoral Córdoba Capital", className="text-center mt-4 mb-2"),
            html.H2("Evolución 2021 - 2023 - 2025 (Actualizado)", className="text-center text-muted mb-4")
        ])
    ]),

    # Métricas principales
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Total Votos", className="card-subtitle text-muted mb-1", style={'fontSize': '12px'}),
                    html.H5(id="metric-total-votos", className="card-title mb-0", style={'fontSize': '20px'})
                ])
            ], className="mb-3")
        ], xs=12, sm=6, md=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Partido Ganador", className="card-subtitle text-muted mb-1", style={'fontSize': '12px'}),
                    html.H5(id="metric-ganador", className="card-title mb-0", style={'fontSize': '13px', 'lineHeight': '1.2'})
                ])
            ], className="mb-3")
        ], xs=12, sm=6, md=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Seccionales Ganadas", className="card-subtitle text-muted mb-1", style={'fontSize': '12px'}),
                    html.Div(id="metric-seccionales", style={'fontSize': '11px', 'lineHeight': '1.4'})
                ])
            ], className="mb-3")
        ], xs=12, sm=6, md=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6("Año Seleccionado", className="card-subtitle text-muted mb-1", style={'fontSize': '12px'}),
                    html.H5(id="metric-year", className="card-title mb-0", style={'fontSize': '20px'})
                ])
            ], className="mb-2")
        ], xs=12, sm=6, md=3)
    ], className="metrics-row"),

    # Mapa principal
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.H3("Mapa Electoral por Seccional"),
                    className="card-header-custom"
                ),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.Label("Año:", className="fw-bold mb-1"),
                            dcc.Slider(
                                id="year-slider",
                                min=2021,
                                max=2025,
                                value=2021,
                                marks={
                                    2021: {'label': '2021', 'style': {'fontSize': '16px'}},
                                    2023: {'label': '2023', 'style': {'fontSize': '16px'}},
                                    2025: {'label': '2025', 'style': {'fontSize': '16px'}}
                                },
                                step=None,
                                included=False
                            )
                        ], md=8),
                        dbc.Col([
                            html.Label("Filtrar por:", className="fw-bold mb-1"),
                            dcc.Dropdown(
                                id="seccional-dropdown",
                                options=[{'label': 'Todas', 'value': 'all'}] +
                                        [{'label': f'Seccional {i}', 'value': str(i)} for i in range(1, 15)],
                                value='all',
                                clearable=False,
                                style={'fontSize': '14px'}
                            )
                        ], md=4)
                    ], className="mb-3"),
                    html.Iframe(
                        id="electoral-map",
                        srcDoc='',
                        style={"height": "60vh", "width": "100%", "border": "none"},
                        className="responsive-map"
                    )
                ])
            ])
        ], xs=12, md=8, lg=8),

        # Panel lateral con gráficos
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4(id="pie-chart-title"), className="card-header-custom"),
                dbc.CardBody([
                    dcc.Graph(
                        id="pie-chart",
                        style={"height": "28vh"},
                        config={'responsive': True}
                    )
                ])
            ], className="mb-3"),
            dbc.Card([
                dbc.CardHeader(html.H4(id="bar-chart-title"), className="card-header-custom"),
                dbc.CardBody([
                    dcc.Graph(
                        id="bar-chart",
                        style={"height": "28vh"},
                        config={'responsive': True}
                    )
                ])
            ])
        ], xs=12, md=4, lg=4)
    ], className="mb-3 map-section"),

    # Tabla comparativa
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H3("Comparativa por Seccional"), className="card-header-custom"),
                dbc.CardBody([
                    html.Div(id="comparison-table")
                ])
            ])
        ])
    ], className="mb-2"),

    # Footer
    dbc.Row([
        dbc.Col([
            html.Hr(),
            html.P([
                "Dashboard Electoral Córdoba Capital | ",
                "Datos: 2021, 2023, 2025 | ",
                html.A("Ver código", href="#", target="_blank")
            ], className="text-center text-muted small")
        ])
    ])

], fluid=True)

# ============================================================================
# CALLBACKS
# ============================================================================

@callback(
    [Output("electoral-map", "srcDoc"),
     Output("metric-total-votos", "children"),
     Output("metric-ganador", "children"),
     Output("metric-seccionales", "children"),
     Output("metric-year", "children"),
     Output("pie-chart", "figure"),
     Output("bar-chart", "figure"),
     Output("pie-chart-title", "children"),
     Output("bar-chart-title", "children")],
    [Input("year-slider", "value"),
     Input("seccional-dropdown", "value")]
)
def update_map_and_metrics(selected_year, selected_seccional):
    """Actualiza mapa y métricas según año y seccional seleccionados"""

    # Filtrar datos del año
    gan_year = ganadores[ganadores['anio'] == selected_year].copy()
    df_year = df_electoral[df_electoral['anio'] == selected_year].copy()

    # Generar mapa Folium
    folium_map = create_folium_map(selected_year)
    map_html = folium_map.get_root().render()
    
    # Inyectar CSS personalizado directamente en el iframe del mapa
    # Esto soluciona los problemas de estilo en móviles que no se arreglan desde el padre
    custom_map_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
        
        body {
            font-family: 'Inter', sans-serif !important;
        }
        
        .leaflet-tooltip {
            background-color: rgba(255, 255, 255, 0.95) !important;
            border: 1px solid #e0e0e0 !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
            border-radius: 8px !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 12px !important;
            font-weight: normal !important;
            color: #333 !important;
            padding: 8px 12px !important;
        }
        
        /* Estilos específicos para móviles */
        @media (max-width: 600px) {
            .leaflet-tooltip {
                font-size: 10px !important;
                padding: 6px 10px !important;
                max-width: 140px !important;
                white-space: normal !important;
                line-height: 1.2 !important;
                border-width: 1px !important;
                margin-top: -20px !important; /* Ajustar posición si es necesario */
            }
            
            /* Reducir tamaño de las etiquetas de marcadores en móvil */
            .leaflet-div-icon div {
                font-size: 9px !important;
            }
        }
    </style>
    """
    
    # Insertar estilos en el head del HTML generado
    if '</head>' in map_html:
        map_html = map_html.replace('</head>', f'{custom_map_css}</head>')
    else:
        # Fallback si no encuentra head (raro en output de folium)
        map_html = f"{custom_map_css}{map_html}"

    # Filtrar por seccional si no es "all"
    if selected_seccional and selected_seccional != 'all':
        df_year_filtered = df_year[df_year['seccional'] == selected_seccional].copy()
        pie_title = f"Distribución de Votos - Seccional {selected_seccional}"
        bar_title = f"Top 5 Partidos - Seccional {selected_seccional}"
    else:
        df_year_filtered = df_year.copy()
        pie_title = "Distribución de Votos - Todas las Seccionales"
        bar_title = "Top 5 Partidos - Todas las Seccionales"

    # Métricas
    total_votos = df_year['votos'].sum()
    ganador_global = df_year.groupby('agrupacion')['votos'].sum().idxmax()

    # Desglose de seccionales ganadas por partido
    seccionales_por_partido = gan_year['agrupacion'].value_counts().sort_values(ascending=False)
    seccionales_breakdown = []
    for partido, count in seccionales_por_partido.items():
        seccionales_breakdown.append(
            html.Div([
                html.Strong(f"{count}", style={'fontSize': '14px', 'color': PARTY_COLORS.get(partido, '#666')}),
                html.Span(f" {partido}", style={'fontSize': '10px'})
            ], style={'marginBottom': '2px'})
        )

    # Pie chart (usando datos filtrados)
    top_parties = df_year_filtered.groupby('agrupacion')['votos'].sum().nlargest(5).reset_index()
    fig_pie = px.pie(
        top_parties,
        values='votos',
        names='agrupacion',
        color='agrupacion',
        color_discrete_map=PARTY_COLORS,
        hole=0.6  # Donut chart más elegante
    )
    fig_pie.update_traces(
        textposition='inside', 
        textinfo='percent',
        hovertemplate='<b>%{label}</b><br>Votos: %{value}<br>Porcentaje: %{percent}'
    )
    fig_pie.update_layout(
        margin=dict(l=20, r=20, t=0, b=20),
        showlegend=False,
        font=dict(family="Inter, sans-serif", size=11),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        annotations=[dict(text=f"Total<br>{df_year_filtered['votos'].sum():,.0f}", x=0.5, y=0.5, font_size=12, showarrow=False)]
    )

    # Bar chart (usando datos filtrados)
    fig_bar = px.bar(
        top_parties,
        x='votos',
        y='agrupacion',
        orientation='h',
        color='agrupacion',
        color_discrete_map=PARTY_COLORS,
        text='votos'
    )
    fig_bar.update_traces(
        texttemplate='%{text:.2s}', 
        textposition='outside',
        marker_line_width=0,
        opacity=0.9
    )
    fig_bar.update_layout(
        margin=dict(l=0, r=20, t=0, b=0),
        showlegend=False,
        yaxis_title=None,
        xaxis_title=None,
        xaxis=dict(showgrid=False, showticklabels=False), # Limpiar eje X
        yaxis=dict(showgrid=False, tickfont=dict(size=10)),
        font=dict(family="Inter, sans-serif", size=11),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        uniformtext_minsize=8, 
        uniformtext_mode='hide'
    )
    
    # Ordenar barras
    fig_bar.update_yaxes(categoryorder='total ascending')

    return (
        map_html,
        f"{total_votos:,}",
        ganador_global,
        seccionales_breakdown,
        str(selected_year),
        fig_pie,
        fig_bar,
        pie_title,
        bar_title
    )

@callback(
    Output("comparison-table", "children"),
    [Input("year-slider", "value")]
)
def update_comparison_table(selected_year):
    """Tabla comparativa de resultados"""

    # Obtener resultados de todos los años
    gan_all = ganadores.pivot(index='seccional', columns='anio', values='agrupacion').reset_index()
    gan_all.columns = ['Seccional'] + [str(int(col)) if col != 'seccional' else col for col in gan_all.columns[1:]]
    gan_all = gan_all.sort_values('Seccional')

    # Crear tabla Bootstrap
    table_header = [
        html.Thead(html.Tr([
            html.Th("Seccional"),
            html.Th("2021"),
            html.Th("2023"),
            html.Th("2025")
        ]))
    ]

    rows = []
    for _, row in gan_all.iterrows():
        rows.append(html.Tr([
            html.Td(f"Seccional {row['Seccional']}", style={'fontWeight': 'bold'}),
            html.Td(row.get('2021', 'N/D'), style={'fontSize': '11px'}),
            html.Td(row.get('2023', 'N/D'), style={'fontSize': '11px'}),
            html.Td(row.get('2025', 'N/D'), style={'fontSize': '11px'})
        ]))

    table_body = [html.Tbody(rows)]

    return dbc.Table(
        table_header + table_body,
        bordered=True,
        hover=True,
        responsive=True,
        striped=True,
        size='sm'
    )

# ============================================================================
# RUN SERVER
# ============================================================================

# Exponer server para gunicorn
server = app.server

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8050))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print("\n" + "="*70)
    print("DASHBOARD ELECTORAL - SERVIDOR INICIADO")
    print("="*70)
    print(f"\nAbre tu navegador en: http://0.0.0.0:{port}/")
    print("\nPresiona Ctrl+C para detener el servidor")
    print("="*70 + "\n")

    app.run(debug=debug, host='0.0.0.0', port=port)
