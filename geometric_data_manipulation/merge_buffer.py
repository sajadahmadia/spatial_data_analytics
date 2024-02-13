#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 16:57:42 2023

@author: sajad
"""

"""
3.2 Merging geometries
"""

from osgeo import gdal, ogr
from osgeo.osr import SpatialReference

schools_file = "/Users/sajad/Library/CloudStorage/GoogleDrive-sajad.ahmadi.arc@gmail.com/My Drive/Uinversity Files/Period 2/Spatial Data Analysis/Labs/Lab2/Lab 2 - data/schools.gpkg"

data_source = ogr.GetDriverByName('GPKG').Open(schools_file, update=1)

buffer_layer = data_source.GetLayerByName('buffer')



if data_source.GetLayerByName("merge"):
    data_source.DeleteLayer("merge")
    
    
## create a new GeoPackage
rdNew = SpatialReference()
rdNew.ImportFromEPSG(28992)


"""
Question: What kind of geometry type does the layer merge need to be?
Answer: it should be a polygon layer
"""

## add a new layer merge
merge_layer = data_source.CreateLayer('merge', srs=rdNew, geom_type=ogr.wkbPolygon)


## checking whether the new layer is created or not and its CRS 
layer_count = data_source.GetLayerCount()
print(layer_count)

buffer_layer_defn = buffer_layer.GetLayerDefn()
buffer_feature = buffer_layer.GetNextFeature()
buffer_geometry = buffer_feature.GetGeometryRef()


merge_feature = ogr.Feature(buffer_layer_defn)
merge_feature.SetGeometry(buffer_geometry)
buffer_layer.CreateFeature(merge_feature)

merge_geometry = buffer_geometry

for feature in buffer_layer:
    buffer_geometry = feature.GetGeometryRef()
    union = merge_geometry.Union(buffer_geometry)
    merge_geometry = union
    

# create a feature and set its geometry to merge_geometry and add the feature to the merge layer.
merge_layer_defn = merge_layer.GetLayerDefn()
outfeature = ogr.Feature(merge_layer_defn)
outfeature.SetGeometry(merge_geometry)
merge_layer.CreateFeature(outfeature)


data_source = None







