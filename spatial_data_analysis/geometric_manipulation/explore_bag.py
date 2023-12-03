#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 11:48:58 2023

@author: sajad
"""

# 2.1 Querying datasets

from osgeo import gdal, ogr


filename = "/Users/sajad/Library/CloudStorage/GoogleDrive-sajad.ahmadi.arc@gmail.com/My Drive/Uinversity Files/Period 2/Spatial Data Analysis/Labs/Lab2/Lab 2 - data/Amsterdam_BAG.gpkg"

data_source = ogr.GetDriverByName('GPKG').Open(filename, update=0)

## get the number of layers
layer_count = data_source.GetLayerCount()

## Task: Print the number of layers included in the dataset.
print("total number of layers is", layer_count)


## Task: Print for each layer the layer name and CRS.

layer_names = []
for i in range(layer_count):
    layer = data_source.GetLayerByIndex(i)
    name = layer.GetName()
    layer_names.append(name)
    index = i
    crs = layer.GetSpatialRef()
    print("layer name", name, " index is", i, "\n")
    print("CRS is", crs,"\n")

print("the list of layers names is","\n",layer_names)

# translation from Dutch to ENG
# ['Pand', 'Verblijfsobject', 'Wijken'] --> ['pledge','Residence object', 'Neighborhoods']



buildings = data_source.GetLayerByName('Verblijfsobject')
print(buildings)

#Task: Print the number of features in the layer.
buildings_count = buildings.GetFeatureCount()
print('\n\n\n',"numer of buildings is",buildings_count)


## getting the attribute table of the Verblijfsobject layer
locations_def = buildings.GetLayerDefn()

## getting the number of fields of the Verblijfsobject layer
verbl_field_count = locations_def.GetFieldCount()
print(verbl_field_count)

## getting the names of the fields of the Verblijfsobject layer
verbl_field_names = []
verbl_field_types = []

for i in range(verbl_field_count):
    field_name = locations_def.GetFieldDefn(i).GetName()
    field_type = locations_def.GetFieldDefn(i).GetTypeName()
    verbl_field_names.append(field_name)
    verbl_field_types.append(field_type)

## Task: Print the name and type of each field in the layer.    
print("the list of field names\n",verbl_field_names,'\n',
      "the list of field types\n",verbl_field_types)


##--> the list of field names ['oppervlakte', 'gebruiksdoel'] 
##--> the list of field types ['Integer', 'String']


## Task: Add code to your script that iterates over all features in the layer, retrieves the value of the field
## oppervlakte (surface area) and adds up the area.

building_surface_areas = []

for i in range(1,buildings_count+1):
    feature = buildings.GetFeature(i)
    surface_area = feature.GetField("oppervlakte")
    building_surface_areas.append(surface_area)

    
## checking the list of building surface areas
print(building_surface_areas[:10],
      len(building_surface_areas))

## result--> 30, 32, 48, 32, 32, 32, 32, 32, 32, 98] 496420
## as we can see, the length of the list is equal to the building counts 

## Question: What is the total surface area given in the location layer?
total_surface_area = sum(building_surface_areas)
print(total_surface_area)

   
## Question: What is the coordinate of the feature with the index 439774?
feature_439774 = buildings.GetFeature(439774)
geometry_439774 = feature_439774.GetGeometryRef()

## Question: What is the coordinate of the feature with the index 439774?
x_coord = geometry_439774.GetX()
y_coord = geometry_439774.GetY()
print("x coord. is ",x_coord," y coord. is ",y_coord)






