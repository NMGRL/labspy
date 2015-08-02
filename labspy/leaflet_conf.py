USGS_TILES = [('USGS Base', 'http://basemap.nationalmap.gov/ArcGIS/rest/services/USGSTopo/MapServer/tile/{z}/{y}/{x}',
               {'attribution': 'USGS'}),
              ('USGS Image',
               'http://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryTopo/MapServer/tile/{z}/{y}/{x}',
               {'attribution': 'USGS'}),
              ('USGS ImageOnly',
               'http://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}',
               {'attribution': 'USGS'})]

OTM_TILES = [('OpenTopMap', 'http://{s}.tile.opentopomap.org/{z}/{x}/{y}.png',
              {'maxZoom': 16,
               'attribution': 'Map data: &copy; <a href="http://www.openstreetmap.org/copyright">'
                              'OpenStreetMap</a>, <a href="http://viewfinderpanoramas.org">SRTM</a> '
                              '| Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> '
                              '(<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)'})]

OSM_TILES = [('OpenStreeMap.Hot',
              'http://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png',
              {'maxZoom': 19,
               'attribution': '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, Tiles courtesy of <a href="http://hot.openstreetmap.org/" target="_blank">Humanitarian OpenStreetMap Team</a>'}
              )]

OVERLAYS = []


def config(tiles=None, overlays=None, **kw):
    if tiles is None:
        tiles = OSM_TILES + USGS_TILES + OTM_TILES

    if overlays is None:
        overlays = OVERLAYS

    cfg = {'DEFAULT_CENTER': (34.060765, -106.890713),
           'DEFAULT_ZOOM': 10,
           'MIN_ZOOM': 3,
           'MAX_ZOOM': 18,
           'TILES': tiles,
           'OVERLAYS': overlays}

    cfg.update(kw)
    return cfg

# [
#         ('Image', 'http://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryTopo/MapServer/tile/{z}/{y}/{x}',
#          {'opacity': 0.5}),
#         ('ImageOnly', 'http://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}',
#          {}),
#         ('Esri.Delorme',
#          'http://server.arcgisonline.com/ArcGIS/rest/services/Specialty/DeLorme_World_Base_Map/MapServer/tile/{z}/{y}/{x}',
#          {'attribution': 'Tiles &copy; Esri &mdash; Copyright: &copy;2012 DeLorme', }),
#
#         ('Modis Snow Cover',
#          'http://map1.vis.earthdata.nasa.gov/wmts-webmerc/MODIS_Terra_Snow_Cover/default/{time}/{tilematrixset}{maxZoom}/{z}/{y}/{x}.{format}',
#          {
#              'attribution': 'Imagery provided by services from the Global Imagery Browse Services (GIBS), operated by the NASA/GSFC/Earth Science Data and Information System (<a href="https://earthdata.nasa.gov">ESDIS</a>) with funding provided by NASA/HQ.',
#              'bounds': [[-85.0511287776, -179.999999975], [85.0511287776, 179.999999975]],
#              'minZoom': 1,
#              'maxZoom': 8,
#              'format': 'png',
#              'time': '',
#              'tilematrixset': 'GoogleMapsCompatible_Level',
#              'opacity': 0.75})
