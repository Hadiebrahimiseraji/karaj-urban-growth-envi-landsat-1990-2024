Research Background and Motivation
====================================

Urbanization and Landscape Change in the Middle East
-----------------------------------------------------

The Middle East and Central Asia have experienced unprecedented rates of urbanization over the past four decades, driven by population growth, economic development, migration from rural areas, and regional geopolitical transitions. Cities in semi-arid environments face particular challenges in managing water resources, maintaining agricultural productivity, and controlling urban sprawl in the context of limited water availability and fragile ecosystems. Understanding the trajectory and magnitude of land use and land cover change is essential for informed policy decisions regarding urban planning, water management, and environmental conservation.

Karaj Municipality: Regional Context
-------------------------------------

Karaj, located in Alborz Province in northwestern Iran, serves as a case study of rapid metropolitan expansion. The city is situated at the foothills of the Alborz Mountains and has experienced accelerating urbanization since the 1980s, driven by migration from rural areas and regional economic development. The expansion of Karaj directly impacts regional water availability, soil conservation, agricultural land preservation, and ecosystem health. Understanding the spatial and temporal patterns of this expansion provides actionable insights for urban management and environmental policy.

The Landsat Archive as a Window on Change
------------------------------------------

The Landsat satellite series, operated jointly by the United States Geological Survey (USGS) and NASA, has continuously acquired multispectral imagery of the Earth's surface since 1972. The program provides free, globally available data at 30-meter spatial resolution with consistent radiometric and geometric properties across decades. This consistency makes Landsat an ideal data source for long-term change detection studies spanning multiple decades, including analyses of urban growth, vegetation change, and water dynamics.

For this research, Landsat 5 Thematic Mapper (TM) data from 1990, 2000, and 2010, and Landsat 8 Operational Land Imager (OLI) data from 2024 provide a consistent foundation for change analysis. Although sensors have evolved, preprocessing algorithms and radiometric normalization enable meaningful temporal comparison.

Spectral Indices as Environmental Indicators
---------------------------------------------

Multispectral satellite imagery records reflectance patterns across multiple electromagnetic wavelengths. Different land cover types exhibit characteristic reflectance signatures: vegetation reflects strongly in the near-infrared and weakly in visible wavelengths; water absorbs strongly across most wavelengths; urban materials (asphalt, concrete, brick) exhibit moderate reflectance with distinct spectral patterns.

Spectral indices are computed from reflectance values across multiple bands to isolate particular environmental phenomena. The Normalized Difference Vegetation Index (NDVI), calculated as (NIR - Red) / (NIR + Red), provides a quantitative measure of vegetation greenness and biomass. The Normalized Difference Built-up Index (NDBI), using shortwave-infrared and near-infrared bands, emphasizes built infrastructure. The Normalized Difference Water Index (NDWI), calculated from near-infrared and shortwave-infrared bands, identifies water bodies and indicates soil moisture conditions.

These indices compress multispectral information into single-band outputs with intuitive interpretation, enabling both visual assessment and automated threshold-based classification.

Supervised Classification Approaches
-------------------------------------

Supervised classification assigns each pixel in an image to a predefined land cover class based on its spectral properties. The approach requires training data: a set of pixels whose land cover class is known with high confidence. These training pixels are used to characterize the spectral signature of each class. A classifier algorithm then generalizes these signatures to all pixels in the image.

Support Vector Machine (SVM) classifiers have become standard in remote sensing because they perform well with limited training data, handle high-dimensional spectral inputs effectively, and are less prone to overfitting than some alternative algorithms. SVM finds optimal boundaries in multidimensional spectral space to separate classes with maximum margin, a property that often improves generalization to independent test data.

Post-classification Change Detection
-------------------------------------

Post-classification comparison is a straightforward change detection method in which land cover maps from different dates are independently classified, then compared pixel-by-pixel to determine transitions. A transition matrix tabulates the number of pixels that changed from each starting class to each ending class. This approach quantifies areal changes, identifies dominant transitions, and is amenable to error assessment.

Advantages include simplicity, transparency, and the ability to map not just change but also stability. Disadvantages include sensitivity to classification errors and the inability to detect subtle spectral changes below the threshold of categorical reclassification. For this research, post-classification comparison is supplemented with index differencing to detect gradual spectral trends even where categorical class boundaries are not crossed.

Thesis Research Questions and Objectives
----------------------------------------

This thesis investigates the following specific research questions:

Primary Objective: Quantify the spatial extent, rate, and spatial patterns of urban expansion in Karaj Municipality from 1990 to 2024, measured in square kilometers and percent increase per decade.

Secondary Objective One: Characterize changes in vegetation extent and vigor, measured by temporal trends in NDVI values and the areal extent of pixels meeting defined vegetation thresholds.

Secondary Objective Two: Assess changes in water and soil moisture conditions, measured by temporal trends in NDWI and the areal extent of water bodies and moisture-rich pixels.

Secondary Objective Three: Identify dominant land cover transitions, particularly the conversion of agricultural and natural land to urban use, quantified in a transition matrix and expressed as areal changes in square kilometers.

Secondary Objective Four: Evaluate the effectiveness and reliability of automated spectral analysis for detecting long-term environmental change, including assessment of classification accuracy, index sensitivity, and consistency across different sensors and temporal periods.

Methodological Innovation and Significance
-------------------------------------------

This research contributes to the remote sensing and urban studies literature in several ways:

Configuration-Driven Reproducibility: By externalizing all processing parameters to configuration files, the pipeline enables other research groups to replicate the methodology exactly, modify parameters systematically, and apply the approach to other geographic regions.

Multi-Sensor Consistency: The pipeline adapts to differences between Landsat 5 TM and Landsat 8 OLI through configuration-driven band mapping, demonstrating methods for extending analysis across sensor generations.

Integrated Change Detection: Combining post-classification comparison with spectral index differencing provides complementary perspectives on change, improving robustness against individual method limitations.

Transparency and Auditability: Complete logging of all processing steps in machine-readable format enables independent verification and supports peer review.

Accessibility: Use of free Landsat data and open-source tools (Python, ENVI, MkDocs) ensures the methodology is accessible to researchers in academic and governmental institutions worldwide, with no licensing barriers.

Expected Contributions
----------------------

This research is expected to contribute

1. An openly available, peer-reviewed analysis of urban expansion in Karaj over three decades, providing baseline information for urban planning and environmental policy.

2. A replicable, documented methodology for multi-temporal change analysis in semi-arid urban regions, applicable to other cities in Iran, Central Asia, and beyond.

3. Insight into the consistency and reliability of spectral indices for detecting long-term change in Mediterranean and semi-arid environments.

4. A template for students and early-career researchers seeking to conduct similar analyses, with complete source code and documentation.

The following sections detail the data, preprocessing, classification, change detection, quality assurance, and reproducibility procedures that underpin this analysis.
