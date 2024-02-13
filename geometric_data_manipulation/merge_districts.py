#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 17:31:39 2023

@author: sajad
"""

"""
Task: Create a second script merge_districts.py to merge the districts from the Wijken input layer
of the Amsterdam_BAG.gpkg dataset. Merge the district geometries to one new geometry and add the
result to the schools.gpkg dataset as the new layer districts.
"""

# opening the amsterdam and centroids data sources 
from osgeo import gdal, ogr
from osgeo.osr import SpatialReference

amsterdam_file = "/Users/sajad/Library/CloudStorage/GoogleDrive-sajad.ahmadi.arc@gmail.com/My Drive/Uinversity Files/Period 2/Spatial Data Analysis/Labs/Lab2/Lab 2 - data/Amsterdam_BAG.gpkg"

amsterdam_data_source = ogr.GetDriverByName('GPKG').Open(amsterdam_file)

# using wijken layer
Wij_layer = amsterdam_data_source.GetLayerByName("Wijken")

schools_file = "/Users/sajad/Library/CloudStorage/GoogleDrive-sajad.ahmadi.arc@gmail.com/My Drive/Uinversity Files/Period 2/Spatial Data Analysis/Labs/Lab2/Lab 2 - data/schools.gpkg"

schools_data_source = ogr.GetDriverByName('GPKG').Open(schools_file, update = 1)


if schools_data_source.GetLayerByName("districts"):
    schools_data_source.DeleteLayer("districts")
    
    
## create a new GeoPackage
rdNew = SpatialReference()
rdNew.ImportFromEPSG(28992)

districts_layer = schools_data_source.CreateLayer('districts', srs=rdNew, geom_type=ogr.wkbMultiPolygon)

Wij_layer_defn = Wij_layer.GetLayerDefn()
Wij_feature = Wij_layer.GetNextFeature()
Wij_geometry = Wij_feature.GetGeometryRef()
Wij_layer.ResetReading()


for feature in Wij_layer:
    buffer_geometry = feature.GetGeometryRef()
    union = Wij_geometry.Union(buffer_geometry)
    Wij_geometry = union
    
    
outfeature = ogr.Feature(districts_layer.GetLayerDefn())
outfeature.SetGeometry(Wij_geometry)
districts_layer.CreateFeature(outfeature)

districts_layer.GetFeatureCount()


amsterdam_data_source = None

schools_data_source = None








