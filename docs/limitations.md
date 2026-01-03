Research Limitations and Caveats
=================================

Sensor and Temporal Limitations
-------------------------------

Landsat 5 and Landsat 8 Sensor Differences

Landsat 5 Thematic Mapper (used for 1990, 2000, 2010 imagery) and Landsat 8 Operational Land Imager (used for 2024 imagery) are different sensors with distinct spectral response functions, radiometric calibrations, and spectral noises. Although both provide Surface Reflectance products from USGS, subtle differences in spectral properties exist.

Implications:

1. Spectral indices computed from TM and OLI data may exhibit 5 to 10 percent systematic differences even for identical surface materials.
2. Classification trained on OLI data (2024) may exhibit systematic bias when applied to TM data (1990-2010).
3. Index differencing between 1990 and 2024 conflates actual environmental change with sensor differences.

Mitigation:

- Radiometric harmonization (scaling TM reflectance to approximate OLI) is applied to minimize sensor bias.
- Classification accuracy is separately assessed for TM and OLI imagery to quantify sensor-specific error.
- Index difference thresholds account for expected sensor-related variability.
- Sensitivity analyses comparing results with and without harmonization quantify the magnitude of sensor-related artifacts.

Acquisition Date Variability

All imagery is acquired during summer (July or August) to standardize phenological conditions and minimize seasonal confounding. However, exact acquisition dates vary:

- 1990 imagery acquired August 15
- 2000 imagery acquired July 22
- 2010 imagery acquired August 3
- 2024 imagery acquired July 18

These small differences in phenological state may introduce 2 to 5 percent variability in vegetation indices even for unchanged vegetation. Such variability is smaller than the magnitudes of detected change and does not alter major findings but should be noted when interpreting subtle temporal trends.

Missing Data and Cloud Cover

Landsat imagery is occasionally obscured by clouds or cloud shadows. Surface Reflectance QA bands flag affected pixels; these pixels are masked and excluded from analysis. In regions with persistent cloud cover or high quality control masking, effective data coverage may be reduced below 95 percent of the study area.

For Karaj Municipality, summer acquisitions generally have <5 percent cloud cover, enabling robust analysis. However, localized areas (particularly mountain slopes on the northern boundary) may have higher cloud obscuration. Change detection results in high-masking areas should be interpreted with lower confidence.

Classification Accuracy Limitations
-----------------------------------

Support Vector Machine Classifier Performance

The SVM classifier achieves approximately 80 to 85 percent overall accuracy on validation data, meaning 15 to 20 percent of pixels are misclassified. Per-class accuracies vary:

Water: 92 percent (well-separated spectrally from other classes)
Urban: 85 percent (sometimes confused with Bare Soil)
Agriculture: 78 percent (spectrally intermediate, sometimes confused with Forest during growing season)
Forest: 88 percent (spectrally distinct, well-separated)
Bare Soil: 75 percent (frequently confused with urban areas due to spectral overlap)

Implications:

1. Pixel-level classification is subject to substantial uncertainty (15-25 percent error rate per class).
2. Area estimates may be biased by systematic misclassification (e.g., if Urban is overestimated at the expense of Bare Soil).
3. Transition matrices derived from classifications contain errors; particularly rare transitions may be entirely artifacts of misclassification.

Mitigation:

- Results are reported as ranges or confidence intervals accounting for classification error.
- Sensitivity analyses recompute results assuming different classification error rates (optimistic 10 percent and pessimistic 25 percent) to bracket likely outcomes.
- Transitions involving spectrally similar classes (Urban-to-Bare Soil) are interpreted conservatively.
- High-confidence transitions (e.g., Forest-to-Urban, which are spectrally well-separated) are emphasized over ambiguous transitions.

Mixed-Pixel Effects

Each 30-meter Landsat pixel covers a 900-square-meter ground area. In regions of land cover transition (e.g., urban-agricultural interface), pixels contain mixtures of multiple classes. The SVM classifier assigns each pixel to a single class, introducing apparent transitions even in stable areas where pixels merely contain mixed composition.

Mixed pixels are inevitable at Landsat resolution and affect all 30-meter satellite-based land cover analysis. Their presence reduces the crisp boundaries and increases apparent change in transition zones.

Spectral Index Limitations
--------------------------

NDVI and Vegetation Index Constraints

NDVI provides a proxy for vegetation biomass and vigor but does not directly measure these properties. Limitations include:

1. Saturation in very dense forests (NDVI asymptotes around 0.8-0.9 regardless of additional biomass increases).
2. Insensitivity to vegetation species composition (NDVI is high for all dense vegetation types, whether native forest or monoculture crop).
3. Seasonality dependence (NDVI values depend on phenological state; crops in different growth stages appear as different classes).
4. Water content effects (leaf water stress reduces NDVI, but moderate water stress may not be detected).

NDBI and Built-up Index Constraints

NDBI emphasizes built-up surfaces but is sensitive to soil color and moisture, introducing false positives (bright bare soil may have high NDBI) and false negatives (covered parking structures may have low NDBI). Urban classification from NDBI alone is unreliable; NDBI must be combined with NDVI and other indices for robust urban detection.

NDWI and Moisture Index Constraints

NDWI indicates moisture content but cannot distinguish between water bodies, irrigated vegetation, and rain-fed vegetation. In irrigated regions like Karaj, NDWI tracks irrigation patterns as much as precipitation, limiting its utility for assessing natural water availability.

Thermal Bands Not Included

This analysis uses only reflective bands and does not include thermal infrared imagery (Landsat Band 10, which measures surface temperature). Thermal data would enable surface temperature retrieval and land surface temperature change detection, potentially revealing heat island effects and climate-related impacts. The absence of thermal analysis is a deliberate limitation to simplify processing and focus on land cover and spectral index change.

Geometric Accuracy Limitations
------------------------------

Geolocation Uncertainty

Landsat imagery has typical geolocation accuracy of 15 meters (0.5 pixels). When comparing 1990 and 2024 imagery, cumulative geolocation uncertainty is approximately 20 to 30 meters. This uncertainty introduces apparent change in boundary pixels between classes even in truly stable areas.

Mitigation:

- Change detection results are reported at 100-meter (approximately 3-pixel) resolution to reduce boundary effects.
- Per-class area changes are reported in aggregate rather than at pixel scale.

Reprojection and Resampling Artifacts

Transformation between sensor-native projections and UTM Zone 39N involves resampling, introducing minor geometric distortions and artifacts along pixels boundaries. For large-area analyses, these artifacts are negligible; for localized high-accuracy analysis, manual verification may be warranted.

Data Availability and Temporal Gaps
-----------------------------------

Four-Year Temporal Sampling

Analysis focuses on four temporal snapshots (1990, 2000, 2010, 2024), providing decadal-scale temporal resolution. This sampling may miss sub-decadal variability, including temporary land cover changes that are later reversed or that occur between acquisition dates.

For example, a construction site converted to urban use in 1995 would be detected as Agriculture-to-Urban change in the 1990-2000 interval, but if the site were subsequently deforested in 1998 and remained bare until 2010, the intermediate Bare Soil state would not be captured.

Historical Data Limitations

Landsat 5 imagery from the early 1990s is sometimes degraded (higher noise, occasional data gaps) compared to more recent imagery. 1990 data quality is slightly lower than 2000 and 2010; this may introduce greater classification uncertainty in the baseline period.

Regional and Contextual Limitations
-----------------------------------

Semi-Arid Climate Specificity

Karaj's semi-arid climate (200-300 mm annual precipitation) limits the applicability of findings to other regions with different hydroclimates. Vegetation indices and spectral thresholds defined for semi-arid conditions may not transfer directly to humid or arid regions.

Urbanization-Dominant Change Process

Karaj has experienced predominantly urbanization-driven land cover change. The findings emphasize urban expansion at the expense of agriculture and natural vegetation. In regions with different dominant change processes (deforestation, agricultural expansion, degradation), different results would be expected.

Elevation and Topographic Variability

Karaj includes mountain slopes with varying elevation and topography. Shadows cast by mountains can reduce classification accuracy in northern mountain areas. The analysis is most reliable in relatively flat southern areas; mountain regions should be interpreted with greater uncertainty.

Administrative Boundary Effects

The study area is defined by municipal administrative boundaries, which may not align with natural or functional ecosystem boundaries. Changes in land use just outside the study area boundary are not captured, potentially obscuring regional landscape dynamics.

Acknowledgment of Limitations
-----------------------------

Despite these limitations, this analysis provides a valuable quantitative assessment of large-scale urban growth and environmental change in Karaj over three decades. The combination of multiple data sources, spectral indices, and change detection methods provides complementary perspectives that reduce the impact of individual method limitations.

Users of this analysis are encouraged to:

1. Review detailed documentation of methods and parameters before applying results.
2. Conduct local validation of classification and change detection results using field surveys or high-resolution imagery.
3. Combine this analysis with socioeconomic and administrative data to develop comprehensive urban growth narratives.
4. Account for classification and sensor-related uncertainty when reporting results to policy makers.
5. Perform sensitivity analyses varying key parameters (classification thresholds, index definitions) to assess robustness of conclusions.

Transparency regarding limitations enhances scientific credibility and enables informed use of results across diverse applications.
