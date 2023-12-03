#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 18:08:35 2023

@author: sajad

Part 3.3
"""


from osgeo import gdal, ogr
from osgeo.osr import SpatialReference

schools_file = "/Users/sajad/Library/CloudStorage/GoogleDrive-sajad.ahmadi.arc@gmail.com/My Drive/Uinversity Files/Period 2/Spatial Data Analysis/Labs/Lab2/Lab 2 - data/schools.gpkg"

data_source = ogr.GetDriverByName('GPKG').Open(schools_file, update=1)

merge_layer =  data_source.GetLayerByName('merge')
districts_layer = data_source.GetLayerByName('districts')

districts_layer.GetFeatureCount()

"""
Question: Which operation will you use to compute the area far away from schools?
Answer: Erase
"""
if data_source.GetLayerByName("away"):
    data_source.DeleteLayer("away")
    
    
## create a new GeoPackage
rdNew = SpatialReference()
rdNew.ImportFromEPSG(28992)

away_layer = data_source.CreateLayer('away', srs=rdNew, geom_type=ogr.wkbMultiPolygon)

away = data_source.GetLayerByName('away')

districts_layer.Erase(merge_layer,away)

away_feature = away.GetNextFeature()
print("the area far away  from schools is" , away_feature.GetGeometryRef().GetArea())


data_source = None









