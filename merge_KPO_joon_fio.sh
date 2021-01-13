#!/bin/bash

fio cat "/media/rocket_gis/Evelyn/veekaitsevoondid/final files/KPO_JOON_5m/KPO_Kaldajoon_Topol_5m_E.shp" \
    "/media/rocket_gis/Evelyn/veekaitsevoondid/final files/KPO_JOON_5m/KPO_Kaldajoon_Topol_5m_W.shp" | fio collect | fio load --driver GPKG --src_crs 'EPSG:3301' --layer KPO_Kaldajoon_Topol_5m KPO_Kaldajoon_Topol_5m.gpkg
