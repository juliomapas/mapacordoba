"""
Dashboard Electoral Córdoba Capital 2021-2025
Versión Mejorada - Responsive y con mejor UX

MEJORAS IMPLEMENTADAS:
- Fase 1: Responsividad completa
- Fase 2: Usabilidad mejorada (loading, tooltips, feedback)

Ejecutar:
    python app_improved.py

Luego abrir: http://127.0.0.1:8050/
"""
import dash
from dash import dcc, html, Input, Output, callback, State
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
try:
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

    print(f"OK Datos cargados: {len(dissolved)} seccionales, {len(df_electoral)} registros")
    DATA_LOADED = True
except Exception as e:
    print(f"ERROR cargando datos: {e}")
    DATA_LOADED = False

# Función para crear mapa Folium
def create_folium_map(selected_year):
    """Crea mapa Folium con colores según partido ganador"""

    if not DATA_LOADED:
        return folium.Map(location=[-31.4201, -64.1888], zoom_start=12)

    gan_year = ganadores[ganadores['anio'] == selected_year].copy()
    gdf_year = dissolved.merge(gan_year, left_on='Seccional', right_on='seccional', how='left')
    gdf_year['color'] = gdf_year['agrupacion'].apply(
        lambda x: PARTY_COLORS.get(x, PARTY_COLORS['DEFAULT']) if pd.notna(x) else PARTY_COLORS['DEFAULT']
    )

    m = folium.Map(
        location=[-31.4201, -64.1888],
        zoom_start=12,
        tiles='CartoDB positron',
        min_zoom=11,
        max_zoom=15
    )

    def style_function(feature):
        seccional = feature['properties']['Seccional']
        seccional_data = gdf_year[gdf_year['Seccional'] == seccional]
        color = seccional_data['color'].iloc[0] if len(seccional_data) > 0 else PARTY_COLORS['DEFAULT']
        return {'fillColor': color, 'fillOpacity': 0.65, 'color': '#2E86AB', 'weight': 1.8, 'opacity': 1}

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
        return {'fillColor': darker_color, 'fillOpacity': 0.85, 'color': '#1a5276', 'weight': 3, 'opacity': 1}

    gdf_for_geojson = gdf_year[['Seccional', 'agrupacion', 'votos', 'porcentaje', 'geometry']].copy()
    gdf_for_geojson['agrupacion'] = gdf_for_geojson['agrupacion'].fillna('Sin datos')
    gdf_for_geojson['votos'] = gdf_for_geojson['votos'].fillna(0).astype(int)
    gdf_for_geojson['porcentaje'] = gdf_for_geojson['porcentaje'].fillna(0)

    geojson = GeoJson(
        data=gdf_for_geojson,
        style_function=style_function,
        highlight_function=highlight_function,
        tooltip=folium.GeoJsonTooltip(
            fields=['Seccional', 'agrupacion', 'votos', 'porcentaje'],
            aliases=['Seccional:', 'Ganador:', 'Votos:', 'Porcentaje:'],
            style="background-color:white;color:#333;font-family:Arial;font-size:14px;font-weight:bold;padding:10px;border:2px solid #2E86AB;border-radius:4px;box-shadow:0 2px 4px rgba(0,0,0,0.2);",
            sticky=False
        )
    )
    geojson.add_to(m)

    for idx, row in gdf_year.iterrows():
        folium.Marker(
            location=[row['lat'], row['lon']],
            icon=folium.DivIcon(html=f'<div style="font-size:11px;font-weight:bold;color:#1a1a1a;text-shadow:-1px -1px 0 #fff,1px -1px 0 #fff,-1px 1px 0 #fff,1px 1px 0 #fff;text-align:center;">Sec. {row["Seccional"]}</div>')
        ).add_to(m)

    return m

# ============================================================================
# INICIALIZAR APP
# ============================================================================

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0, maximum-scale=1.0"}
    ]
)

app.title = "Dashboard Electoral Córdoba"

# Expose server for deployment
server = app.server

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def create_info_tooltip(text):
    """Crea un tooltip de información"""
    return html.Span(
        "ⓘ",
        className="info-icon",
        title=text,
        **{"data-toggle": "tooltip", "data-placement": "top"}
    )

# ============================================================================
# LAYOUT
# ============================================================================

app.layout = dbc.Container([
    # Loading overlay
    html.Div(id="loading-overlay", style={"display": "none"}),

    # Header con gradiente
    dbc.Row([
        dbc.Col([
            html.H1("Dashboard Electoral Córdoba Capital",
                   className="text-center mt-4 mb-2 text-gradient"),
            html.H2("Evolución 2021 - 2023 - 2025",
                   className="text-center text-muted mb-4"),
            html.P("Explora los resultados electorales por seccional y año",
                  className="text-center text-muted small")
        ])
    ]),

    # Métricas principales - MEJORADAS
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.H6("Total Votos", className="card-subtitle text-muted mb-1",
                               style={'fontSize': '12px'}),
                        create_info_tooltip("Suma total de votos del año seleccionado")
                    ]),
                    html.H5(id="metric-total-votos", className="card-title mb-0 metric-value",
                           style={'fontSize': '20px'})
                ])
            ], className="mb-3 metric-card")
        ], xs=12, sm=6, md=6, lg=3),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.H6("Partido Ganador", className="card-subtitle text-muted mb-1",
                               style={'fontSize': '12px'}),
                        create_info_tooltip("Partido con más votos a nivel general")
                    ]),
                    html.H5(id="metric-ganador", className="card-title mb-0",
                           style={'fontSize': '13px', 'lineHeight': '1.2'})
                ])
            ], className="mb-3 metric-card")
        ], xs=12, sm=6, md=6, lg=3),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.H6("Seccionales Ganadas", className="card-subtitle text-muted mb-1",
                               style={'fontSize': '12px'}),
                        create_info_tooltip("Distribución de seccionales ganadas por partido")
                    ]),
                    html.Div(id="metric-seccionales", style={'fontSize': '11px', 'lineHeight': '1.4'})
                ])
            ], className="mb-3 metric-card")
        ], xs=12, sm=6, md=6, lg=3),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.H6("Año Seleccionado", className="card-subtitle text-muted mb-1",
                               style={'fontSize': '12px'}),
                        create_info_tooltip("Año actualmente visualizado")
                    ]),
                    html.H5(id="metric-year", className="card-title mb-0 metric-value",
                           style={'fontSize': '20px'})
                ])
            ], className="mb-3 metric-card")
        ], xs=12, sm=6, md=6, lg=3)
    ]),

    # Sección principal - Mapa y gráficos
    dbc.Row([
        # Columna del mapa
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H3("Mapa Electoral por Seccional", className="mb-0")),
                dbc.CardBody([
                    # Controles en una sección destacada
                    html.Div([
                        dbc.Row([
                            dbc.Col([
                                html.Label([
                                    "Año:",
                                    create_info_tooltip("Selecciona el año electoral a visualizar")
                                ], className="fw-bold mb-2"),
                                dcc.Slider(
                                    id="year-slider",
                                    min=2021,
                                    max=2025,
                                    value=2023,
                                    marks={
                                        2021: {'label': '2021', 'style': {'fontSize': '14px'}},
                                        2023: {'label': '2023', 'style': {'fontSize': '14px'}},
                                        2025: {'label': '2025', 'style': {'fontSize': '14px'}}
                                    },
                                    step=None,
                                    included=False
                                )
                            ], xs=12, md=7),
                            dbc.Col([
                                html.Label([
                                    "Filtrar por:",
                                    create_info_tooltip("Filtra los gráficos por una seccional específica")
                                ], className="fw-bold mb-2"),
                                dcc.Dropdown(
                                    id="seccional-dropdown",
                                    options=[{'label': 'Todas las Seccionales', 'value': 'all'}] +
                                            [{'label': f'Seccional {i}', 'value': str(i)} for i in range(1, 15)],
                                    value='all',
                                    clearable=False,
                                    style={'fontSize': '14px'}
                                )
                            ], xs=12, md=5)
                        ])
                    ], className="control-section"),

                    # Mapa con altura responsiva
                    html.Div([
                        dcc.Loading(
                            id="loading-map",
                            type="circle",
                            color="#2E86AB",
                            children=[
                                html.Iframe(
                                    id="electoral-map",
                                    srcDoc='',
                                    style={
                                        "height": "60vh",
                                        "width": "100%",
                                        "border": "none",
                                        "minHeight": "400px"
                                    }
                                )
                            ]
                        )
                    ], className="map-container")
                ])
            ], className="mb-3")
        ], xs=12, lg=8),

        # Columna de gráficos - MEJORADA
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4(id="pie-chart-title", className="mb-0")),
                dbc.CardBody([
                    dcc.Loading(
                        id="loading-pie",
                        type="circle",
                        color="#2E86AB",
                        children=[
                            dcc.Graph(
                                id="pie-chart",
                                style={"height": "30vh", "minHeight": "250px"},
                                config={'responsive': True, 'displayModeBar': False}
                            )
                        ]
                    )
                ], className="chart-container")
            ], className="mb-3"),

            dbc.Card([
                dbc.CardHeader(html.H4(id="bar-chart-title", className="mb-0")),
                dbc.CardBody([
                    dcc.Loading(
                        id="loading-bar",
                        type="circle",
                        color="#2E86AB",
                        children=[
                            dcc.Graph(
                                id="bar-chart",
                                style={"height": "30vh", "minHeight": "250px"},
                                config={'responsive': True, 'displayModeBar': False}
                            )
                        ]
                    )
                ], className="chart-container")
            ])
        ], xs=12, lg=4)
    ], className="mb-4"),

    # Tabla comparativa - COLAPSABLE
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.Div([
                        html.H3("Comparativa por Seccional", className="d-inline mb-0"),
                        html.Button(
                            [
                                "Ver tabla ",
                                html.Span("▼", id="collapse-icon", className="collapse-icon")
                            ],
                            id="collapse-button",
                            className="btn btn-link float-end",
                            style={"color": "white", "textDecoration": "none"}
                        )
                    ], className="d-flex justify-content-between align-items-center")
                ]),
                dbc.Collapse(
                    dbc.CardBody([
                        html.P("Ganadores por seccional en cada año electoral",
                              className="text-muted small mb-3"),
                        html.Div([
                            dcc.Loading(
                                id="loading-table",
                                type="circle",
                                color="#2E86AB",
                                children=[html.Div(id="comparison-table")]
                            )
                        ], className="table-responsive")
                    ]),
                    id="table-collapse",
                    is_open=False
                )
            ])
        ])
    ], className="mb-4"),

    # Footer mejorado
    html.Footer([
        dbc.Row([
            dbc.Col([
                html.Hr(),
                html.P([
                    html.Strong("Dashboard Electoral Córdoba Capital"),
                    " | Datos: 2021, 2023, 2025 | ",
                    html.A("GitHub", href="https://github.com", target="_blank", className="text-decoration-none")
                ], className="text-center text-muted small mb-2"),
                html.P("Desarrollado con Dash y Plotly",
                      className="text-center text-muted small")
            ])
        ])
    ])

], fluid=True, className="px-3 px-md-4")

# ============================================================================
# CALLBACKS
# ============================================================================

# Callback para colapsar/expandir tabla
@callback(
    [Output("table-collapse", "is_open"),
     Output("collapse-icon", "children")],
    [Input("collapse-button", "n_clicks")],
    [State("table-collapse", "is_open")]
)
def toggle_collapse(n_clicks, is_open):
    if n_clicks:
        return not is_open, "▲" if not is_open else "▼"
    return is_open, "▼"

# Callback principal
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
def update_dashboard(selected_year, selected_seccional):
    """Actualiza todo el dashboard"""

    if not DATA_LOADED:
        empty_fig = go.Figure()
        empty_fig.add_annotation(text="Error cargando datos", showarrow=False)
        return ("", "Error", "Error", [], "Error", empty_fig, empty_fig, "Error", "Error")

    # Filtrar datos
    gan_year = ganadores[ganadores['anio'] == selected_year].copy()
    df_year = df_electoral[df_electoral['anio'] == selected_year].copy()

    # Generar mapa
    folium_map = create_folium_map(selected_year)
    map_html = folium_map._repr_html_()

    # Filtrar por seccional
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

    # Desglose seccionales
    seccionales_por_partido = gan_year['agrupacion'].value_counts().sort_values(ascending=False)
    seccionales_breakdown = []
    for partido, count in seccionales_por_partido.items():
        seccionales_breakdown.append(
            html.Div([
                html.Strong(f"{count}", style={'fontSize': '14px', 'color': PARTY_COLORS.get(partido, '#666')}),
                html.Span(f" {partido}", style={'fontSize': '10px'})
            ], style={'marginBottom': '2px'})
        )

    # Gráficos
    top_parties = df_year_filtered.groupby('agrupacion')['votos'].sum().nlargest(5).reset_index()

    fig_pie = px.pie(top_parties, values='votos', names='agrupacion', color='agrupacion',
                     color_discrete_map=PARTY_COLORS, hole=0.4)
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    fig_pie.update_layout(margin=dict(l=0, r=0, t=0, b=0), showlegend=False, font=dict(size=10))

    fig_bar = px.bar(top_parties, x='votos', y='agrupacion', orientation='h',
                     color='agrupacion', color_discrete_map=PARTY_COLORS)
    fig_bar.update_layout(margin=dict(l=0, r=0, t=0, b=0), showlegend=False,
                         yaxis_title=None, xaxis_title="Votos", font=dict(size=10))
    fig_bar.update_yaxes(categoryorder='total ascending')

    return (map_html, f"{total_votos:,}", ganador_global, seccionales_breakdown,
            str(selected_year), fig_pie, fig_bar, pie_title, bar_title)

# Callback tabla
@callback(
    Output("comparison-table", "children"),
    [Input("year-slider", "value")]
)
def update_table(selected_year):
    """Tabla comparativa"""

    if not DATA_LOADED:
        return html.P("Error cargando datos", className="text-danger")

    gan_all = ganadores.pivot(index='seccional', columns='anio', values='agrupacion').reset_index()
    gan_all.columns = ['Seccional'] + [str(int(col)) if col != 'seccional' else col for col in gan_all.columns[1:]]
    gan_all = gan_all.sort_values('Seccional')

    table_header = [html.Thead(html.Tr([
        html.Th("Seccional"), html.Th("2021"), html.Th("2023"), html.Th("2025")
    ]))]

    rows = []
    for _, row in gan_all.iterrows():
        rows.append(html.Tr([
            html.Td(f"Seccional {row['Seccional']}", style={'fontWeight': 'bold'}),
            html.Td(row.get('2021', 'N/D'), style={'fontSize': '11px'}),
            html.Td(row.get('2023', 'N/D'), style={'fontSize': '11px'}),
            html.Td(row.get('2025', 'N/D'), style={'fontSize': '11px'})
        ]))

    return dbc.Table(table_header + [html.Tbody(rows)], bordered=True, hover=True,
                    responsive=True, striped=True, size='sm', className="comparison-table")

# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*70)
    print("DASHBOARD ELECTORAL - VERSIÓN MEJORADA")
    print("="*70)
    print("\nMEJORAS IMPLEMENTADAS:")
    print("  - Fase 1: Responsividad completa")
    print("  - Fase 2: Usabilidad mejorada")
    print("\nCaracteristicas:")
    print("  - Loading indicators")
    print("  - Tooltips informativos")
    print("  - Tabla colapsable")
    print("  - Diseno responsive")
    print("  - Visual feedback")
    print("\nAbre tu navegador en: http://127.0.0.1:8050/")
    print("Presiona Ctrl+C para detener el servidor")
    print("="*70 + "\n")

    app.run(debug=True, host='127.0.0.1', port=8050)
