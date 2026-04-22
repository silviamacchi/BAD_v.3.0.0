🔧 <b>BAD PLUGIN 3.0.0</b> - Key Features
<br>
The BAD 3.0.0 plugin introduces new functionalities over BAD 2.0.0 to improve the workflow of burned area detection and validation. These include:

🛰️ Added the possibility to search and download Sentinel-2 L2A, both single images and mosaicking of more images, directly from the plugin.

🔎 ​Added spectral indices computation to feature extraction.

📊 Expanded the customization of OWA parameters.

<br>
🔧 <b>BAD PLUGIN 2.0.0</b> - Key Features
<br>
The BAD 2.0.0 plugin introduces major enhancements over the original version to streamline the workflow of burned area detection and validation. These include:

<br>🎯 SCL Band Masking
Perform masking of unwanted Scene Classification Layer (SCL) classes from Sentinel-2 imagery for both pre-fire and post-fire datasets. This removes noise (e.g., clouds, water, snow) and improves classification accuracy.

🛰️ OWA Layer Preview
Visually inspect Ordered Weighted Averaging (OWA) layers to help select optimal threshold values for generating seed and grow layers. An interactive preview allows accurate threshold tuning using real-time image feedback.

✅ Burned Area Map Validation
Validate the burned area output by comparing with reference data using a confusion matrix. Compute accuracy metrics such as commission/omission errors and the Dice coefficient, and generate a pixel-wise Agreement Map.

🔥 Burn Severity Validation
Validate burn severity output by reclassifying and comparing the severity layer with reference data, including full error matrix evaluation and export of metrics for reporting.

📦 Modular Workflow
Each tab in the plugin works independently—users can start at any stage (e.g., OWA, Region Growing) using intermediate inputs, enhancing flexibility and efficiency.

📊 Export of Validation Results
All validation results, including accuracy metrics and confusion matrices, are exportable in .html format for inclusion in reports or publications.

🌐 QGIS Native
Fully integrated within the QGIS environment with a PyQt-based graphical interface and support for native raster and vector operations.