Preprocessing Methodology
=========================

Objective and Overview
----------------------

Preprocessing transforms raw Landsat Surface Reflectance imagery into a standardized, analysis-ready format suitable for spectral index calculation and classification. The preprocessing pipeline accomplishes four primary objectives: band subsetting to retain only reflective bands, wavelength metadata injection to enable spectral calculations, geometric validation to ensure spatial consistency, and quality assessment masking to exclude corrupted or ambiguous pixels.

Band Subsetting
---------------

Rationale for Band Selection

Landsat imagery contains six reflective bands and one thermal band. For this analysis, only the six reflective bands are retained:

Landsat 5 TM: Bands 1 (Blue), 2 (Green), 3 (Red), 4 (Near-Infrared), 5 (SWIR1), and 7 (SWIR2).
Landsat 8 OLI: Bands 2 (Blue), 3 (Green), 4 (Red), 5 (Near-Infrared), 6 (SWIR1), and 7 (SWIR2).

Bands are reordered and renamed to a common scheme (Band 1 through Band 6) to allow unified processing across sensors. Thermal bands are excluded to simplify processing and to avoid the additional calibration required for surface temperature retrieval.

Procedure

The ENVI batch pipeline reads the band_mapping.yaml configuration file to identify which input files correspond to which bands. The ENVI SUBSET task is invoked to extract only the specified bands, creating a subset image file for each date. Subset imagery is stored as temporary files in the outputs/ directory with naming convention subset_[YEAR].dat.

Wavelength Metadata Injection
-----------------------------

Why Wavelength Metadata Matters

Spectral indices such as NDVI are computed using specific band wavelengths. For example, NDVI uses the Near-Infrared and Red bands. Proper index calculation requires that the computational software knows the central wavelengths of each band. The Landsat TM and OLI sensors have slightly different band definitions and central wavelengths.

To ensure reproducibility and scientific rigor, central wavelengths are explicitly embedded in imagery headers at the preprocessing stage. This approach guarantees that any subsequent analysis, whether performed in ENVI, Python, or other software, uses identical wavelength definitions.

Implementation

After band subsetting, the ENVI WRITE_ENVI_HEADER task is used to write file headers that include central wavelength and bandwidth information for each band. Wavelengths are read from band_mapping.yaml and are specified in micrometers:

For Landsat 5 TM:
Band 1 (Blue): 0.485 micrometers
Band 2 (Green): 0.560 micrometers
Band 3 (Red): 0.660 micrometers
Band 4 (Near-Infrared): 0.830 micrometers
Band 5 (SWIR1): 1.650 micrometers
Band 6 (SWIR2): 2.215 micrometers

For Landsat 8 OLI:
Band 1 (Blue): 0.482 micrometers
Band 2 (Green): 0.562 micrometers
Band 3 (Red): 0.655 micrometers
Band 4 (Near-Infrared): 0.865 micrometers
Band 5 (SWIR1): 1.609 micrometers
Band 6 (SWIR2): 2.201 micrometers

This metadata injection step ensures that index calculations are traceable and reproducible, allowing other researchers to verify wavelength assumptions.

Geometric Consistency Check
---------------------------

Verification of Spatial Reference

All input imagery is verified to be in UTM Zone 39 North, WGS84 datum. The ENVI batch pipeline checks the spatial reference information in each input file and reports any discrepancies. If imagery is in a different projection, it is reprojected to UTM Zone 39N using nearest-neighbor resampling for categorical data or bilinear interpolation for continuous data.

Alignment Verification

For multi-temporal analysis, all imagery must be precisely co-registered so that pixels at the same UTM coordinates represent the same ground location across all dates. Prior to classification, imagery from different dates is checked for geometric alignment by computing overlap statistics. Any misalignment exceeding one pixel (30 meters) is flagged for manual inspection and correction.

Quality Assessment and Masking Strategy
---------------------------------------

Source of Quality Information

Landsat Surface Reflectance products include a Quality Assessment (QA) band for each scene, a pixel-level mask indicating data quality. The QA band encodes information about cloud presence, cloud shadow, snow, water presence, vegetation, built-up areas, and other features. Cloud and shadow pixels are identified and masked prior to analysis.

Masking Approach

Pixels flagged as cloud or cloud shadow in the QA band are excluded from classification and index calculation. These pixels are assigned a null or no-data value (typically -9999) in output indices and classifications. Vegetation and water pixels identified in the QA band are flagged as potentially useful information but are not automatically excluded, allowing the classification algorithm to use spectral properties for independent determination.

Conceptual Rationale

QA-based masking removes pixels whose reflectance values are unreliable due to atmospheric obscuration. Retaining these pixels would introduce noise into classifications and indices. By masking clouds and shadows, preprocessing ensures that only pixels with high-confidence reflectance measurements are used in subsequent analysis.

Masking Implementation

The ENVI batch pipeline reads the QA band and creates a binary mask file with value 1 (valid) where reflectance is reliable and 0 (masked) where clouds or shadows are present. This mask is applied to all spectral bands and indices generated subsequently. Statistics (area, pixel counts) exclude masked pixels.

Radiometric Consistency
-----------------------

Surface Reflectance Scaling

Landsat Surface Reflectance products are scaled to integer values ranging from 0 to 10,000, representing 0 to 100 percent reflectance in units of 0.01 percent reflectance. This integer scaling preserves radiometric precision while reducing file sizes and enabling efficient integer arithmetic in processing software.

All downstream processing (spectral indices, classification, change detection) operates on these scaled integer values without conversion to decimal reflectance, as the relative relationships among bands are preserved by integer scaling. Output indices range from -10,000 to 10,000, representing -1.0 to 1.0 in normalized form.

No Radiometric Normalization Across Sensors

Landsat 5 TM and Landsat 8 OLI have slightly different radiometric characteristics, including sensor noise profiles, calibration, and spectral response functions. This analysis does not apply cross-sensor radiometric normalization, instead accepting that 1990-2010 imagery and 2024 imagery represent different physical sensors with consistent but not identical radiometric properties.

This approach is scientifically defensible because indices such as NDVI are normalized differences that reduce sensor-specific calibration errors. Index values from TM and OLI imagery are comparable for classification and trend detection despite sensor differences. Sensitivity analyses comparing TM and OLI imagery from overlapping dates (2013-2014) have demonstrated acceptable consistency for land cover classification.

File Naming and Organization
-----------------------------

Preprocessed imagery is organized in the outputs/ directory with the following structure:

outputs/[YEAR]/
outputs/1990/
outputs/2000/
outputs/2010/
outputs/2024/

Within each year folder, preprocessed files are named:

subset_[YEAR].dat and subset_[YEAR].hdr: Band-subset imagery with wavelength metadata.

IntermediateENVI products (.dat, .hdr files) are temporary and are not committed to the repository. Final PNG outputs derived from these products are committed and distributed via the documentation website.

Quality Control Procedures
--------------------------

Data Integrity Checks

After preprocessing, each raster is validated for:

1. Correct dimensions matching expected AOI extents.
2. Correct number of bands (6 reflective bands).
3. Correct data type (unsigned 16-bit integer for reflectance, signed 16-bit for indices).
4. Absence of unexpected null values outside designated QA-masked regions.
5. Reasonable reflectance ranges (0 to 10,000) for input imagery.

These checks are automated and logged in the run_log.json file.

Visual Inspection

Truecolor composite images (Red-Green-Blue) are generated from Band 3 (Red), Band 2 (Green), and Band 1 (Blue) for each date and visually inspected to verify that preprocessing has preserved expected landscape features and that no unexpected artifacts are present.

Before and After Comparison

Statistical summaries (minimum, maximum, mean, standard deviation) of reflectance values are computed for each band before and after preprocessing. Large unexplained changes in statistics indicate potential preprocessing errors and trigger manual review.

Documentation and Logging
--------------------------

All preprocessing steps are logged in machine-readable JSON format in outputs/run_log.json with the following information:

Step name and timestamp
Input file paths
Output file paths
Parameters used (band indices, wavelengths, QA thresholds)
Status (success or error)
File sizes and statistics

This logging enables complete traceability of preprocessing decisions and supports reproducibility by recording all parameter values used.
