{% set CONDA_HOME = salt['environ.get']('CONDA_HOME') %}
{% set TETHYS_PERSIST = salt['environ.get']('TETHYS_PERSIST') %}
{% set DAM_INVENTORY_MAX_DAMS = salt['environ.get']('DAM_INVENTORY_MAX_DAMS') %}

{% set POSTGIS_SERVICE_NAME = 'tethys_postgis' %}
{% set GEOSERVER_SERVICE_NAME = 'tethys_geoserver' %}

Add_SIRBA_to_Installed_Apps:
  cmd.run:
    - name: >
        . {{ CONDA_HOME }}/bin/activate tethys &&
        tethys settings --set INSTALLED_APPS "['tethysapp.sirba_forecast']" &&
        tethys db migrate
    - shell: /bin/bash
    - unless: /bin/bash -c "[ -f "{{ TETHYS_PERSIST }}/init_apps_setup_complete" ];"

Sync_Apps:
  cmd.run:
    - name: >
        . {{ CONDA_HOME }}/bin/activate tethys &&
        tethys db sync
    - shell: /bin/bash
    - unless: /bin/bash -c "[ -f "{{ TETHYS_PERSIST }}/init_apps_setup_complete" ];"

Set_Custom_Settings:
  cmd.run:
    - name: >
        . {{ CONDA_HOME }}/bin/activate tethys &&
        tethys app_settings set dam_inventory max_dams {{ DAM_INVENTORY_MAX_DAMS }}
    - shell: /bin/bash
    - unless: /bin/bash -c "[ -f "{{ TETHYS_PERSIST }}/init_apps_setup_complete" ];"

Link_Tethys_Services_to_Apps:
  cmd.run:
    - name: >
        . {{ CONDA_HOME }}/bin/activate tethys &&
        tethys link persistent:{{ POSTGIS_SERVICE_NAME }} dam_inventory:ps_database:primary_db &&
        tethys link persistent:{{ POSTGIS_SERVICE_NAME }} postgis_app:ps_database:flooded_addresses &&
        tethys link spatial:{{ GEOSERVER_SERVICE_NAME }} sirba_forecast:ds_spatial:primary_geoserver
    - shell: /bin/bash
    - unless: /bin/bash -c "[ -f "{{ TETHYS_PERSIST }}/init_apps_setup_complete" ];"

Sync_App_Persistent_Stores:
  cmd.run:
    - name: >
        . {{ CONDA_HOME }}/bin/activate tethys &&
        tethys syncstores all
    - shell: /bin/bash
    - unless: /bin/bash -c "[ -f "{{ TETHYS_PERSIST }}/init_apps_setup_complete" ];"

Flag_Init_Apps_Setup_Complete:
  cmd.run:
    - name: touch {{ TETHYS_PERSIST }}/init_apps_setup_complete
    - shell: /bin/bash
    - unless: /bin/bash -c "[ -f "{{ TETHYS_PERSIST }}/init_apps_setup_complete" ];"
