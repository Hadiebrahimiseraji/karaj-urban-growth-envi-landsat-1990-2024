Land Use and Land Cover Classification
========================================

Classification Approach
-----------------------

SupervisedcClassification assigns each pixel in the preprocessed imagery to one of five predefined land cover classes based on its spectral reflectance signature across multiple bands. Supervised classification requires training data: a set of pixels whose class membership is known. The classifier learns the spectral characteristics of each class from the training data and generalizes these characteristics to unclassified pixels.

This analysis employs a Support Vector Machine (SVM) classifier, a machine learning algorithm well-suited to remote sensing applications. SVM finds optimal decision boundaries in high-dimensional spectral space, balancing training accuracy with generalization to independent test data.

Land Cover Class Schema
-----------------------

Five mutually exclusive, exhaustive land cover classes are defined for Karaj Municipality. Class definitions are semantic (based on visual and functional characteristics) and spectrally motivated (classes exhibit distinct spectral signatures in multispectral imagery).

Water

Definition: Open water bodies including rivers, reservoirs, ponds, and wetland areas with standing water. Includes water with vegetation <20 percent cover and water-adjacent pixels dominated by wet bare substrate.

Spectral Signature: Strong absorption across all wavelengths, particularly in shortwave-infrared. NDVI negative, NDBI negative, NDWI positive (>0.3).

Urban

Definition: Developed areas with dense buildings, roads, parking areas, commercial zones, and industrial facilities. Includes residential neighborhoods with >50 percent impervious surface and mixed urban-agricultural areas with >30 percent urbanization.

Spectral Signature: Moderate reflectance in visible and near-infrared, higher reflectance in shortwave-infrared due to concrete, asphalt, and metal roofing. NDVI low (<0.3), NDBI positive (>0.05), NDWI negative.

Agriculture

Definition: Cultivated croplands and irrigated fields, including seasonal crops, permanent orchards, and agricultural greenhouses. Includes fallow agricultural land without active vegetation.

Spectral Signature: Depends on crop type and phenological stage. Growing crops exhibit high NDVI (0.5 to 0.8), moderate NDBI (slightly negative to 0.0), and high NDWI (>0.1) due to irrigation. Fallow fields exhibit low to moderate NDVI (<0.4).

Forest

Definition: Dense woody vegetation with >40 percent canopy cover, including natural forests, planted woodlots, and tree-lined corridors. Excludes isolated trees and sparse tree cover (<40 percent).

Spectral Signature: Very high NDVI (>0.6), negative to zero NDBI, high NDWI (>0.1) due to leaf moisture content.

Bare Soil

Definition: Exposed mineral soil with <10 percent vegetation cover. Includes eroded areas, construction sites, and naturally unvegetated rocky outcrops.

Spectral Signature: Low NDVI (<0.2), variable NDBI depending on soil color and moisture, variable NDWI depending on soil moisture.

Support Vector Machine Classifier
----------------------------------

Why SVM for This Application

SVM classifiers have several advantages for remote sensing land cover classification:

1. Effectiveness with Limited Training Data: Unlike some alternatives, SVM performs well when training samples are limited relative to the number of spectral bands, a common constraint in remote sensing.

2. High-Dimensional Spectral Inputs: SVM inherently handles six-band reflectance data and computed indices without overfitting, through regularization and optimal margin maximization.

3. Multi-Class Capability: SVM naturally extends to multi-class problems (five classes in this case) through one-versus-one or one-versus-rest strategies.

4. Robustness: SVM is less sensitive to outliers and noise than some alternatives, important when training data contains labeling errors.

5. Reproducibility: SVM parameters and results are deterministic given fixed training data and kernel settings.

SVM Implementation

The ENVI SVM classification task is configured with the following specifications:

Kernel: Radial basis function (RBF), which implicitly maps spectral data to high-dimensional space, enabling nonlinear decision boundaries.

Regularization Parameter (C): Set to 1.0, balancing training accuracy against generalization. Higher values prioritize training accuracy; lower values emphasize generalization.

RBF Gamma: Set to default, controlling the influence of individual training samples.

One-Versus-One Strategy: Five binary SVM classifiers are trained (Water vs. Urban, Water vs. Agriculture, etc.), and class membership is determined by majority voting.

Training Data and Regions of Interest
-------------------------------------

Manual Delineation of Training Regions

Training regions of interest (ROI) are delineated manually on high-resolution reference imagery or orthorectified aerial photography for 2024. For each of the five classes, 20 to 50 distinct training regions are outlined, distributed across the study area to capture spectral variability within each class.

Training regions are stored as vector shapefiles or GeoJSON files in data/roi/, with a class attribute field indicating the assigned class. Region size varies from 100 square meters (a few pixels) to several hectares, capturing both homogeneous and mixed-composition examples of each class.

Training Sample Extraction

For each delineated ROI, all pixels within the region are extracted and their spectral values recorded. Spectral values are computed from the preprocessed multispectral imagery (six reflective bands) and spectral indices (NDVI, NDBI, NDWI). Thus, each training sample is an eight-dimensional vector (six bands plus two indices).

Total training samples number approximately 5,000 to 10,000 pixels distributed across five classes. Class balance is attempted, with similar sample counts across classes to avoid training bias. However, if natural spatial distributions are very unequal (e.g., agriculture is scarcer than urban), training samples are weighted accordingly.

Quality Control of Training Data

Training regions are visually inspected to ensure that delineated areas are homogeneous and correctly labeled according to class definitions. Misclassified or ambiguous regions are removed. Spectral outliers (e.g., a forest ROI with one pixel having water-like reflectance due to shadow) are filtered from training data.

Applying Training Data Across Time

Training ROIs are delineated on 2024 reference data. For classification of 1990, 2000, and 2010 imagery, the same ROI boundaries are applied, with manual verification to ensure that class definitions remain consistent across time. This approach maintains class definitions as fixed throughout the analysis period.

Alternatively, sample reflectance values from each ROI are recomputed for each date, adapting to potential spectral shifts due to sensor differences while preserving class label consistency. This approach is more robust to temporal spectral variability.

SVM Classifier Training and Validation
--------------------------------------

Split Validation Approach

Training samples are randomly divided into training (70 percent) and validation (30 percent) subsets. The SVM is trained on the training subset; validation samples are independently classified and compared against their known labels to estimate classification accuracy.

Accuracy Metrics

Validation accuracy is assessed using:

Overall Accuracy: The percentage of all validation pixels correctly classified.

Per-Class User's Accuracy: The percentage of pixels classified as a given class that are correct (confidence in the classifier output).

Per-Class Producer's Accuracy: The percentage of validation pixels of a given class that the classifier correctly identifies (ability to find all members of a class).

Kappa Statistic: A measure of agreement beyond chance, accounting for expected random agreement.

Minimum acceptable overall accuracy is 80 percent; if validation accuracy falls below this threshold, the classifier is retrained with adjusted parameters or additional training samples.

Application to All Dates

Once validation confirms acceptable accuracy (>80 percent overall), the SVM classifier is applied to all preprocessed imagery (1990, 2000, 2010, 2024) to produce land cover classification maps. The classifier trained on 2024 data is used for all dates, maintaining consistent class definitions and reducing the influence of sensor-specific spectral shifts.

Classification Output and Representation
-----------------------------------------

Output Format

Classification results are stored as single-band raster files with integer data type, where pixel values correspond to class codes:

1 = Water
2 = Urban
3 = Agriculture
4 = Forest
5 = Bare Soil
0 = Masked (cloud, shadow, or no-data)

Output files are named lulc_[YEAR].dat and lulc_[YEAR].hdr and stored in outputs/[YEAR]/.

Color Mapping for Visualization

For visualization and reporting, classification rasters are color-mapped using intuitive colors:

Water: Blue (RGB 0, 0, 255)
Urban: Gray (RGB 128, 128, 128)
Agriculture: Yellow-Green (RGB 173, 255, 47)
Forest: Dark Green (RGB 34, 139, 34)
Bare Soil: Tan (RGB 210, 180, 140)

Color-mapped classification results are exported as PNG images for inclusion in the documentation website.

Post-Classification Processing

Smoothing and Majority Filtering

To reduce salt-and-pepper noise (isolated misclassified pixels), a 3x3 majority filter is optionally applied. Each pixel is reclassified as the majority class among itself and its eight neighbors. This filter is applied selectively to regions with high classification uncertainty and preserves sharp boundaries between classes.

Boundary Refinement

Classification boundaries are checked against reference imagery. If boundaries do not align with visible features (e.g., a sharp boundary cutting across a homogeneous building complex), localized manual adjustment is performed.

Handling Mixed Pixels

Some 30-meter pixels in areas of transition (e.g., urban-agricultural interface) contain mixture of two classes. SVM assigns each pixel to a single class, potentially introducing misclassification. This limitation is noted in the analysis; mixed-pixel areas are flagged for additional attention in change detection and accuracy assessment.

Classification Consistency Across Years
---------------------------------------

Maintaining Class Definitions

To enable fair temporal comparison, class definitions are held constant across all analysis dates. Training data, class names, class codes, and validation procedures remain identical for 1990, 2000, 2010, and 2024.

Handling Sensor Differences

Despite constant class definitions, Landsat 5 TM and Landsat 8 OLI exhibit different spectral response functions. A classifier trained on OLI data (2024) may exhibit bias when applied to TM data (1990-2010). To minimize this bias, radiometric harmonization (affine transformation of reflectance values) is optionally applied to TM data prior to classification, scaling reflectance values to approximate OLI characteristics.

Alternatively, the classifier is applied without harmonization, accepting cross-sensor bias as a known systematic error. Sensitivity analyses comparing harmonized and non-harmonized results quantify this error source.
