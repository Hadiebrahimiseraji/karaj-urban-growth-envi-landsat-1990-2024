Quality Assurance Procedures
============================

QA Framework
------------

Quality assurance procedures are implemented at multiple analysis stages to identify and mitigate errors, ensure consistency, and document data fitness for publication and policy application. The QA framework spans input validation, processing verification, output validation, and cross-method consistency checks.

Input Data Validation
---------------------

File Existence and Completeness

Before processing begins, the validate_inputs.py script confirms that all input imagery files referenced in pipeline_config.yaml exist in data/raw/. Missing files prevent pipeline execution and trigger an error report.

Raster Metadata Inspection

For each input raster, metadata is extracted and validated:

Spatial Reference: Imagery must be in UTM Zone 39 North, WGS84 datum. Imagery in other projections is reprojected or flagged as incompatible.

Dimensions: Imagery must match expected dimensions (typically 450 rows by 400 columns for the Karaj study area). Unexpected dimensions trigger investigation.

Data Type: Reflectance imagery must be unsigned 16-bit integer (uint16). Other data types are flagged.

Band Count: Landsat 5 TM subset must contain six reflective bands; Landsat 8 OLI subset must contain six reflective bands corresponding to TM Band equivalents. Incorrect band counts prevent processing.

Raster Statistics Check

Minimum and maximum reflectance values are computed for each band. Expected ranges for Surface Reflectance are 0 to 10,000 (representing 0 to 100 percent reflectance). Values outside this range indicate potential data corruption or incorrect radiometric calibration and trigger warnings.

Band-Specific Statistics

For each band, the distribution of reflectance values is examined. Unusually narrow distributions (indicating insufficient spectral variability) or bimodal distributions (indicating unmerged scenes or processing errors) are flagged for review.

Geometric Validation
--------------------

Spatial Extent Check

All preprocessed imagery must cover the full study area (Karaj Municipality) without gaps. Imagery extent is verified by comparing actual extent to expected bounds (UTM Zone 39N, 366,000 to 378,000 East, 3,965,000 to 3,980,000 North). Partial coverage is flagged, and processing is halted until complete data is obtained.

Co-Registration Verification

Multi-temporal classification requires precise alignment (to within one pixel, or 30 meters) across all dates. Co-registration is verified by computing a correlation coefficient between temporally proximal imagery (e.g., 2024 Band 4 with a 2024 reference). High correlation (>0.90) indicates good alignment.

If misalignment is detected, automatic image-to-image registration is attempted using ENVI image registration tasks. Manual verification is required if automatic registration fails.

No-Data Value Consistency

All imagery must use a consistent no-data value (typically -9999 or 0 for masked pixels). Inconsistent no-data values across bands introduce errors in index calculations. Metadata is checked to ensure consistent no-data value specification.

Preprocessing QA
----------------

Band Subsetting Verification

After band subsetting, output imagery is checked to confirm that the correct bands were retained. Band statistics are compared to input imagery to ensure data integrity was preserved.

Wavelength Metadata Verification

Embedded wavelength values are read from output imagery headers and compared against configured values in band_mapping.yaml. Discrepancies trigger warnings.

QA Mask Application

QA-based cloud and shadow masking is verified by visual inspection. Masked pixels should correspond to visible clouds or shadows in true-color composites. If masking appears excessive (>50 percent of image masked) or insufficient, thresholds are adjusted and masking is reapplied.

Index Calculation QA
--------------------

Range Checks

All indices (NDVI, NDBI, NDWI) must have output values within -10,000 to 10,000. Pixels with out-of-range values are flagged and investigated. Calculation errors typically produce extreme values (e.g., values >1 billion) that are easily detected.

NaN Detection

Not-a-Number (NaN) values in index output indicate division by zero (e.g., if NDVI denominator NIR + Red equals zero) or other calculation errors. The count and spatial distribution of NaN pixels are recorded. If NaN pixels exceed 5 percent of the image, index calculation is reviewed for errors.

Statistical Reasonableness

Index histograms are examined to ensure they match expected distributions. For example, NDVI should be skewed toward positive values in vegetated areas (mean typically 0.2 to 0.5 for mixed landscapes). Histograms showing unexpected shapes trigger investigation.

Index Correlation

Correlation between indices is computed. High correlation between NDVI and NDBI (>0.8) would be unexpected, as vegetation-rich areas should have high NDVI but low NDBI. Unexpected correlations may indicate calculation errors or data mixing.

Cross-Band Consistency

For pixels with very high values in all bands (indicating very bright surfaces), index values should be consistent with surface type (e.g., high NDBI for urban, low NDVI). Inconsistencies may indicate data errors.

Classification QA
------------------

Training Data Inspection

Training regions of interest are visually overlaid on reference imagery to confirm that delineations are accurate and homogeneous. Regions containing spectrally mixed or misclassified pixels are removed. Training sample counts are verified to be roughly balanced across classes.

Split Validation Accuracy

The SVM classifier is validated using independent test data (30 percent of training samples withheld from training). Overall accuracy and per-class accuracies are computed. Minimum acceptable overall accuracy is 80 percent. If accuracy falls below this threshold:

1. Training data quality is reviewed for mislabeling.
2. Training sample size is increased.
3. SVM parameters (kernel, regularization) are adjusted.
4. Classification is retrained and revalidated.

Confusion Matrix Analysis

The confusion matrix (showing for each class what percentage of pixels are correctly classified versus misclassified) is examined for systematic biases. For example, if Urban pixels are frequently misclassified as Bare Soil, this suggests spectral overlap or training data inadequacy for one of these classes. Confusion matrix results inform improvements to training data or classification parameters.

Classification Noise Detection

Salt-and-pepper noise (isolated pixels of different class surrounded by different pixels) suggests misclassification. Spatial autocorrelation is computed to quantify whether classified pixels tend to cluster by class (indicating reliable classification) or are randomly scattered (indicating poor classification). Low spatial autocorrelation is flagged for review.

Temporal Consistency Check

When the same SVM classifier is applied to multiple dates, similar land cover in unchanged areas should be assigned the same class. Classification is checked to ensure temporal consistency in stable areas. If a forest area in 2010 is misclassified as Bare Soil in 2010 but correctly classified as Forest in 2024, this temporal inconsistency triggers investigation of possible data or processing errors.

Change Detection QA
-------------------

Stability Validation

In areas where no change is expected (locked-down study sites with known stable land cover), post-classification comparison should show no transitions (diagonal of transition matrix dominates). If significant transitions are incorrectly detected in stable areas, change detection thresholds or classification methods require adjustment. Stability validation confirms that false change alarms are minimal.

Physical Plausibility

Detected changes must be physically plausible. For example, detecting Forest-to-Water transitions in upland areas is implausible and suggests classification error. Implausible transitions are reviewed and potentially excluded from final results.

Consistency Across Change Methods

Post-classification comparison and index differencing are expected to show general agreement about where changes occurred. Pixels detected by both methods are high-confidence change locations. Pixels detected by only one method are flagged as intermediate confidence. Perfect agreement is not expected due to methodological differences; typical agreement is 60 to 80 percent.

Boundary Analysis

Change map boundaries (transitions between changed and unchanged areas) are examined. Abrupt boundaries that cut across homogeneous land cover units suggest classification or change detection errors. Gradual boundaries that align with visible features (roads, property lines, field boundaries) indicate reliable change detection.

Output Data Validation
-----------------------

File Integrity

After all processing, output files are checked for:

1. Correct file size (large output files should be several MB to hundreds of MB; unusually small files may indicate processing errors).
2. Valid file format (GeoTIFF for archives, PNG for visualization).
3. Readable metadata (projections, extents, descriptions).

Output Raster Checks

Each output raster (classification, change map, indices) is spot-checked by random sampling:

1. Visual inspection of true-color composites and color-mapped classification output.
2. Verification that raster extent matches expected study area.
3. Verification that data types and value ranges are correct.
4. Absence of unexpected null or no-data pixels outside QA-masked regions.

Statistical Audit

Summary statistics for all output rasters are generated and logged:

- Minimum and maximum values.
- Mean and standard deviation.
- Pixel counts per class (for classification output).
- Area per class in square kilometers.

These statistics are compared against expected ranges. For example, total area (sum of all pixels across all classes) should equal the study area (approximately 393 square kilometers for Karaj Municipality). Discrepancies of more than 1 percent indicate errors.

Cross-Method Audit

Classification-based area estimates are compared to index-based area estimates. For example, the area of pixels classified as Water should approximately match the area of pixels with high NDWI (>0.3). Large discrepancies indicate potential methodological conflicts or errors.

Logging and Reporting
---------------------

Machine-Readable Logs

All QA checks are logged in JSON format in outputs/run_log.json with the following structure:

{
  "analysis_date": "2026-01-04",
  "qa_checks": [
    {
      "check_name": "file_existence",
      "status": "passed",
      "details": "All input files found"
    },
    {
      "check_name": "raster_metadata",
      "status": "passed",
      "rasters_checked": 6,
      "issues": []
    },
    {
      "check_name": "classification_accuracy",
      "status": "passed",
      "overall_accuracy": 0.847,
      "kappa": 0.802
    }
  ]
}

QA Summary Report

After all checks, a human-readable QA summary report is generated for inclusion in project documentation. The report lists all checks performed, their status (passed/failed/warning), and any remedial actions taken.

Fail-Safe Procedures

If any critical QA check fails (e.g., overall classification accuracy <75 percent), pipeline execution is halted with clear error messaging. Re-execution is prevented until the underlying issue is resolved. This approach prevents propagation of errors into final outputs.

Incremental Validation

QA checks are performed incrementally as each processing stage completes. Early detection of errors prevents waste of computation time on downstream steps that depend on correct upstream results.
