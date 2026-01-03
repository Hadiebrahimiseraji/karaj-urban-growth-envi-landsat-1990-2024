Karaj Urban Growth and Environmental Impacts Analysis
======================================================

Executive Summary
-----------------

Karaj Municipality has experienced rapid urbanization over the past three decades, transforming from a predominantly agricultural and natural landscape into a major metropolitan center in northwestern Iran. This repository provides a comprehensive, reproducible analysis of land use and land cover change in Karaj from 1990 to 2024, combining multispectral Landsat satellite imagery with automated spectral analysis, machine learning classification, and temporal change detection.

The research quantifies urbanization patterns, vegetation loss, water body changes, and soil moisture dynamics through the derivation of normalized spectral indices (NDVI, NDBI, NDWI) and supervised classification of five land cover categories. All processing is driven by configuration files, ensuring transparency and replicability for peer review, policy application, and comparative studies in other regions.

Core Research Questions
-----------------------

This investigation addresses the following spatial and temporal research questions:

1. What is the spatial extent and rate of urban expansion in Karaj over the 34-year analysis period?
2. How have vegetation index values and vegetation extent changed in response to urbanization?
3. What trends are observable in water and soil moisture indices as land conversion progresses?
4. Which dominant land cover transitions characterize the landscape, and what are their areal magnitudes in square kilometers?
5. To what degree can automated multispectral indices reliably detect long-term environmental change in a semi-arid urban setting?

Analytical Workflow
-------------------

The complete pipeline proceeds through the following sequential steps:

Step One: Data Assembly and Validation

Landsat reflective bands for 1990, 2000, 2010, and 2024 are placed in data/raw/ and validated against configuration metadata. The validate_inputs.py script confirms file presence and structure.

Step Two: Reflective Band Subsetting

The ENVI batch pipeline reads band mapping configuration and selects reflective bands appropriate for each sensor (Landsat 5 TM or Landsat 8 OLI). Thermal bands are excluded to avoid complexity in surface temperature retrieval.

Step Three: Wavelength Metadata Injection

Central wavelengths and bandwidth information are programmatically embedded into imagery headers, ensuring all spectral calculations remain scientifically traceable and conform to radiometric standards.

Step Four: Spectral Index Calculation

Three standardized indices are calculated: Normalized Difference Vegetation Index (NDVI) quantifies vegetation vigor; Normalized Difference Built-up Index (NDBI) isolates urban and built surfaces; Normalized Difference Water Index (NDWI) identifies water bodies and soil moisture. Index values range from -1 to 1, with interpretable thresholds for environmental classification.

Step Five: Supervised Classification

A Support Vector Machine classifier is trained on manually delineated regions of interest for five land cover classes: Water, Urban, Agriculture, Forest, and Bare Soil. Class membership is assigned pixel-by-pixel to generate categorical land use and land cover maps.

Step Six: Change Detection

Post-classification comparison between 1990 and 2024 generates a transition matrix showing area changes among all class pairs. Index differencing quantifies temporal trends in spectral properties.

Step Seven: Statistics Export

Per-class areas and percentages are tabulated and exported to CSV format for statistical analysis, charting, and reporting.

Step Eight: Documentation Publishing

Processed PNG outputs are published to the documentation website, and a complete MkDocs site is deployed to GitHub Pages.

Technical Architecture
----------------------

The pipeline is implemented as a Windows-native system using Python 3.8 and ENVI 5.6 with the Task Engine module (envipyengine). All processing parameters are externalized to YAML configuration files in the configs/ directory, enabling modification without code editing. The approach is modular, allowing individual steps to be executed independently or as a complete chain.

Key Design Principles

Configuration-Driven Execution: All file paths, parameter values, spectral index definitions, class schemas, and processing options are specified in YAML files rather than hard-coded into scripts. This ensures portability and facilitates comparison across different geographic regions or temporal periods.

Deterministic Reproducibility: Identical input imagery and configuration files produce identical outputs, a property essential for peer review and method replication.

Graceful Degradation: Scripts detect the absence of optional dependencies (such as envipyengine in non-Windows or non-ENVI environments) and continue with informative fallback behavior, allowing documentation build and validation checks to proceed even in constrained computing environments.

Transparent Logging: All processing steps are logged in machine-readable JSON format with timestamps, input file references, and output file paths for complete provenance tracking.

Study Area and Temporal Scope
------------------------------

The study area is defined as Karaj Municipality, located in Alborz Province, northwestern Iran. The municipality encompasses an area of approximately 393 square kilometers and is situated at the foothills of the Alborz Mountains. The region is characterized by semi-arid climate, significant groundwater resources, and dynamic land use patterns driven by agricultural conversion and urban sprawl.

Analysis covers four temporal snapshots: 1990 (baseline), 2000 (decade one), 2010 (decade two), and 2024 (current). This sampling strategy balances temporal resolution with data availability and computational efficiency.

Outputs and Deliverables
------------------------

Processed outputs include:

Raster Imagery: True-color composite images, spectral index rasters, and land cover classifications in GeoTIFF format for archival and further analysis.

PNG Visualizations: Simplified PNG versions for web display, organized by year and product type in docs/assets/outputs/.

Statistical Tables: CSV files containing per-class areas, percentages, and transition matrices for statistical software such as SPSS or R.

Documentation Website: A complete MkDocs Material site deployable to GitHub Pages with interactive navigation, embedded images, and full methodology description.

Machine-Readable Logs: JSON-formatted execution logs and metadata files for automated quality assurance and reproducibility verification.

For Additional Information
--------------------------

Detailed sections on research background, data specifications, preprocessing methodology, spectral index interpretation, classification procedures, change detection strategies, quality assurance protocols, reproducibility procedures, and limitations are provided in the documentation pages. Complete references are available in the References section.
