#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 16:56:04 2023

@author: sajad
"""

from osgeo import gdal, ogr
from osgeo.osr import SpatialReference

schools_file = "/Users/sajad/Library/CloudStorage/GoogleDrive-sajad.ahmadi.arc@gmail.com/My Drive/Uinversity Files/Period 2/Spatial Data Analysis/Labs/Lab2/Lab 2 - data/schools.gpkg"

data_source = ogr.GetDriverByName('GPKG').Open(schools_file, update=1)

point_layer = data_source.GetLayerByName('locations')



if data_source.GetLayerByName("buffer"):
    data_source.DeleteLayer("buffer")
    
    
## create a new GeoPackage
rdNew = SpatialReference()
rdNew.ImportFromEPSG(28992)

## add a new layer buffer

buffer_layer = data_source.CreateLayer('buffer', srs=rdNew, geom_type=ogr.wkbPolygon)


## checking whether the new layer is created or not and its CRS 
layer_count = data_source.GetLayerCount()
print(layer_count)

"""
Question: What kind of geometry type does the layer buffer need to be?
Answer: it should be a polygon, determined by geom_type=ogr.wkbPolygon parameter
"""

point_layer_feature_count = point_layer.GetFeatureCount()
print(point_layer_feature_count)


#buffer_field = ogr.FieldDefn('area', ogr.OFTReal)
#layer.CreateField(field)


buffer_layer_defn = buffer_layer.GetLayerDefn()


"""
Task: Create new features for the buffer geometries and add them to the buffer layer.
"""

for point_feature in point_layer:
    point_geometry = point_feature.GetGeometryRef()
    buffer_geometry = point_geometry.Buffer(250)
    
    outFeature = ogr.Feature(buffer_layer_defn)
    outFeature.SetGeometry(buffer_geometry)
    buffer_layer.CreateFeature(outFeature)
    


# checking whether the new features are created or not:
print(buffer_layer.GetFeatureCount())



data_source = None















