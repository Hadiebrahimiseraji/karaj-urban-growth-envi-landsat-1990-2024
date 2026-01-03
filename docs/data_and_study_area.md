Data and Study Area
===================

Study Area Definition
---------------------

The study area is Karaj Municipality, located in Alborz Province, northwestern Iran. The municipality is situated at approximately 35.8 degrees North latitude and 51.0 degrees East longitude, at the base of the Alborz Mountains on the southern flank of the Caspian Depression. The municipality encompasses approximately 393 square kilometers and functions as a major urban center for the region and a satellite city for the Tehran metropolitan area.

Geographic and Climatic Setting

Karaj is characterized by a semi-arid continental climate with cold winters and warm summers. Average annual precipitation ranges from 200 to 300 millimeters, concentrated in late autumn, winter, and early spring. Summers are dry. The region is historically dependent on groundwater and surface water resources from the Alborz Mountains for irrigation and municipal use.

Pre-urbanization landscapes in the Karaj area consisted of mixed agricultural fields, scattered forests on mountain slopes, sparse grasslands, and shallow water bodies in lowland areas. Since the 1980s, the municipality has experienced rapid urbanization driven by population migration from rural areas, industrial development, and regional economic growth.

Coordinate System and Spatial Reference
---------------------------------------

All imagery is projected to Universal Transverse Mercator (UTM) Zone 39 North, World Geodetic System 1984 (WGS84) datum. This projection is standard for remote sensing work in the Middle East region and minimizes distortion for the study area. Imagery coordinates should be referenced as UTM eastings and northings in meters.

The bounding box of the study area in UTM Zone 39N is approximately:

Western boundary: 366,000 meters East
Eastern boundary: 378,000 meters East
Southern boundary: 3,965,000 meters North
Northern boundary: 3,980,000 meters North

All output rasters conform to this extent and coordinate system.

Landsat Data Description and Rationale
---------------------------------------

Source and Availability

Landsat data is provided free of charge by the United States Geological Survey through EarthExplorer (https://earthexplorer.usgs.gov). Data is available in Surface Reflectance (SR) format, which has been radiometrically processed to remove atmospheric effects and scaled to values between 0 and 10,000 (representing 0 to 100 percent reflectance). Surface Reflectance products are preferred over Top-of-Atmosphere Reflectance for land cover classification because they represent intrinsic land surface properties after atmospheric correction.

Sensor Specifications

For temporal snapshots 1990, 2000, and 2010, Landsat 5 Thematic Mapper (TM) data is used. The TM sensor has six reflective bands and one thermal band:

Band 1: Blue (0.45 to 0.52 micrometers, central 0.485 micrometers)
Band 2: Green (0.52 to 0.60 micrometers, central 0.560 micrometers)
Band 3: Red (0.63 to 0.69 micrometers, central 0.660 micrometers)
Band 4: Near-Infrared (0.76 to 0.90 micrometers, central 0.830 micrometers)
Band 5: Shortwave-Infrared 1 (1.55 to 1.75 micrometers, central 1.650 micrometers)
Band 7: Shortwave-Infrared 2 (2.08 to 2.35 micrometers, central 2.215 micrometers)

For the 2024 snapshot, Landsat 8 Operational Land Imager (OLI) data is used. The OLI sensor has improved spectral and radiometric characteristics but preserves general compatibility with TM:

Band 2: Blue (0.43 to 0.45 micrometers, central 0.482 micrometers)
Band 3: Green (0.53 to 0.59 micrometers, central 0.562 micrometers)
Band 4: Red (0.64 to 0.67 micrometers, central 0.655 micrometers)
Band 5: Near-Infrared (0.85 to 0.88 micrometers, central 0.865 micrometers)
Band 6: Shortwave-Infrared 1 (1.57 to 1.65 micrometers, central 1.609 micrometers)
Band 7: Shortwave-Infrared 2 (2.11 to 2.29 micrometers, central 2.201 micrometers)

Spatial resolution for all reflective bands is 30 meters by 30 meters, translating to a ground area of 900 square meters per pixel.

Rationale for Surface Reflectance and Spectral Band Selection

Surface Reflectance products are employed because land cover classification depends on the intrinsic spectral properties of land surface materials, not atmospheric conditions varying with humidity, aerosols, and viewing geometry. SR products normalize these variations, improving classification consistency across dates and atmospheric conditions.

The reflective bands (Bands 1, 2, 3, 4, 5, and 7 for Landsat 5; Bands 2, 3, 4, 5, 6, and 7 for Landsat 8) are selected because they provide comprehensive spectral coverage from visible through shortwave-infrared wavelengths. Thermal bands are excluded to avoid the complexity of surface temperature retrieval, which requires additional calibration and validation data beyond the scope of this analysis.

Data Acquisition Dates
----------------------

Temporally representative Landsat scenes for each epoch are selected as follows:

Epoch 1990: Landsat 5 TM acquisition from summer 1990 (July or August), selected to represent vegetation at peak seasonal greenness and to minimize cloud and snow cover.

Epoch 2000: Landsat 5 TM acquisition from summer 2000, similarly selected for phenological consistency with 1990.

Epoch 2010: Landsat 5 TM acquisition from summer 2010, maintaining consistency with prior decades.

Epoch 2024: Landsat 8 OLI acquisition from summer 2024, selected to match seasonal conditions of prior epochs.

Summer acquisitions are preferred because they maximize vegetation vigor, minimize snow cover on mountain areas, and reduce cloud obscuration in the semi-arid environment. This consistency in acquisition timing reduces confounding seasonal effects.

Data Organization and Naming Conventions
-----------------------------------------

Raw Landsat Surface Reflectance data is downloaded from EarthExplorer in GeoTIFF format and organized in the data/raw/ directory according to the following naming convention:

landsat_[SENSOR]_[YEAR]_sr_b[N].tif

Where [SENSOR] is either "tm5" or "oli8", [YEAR] is the acquisition year (1990, 2000, 2010, or 2024), and [N] is the band number. All reflective bands for a given date must be present in data/raw/ for processing to proceed.

Example file names:

landsat_tm5_1990_sr_b1.tif
landsat_tm5_1990_sr_b2.tif
landsat_tm5_1990_sr_b3.tif
landsat_tm5_1990_sr_b4.tif
landsat_tm5_1990_sr_b5.tif
landsat_tm5_1990_sr_b7.tif
landsat_oli8_2024_sr_b2.tif
landsat_oli8_2024_sr_b3.tif
landsat_oli8_2024_sr_b4.tif
landsat_oli8_2024_sr_b5.tif
landsat_oli8_2024_sr_b6.tif
landsat_oli8_2024_sr_b7.tif

All file names are case-sensitive and must match the configuration in pipeline_config.yaml exactly.

Auxiliary Data: Area of Interest and Regions of Interest
---------------------------------------------------------

Area of Interest (AOI)

The Area of Interest is defined as a polygon boundary encompassing Karaj Municipality. This AOI is used to subset input imagery to the relevant geographic area, reducing file sizes and computation time. The AOI is stored as a shapefile or GeoJSON in data/aoi/ and is referenced in the pipeline configuration.

Regions of Interest (ROI) for Training

Supervised classification requires training data in the form of Regions of Interest, wherein pixels are manually or semi-automatically labeled with their known land cover class. These regions are delineated on high-resolution imagery or via field survey and stored in data/roi/ as shapefiles, with class attribute fields. Best practice involves delineating 20 to 50 distinct training regions per class, scattered across the study area, to capture spectral variability within each class.

For this research, ROIs are delineated on the 2024 Landsat 8 imagery and then applied to earlier dates, with manual verification to ensure consistency. This approach maintains class definitions constant across time, improving change detection reliability.

Metadata and Documentation
--------------------------

Metadata for all imagery, including acquisition date, sensor, radiometric resolution (surface reflectance in 0.0001 SR units), and spatial reference, is recorded in configuration files and archived with outputs for full provenance tracking. This enables future researchers to assess data quality and conduct sensitivity analyses regarding metadata assumptions.
