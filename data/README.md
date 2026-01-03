Data Directory
==============

Contents and Organization
--------------------------

This directory contains input data for the Karaj urban growth analysis pipeline.

raw/

Contains raw Landsat Surface Reflectance imagery files in GeoTIFF format. These files are not committed to the repository due to their large size (100-500 MB per scene). Users must download Landsat imagery independently from the USGS EarthExplorer (https://earthexplorer.usgs.gov) and place files here.

File Naming Convention

All raw Landsat imagery files must follow the naming convention:

landsat_[SENSOR]_[YEAR]_sr_b[N].tif

Where:
- [SENSOR] is either "tm5" (Landsat 5 Thematic Mapper) or "oli8" (Landsat 8 Operational Land Imager)
- [YEAR] is the acquisition year (1990, 2000, 2010, or 2024)
- [N] is the band number

Example:
landsat_tm5_1990_sr_b1.tif (Landsat 5 TM, 1990, Band 1 - Blue)
landsat_oli8_2024_sr_b5.tif (Landsat 8 OLI, 2024, Band 5 - Near-Infrared)

Required Bands

For each year and sensor, the following reflective bands must be provided:

Landsat 5 TM (1990, 2000, 2010):
- Band 1 (Blue): landsat_tm5_[YEAR]_sr_b1.tif
- Band 2 (Green): landsat_tm5_[YEAR]_sr_b2.tif
- Band 3 (Red): landsat_tm5_[YEAR]_sr_b3.tif
- Band 4 (Near-Infrared): landsat_tm5_[YEAR]_sr_b4.tif
- Band 5 (SWIR1): landsat_tm5_[YEAR]_sr_b5.tif
- Band 7 (SWIR2): landsat_tm5_[YEAR]_sr_b7.tif

Landsat 8 OLI (2024):
- Band 2 (Blue): landsat_oli8_2024_sr_b2.tif
- Band 3 (Green): landsat_oli8_2024_sr_b3.tif
- Band 4 (Red): landsat_oli8_2024_sr_b4.tif
- Band 5 (Near-Infrared): landsat_oli8_2024_sr_b5.tif
- Band 6 (SWIR1): landsat_oli8_2024_sr_b6.tif
- Band 7 (SWIR2): landsat_oli8_2024_sr_b7.tif

Data Specifications

All imagery must meet the following specifications:

- Projection: UTM Zone 39 North, WGS84 datum
- Resolution: 30 meters per pixel
- Radiometry: Surface Reflectance (SR), scaled to 0-10,000 representing 0-100 percent reflectance
- Format: GeoTIFF (.tif)
- Data Type: Unsigned 16-bit integer (uint16)

aoi/

Area of Interest vector data defining Karaj Municipality boundary. Contains:

karaj_municipality.shp: Shapefile polygon boundary of Karaj Municipality
karaj_municipality.shx: Shapefile index
karaj_municipality.dbf: Shapefile attribute database
karaj_municipality.prj: Spatial reference information

The AOI is used to subset input imagery to the study area, reducing file sizes and computation time.

roi/

Regions of Interest vector data for supervised classification training. Contains:

training_regions.shp: Polygons delineating training regions for each land cover class
training_regions.shx: Shapefile index
training_regions.dbf: Attribute database with class labels
training_regions.prj: Spatial reference information

Training regions should be delineated on high-resolution reference imagery and distributed across the study area to capture spectral variability within each class. Each region must have an attribute field "class" with values 1-5 corresponding to the land cover classes defined in configs/class_schema.yaml.

Obtaining Data
---------------

Landsat Imagery

1. Visit USGS EarthExplorer: https://earthexplorer.usgs.gov
2. Define search area: Enter Karaj Municipality bounding coordinates or upload AOI shapefile
3. Select data: Landsat 5-8 Collection 2 Level-2 Surface Reflectance
4. Filter: Set date ranges: 1990, 2000, 2010, 2024 (June-August to match seasonal conditions)
5. Sort by cloud cover: Select scenes with <10 percent cloud cover
6. Download: Download individual bands or band collections
7. Organize: Rename files to match the naming convention above
8. Place files: Copy all .tif files to data/raw/

AOI and ROI Data

AOI and ROI vector data can be prepared using ArcGIS, QGIS, or other GIS software. The AOI should encompass Karaj Municipality boundaries. ROIs should be delineated on reference imagery (e.g., Google Earth imagery, high-resolution Sentinel-2, or USGS orthoimagery) with representative samples of each land cover class.

Data Quality

Before running the pipeline, verify that all data files are:

- Named exactly according to conventions (case-sensitive)
- Present in the correct directories
- Complete (all six bands for each date)
- In the correct projection (UTM Zone 39N)
- Free of data corruption (validate file sizes and checksums)

Run the validation script to confirm data readiness:

python scripts/validate_inputs.py

Data Rights and Attribution

Landsat data is publicly provided by the United States Geological Survey. Please cite:

USGS Earth Explorer. https://earthexplorer.usgs.gov

When publishing results derived from this data, acknowledge USGS and Landsat in your citations and methods.
