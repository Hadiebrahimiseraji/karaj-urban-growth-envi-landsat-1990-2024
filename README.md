Karaj Urban Growth and Environmental Impacts (1990–2024) Using ENVI and Landsat
=====================================================================================

Overview
--------

This repository presents a reproducible analytical pipeline for quantifying land use and land cover change in Karaj Municipality, Iran, over a 34-year period using Landsat multispectral imagery and ENVI 5.6. The research combines spectral index analysis, supervised classification, and temporal change detection to address the following research questions:

1. What is the spatial extent and rate of urban expansion in Karaj over three decades?
2. How has vegetation extent and density changed, particularly in response to urbanization?
3. What are the trends in water and soil moisture availability as a function of land conversion?
4. Which land cover transitions dominate the landscape, and what are their area magnitudes?
5. Can automated spectral indices reliably detect multi-decadal change signals in a semi-arid urban region?

This work demonstrates the practical application of open-source configuration-driven workflows for replicable change analysis in support of urban planning, environmental assessment, and climate adaptation research.

Methodology Overview
--------------------

The pipeline executes the following integrated workflow:

1. Reflective band selection: Landsat 5 Thematic Mapper and Landsat 8 Operational Land Imager bands are subset to retain multispectral information across visible, near-infrared, and shortwave-infrared domains.

2. Wavelength metadata handling: Central wavelengths and bandwidth information are injected into imagery headers to ensure spectral calculations remain traceable and reproducible.

3. Spectral indices calculation: Normalized Difference Vegetation Index (NDVI), Normalized Difference Built-up Index (NDBI), and Normalized Difference Water Index (NDWI) are derived to isolate environmental features.

4. Supervised land use and land cover classification: Training regions of interest are delineated for five land cover classes (Water, Urban, Agriculture, Forest, Bare Soil), and Support Vector Machine classification is applied consistently across all temporal snapshots.

5. Change detection analysis: Post-classification comparison and index differencing quantify area transitions and temporal trends.

6. Statistics export: Per-class area and percentage metrics are exported to CSV format for statistical analysis and reporting.

7. Documentation and reporting: Analysis outputs are automatically published to a MkDocs Material site suitable for GitHub Pages hosting.

Running the Pipeline on Windows
--------------------------------

This project is designed for Windows systems running Python 3.8 and ENVI 5.6. The pipeline is entirely configuration-driven; all parameters are externalized to YAML configuration files in the configs/ directory.

Prerequisite Installation

1. Install Python 3.8 from python.org. During installation, ensure the option to add Python to the system PATH is selected.

2. Install ENVI 5.6 and ensure it includes the ENVI Task Engine. Verify that the envipyengine module is accessible from the Python environment.

3. From the repository root, install Python dependencies:

   python -m pip install -r requirements.txt

Running the Complete Pipeline

1. Open PowerShell and navigate to the repository root directory.

2. Execute the primary orchestration script:

   powershell -ExecutionPolicy Bypass -File scripts/run_all.ps1

This command executes the following steps in sequence:

   A. Validates that all input data files referenced in pipeline_config.yaml exist in data/raw.
   B. Invokes the ENVI batch pipeline to process all imagery, generate indices, classify land cover, detect change, and produce PNG outputs.
   C. Publishes PNG outputs from outputs/ into docs/assets/outputs/ for website display.
   D. Exports per-class statistics to CSV format for analysis and reporting.

Individual Script Execution

If you need to run individual steps:

python scripts/validate_inputs.py

This validates data input file existence and structure against the configuration.

python scripts/envi_batch_pipeline_png.py

This executes the core ENVI processing pipeline, generating indices, classifications, and change detection outputs.

python scripts/publish_assets.py

This copies finalized PNG outputs to the documentation site assets directory.

python scripts/export_stats_csv.py

This generates a CSV summary table of land cover areas and percentages per year.

Data Handling and Archiving Policy
----------------------------------

Input Imagery

Raw GeoTIFF imagery files from Landsat are stored in data/raw and are not committed to the repository. These files are typically 100–500 MB per scene and should be acquired directly from USGS EarthExplorer or similar sources. File naming follows the configuration in pipeline_config.yaml and is case-sensitive.

Output Imagery

Intermediate ENVI products (files with extensions .dat and .hdr) are generated during processing and are not committed. These are temporary artifacts.

Documentation Assets

Final PNG outputs—such as true-color composites, spectral indices, land cover classifications, and change maps—are committed to docs/assets/outputs/ and organized by year. These lightweight (typically 2–10 MB per year) PNG files are essential for populating the documentation website and are intended for public viewing.

Configuration and Reproducibility
----------------------------------

All processing decisions—input file names, output directory structure, spectral index definitions, class schemas, and change detection parameters—are centralized in the configs/ directory as YAML files. This design ensures reproducibility: different research groups can replicate the exact workflow by obtaining the same source imagery and running the pipeline with the provided configuration.

The four primary configuration files are:

pipeline_config.yaml
The master configuration file defining project-level metadata, input naming conventions, output directory paths, a list of spectral indices to calculate, classification algorithm settings, the temporal range for change detection, and the target directory for publishing assets to the documentation site.

band_mapping.yaml
Specifies Landsat 5 and Landsat 8 reflective band indices and their central wavelengths in micrometers. This enables the pipeline to adapt to different sensors and to correctly label spectral information.

class_schema.yaml
Defines the five land cover classes with unique numeric identifiers, readable names, and semantic descriptions.

export_plan.yaml
Specifies the exact PNG outputs required per year, including standardized filenames such as 01_RGB.png, 02_NDVI.png, 03_NDBI.png, 04_NDWI.png, and 05_LULC.png, as well as change map artifacts.

Configuration-Driven Execution

The Python scripts and ENVI pipeline read these YAML files at runtime and dynamically adapt their behavior. This approach eliminates hard-coded file paths and parameters, making the pipeline portable and maintainable. Users can modify configuration values without editing code.

Deterministic Outputs

When the same input imagery and configuration are applied, the pipeline produces deterministic outputs. This property is critical for peer review and scientific reproducibility. Outputs are dated and logged in machine-readable JSON format to track provenance.

Documentation and GitHub Pages Deployment
------------------------------------------

This repository is configured to deploy a MkDocs Material-based documentation site automatically to GitHub Pages. The site includes:

- An executive summary and workflow overview.
- Research background and motivation.
- Data and study area description.
- Detailed preprocessing methodology.
- Spectral indices definitions and interpretation.
- Classification schema and training strategy.
- Change detection methods and results.
- Quality assurance procedures.
- A visual gallery of outputs organized by year.
- Reproducibility and limitations sections.
- Complete references list.

To enable automatic deployment:

1. Ensure the repository is public.
2. In GitHub repository settings, navigate to Pages.
3. Set the source to GitHub Actions.
4. The workflow .github/workflows/gh-pages.yml will automatically build and deploy the site on each push to main.

The site will be published to https://yourusername.github.io/karaj-urban-growth-envi-landsat-1990-2024.

Citation
--------

To cite this work, please reference the CITATION.cff file:

Hadiebrahimiseraji. Karaj Urban Growth and Environmental Impacts (1990–2024) Using ENVI and Landsat. Version 1.0.0. Retrieved from https://github.com/Hadiebrahimiseraji/karaj-urban-growth-envi-landsat-1990-2024.

A full citation.cff is included in the repository root for direct use in research workflows.

License
-------

This project is licensed under the MIT License. See LICENSE file for details.

Acknowledgments
---------------

This research was conducted as part of an academic thesis investigating long-term urban development and landscape change. ENVI software is provided by L3Harris Geospatial. Landsat data is provided by the United States Geological Survey.

Questions and Support
---------------------

For questions regarding this pipeline, please consult the docs/reproducibility.md file for detailed technical guidance, or review the references in docs/references.md for foundational literature on the methods used.
