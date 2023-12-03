#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 10:58:48 2023

@author: sajad
"""

from osgeo import gdal, ogr
from osgeo.osr import SpatialReference


filename = "/Users/sajad/Library/CloudStorage/GoogleDrive-sajad.ahmadi.arc@gmail.com/My Drive/Uinversity Files/Period 2/Spatial Data Analysis/Labs/Lab2/Lab 2 - data/Amsterdam_BAG.gpkg"

data_source = ogr.GetDriverByName('GPKG').Open(filename, update=0)

pand_layer = data_source.GetLayerByName('Pand')


## create a new GeoPackage
rdNew = SpatialReference()
rdNew.ImportFromEPSG(28992)

## Create the new dataset with the output layer centroids using a point geometry type
centroid_source = ogr.GetDriverByName('GPKG').CreateDataSource('centroids.gpkg')
centroid_layer = centroid_source.CreateLayer('centroids', srs=rdNew, geom_type=ogr.wkbPoint)


## checking whether the new layer is created or not and its CRS 
layer_count = centroid_source.GetLayerCount()

layer_names = []
for i in range(layer_count):
    layer = centroid_source.GetLayerByIndex(i)
    name = layer.GetName()
    layer_names.append(name)
    index = i
    crs = layer.GetSpatialRef()
    print("layer name", name, " index is", i, "\n")
    print("CRS is", crs,"\n")

## ressult --> layer_names = ['centroids']


## Task: Add a field area to your layer centroids.
field = ogr.FieldDefn('area', ogr.OFTReal)
centroid_layer.CreateField(field)


centroid_layer_def = centroid_layer.GetLayerDefn()

## checking whetehr the new filed is added to the centroid_layer or not and its name
centroid_field_name = centroid_layer_def.GetFieldDefn(0).GetName()
print(centroid_field_name)


# counting the number of features in the pand_layer
pand_layer_feature_count = pand_layer.GetFeatureCount()
print(f"Number of features: {pand_layer_feature_count}")


## Task: Calculate the area and the centroid location of each building.
for i in range(1,pand_layer_feature_count+1):
    feature = pand_layer.GetFeature(i)
    house_geometry = feature.GetGeometryRef()
    centroid = house_geometry.Centroid()
    house_area = house_geometry.GetArea()
    
    point_feature = ogr.Feature(centroid_layer_def)
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(centroid.GetX(), centroid.GetY())
    point_feature.SetGeometry(point)
    point_feature.SetField('area', house_area)
    centroid_layer.CreateFeature(point_feature)
    

# now find the features of the centroid layer and their values in a list
feature_count = centroid_layer.GetFeatureCount()
print(f"Number of features: {feature_count}")

# Get the layer's definition
centroid_def = centroid_layer.GetLayerDefn()

# Get the number of fields (attributes)
field_count = centroid_def.GetFieldCount()
print(f"Number of fields: {field_count}")


