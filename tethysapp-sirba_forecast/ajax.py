from sirba_forecast.app import SirbaForecast as app

geoserver_engine = app.get_spatial_dataset_service('primary_geoserver', as_engine=True)

