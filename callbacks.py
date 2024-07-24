from dash.dependencies import Input, Output, State
import dash_dangerously_set_inner_html as ddsih
import xarray as xr
import os
import dash
import matplotlib
matplotlib.use('Agg')  # Utilisation du backend 'Agg' pour Matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from io import BytesIO
import base64
import numpy as np
import requests

def get_max_timestep(file, variable):
    dataset_path = f'data/{file}'
    ds = xr.open_zarr(dataset_path)
    return ds.sizes['time'] - 1

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

def get_local_files(path):
    files = []
    for file_name in os.listdir(path):
        if not file_name.startswith('.'):
            files.append({'label': file_name, 'value': file_name})
    return files

def get_dataset_variables(file):
    dataset_path = f'data/{file}'
    ds = xr.open_zarr(dataset_path)
    variables = list(ds.data_vars.keys())
    return [{'label': var, 'value': var} for var in variables]

def plot_with_rectangle(dataset, variable, lat, lon, level, time, width):
    half_width = width / 2
    bottom_left_lat = lat - half_width
    bottom_left_lon = lon - half_width

    fig, ax = plt.subplots(figsize=(15, 15))
    if level is not None and 'level' in dataset[variable].dims:
        dataset[variable].sel(level=level).isel(time=time).plot(ax=ax, cmap='coolwarm', alpha=0.1)
    else:
        dataset[variable].isel(time=time).plot(ax=ax, cmap='coolwarm')

    rect = patches.Rectangle((bottom_left_lon, bottom_left_lat), width, width, linewidth=2, edgecolor='red', facecolor='none')
    ax.add_patch(rect)

    ax.scatter(lon, lat, color='red')
    ax.annotate(f'(lon: {lon}, lat: {lat})', xy=(lon, lat), xytext=(5, 5), textcoords='offset points', color='black', fontsize=12, ha='center')

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return f'data:image/png;base64,{encoded}'

def calculate_average_absolute_error(ground_truth, prediction):
    return abs(ground_truth - prediction).mean(dim=['longitude', 'latitude'])

def obtenir_dimensions_sans_time(data):
    return [dim for dim in data.dims if dim != 'time']

def register_callbacks(app):
    @app.callback(
        Output('graph1-plot', 'src'),
        [Input('generate-button1', 'n_clicks')],
        [State('file-dropdown1', 'value'),
         State('variable-dropdown1', 'value'),
         State('latitude-input1', 'value'),
         State('longitude-input1', 'value'),
         State('level-input1', 'value'),
         State('timestep-input1', 'value')]
    )
    def update_graph1(n_clicks, file, variable, lat, lon, level, timestep):
        if n_clicks > 0 and file and variable is not None and lat is not None and lon is not None and timestep is not None:
            dataset_path = f'data/{file}'
            ds = xr.open_zarr(dataset_path)
            image = plot_with_rectangle(ds, variable, lat, lon, level, timestep, width=20)
            return image
        return dash.no_update

    @app.callback(
        Output('graph2-plot', 'src'),
        [Input('generate-button2', 'n_clicks')],
        [State('file-dropdown2', 'value'),
         State('variable-dropdown2', 'value'),
         State('latitude-input2', 'value'),
         State('longitude-input2', 'value'),
         State('level-input2', 'value'),
         State('timestep-input2', 'value')]
    )
    def update_graph2(n_clicks, file, variable, lat, lon, level, timestep):
        if n_clicks > 0 and file and variable is not None and lat is not None and lon is not None and timestep is not None:
            dataset_path = f'data/{file}'
            ds = xr.open_zarr(dataset_path)
            image = plot_with_rectangle(ds, variable, lat, lon, level, timestep, width=20)
            return image
        return dash.no_update

    @app.callback(
        Output('comparison-plot', 'src'),
        [Input('generate-button3', 'n_clicks')],
        [State(f'dataset{i}-dropdown', 'value') for i in range(1, 6)] +
        [State(f'dataset{i}-variable-dropdown', 'value') for i in range(1, 6)]
    )
    def update_comparison_plot(n_clicks, *args):
        datasets = args[:5]
        variables = args[5:]
        if n_clicks > 0:
            ground_truth_path = f'data/{datasets[0]}'
            ground_truth_variable = variables[0]
            ds_ground_truth = xr.open_zarr(ground_truth_path)
            ground_truth_data = ds_ground_truth[ground_truth_variable]

            fig, ax = plt.subplots(figsize=(10, 5))
            for dataset, variable in zip(datasets[1:], variables[1:]):
                if dataset and variable:
                    ds_prediction = xr.open_zarr(f'data/{dataset}')
                    prediction_data = ds_prediction[variable]
                    aae = abs(ground_truth_data - prediction_data)
                    dimensions = obtenir_dimensions_sans_time(ground_truth_data)
                    aae_mean = aae.mean(dim=dimensions)
                    
                    ax.plot(range(len(aae_mean)), aae_mean, label=f'{dataset}-{variable}')  # Utilisation de range(len(aae_mean)) pour l'axe x

            ax.set_ylabel("Averaged Absolute Error")
            ax.set_xlabel("Time")
            ax.legend()

            buf = BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            encoded = base64.b64encode(buf.read()).decode('utf-8')
            plt.close(fig)
            return f'data:image/png;base64,{encoded}'
        return dash.no_update

    @app.callback(
        Output('file-dropdown1', 'options'),
        [Input('file-dropdown1', 'value')]
    )
    def update_file_dropdown1(selected_file):
        local_path = 'data'
        if os.path.exists(local_path):
            files = get_local_files(local_path)
        else:
            owner = 'yanktm'
            repo = 'testEra5dash'
            path = 'data'
            files = get_github_repo_contents(owner, repo, path)
        return files

    @app.callback(
        Output('file-dropdown2', 'options'),
        [Input('file-dropdown2', 'value')]
    )
    def update_file_dropdown2(selected_file):
        local_path = 'data'
        if os.path.exists(local_path):
            files = get_local_files(local_path)
        else:
            owner = 'yanktm'
            repo = 'testEra5dash'
            path = 'data'
            files = get_github_repo_contents(owner, repo, path)
        return files

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
        Output('variable-dropdown1', 'options'),
        [Input('file-dropdown1', 'value')]
    )
    def update_variable_dropdown1(selected_file):
        if selected_file:
            variables = get_dataset_variables(selected_file)
            return variables
        return []

    @app.callback(
        Output('variable-dropdown2', 'options'),
        [Input('file-dropdown2', 'value')]
    )
    def update_variable_dropdown2(selected_file):
        if selected_file:
            variables = get_dataset_variables(selected_file)
            return variables
        return []

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



    def create_file_dropdown_callback(button_id, dropdown_id):
        @app.callback(
            Output(dropdown_id, 'options'),
            [Input(button_id, 'n_clicks')]
        )
        def update_file_dropdown(n_clicks):
            local_path = 'data'
            if os.path.exists(local_path):
                files = get_local_files(local_path)
            else:
                owner = 'yanktm'
                repo = 'testEra5dash'
                path = 'data'
                files = get_github_repo_contents(owner, repo, path)
            return files

    def create_variable_dropdown_callback(button_id, file_dropdown_id, variable_dropdown_id):
        @app.callback(
            Output(variable_dropdown_id, 'options'),
            [Input(button_id, 'n_clicks')],
            [State(file_dropdown_id, 'value')]
        )
        def update_variable_dropdown(n_clicks, selected_file):
            if n_clicks > 0 and selected_file:
                variables = get_dataset_variables(selected_file)
                return variables
            return []

    for i in range(1, 6):
        create_file_dropdown_callback(f'button-dataset{i}', f'dataset{i}-dropdown')
        create_variable_dropdown_callback(f'button-variable{i}', f'dataset{i}-dropdown', f'dataset{i}-variable-dropdown')
