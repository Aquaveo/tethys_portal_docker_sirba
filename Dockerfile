FROM tethysplatform/tethys-core:3.4.1

# ENVIRONMENT
ENV DAM_INVENTORY_MAX_DAMS="50"
ENV TETHYS_GS_PROTOCOL http
ENV TETHYS_GS_HOST geoserver
ENV TETHYS_GS_PORT 8181
ENV TETHYS_GS_PROTOCOL_PUB https
ENV TETHYS_GS_HOST_PUB geoserver
ENV TETHYS_GS_PORT_PUB 443
ENV TETHYS_GS_USERNAME admin
ENV TETHYS_GS_PASSWORD geoserver


# ADD FILES
COPY tethysapp-dam_inventory ${TETHYS_HOME}/apps/tethysapp-dam_inventory
COPY tethysapp-postgis_app ${TETHYS_HOME}/apps/tethysapp-postgis_app
COPY tethysapp-sirba_forecast ${TETHYS_HOME}/apps/tethysapp-sirba_forecast

# ADD THEME FILES
COPY images/ /tmp/custom_theme/images/

# INSTALL APPS
# Dam Inventory
RUN /bin/bash -c "cd ${TETHYS_HOME}/apps/tethysapp-dam_inventory && \
    . ${CONDA_HOME}/bin/activate tethys && \
    tethys install --no-db-sync"
# PostGIS App
RUN /bin/bash -c "cd ${TETHYS_HOME}/apps/tethysapp-postgis_app && \
    . ${CONDA_HOME}/bin/activate tethys && \
    tethys install --no-db-sync"
# SIRBA Forecast
RUN /bin/bash -c "cd ${TETHYS_HOME}/apps/tethysapp-sirba_forecast && \
    . ${CONDA_HOME}/bin/activate tethys && \
    tethys install --no-db-sync"

# ADD SALT FILES
COPY salt/ /srv/salt/

# PORTS
EXPOSE 80

# RUN
WORKDIR ${TETHYS_HOME}
CMD bash run.sh
