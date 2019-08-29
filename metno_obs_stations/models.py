from django.db import models

from geospaas.catalog.models import Dataset as CatalogDataset

from metno_obs_stations.managers import MetObsStationManager

class MetObsStation(CatalogDataset):
    class Meta:
        proxy = True
    objects = MetObsStationManager()

