
# CGM Analyzer

A Python-based Continuous Glucose Monitoring (CGM) analytics platform for diabetes data analysis, prediction, and risk assessment.

---

# Features

## Version 1
- Data loading
- Cleaning and preprocessing

## Version 2
- Statistical analysis
- Descriptive metrics

## Version 3
- Data visualization
- Daily glucose trends

## Version 4
- Multi-horizon glucose prediction
- 5, 30 and 60 minute forecasting

## Version 5
- Hypoglycemia prediction
- Machine learning classification
- Feature importance analysis

## Version 6
- Clinical risk assessment
- Automated reporting system

---

# Dataset

This project uses real Continuous Glucose Monitoring datasets.

Input includes:

- Timestamp
- Glucose values
- Meal information (optional)

---

# Project Structure

```text
CGM_Analyzer/

│
├── data/
│
├── output/
│   ├── glucose_plot.png
│   ├── glucose_histogram.png
│   ├── prediction.png
│   ├── prediction_30.png
│   ├── prediction_60.png
│   ├── hypo_confusion_matrix.png
│   ├── feature_importance.png
│   ├── risk_pie.png
│   └── report.txt
│
├── main.py
├── progress.md
├── requirements.txt
└── README.md