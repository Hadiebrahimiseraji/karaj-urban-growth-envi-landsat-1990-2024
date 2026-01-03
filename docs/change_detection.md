Change Detection Analysis
=========================

Change Detection Objectives
---------------------------

Change detection quantifies and maps land cover transitions between baseline (1990) and final (2024) time periods, as well as intermediate states in 2000 and 2010. Two complementary change detection methods are employed: post-classification comparison (categorical transitions) and index differencing (spectral trend analysis).

Post-Classification Comparison
------------------------------

Method Description

Post-classification comparison independently classifies imagery from two dates into five land cover classes, then compares the classifications pixel-by-pixel to generate a transition matrix and change map. This method is transparent, allowing pixel-level examination of specific transitions, and is less sensitive to some forms of classification error than spectral differencing alone.

Transition Matrix Construction

A transition matrix tabulates the number of pixels that transition from each class at time T1 to each class at time T2:

T1 Class \ T2 Class | Water | Urban | Agriculture | Forest | Bare Soil | Masked
Water | n_ww | n_wu | n_wa | n_wf | n_wb | n_wm
Urban | n_uw | n_uu | n_ua | n_uf | n_ub | n_um
Agriculture | n_aw | n_au | n_aa | n_af | n_ab | n_am
Forest | n_fw | n_fu | n_fa | n_ff | n_fb | n_fm
Bare Soil | n_bw | n_bu | n_ba | n_bf | n_bb | n_bm
Masked | n_mw | n_mu | n_ma | n_mf | n_mb | n_mm

Diagonal elements (n_ww, n_uu, etc.) represent pixels that did not change class. Off-diagonal elements represent transitions. Masked pixels from either date are excluded or reported separately.

Area Calculations

Transition matrix element counts are converted to area by multiplying by the pixel area (900 square meters = 0.0009 square kilometers per pixel). Net area change for each class is calculated as:

Net Change (class i) = Sum of pixels gaining class i minus sum of pixels losing class i

Per-class area and percentage changes are tabulated for reporting.

Transition Interpretation

Large off-diagonal transitions reveal dominant land cover changes. For example, in semi-arid regions undergoing urbanization, large values in the Agriculture-to-Urban and Forest-to-Urban cells indicate urban expansion at the expense of agricultural and natural land. Examining specific transitions enables detailed characterization of landscape transformation.

Post-Classification Comparison Caveats

Classification errors in either date propagate to the transition matrix. A pixel misclassified as Agriculture in 1990 but correctly classified as Urban in 2024 will be recorded as an Agriculture-to-Urban transition even if no actual change occurred. The magnitude of this error depends on individual classification accuracy and the correlation of errors across dates.

To quantify the influence of classification error, transition matrices are recalculated assuming optimistic (10 percent classification error) and pessimistic (25 percent classification error) error scenarios. If conclusions remain unchanged across scenarios, confidence in results is higher.

Spectral Index Differencing
---------------------------

Complementary Approach

Index differencing provides an alternative change detection perspective independent of classification. Temporal differences in NDVI, NDBI, and NDWI at the pixel level directly reveal spectral changes, enabling detection of gradual environmental change that may not cross categorical thresholds.

Index Difference Calculation

For each spectral index, the difference between end-of-period (2024) and baseline (1990) values is computed:

Delta NDVI = NDVI_2024 - NDVI_1990
Delta NDBI = NDBI_2024 - NDBI_1990
Delta NDWI = NDWI_2024 - NDWI_1990

Positive differences indicate increases in index values; negative differences indicate decreases.

Interpretation

Delta NDVI:
Large negative values indicate vegetation loss (urbanization, deforestation, agricultural abandonment).
Large positive values indicate vegetation gain (afforestation, agricultural expansion, recovery).
Values near zero indicate stable vegetation conditions.

Delta NDBI:
Large positive values indicate urban expansion and increased built-up area.
Large negative values indicate conversion from urban to non-urban (unusual but possible if buildings are demolished).
Values near zero indicate stable urban extent.

Delta NDWI:
Large negative values indicate decreased water availability and moisture stress.
Large positive values indicate increased water availability and moisture conditions.
Values near zero indicate stable moisture conditions.

Regional Averages

Mean Delta values are computed for each class from the 1990 classification. For example, the mean Delta NDVI for pixels classified as Agriculture in 1990 reveals average vegetation change within historical agricultural areas. This allows assessment of whether specific land cover types experienced systematic change.

Index Difference Uncertainty

Index differences are subject to radiometric calibration differences between Landsat 5 TM and Landsat 8 OLI sensors. Although both sensors provide consistent reflectance measurements, sensor-to-sensor differences may introduce systematic biases of 5 to 10 percent. Radiometric harmonization (applying calibration transforms to align TM and OLI reflectance) can reduce this bias.

Change Magnitude and Significance

Threshold-Based Change Detection

Pixels with index differences exceeding defined thresholds are flagged as changed. Thresholds are set based on index stability analysis in known-unchanged areas:

For NDVI and NDBI: Threshold set at mean absolute difference in stable areas plus two standard deviations, typically 0.05 to 0.10 in integer-scaled units (500 to 1000).

For NDWI: Threshold set analogously, typically 0.05 to 0.08.

Pixels meeting thresholds are classified as changed; others are classified as stable.

Change Map Production

Change detection results are synthesized into a change map showing:

Stable pixels: No classification change and index changes below thresholds.
Changed pixels: Classified transition and/or index change exceeding threshold.
Uncertain pixels: Classification uncertainty prevents clear change determination.

The change map is stored as lulc_change_1990_2024.dat and exported as lulc_change_1990_2024.png for visualization.

Temporal Sequencing
-------------------

Multi-Date Analysis

Beyond the primary 1990-to-2024 comparison, intermediate dates (2000 and 2010) enable assessment of change trajectory. Net change can be decomposed:

Total 1990-2024 change = (1990-2000 change) + (2000-2010 change) + (2010-2024 change)

This decomposition reveals whether change was gradual and steady or occurred in pulses during specific intervals. Urban expansion might accelerate in certain periods (e.g., 2000-2010) and decelerate in others (e.g., 2010-2024).

Temporal Trend Analysis

For pixels that changed class, the number of intermediate class changes is noted. A pixel might transition Agriculture (1990) to Urban (2024) directly, or might follow the sequence Agriculture (1990) to Bare Soil (2000) to Urban (2024). Examining these sequences provides insight into process dynamics.

Statistical Summary of Changes
------------------------------

Area Change Summary

Per-class area changes are reported in two formats:

Absolute Area: Change in square kilometers and percentage of total study area.
Relative Percentage: Percent change relative to 1990 area (e.g., a class doubling in area shows +100 percent change).

Example output table:

Class | 1990 Area (km2) | 2024 Area (km2) | Absolute Change (km2) | Percent Change
Water | 12 | 11 | -1 | -8.3
Urban | 45 | 125 | 80 | 177.8
Agriculture | 220 | 160 | -60 | -27.3
Forest | 85 | 70 | -15 | -17.6
Bare Soil | 31 | 27 | -4 | -12.9

Transition Magnitude

For the dominant transitions identified in the transition matrix, magnitudes are reported:

Transition | Pixels | Area (km2) | Percent of 1990 Class Area
Agriculture to Urban | 89,000 | 80.1 | 36.4
Forest to Bare Soil | 12,500 | 11.25 | 13.2
Bare Soil to Urban | 4,200 | 3.78 | 12.2

Temporal Rates

Average annual change rates are calculated:

Annual Urban Area Change = (2024 Urban Area - 1990 Urban Area) / 34 years

If urban area increased from 45 to 125 km2, the annual rate is (125 - 45) / 34 = 2.35 km2/year, representing the long-term trend.

Quality Assurance for Change Detection
--------------------------------------

Stability Check

In known-stable areas (areas where no change is expected based on reference data), change detection results should show minimal detected change. If significant change is incorrectly detected in truly stable areas, the change detection method requires adjustment (e.g., threshold recalibration).

Consistency Check

Results from post-classification comparison and index differencing should show general agreement. Pixels detected as changed by both methods are more reliable than pixels detected by only one method. Areas of disagreement are investigated to understand the source of discrepancy.

Multi-Method Consensus

A consensus change map is generated by requiring agreement between multiple detection methods (post-classification comparison, NDVI differencing, and NDBI differencing). Pixels flagged by two or three methods are classified as highly confident change; pixels detected by one method are intermediate confidence; pixels detected by no methods are stable.

Change Reporting

Final change detection results are reported in the documentation website with maps, transition matrices, and statistical tables suitable for inclusion in academic publications and policy briefings.
