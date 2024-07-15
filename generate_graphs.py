import plotly.graph_objs as go
import xarray as xr
import pandas as pd

def generate_map(data):
    variable = '2m_temperature'  # Choisissez une variable par défaut
    start_date = '2020-01-01'
    end_date = '2020-12-31'
    filtered_data = data[variable].sel(time=slice(start_date, end_date))
    mean_data = filtered_data.mean(dim='time')
    figure = go.Figure(data=go.Contour(
        z=mean_data.values,
        x=mean_data.longitude.values,
        y=mean_data.latitude.values,
        colorscale='Viridis'
    ))
    figure.update_layout(
        title=f'Mean {variable} from {start_date} to {end_date}',
        xaxis_title='Longitude',
        yaxis_title='Latitude'
    )
    return figure

def generate_time_series(data):
    variable = '2m_temperature'  # Choisissez une variable par défaut
    start_date = '2020-01-01'
    end_date = '2020-12-31'
    filtered_data = data[variable].sel(time=slice(start_date, end_date))
    time_series = filtered_data.mean(dim=['latitude', 'longitude'])
    figure = go.Figure(data=go.Scatter(
        x=pd.to_datetime(time_series.time.values),
        y=time_series.values,
        mode='lines'
    ))
    figure.update_layout(
        title=f'Time Series of {variable} from {start_date} to {end_date}',
        xaxis_title='Time',
        yaxis_title=variable
    )
    return figure
