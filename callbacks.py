from dash.dependencies import Input, Output, State
import dash_dangerously_set_inner_html as ddsih
import xarray as xr
import os
import dash
import requests

# Chemin du fichier NetCDF (à adapter selon votre arborescence)
file_path = 'data/title.nc'

# Vérifiez si le fichier existe
if not os.path.exists(file_path):
    raise FileNotFoundError(f"Le fichier spécifié n'existe pas : {file_path}")

# Charger les données ERA5
data = xr.open_dataset(file_path)

# Simulate getting max timestep from dataset (this should be replaced with actual logic)
def get_max_timestep(file, variable):
    return 10  # Replace with actual logic to determine max timestep

def get_github_repo_contents(owner, repo, path='', token=None):
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
    headers = {'Authorization': f'token {token}'} if token else {}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        contents = response.json()
        files = [{'label': content['name'], 'value': content['name']} for content in contents if not content['name'].startswith('.')]
        return files
    else:
        return [{"label": "Unable to fetch directory contents.", "value": "error"}]

def register_callbacks(app):
    @app.callback(
        Output('graph1-plot', 'figure'),
        [Input('generate-button1', 'n_clicks')]
    )
    def update_graph1(n_clicks):
        if n_clicks > 0:
            return {"data": [], "layout": {"title": "Graphique 1"}}
        return dash.no_update

    @app.callback(
        Output('graph2-plot', 'figure'),
        [Input('generate-button2', 'n_clicks')]
    )
    def update_graph2(n_clicks):
        if n_clicks > 0:
            return {"data": [], "layout": {"title": "Graphique 2"}}
        return dash.no_update

    @app.callback(
        Output('lower-right-plot', 'figure'),
        [Input('generate-button3', 'n_clicks')]
    )
    def update_lower_right_plot(n_clicks):
        if n_clicks > 0:
            return {"data": [], "layout": {"title": "Comparaison"}}
        return dash.no_update

    @app.callback(
        Output('file-dropdown1', 'options'),
        [Input('button1-11', 'n_clicks')]
    )
    def update_file_dropdown1(n_clicks):
        if n_clicks > 0:
            owner = 'yanktm'
            repo = 'testEra5dash'
            path = ''
            files = get_github_repo_contents(owner, repo, path)
            return files
        return []

    @app.callback(
        Output('file-dropdown2', 'options'),
        [Input('button2-11', 'n_clicks')]
    )
    def update_file_dropdown2(n_clicks):
        if n_clicks > 0:
            owner = 'yanktm'
            repo = 'testEra5dash'
            path = ''
            files = get_github_repo_contents(owner, repo, path)
            return files
        return []

    @app.callback(
        [Output('max-timestep1', 'children'),
         Output('max-timestep2', 'children')],
        [Input('file-dropdown1', 'value'),
         Input('file-dropdown2', 'value'),
         Input('variable-dropdown1', 'value'),
         Input('variable-dropdown2', 'value')]
    )
    def update_max_timestep(file1, file2, var1, var2):
        max_timestep1 = get_max_timestep(file1, var1) if file1 and var1 else "N/A"
        max_timestep2 = get_max_timestep(file2, var2) if file2 and var2 else "N/A"
        return f"(max timestep = {max_timestep1})", f"(max timestep = {max_timestep2})"

    @app.callback(
        Output('file-viewer', 'children'),
        [Input('file-dropdown1', 'value'),
         Input('file-dropdown2', 'value')]
    )
    def display_github_file(selected_file1, selected_file2):
        if selected_file1:
            return ddsih.DangerouslySetInnerHTML(f'<p>Selected file from dropdown 1: {selected_file1}</p>')
        elif selected_file2:
            return ddsih.DangerouslySetInnerHTML(f'<p>Selected file from dropdown 2: {selected_file2}</p>')
        return ddsih.DangerouslySetInnerHTML('<p>No file selected.</p>')
