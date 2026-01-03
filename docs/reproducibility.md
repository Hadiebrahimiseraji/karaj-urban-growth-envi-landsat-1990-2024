Reproducibility and Workflow Documentation
============================================

Core Principle of Configuration-Driven Processing
--------------------------------------------------

This project is designed around a core principle: all processing decisions and parameter values are externalized to configuration files rather than embedded in code. This design enables perfect reproducibility, transparency, and portability. Any researcher with access to the same source imagery can replicate the entire analysis by running the scripts with the provided configuration files.

Configuration File Hierarchy
----------------------------

Four primary configuration files define the complete analysis workflow:

pipeline_config.yaml: Master configuration file specifying project metadata, input file naming conventions, output directories, spectral indices to calculate, classification parameters, change detection options, and the target directory for publishing assets to the documentation site.

band_mapping.yaml: Defines Landsat 5 TM and Landsat 8 OLI reflective band indices and central wavelengths in micrometers. This enables the pipeline to adapt to different sensors and ensures wavelength metadata is consistent across analysis.

class_schema.yaml: Specifies the five land cover classes with numeric identifiers, readable names, and semantic descriptions. Maintains consistency of class definitions across all processing steps.

export_plan.yaml: Specifies required PNG outputs per year and change period, including standardized filenames such as 01_RGB.png, 02_NDVI.png, through 05_LULC.png, and change map artifacts.

Step-by-Step Workflow Reproduction
-----------------------------------

Input Data Acquisition

1. Obtain Landsat 5 TM Surface Reflectance imagery for years 1990, 2000, and 2010 from USGS EarthExplorer (https://earthexplorer.usgs.gov).
2. Obtain Landsat 8 OLI Surface Reflectance imagery for year 2024 from USGS EarthExplorer.
3. For each date, download all six reflective bands (Blue, Green, Red, Near-Infrared, SWIR1, SWIR2).
4. Organize downloaded files in data/raw/ according to the naming convention specified in pipeline_config.yaml.
5. Verify file names match exactly (case-sensitive).

Delineate Training Data

1. Obtain high-resolution reference imagery (aerial photos, orthoimagery, or high-resolution satellite imagery) for the Karaj study area.
2. For each of five land cover classes (Water, Urban, Agriculture, Forest, Bare Soil), manually delineate 20 to 50 distinct training regions of interest (ROI).
3. Distribute ROIs geographically across the study area to capture spectral variability within each class.
4. Store ROI polygons as vector files (shapefiles or GeoJSON) in data/roi/ with class attribute fields.
5. Verify that ROI coverage is adequate (>5,000 total training pixels distributed across classes).

Step 1: Validate Input Data

Execute the input validation script:

python scripts/validate_inputs.py

This script:

- Reads configuration from configs/pipeline_config.yaml.
- Verifies that all input files referenced in the configuration exist in data/raw/.
- Optionally reads raster metadata from input files and reports dimensions, data types, and extent.
- Writes a validation report to outputs/validation_report.txt.
- Exits with status code 0 if all files are present and valid, or status code 2 if files are missing.

Expected output: validation_report.txt confirming presence of all six Landsat TM bands for each of 1990, 2000, 2010, and all six Landsat OLI bands for 2024.

Step 2: Execute ENVI Batch Pipeline

Execute the ENVI processing pipeline:

python scripts/envi_batch_pipeline_png.py

This script:

- Reads all configuration files from configs/.
- Detects ENVI Task Engine availability (envipyengine module).
- If envipyengine is available:
  - Subsets input imagery to reflective bands only.
  - Injects wavelength metadata into imagery headers.
  - Calculates spectral indices (NDVI, NDBI, NDWI) for each date.
  - Applies QA-based cloud and shadow masking.
  - Generates true-color composite imagery.
  - Trains and applies SVM land cover classification.
  - Performs post-classification change detection.
  - Exports all outputs as both GeoTIFF (for archival) and PNG (for visualization).
- If envipyengine is unavailable:
  - Prints an informative message and exits with status code 3.

Expected output: Processed rasters and PNG images organized in outputs/1990, outputs/2000, outputs/2010, outputs/2024, and outputs/change_1990_2024, plus run_log.json with processing provenance.

Step 3: Publish Assets to Documentation

Copy PNG outputs to the documentation website asset directory:

python scripts/publish_assets.py

This script:

- Reads the export_plan.yaml to identify which PNG files to publish.
- Copies PNG files from outputs/ to docs/assets/outputs/, preserving year folder structure.
- Creates missing directories as needed.
- Writes docs/assets/outputs/publish_log.json summarizing copied files and sizes.

Expected output: PNG files now available in docs/assets/outputs/ for website rendering.

Step 4: Export Statistical Summary

Generate a CSV table suitable for statistical analysis:

python scripts/export_stats_csv.py

This script:

- Reads classification output rasters from outputs/.
- Computes per-class pixel counts for each year.
- Converts pixel counts to area (square kilometers) and percentage of total study area.
- Writes outputs/lulc_stats.csv with one row per year and columns for each class area and percentage.
- If classification outputs are unavailable, writes CSV with empty data fields but correct headers and explanatory messages.

Expected output: lulc_stats.csv suitable for import into spreadsheet software or statistical software (SPSS, R, Python).

Step 5: Build Documentation Website

Generate the MkDocs Material website:

mkdocs build

This command:

- Reads mkdocs.yml configuration.
- Processes all Markdown files in docs/.
- Copies static assets (images in docs/assets/) to the website.
- Generates HTML output in site/ directory.
- Outputs can be previewed locally with mkdocs serve (opens http://localhost:8000).

Expected output: Complete HTML documentation website in site/, ready for deployment.

Parameter Variations and Sensitivity Analysis
-----------------------------------------------

Modifying Processing Parameters

Without changing code, the analysis can be modified by editing YAML configuration files:

1. To change classification algorithm parameters, edit pipeline_config.yaml and modify svm_kernel, svm_c_parameter, etc.
2. To add or remove spectral indices, edit pipeline_config.yaml indices list and modify index calculation logic accordingly.
3. To change the change detection threshold, edit pipeline_config.yaml change_detection_threshold value.
4. To modify class definitions or add/remove classes, edit class_schema.yaml.

Rerunning with Modified Parameters

After modifying configuration files, simply rerun the pipeline:

powershell -ExecutionPolicy Bypass -File scripts/run_all.ps1

All downstream steps adapt automatically to the new parameters. Outputs are generated with the same file structure, enabling easy comparison of results across parameter variations.

Deterministic Output Verification

For reproducibility verification, run the pipeline on the same input data twice. Outputs should be byte-for-byte identical (same file sizes and checksums). If outputs differ, it suggests non-determinism in the pipeline (possibly floating-point arithmetic differences or random number generation not controlled by a fixed seed).

To verify determinism:

1. Run the complete pipeline and record file checksums (using Windows command certutil -hashfile filename SHA256).
2. Delete outputs/ directory.
3. Rerun the pipeline.
4. Compare checksums of new outputs to original checksum values.
5. All checksums should match exactly, confirming deterministic processing.

Documentation Conventions
---------------------------

Folder Organization

data/: Input data directory (raw imagery not committed).
  raw/: Raw Landsat imagery files (GeoTIFF format, not committed).
  aoi/: Area of Interest polygon (Karaj Municipality boundary).
  roi/: Regions of Interest for training (training polygons with class labels).

configs/: Configuration files (YAML format, committed).
  pipeline_config.yaml: Master configuration.
  band_mapping.yaml: Sensor and wavelength specifications.
  class_schema.yaml: Land cover class definitions.
  export_plan.yaml: Output file specifications.

scripts/: Python and PowerShell scripts (committed).
  validate_inputs.py: Input data validation.
  envi_batch_pipeline_png.py: ENVI processing pipeline.
  publish_assets.py: Publish outputs to documentation.
  export_stats_csv.py: Generate statistics CSV.
  run_all.ps1: Master orchestration script.

outputs/: Processing outputs directory (year folders committed with PNG files, intermediate .dat/.hdr files not committed).
  [YEAR]/: Per-year subdirectories.
    [YEAR]/01_RGB.png through 05_LULC.png
    [YEAR]/*.dat and *.hdr (intermediate ENVI files, not committed)
  change_1990_2024/: Change analysis outputs.
  validation_report.txt
  run_log.json
  lulc_stats.csv

docs/: Documentation source files (Markdown, committed).
  index.md through references.md: Documentation pages.
  assets/outputs/: PNG files for website display (committed).
    1990/, 2000/, 2010/, 2024/: Per-year galleries.
    change_1990_2024/: Change map galleries.

.github/workflows/: GitHub Actions workflows (committed).
  gh-pages.yml: Automated MkDocs deployment to GitHub Pages.

File Naming Conventions

All file names follow consistent patterns:

Input files: landsat_[SENSOR]_[YEAR]_sr_b[N].tif (e.g., landsat_tm5_1990_sr_b4.tif)
Index outputs: [INDEX]_[YEAR].{dat,hdr} (e.g., ndvi_1990.dat)
Classification outputs: lulc_[YEAR].{dat,hdr,png} (e.g., lulc_2024.png)
Change outputs: change_[YEAR1]_[YEAR2].{dat,hdr,png} (e.g., change_1990_2024.png)

Consistency check: All file names are case-sensitive and must match configuration references exactly.

Logging and Debugging
---------------------

Machine-Readable Logs

Complete processing provenance is recorded in outputs/run_log.json in JSON format:

{
  "analysis_date": "2026-01-04T14:32:00Z",
  "processing_steps": [
    {
      "step_name": "band_subset",
      "step_number": 1,
      "start_time": "2026-01-04T14:32:05Z",
      "end_time": "2026-01-04T14:33:22Z",
      "status": "success",
      "inputs": ["landsat_tm5_1990_sr_b1.tif", ...],
      "outputs": ["subset_1990.dat"],
      "parameters": {"bands": [1, 2, 3, 4, 5, 7]}
    },
    ...
  ],
  "qa_summary": {
    "total_checks": 42,
    "passed": 41,
    "warnings": 1,
    "failures": 0
  }
}

These logs enable automatic verification of processing completeness and enable users to reconstruct exactly what parameters were used in any execution.

Error Messages and Recovery

If the pipeline encounters an error, the run_log.json includes detailed error messages. Common errors and recovery procedures:

Error: "Input file not found"
Recovery: Verify file names in data/raw/ match pipeline_config.yaml exactly (case-sensitive).

Error: "envipyengine module not found"
Recovery: This is expected in non-ENVI environments. Proceed with documentation build and validation checks; ENVI-dependent processing can be completed separately on a system with ENVI installed.

Error: "Classification accuracy below threshold"
Recovery: Review training data for mislabeling, increase training sample counts, or adjust SVM parameters in pipeline_config.yaml.

Performance and Computational Requirements
-------------------------------------------

Estimated Processing Time

On a modern desktop computer with ENVI 5.6 installed:

- Input validation: <1 minute
- Band subsetting and preprocessing (all four dates): 20-30 minutes
- Spectral index calculation: 30-40 minutes
- Classification training and application: 30-45 minutes
- Change detection: 15-20 minutes
- Asset publishing: 5-10 minutes
- Total pipeline: approximately 2-3 hours

Disk Space Requirements

- Raw Landsat imagery (six bands per date, four dates): 3-5 GB
- Intermediate ENVI products (temporary): 4-6 GB
- Final outputs (GeoTIFF + PNG): 500 MB - 1 GB
- Documentation website: 50-100 MB
- Total: 8-12 GB minimum free disk space recommended

Memory Requirements

- Python environment: 2-4 GB RAM
- ENVI processing: 4-8 GB RAM (varies with image size and complexity)
- Total: 8 GB RAM recommended; 16 GB strongly recommended for large study areas or higher resolution imagery
