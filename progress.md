# CGM Analyzer Progress

---

# Version 1.0 
Date: 10 July 2026

## Objective
Build a CGM analysis system using real Type 1 Diabetes data.

## Completed Features

### Dataset
- Downloaded OhioT1DM dataset
- Worked with real XML CGM files
- Understood research-grade diabetes datasets

### Data Processing
- Parsed XML files using ElementTree
- Extracted glucose readings and timestamps
- Converted data into pandas DataFrame
- Converted timestamps into datetime format

### Visualization
- Generated CGM glucose trend plots
- Added glucose thresholds:
  - Hypoglycemia line (70 mg/dL)
  - Hyperglycemia line (180 mg/dL)

### Clinical Metrics
Calculated:

- Average Glucose
- Maximum Glucose
- Minimum Glucose
- Time In Range (TIR)
- Time Above Range (TAR)
- Time Below Range (TBR)
- Hypoglycemia Events
- Hyperglycemia Events
- Standard Deviation (SD)
- Coefficient of Variation (CV)
- Glucose Management Indicator (GMI)

## Current Results (Patient 559)

Average Glucose: 166.69 mg/dL

Maximum Glucose: 400 mg/dL

Minimum Glucose: 40 mg/dL

Time In Range (TIR): 56.23%

Hypoglycemia Events: 409

Hyperglycemia Events: 4316

## Skills Learned

- Python
- Pandas
- Matplotlib
- XML Parsing
- Biomedical Time-Series Analysis
- Research Dataset Handling
- Debugging and Project Structure
- Git Basics

---

# Version 1.1 (Next)

## Goals

- Histogram of glucose values
- Time-in-range pie chart
- Daily glucose profiles
- Daily statistics
- Automatic report generation
- Missing data handling

## Version 1.1

Added:
- Data quality analysis
- Detection of missing CGM intervals
- Maximum gap analysis
- Handling of large gaps before plotting
- Improved visualization by preventing misleading lines

Results:
- Maximum missing gap: 13 hours 3 minutes
- Number of large gaps: X

# Version 1.2 
Date: 10 July 2026

### Daily Statistics Added

For every day:

- Daily average glucose
- Daily maximum glucose
- Daily minimum glucose

### Report Generation

Automatically saves results into:

output/report.txt

### Example Report

- Average glucose
- Time in Range
- TAR
- TBR
- SD
- CV
- GMI
- Daily statistics

### Notes
Learned:

- Grouping data by date
- Exporting results to text files
- Building reusable reports

---

# Version 2.0 (In Progress)

### Advanced Visualizations Added

✅ Glucose Histogram

Shows glucose distribution.

✅ Time in Different Glucose Ranges Pie Chart

Displays:

- Below Range
- In Range
- Above Range

### Remaining Tasks

⬜ Daily Average Trend Graph

---

# Version 2.1  Planned

### Multi-Patient Support

Goals:

- Allow user to select any patient XML file
- Remove hardcoded filename
- Analyze multiple patients automatically
- Compare different patients

---

# Future Roadmap

## Version 3.0
- Meal analysis
- Insulin analysis
- Activity analysis

## Version 4.0
- Hypoglycemia prediction
- Hyperglycemia prediction
- Machine Learning models

## Version 5.0
- Interactive Dashboard
- Streamlit Web App
- Patient comparison dashboard
- Deployment

# Version 2.1

## Added
- Multi-patient support
- User can select XML file at runtime
- Patient-specific reports
- Patient-specific plots
- Automatic file listing

## Output Example
report_559-ws-training.txt
report_591-ws-training.txt
glucose_plot_559-ws-training.png
glucose_plot_591-ws-training.png
tir_pie_559-ws-training.png
tir_pie_591-ws-training.png

Status: Completed 

# Version 3.0

Added:

- Meal extraction
- Meal DataFrame
- Daily carbohydrate statistics
- Meal type statistics
- Daily carbohydrate visualization
- Post-meal glucose spike analysis
- Carbohydrate-spike correlation

## Version 4.0
Created lag features
Trained first ML model
Predicted future glucose
Calculated MAE
Generated prediction plots

## Version 4.1

 30 minute prediction
 60 minute prediction
 Multi-horizon forecasting
 Compared prediction errors
 Added new prediction plots

 # Version 5.0

Added:

- Hypoglycemia warning system
- Binary classification target
- Random Forest classifier
- Accuracy calculation
- Confusion matrix
- Precision / Recall / F1 metrics

## Version 5.1 - Model Tuning

Changes:
- Increased Random Forest estimators from 100 → 200.
- Reduced false positives from 45 → 38.

Results:
Accuracy: 96.12%
Precision (Hypo): 0.19
Recall (Hypo): 0.16
F1 Score: 0.18

Observation:
Overall accuracy improved slightly but hypoglycemia recall remained low due to severe class imbalance.

