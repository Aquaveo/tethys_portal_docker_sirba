from tethys_sdk.base import TethysAppBase, url_map_maker
from tethys_sdk.app_settings import SpatialDatasetServiceSetting


class SirbaForecast(TethysAppBase):
    """
    Tethys app class for Sirba Forecast System.
    """

    name = 'Sirba Forecast System'
    index = 'sirba_forecast:home'
    icon = 'sirba_forecast/images/logo.gif'
    #icon = 'sirba_forecast/images/icon.gif'
    package = 'sirba_forecast'
    root_url = 'sirba-forecast'
    color = '#f39c12'
    description = '"This application allows to get data from VIC model"'
    tags = '"Sirba", "Forecast", "BRECcIA"'
    enable_feedback = False
    feedback_emails = []

    def url_maps(self):
        """
        Add controllers
        """
        UrlMap = url_map_maker(self.root_url)

        url_maps = (
            UrlMap(
                name='home',
                url='sirba_forecast',
                controller='sirba_forecast.controllers.home'
            ),
            UrlMap(
                name='home',
                url='sirba_forecast',
                controller='sirba_forecast.controllers.base'
            ),
            UrlMap(
                name='run',
                url='run_historical/run',
                controller='sirba_forecast.ajax_controllers.run_historical'
            ),
            UrlMap(
                name='download',
                url='sirba_forecast/download',
                controller='sirba_forecast.ajax_controllers.download_data'
            )
        )

        return url_maps
    
    def spatial_dataset_service_settings(self):
        """
        Example spatial_dataset_service_settings method.
        """
        return (
            SpatialDatasetServiceSetting(
                name='primary_geoserver',
                description='Geoserver for serving user uploaded shapefiles',
                engine=SpatialDatasetServiceSetting.GEOSERVER,
                required=True,
            ),
        )