from django.shortcuts import render
from tethys_sdk.permissions import login_required
from tethys_sdk.gizmos import *
import os, datetime
from .forms import accessCodeForm

import random
import string

from django.shortcuts import render
from tethys_sdk.permissions import login_required

from tethys_sdk.gizmos import *
from .app import SirbaForecast as app

WORKSPACE = 'nasaaccess'
GEOSERVER_URI = 'nasaaccess'

@login_required()
def home(request):
    """
    Controller for the app home page.
    """
    

    accesscodeform = accessCodeForm()
    
    # Set date picker options
    start = 'Jan 01, 1981'
    end='Dec 31, 2010'
    #end = datetime.datetime.now().strftime("%b %d, %Y")
    format = 'M d, yyyy'
    startView = 'decade'
    minView = 'days'
    #Set variables options
    variables=[("Discharge", "Discharge"), ("Surface Runoff", "runoff"), ("Baseflow", "baseflow"), 
    ("Evapotranspiration", "etp"), ("Precipitation", "precip")]

    job_title = SelectInput(display_text='',
                              name='job_title',
                              multiple=False,
                              original=False,
                              options=[],
                              select2_options={'placeholder': 'HYPE Return Period Analysis',
                                               'allowClear': False},
                                               )
    select_comid = TextInput(display_text='',
                       name='inputAmount',
                       placeholder='14032264',
                       prepend='id')

    select_variable = SelectInput(display_text='',
                              name='select_variable',
                              original=True,
                              initial=[("Surface Runoff", "runoff")],
                              options=variables,
                              select2_options={'placeholder': 'Select Variable',
                                               'allowClear': False},
                              )

    start_pick = DatePicker(
        name='start_pick',
        autoclose=True,
        format=format,
        min_view_mode=minView,
        start_date=start,
        end_date=end,
        start_view=startView,
        today_button=False,
        initial='Jan 01, 1981'
    )

    end_pick = DatePicker(name='end_pick',
                          autoclose=True,
                          format=format,
                          min_view_mode=minView,
                          start_date=start,
                          end_date=end,
                          start_view=startView,
                          today_button=False,
                          initial='Dec 31, 2010'
                          )
   # Define map view options

    view_options = MVView(
        projection='EPSG:4326',
        center=[0, 13.12],
        zoom=8,
        maxZoom=18,
        minZoom=2
        )
    #drawing_options = MVDraw(
    #    controls=['Modify', 'Delete', 'Move', 'Point', 'LineString', 'Polygon', 'Box'],
    #    initial='Point',
    #    output_format='WKT'
    #    )

    # Define GeoJSON layer
    geojson_object = {
    'type': 'FeatureCollection',
    'crs': {
        'type': 'name',
        'properties': {
        'name': 'EPSG:3857'
        }
    },
    'features': [
        {
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [0, 0]
        }
        },
        {
        'type': 'Feature',
        'geometry': {
            'type': 'LineString',
            'coordinates': [[4e6, -2e6], [8e6, 2e6]]
        }
        },
        {
        'type': 'Feature',
        'geometry': {
            'type': 'Polygon',
            'coordinates': [[[-5e6, -1e6], [-4e6, 1e6], [-3e6, -1e6]]]
        }
        }
    ]
    }

    # Define GeoJSON point layer
    geojson_point_object = {
    'type': 'FeatureCollection',
    'crs': {
        'type': 'name',
        'properties': {
        'name': 'EPSG:3857'
        }
    },
    'features': [
        {
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [0, 0]
        }
        },
    ]
    }

    style = {'ol.style.Style': {
        'stroke': {'ol.style.Stroke': {
            'color': 'blue',
            'width': 2
        }},
        'fill': {'ol.style.Fill': {
            'color': 'green'
        }},
        'image': {'ol.style.Circle': {
            'radius': 10,
            'fill': None,
            'stroke': {'ol.style.Stroke': {
                'color': 'red',
                'width': 2
            }}
        }}
    }}

    geojson_layer = MVLayer(
        source='GeoJSON',
        options=geojson_object,
        layer_options={'style': style},
        legend_title='Test GeoJSON',
        legend_extent=[-46.7, -48.5, 74, 59],
        legend_classes=[
            MVLegendClass('polygon', 'Polygons', fill='green', stroke='blue'),
            MVLegendClass('line', 'Lines', stroke='blue')
        ]
    )

    geojson_point_layer = MVLayer(
        source='GeoJSON',
        options=geojson_point_object,
        legend_title='Test GeoJSON',
        legend_extent=[-46.7, -48.5, 74, 59],
        legend_classes=[
            MVLegendClass('line', 'Lines', stroke='#3d9dcd')
        ],
    )


    # Retrieve a geoserver engine
    geoserver_engine = app.get_spatial_dataset_service(name='primary_geoserver', as_engine=True)

    # Check for workspace and create workspace for app if it doesn't exist
    response = geoserver_engine.list_workspaces()

    if response['success']:
        workspaces = response['result']

        if WORKSPACE not in workspaces:
            geoserver_engine.create_workspace(workspace_id=WORKSPACE, uri=GEOSERVER_URI)

    # Case where the form has been submitted
    if request.POST and 'submit' in request.POST:
        # Verify files are included with the form
        if request.FILES and 'files' in request.FILES:
            # Get a list of the files
            file_list = request.FILES.getlist('files')

            # Upload shapefile
            store = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
            store_id = WORKSPACE + ':' + store
            geoserver_engine.create_shapefile_resource(
                store_id=store_id,
                shapefile_upload=file_list,
                overwrite=True
            )
    # Define GeoServer Layer
    
    geoserver_layer = MVLayer(
    source='ImageWMS',
    options={'url': 'http://localhost:8080/geoserver/wms',
           'params': {'LAYERS': 'nasaaccess:cat_pfaf_1_MERIT_Hydro_v07_Basins_v01_sirba'},
           'serverType': 'geoserver'},
    legend_title='Bassin de la Sirba',
    legend_classes=[ ]
    )

    geoserver_layer1 = MVLayer(
    source='ImageWMS',
    options={'url': 'http://localhost:8080/geoserver/wms',
           'params': {'LAYERS': 'nasaaccess:riv_pfaf_1_MERIT_Hydro_v07_Basins_v01_sirba'},
           'serverType': 'geoserver'},
    legend_title='Reseau hydrographique',
    legend_classes=[ ]
    )


    map_view_options = MapView(
        height='600px',
        width='100%',
        controls=['ZoomSlider', 'Rotate', 'FullScreen',
            {'MousePosition': {'projection': 'EPSG:4326'}},
            {'ZoomToExtent': {'projection': 'EPSG:4326', 'extent': [-25, 25, 0, 25]}}],
        layers=[geoserver_layer1, geoserver_layer ],
        view=view_options,
        basemap=None,
        draw=None,
        legend=True
        )

    context = {
        'job_title': job_title,
        'start_pick': start_pick,
        'end_pick': end_pick,
        'map_view_options': map_view_options,
        'select_variable': select_variable,
        'select_comid': select_comid,
        'accesscodeform': accesscodeform,
    }

    return render(request, 'sirba_forecast/home.html', context)


@login_required()
def base(request):
    """
    Controller for the app home page.
    """
    # Set date picker options
    start = 'Jan 01, 1981'
    end = datetime.datetime.now().strftime("%b %d, %Y")
    format = 'M d, yyyy'
    startView = 'decade'
    minView = 'days'
    #Set variables options
    variables=[("Surface Runoff", "runoff"), ("Baseflow", "baseflow"), 
    ("Evapotranspiration", "etp"), ("Precipitation", "precip")]

    job_title = SelectInput(display_text='',
                              name='job_title',
                              multiple=False,
                              original=False,
                              options=[],
                              select2_options={'placeholder': 'HYPE Return Period Analysis',
                                               'allowClear': False},
                                               )
    select_comid = TextInput(display_text='',
                       name='inputAmount',
                       placeholder='964',
                       prepend='id')

    select_variable = SelectInput(display_text='',
                              name='select_variable',
                              original=True,
                              initial=[("Surface Runoff", "runoff")],
                              options=variables,
                              select2_options={'placeholder': 'Select Variable',
                                               'allowClear': False},
                              )

    start_pick = DatePicker(
        name='start_pick',
        autoclose=True,
        format=format,
        min_view_mode=minView,
        start_date=start,
        end_date=end,
        start_view=startView,
        today_button=False,
        initial='Start Date'
    )

    end_pick = DatePicker(name='end_pick',
                          autoclose=True,
                          format=format,
                          min_view_mode=minView,
                          start_date=start,
                          end_date=end,
                          start_view=startView,
                          today_button=False,
                          initial='End Date'
                          )
   # Define map view options

    view_options = MVView(
        projection='EPSG:4326',
        center=[0, 13.12],
        zoom=8,
        maxZoom=18,
        minZoom=2
        )
    drawing_options = MVDraw(
        controls=['Modify', 'Delete', 'Move', 'Point', 'LineString', 'Polygon', 'Box'],
        initial='Point',
        output_format='WKT'
        )

    # Define GeoJSON layer
    geojson_object = {
    'type': 'FeatureCollection',
    'crs': {
        'type': 'name',
        'properties': {
        'name': 'EPSG:3857'
        }
    },
    'features': [
        {
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [0, 0]
        }
        },
        {
        'type': 'Feature',
        'geometry': {
            'type': 'LineString',
            'coordinates': [[4e6, -2e6], [8e6, 2e6]]
        }
        },
        {
        'type': 'Feature',
        'geometry': {
            'type': 'Polygon',
            'coordinates': [[[-5e6, -1e6], [-4e6, 1e6], [-3e6, -1e6]]]
        }
        }
    ]
    }

    # Define GeoJSON point layer
    geojson_point_object = {
    'type': 'FeatureCollection',
    'crs': {
        'type': 'name',
        'properties': {
        'name': 'EPSG:3857'
        }
    },
    'features': [
        {
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [0, 0]
        }
        },
    ]
    }

    style = {'ol.style.Style': {
        'stroke': {'ol.style.Stroke': {
            'color': 'blue',
            'width': 2
        }},
        'fill': {'ol.style.Fill': {
            'color': 'green'
        }},
        'image': {'ol.style.Circle': {
            'radius': 10,
            'fill': None,
            'stroke': {'ol.style.Stroke': {
                'color': 'red',
                'width': 2
            }}
        }}
    }}

    geojson_layer = MVLayer(
        source='GeoJSON',
        options=geojson_object,
        layer_options={'style': style},
        legend_title='Test GeoJSON',
        legend_extent=[-46.7, -48.5, 74, 59],
        legend_classes=[
            MVLegendClass('polygon', 'Polygons', fill='green', stroke='blue'),
            MVLegendClass('line', 'Lines', stroke='blue')
        ]
    )

    geojson_point_layer = MVLayer(
        source='GeoJSON',
        options=geojson_point_object,
        legend_title='Test GeoJSON',
        legend_extent=[-46.7, -48.5, 74, 59],
        legend_classes=[
            MVLegendClass('line', 'Lines', stroke='#3d9dcd')
        ],
    )


    # Retrieve a geoserver engine
    geoserver_engine = app.get_spatial_dataset_service(name='primary_geoserver', as_engine=True)

    # Check for workspace and create workspace for app if it doesn't exist
    response = geoserver_engine.list_workspaces()

    if response['success']:
        workspaces = response['result']

        if WORKSPACE not in workspaces:
            geoserver_engine.create_workspace(workspace_id=WORKSPACE, uri=GEOSERVER_URI)

    # Case where the form has been submitted
    if request.POST and 'submit' in request.POST:
        # Verify files are included with the form
        if request.FILES and 'files' in request.FILES:
            # Get a list of the files
            file_list = request.FILES.getlist('files')

            # Upload shapefile
            store = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
            store_id = WORKSPACE + ':' + store
            geoserver_engine.create_shapefile_resource(
                store_id=store_id,
                shapefile_upload=file_list,
                overwrite=True
            )
    # Define GeoServer Layer
    
    geoserver_layer = MVLayer(
    source='ImageWMS',
    options={'url': 'http://localhost:8080/geoserver/wms',
           'params': {'LAYERS': 'nasaaccess:cat_pfaf_1_MERIT_Hydro_v07_Basins_v01_sirba'},
           'serverType': 'geoserver'},
    legend_title='Bassin de la Sirba',
    legend_classes=[ ]
    )

    geoserver_layer1 = MVLayer(
    source='ImageWMS',
    options={'url': 'http://localhost:8080/geoserver/wms',
           'params': {'LAYERS': 'nasaaccess:riv_pfaf_1_MERIT_Hydro_v07_Basins_v01_sirba'},
           'serverType': 'geoserver'},
    legend_title='Reseau hydrographique',
    legend_classes=[ ]
    )


    map_view_options = MapView(
        height='600px',
        width='100%',
        controls=['ZoomSlider', 'Rotate', 'FullScreen',
            {'MousePosition': {'projection': 'EPSG:4326'}},
            {'ZoomToExtent': {'projection': 'EPSG:4326', 'extent': [-25, 25, 0, 25]}}],
        layers=[geoserver_layer1, geoserver_layer ],
        view=view_options,
        basemap=None,
        draw=drawing_options,
        legend=True
        )

    context = {
        'job_title': job_title,
        'start_pick': start_pick,
        'end_pick': end_pick,
        'map_view_options': map_view_options,
        'select_variable': select_variable,
        'select_comid': select_comid,
    }
    
    return render(request, 'sirba_forecast/base.html', context)