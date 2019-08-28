import netCDF4
from dateutil.parser import parse

import pythesint as pti

from django.db import models
from django.contrib.gis.geos import GEOSGeometry

from geospaas.vocabularies.models import Platform
from geospaas.vocabularies.models import Instrument
from geospaas.vocabularies.models import DataCenter
from geospaas.vocabularies.models import ISOTopicCategory
from geospaas.catalog.models import GeographicLocation
from geospaas.catalog.models import DatasetURI, Source, Dataset

# test url
# uri = https://thredds.met.no/thredds/dodsC/met.no/observations/stations/SN99938.nc
class MetObsStationManager(models.Manager):

    def get_or_create(self, uri, *args, **kwargs):
        ''' Create dataset and corresponding metadata

        Parameters:
        ----------
            uri : str
                  URI to file or stream openable by netCDF4.Dataset
        Returns:
        -------
            dataset and flag
        '''
        # check if dataset already exists
        uris = DatasetURI.objects.filter(uri=uri)
        if len(uris) > 0:
            return uris[0].dataset, False

        # set source
        platform = pti.get_gcmd_platform('meteorological stations')
        instrument = pti.get_gcmd_instrument('in situ/laboratory instruments')

        pp = Platform.objects.get(
                category=platform['Category'],
                series_entity=platform['Series_Entity'],
                short_name=platform['Short_Name'],
                long_name=platform['Long_Name']
            )
        ii = Instrument.objects.get(
                category = instrument['Category'],
                instrument_class = instrument['Class'],
                type = instrument['Type'],
                subtype = instrument['Subtype'],
                short_name = instrument['Short_Name'],
                long_name = instrument['Long_Name']
            )
        source = Source.objects.get_or_create(
            platform = pp,
            instrument = ii)[0]

        nc_dataset = netCDF4.Dataset(uri)

        station_name = nc_dataset.station_name
        longitude = nc_dataset.variables['longitude'][0]
        latitude = nc_dataset.variables['latitude'][0]
        location = GEOSGeometry('POINT(%s %s)' % (longitude, latitude))

        geolocation = GeographicLocation.objects.get_or_create(
                            geometry=location)[0]

        entrytitle = nc_dataset.title
        dc = DataCenter.objects.get(short_name='NO/MET')
        iso_category = ISOTopicCategory.objects.get(name='Climatology/Meteorology/Atmosphere')
        summary = nc_dataset.summary

        ds = Dataset(
                entry_id = 'NOAA_NDBC_%s'%nc_dataset.station,
                entry_title=entrytitle,
                ISO_topic_category = iso_category,
                data_center = dc,
                summary = summary,
                time_coverage_start=parse(nc_dataset.time_coverage_start),
                time_coverage_end=parse(nc_dataset.time_coverage_end),
                source=source,
                geographic_location=geolocation)
        ds.save()

        ds_uri = DatasetURI.objects.get_or_create(uri=uri, dataset=ds)[0]


        return ds, True


