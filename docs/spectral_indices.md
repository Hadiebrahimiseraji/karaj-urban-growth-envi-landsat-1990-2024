Spectral Indices and Their Interpretation
===========================================

Overview of Spectral Indices
----------------------------

Spectral indices are mathematical combinations of reflectance values from multiple bands, designed to highlight specific environmental features. Each index normalizes reflectance differences to produce output values ranging from -1.0 to 1.0 (or -10,000 to 10,000 in integer-scaled form), with intuitive interpretation: positive values indicate presence of the target feature, negative values indicate absence, and zero indicates neutral conditions.

This analysis employs three standardized indices: Normalized Difference Vegetation Index (NDVI) for vegetation assessment, Normalized Difference Built-up Index (NDBI) for urban feature detection, and Normalized Difference Water Index (NDWI) for water and soil moisture assessment. These indices are derived automatically by the ENVI batch pipeline from the preprocessed multispectral imagery.

Normalized Difference Vegetation Index (NDVI)
-----------------------------------------------

Definition and Calculation

The Normalized Difference Vegetation Index is calculated as:

NDVI = (NIR - Red) / (NIR + Red)

Where NIR is the near-infrared reflectance (Landsat Band 4 for TM, Band 5 for OLI) and Red is the red-wavelength reflectance (Band 3 for TM, Band 4 for OLI).

Physical Rationale

Healthy green vegetation exhibits strong reflectance in the near-infrared (0.7 to 1.0 micrometers) due to the structure of leaf cells, which scatter NIR photons. In contrast, vegetation absorbs strongly in the red wavelength (0.6 to 0.7 micrometers) for photosynthesis. Thus, the difference (NIR - Red) is large for vegetation and small for non-vegetated surfaces such as water, soil, and urban materials.

Normalization by (NIR + Red) provides scale-invariance, reducing the influence of overall illumination brightness and making NDVI comparable across different atmospheric conditions and acquisition dates. This normalization is critical for multi-temporal analysis.

Interpretation and Thresholds

NDVI values typically range from -0.2 to 0.9 across natural landscapes:

NDVI < 0.0: Water bodies and water-adjacent areas. Negative values indicate stronger red absorption than NIR reflectance, characteristic of water.

0.0 to 0.3: Sparse vegetation, bare soil, and urban materials. These surfaces lack the strong NIR reflectance signature of vegetation.

0.3 to 0.6: Moderate vegetation, including grasslands, shrublands, and partially vegetated areas. NDVI in this range indicates some vegetation presence but not dense canopy.

0.6 to 0.9: Dense vegetation, including forests and irrigated croplands. High NDVI values indicate strong vegetation vigor and biomass.

Approximately 0.4 to 0.5 serves as a practical threshold between vegetated and non-vegetated pixels; pixels with NDVI greater than 0.45 are typically classified as vegetation.

Expected Trends in Karaj

From 1990 to 2024, NDVI in the Karaj region is expected to decline in areas converted from agriculture or forest to urban use. Irrigated agricultural areas should maintain moderate to high NDVI. Newly urbanized areas will exhibit low or negative NDVI due to asphalt, concrete, and other impervious surfaces. Parks, green roofs, and tree-lined streets may retain localized high NDVI pixels.

Application in This Research

NDVI is used to identify and track vegetation extent, to distinguish vegetated from non-vegetated areas for classification purposes, and to quantify temporal trends in vegetation vigor over the 34-year period.

Normalized Difference Built-up Index (NDBI)
---------------------------------------------

Definition and Calculation

The Normalized Difference Built-up Index is calculated as:

NDBI = (SWIR1 - NIR) / (SWIR1 + NIR)

Where SWIR1 is shortwave-infrared reflectance (Landsat Band 5 for TM, Band 6 for OLI) and NIR is near-infrared reflectance (Band 4 for TM, Band 5 for OLI).

Physical Rationale

Urban materials including concrete, asphalt, brick, and metal roofing exhibit relatively high reflectance in the shortwave-infrared (1.55 to 1.75 micrometers) compared to near-infrared. In contrast, vegetation absorbs strongly in SWIR due to leaf water content. Thus, the difference (SWIR1 - NIR) is positive for built-up areas and negative for vegetation.

The NDBI index isolates built-up surfaces and urban areas, complementing NDVI by providing an urban-specific signal.

Interpretation and Thresholds

NDBI values typically range from -0.5 to 0.5 across mixed landscapes:

NDBI < -0.2: Dense vegetation and agricultural areas. Strong leaf water absorption in SWIR produces negative values.

-0.2 to 0.1: Mixed urban-vegetation areas, including sparse urban development with tree cover or irrigated fields.

0.1 to 0.4: Developed urban areas with high density of buildings and paved surfaces.

NDBI > 0.4: Highly developed urban areas, industrial zones, and barren areas with minimal vegetation.

Approximately 0.05 to 0.10 serves as a practical threshold for distinguishing urban from non-urban areas, though this threshold varies with local building materials and urban density.

Expected Trends in Karaj

NDBI is expected to increase in areas undergoing urbanization, with the greatest increases in newly developed residential and commercial zones. Agricultural and forested areas should retain negative NDBI values throughout the analysis period.

Application in This Research

NDBI is used to detect and map urban expansion, to distinguish urban from agricultural and natural land cover, and to quantify the areal extent of urbanization changes over time.

Normalized Difference Water Index (NDWI)
------------------------------------------

Definition and Calculation

The Normalized Difference Water Index is calculated as:

NDWI = (NIR - SWIR1) / (NIR + SWIR1)

Where NIR is near-infrared reflectance (Band 4 for TM, Band 5 for OLI) and SWIR1 is shortwave-infrared reflectance (Band 5 for TM, Band 6 for OLI).

Physical Rationale

Water strongly absorbs electromagnetic radiation across shortwave-infrared wavelengths and absorbs somewhat less strongly in near-infrared. Vegetation and moist soil exhibit higher NIR reflectance than water. Thus, NDWI is high for water bodies and vegetated areas with high moisture content, and low for dry soil and urban materials.

NDWI is particularly useful in semi-arid environments for identifying moisture-stressed vegetation and detecting changes in water availability and soil moisture.

Interpretation and Thresholds

NDWI values typically range from -0.5 to 0.6 in natural and semi-arid landscapes:

NDWI > 0.3: Open water bodies and very moist vegetation. High NDWI indicates strong water absorption in SWIR.

0.0 to 0.3: Moderately moist vegetation and irrigated fields. NDWI in this range indicates adequate moisture for vegetation growth.

-0.3 to 0.0: Dry vegetation and bare soil. NDWI values approach zero or become slightly negative as moisture stress increases.

NDWI < -0.3: Very dry bare soil and impervious urban surfaces. Negative values indicate negligible moisture content.

Approximately 0.0 to 0.1 serves as a practical threshold for identifying water-related features and moisture-rich areas.

Expected Trends in Karaj

NDWI in the Karaj region is expected to correlate with irrigation patterns, with high values in irrigated agricultural areas and declining values as agriculture is replaced by urban use. Seasonal variations in water availability will influence NDWI even in stable land cover areas. Long-term NDWI trends may reflect changes in groundwater levels and regional water availability.

Application in This Research

NDWI is used to identify water bodies and irrigated agricultural areas, to track changes in moisture availability, and to assess environmental impacts of urbanization on water resources and vegetation moisture stress.

Index Calculation and Output
-----------------------------

Automated Calculation

All three indices are calculated automatically within the ENVI batch pipeline using the ENVI MATH task, which applies the algebraic formulas to the preprocessed imagery. Output indices are stored as single-band rasters with data type signed 16-bit integer, representing values from -10,000 to 10,000.

Output File Organization

Index rasters are saved in outputs/[YEAR]/ with filenames:

ndvi_[YEAR].dat and ndvi_[YEAR].hdr
ndbi_[YEAR].dat and ndbi_[YEAR].hdr
ndwi_[YEAR].dat and ndwi_[YEAR].hdr

Index values are integer-scaled (multiplied by 10,000) to preserve precision in integer format. Software reading these indices should divide by 10,000 to recover decimal values in the range -1.0 to 1.0.

Statistical Summaries

After index calculation, minimum, maximum, mean, and standard deviation statistics are computed for each index raster. These statistics are recorded in outputs/run_log.json and are used for quality control and interpretation.

Index-Specific Quality Assurance
-------------------------------

Value Range Checks

All index output rasters are checked to ensure that values remain within expected ranges (-10,000 to 10,000). Pixels with out-of-range values indicate calculation errors or data corruption and are flagged for investigation.

Masking Consistency

Pixels masked as cloud or shadow in the preprocessing stage are assigned no-data values in all indices. Statistics exclude masked pixels to prevent distortion of trends.

Index Correlation Analysis

Correlation between indices is examined to identify potential data quality issues. For example, very high positive correlation between NDVI and NDBI suggests possible calculation or data errors, as vegetation-rich areas should have high NDVI and low NDBI.

Multi-Temporal Consistency

Indices computed for the same land cover class in different years should exhibit similar values if preprocessing and calculation are consistent. Large unexplained changes in index values for stable land cover areas suggest systematic errors.

Interpretation Notes for Karaj Region
-------------------------------------

Semi-Arid Conditions

Karaj's semi-arid climate (200–300 mm annual precipitation) means that vegetation is dependent on irrigation in agricultural areas and on groundwater availability in natural areas. Index values and temporal trends must be interpreted in this hydrological context.

Seasonal Considerations

All imagery is acquired in summer (July or August) to standardize seasonal conditions. However, residual seasonal variability in vegetation vigor, soil moisture, and water availability will influence index values.

Cross-Sensor Differences

Landsat 5 TM and Landsat 8 OLI have slightly different spectral response functions and calibration. Index values computed from the two sensors may differ by 5 to 10 percent for the same surface. This difference is acceptable for classification and trend detection but should be recognized when comparing absolute values across the 1990–2010 and 2024 periods.
