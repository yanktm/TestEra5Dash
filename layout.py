from dash import dcc, html

layout = html.Div([
    # Grand titre pour toute la page
    html.H1("Comparaison Graphique et Métriques de Modèles", style={'textAlign': 'center', 'padding': '20px'}),

    # Section pour la comparaison des graphes
    html.Div([
        html.H2("Comparaison Graphique", style={'textAlign': 'center', 'padding': '10px'}),

        # Division pour les graphiques côte à côte
        html.Div([
            # Division pour Graph1 à gauche
            html.Div([
                html.Img(id='graph1-plot', style={'width': '100%', 'height': 'auto'}),
                html.Div("Graphique 1", style={'textAlign': 'center', 'fontWeight': 'bold', 'margin-top': '20px'}),
                html.Div([
                    dcc.Dropdown(id='file-dropdown1', options=[], placeholder='Select a file'),
                    html.Button('SELECT DATASET', id='button1-12', n_clicks=0, style={'margin': '5px'}),
                ]),
                html.Div([
                    dcc.Dropdown(id='variable-dropdown1', options=[], placeholder='Select a variable'),
                    html.Button('SELECT VARIABLE', id='button1-2', n_clicks=0, style={'margin': '5px'}),
                ]),
                html.Div([
                    dcc.Input(id='latitude-input1', type='number', placeholder='Latitude'),
                    html.Button('LATITUDE', id='button1-lat', n_clicks=0, style={'margin': '5px'})
                ], style={'textAlign': 'center'}),
                html.Div([
                    dcc.Input(id='longitude-input1', type='number', placeholder='Longitude'),
                    html.Button('LONGITUDE', id='button1-lon', n_clicks=0, style={'margin': '5px'})
                ], style={'textAlign': 'center'}),
                html.Div([
                    dcc.Input(id='level-input1', type='number', placeholder='Level'),
                    html.Button('LEVEL', id='button1-level', n_clicks=0, style={'margin': '5px'})
                ], style={'textAlign': 'center'}),
                html.Div([
                    dcc.Input(id='timestep-input1', type='number', min=0, placeholder='Timestep'),
                    html.Button('TIME STEP', id='button1-3', n_clicks=0, style={'margin': '5px'}),
                    html.Span(id='max-timestep1', style={'margin-left': '10px'})
                ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
                html.Button('Generate', id='generate-button1', n_clicks=0, style={'margin': '5px'})
            ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px', 'verticalAlign': 'top'}),

            # Division pour Graph2 à droite
            html.Div([
                html.Img(id='graph2-plot', style={'width': '100%', 'height': 'auto'}),
                html.Div("Graphique 2", style={'textAlign': 'center', 'fontWeight': 'bold', 'margin-top': '20px'}),
                html.Div([
                    dcc.Dropdown(id='file-dropdown2', options=[], placeholder='Select a file'),
                    html.Button('SELECT DATASET', id='button2-12', n_clicks=0, style={'margin': '5px'}),
                ]),
                html.Div([
                    dcc.Dropdown(id='variable-dropdown2', options=[], placeholder='Select a variable'),
                    html.Button('SELECT VARIABLE', id='button2-2', n_clicks=0, style={'margin': '5px'}),
                ]),
                html.Div([
                    dcc.Input(id='latitude-input2', type='number', placeholder='Latitude'),
                    html.Button('LATITUDE', id='button2-lat', n_clicks=0, style={'margin': '5px'})
                ], style={'textAlign': 'center'}),
                html.Div([
                    dcc.Input(id='longitude-input2', type='number', placeholder='Longitude'),
                    html.Button('LONGITUDE', id='button2-lon', n_clicks=0, style={'margin': '5px'})
                ], style={'textAlign': 'center'}),
                html.Div([
                    dcc.Input(id='level-input2', type='number', placeholder='Level'),
                    html.Button('LEVEL', id='button2-level', n_clicks=0, style={'margin': '5px'})
                ], style={'textAlign': 'center'}),
                html.Div([
                    dcc.Input(id='timestep-input2', type='number', min=0, placeholder='Timestep'),
                    html.Button('TIME STEP', id='button2-3', n_clicks=0, style={'margin': '5px'}),
                    html.Span(id='max-timestep2', style={'margin-left': '10px'})
                ], style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
                html.Button('Generate', id='generate-button2', n_clicks=0, style={'margin': '5px'})
            ], style={'width': '50%', 'display': 'inline-block', 'padding': '10px', 'verticalAlign': 'top'})
        ], style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'flex-start'})
    ], style={'width': '100%', 'padding': '20px'}),

    # Section pour la comparaison des modèles
    html.Div([
        html.H2("Métrique de Comparaison des Modèles", style={'textAlign': 'center', 'padding': '10px'}),

        # Division pour les sélections de datasets et variables côte à côte
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id=f'dataset{i}-dropdown', options=[], placeholder=f'Select Dataset {i}'),
                    html.Button('SELECT DATASET', id=f'button-dataset{i}', n_clicks=0, style={'margin': '5px'}),
                ]),
                html.Div([
                    dcc.Dropdown(id=f'dataset{i}-variable-dropdown', options=[], placeholder='Select Variable'),
                    html.Button('SELECT VARIABLE', id=f'button-variable{i}', n_clicks=0, style={'margin': '5px'}),
                ]),
            ], style={'width': '45%', 'display': 'inline-block', 'padding': '10px'}) for i in range(1, 6)
        ], style={'display': 'flex', 'justifyContent': 'space-around'}),

        # Bouton pour générer la comparaison
        html.Div([
            html.Button('Generate Comparison', id='generate-button3', n_clicks=0, style={'margin': '5px'})
        ], style={'textAlign': 'center', 'padding': '10px'}),

        # Placeholder for comparison plot
        html.Div([
            html.Img(id='comparison-plot', style={'width': '100%', 'height': 'auto'})
        ], style={'textAlign': 'center', 'padding': '10px'})
    ], style={'width': '100%', 'padding': '20px'}),
])
