print("start")


import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
import os

filename = input(
    "Enter XML filename: "
)
patient_id = filename.replace(".xml", "")

print("\nAvailable Files:\n")

for file in os.listdir("data"):
    if file.endswith(".xml"):
        print(file)

# -------------------------
# Load XML File
# -------------------------

tree = ET.parse(
    f"data/{filename}"
)
root = tree.getroot()

timestamps = []
glucose = []

# -------------------------
# Read CGM Events
# -------------------------

for event in root.find("glucose_level"):

    timestamps.append(event.attrib["ts"])
    glucose.append(int(event.attrib["value"]))

# -------------------------
# Create DataFrame
# -------------------------

df = pd.DataFrame({
    "Timestamp": timestamps,
    "Glucose": glucose
})

df["Timestamp"] = pd.to_datetime(
    df["Timestamp"],
    format="%d-%m-%Y %H:%M:%S"
)

# -------------------------
# Statistics
# -------------------------

average = df["Glucose"].mean()
maximum = df["Glucose"].max()
minimum = df["Glucose"].min()

tir = (
    (df["Glucose"] >= 70) &
    (df["Glucose"] <= 180)
).mean()*100

hypo = (df["Glucose"] < 70).sum()
hyper = (df["Glucose"] > 180).sum()

# -------------------------
# Print
# -------------------------

print("="*40)
print("CGM ANALYSIS REPORT")
print("="*40)

print(f"Average : {average:.2f}")
print(f"Maximum : {maximum}")
print(f"Minimum : {minimum}")
print(f"Time in Range : {tir:.2f}%")
print(f"Hypoglycemia : {hypo}")
print(f"Hyperglycemia : {hyper}")

# -------------------------
# Plot
# -------------------------

plt.figure(figsize=(16,6))

df_plot = df.copy()

gaps = (
    df_plot["Timestamp"].diff()
    > pd.Timedelta(minutes=10)
)

df_plot.loc[gaps, "Glucose"] = None

print("Maximum gap:",
      df["Timestamp"].diff().max())

print("Number of large gaps:",
      gaps.sum())

# Plot only the first 500 readings
sample_plot = df_plot.iloc[:500]

plt.plot(
    sample_plot["Timestamp"],
    sample_plot["Glucose"],
    color="blue",
    linewidth=2
)

plt.axhline(70, color="red", linestyle="--", label="Low (70)")
plt.axhline(180, color="green", linestyle="--", label="High (180)")

plt.title("CGM Glucose Trend")
plt.xlabel("Time")
plt.ylabel("Glucose (mg/dL)")
plt.legend()

plt.xticks(rotation=45)
plt.tight_layout()

plt.axhline(70, linestyle="--")
plt.axhline(180, linestyle="--")

plt.title("CGM Data")

plt.xlabel("Time")

plt.ylabel("Glucose (mg/dL)")

plt.xticks(rotation=45)

plt.tight_layout()

os.makedirs("output", exist_ok=True)

plt.savefig(
    f"output/glucose_plot_{patient_id}.png"
)

plt.show()

plt.figure(figsize=(8,5))

plt.hist(
    df["Glucose"],
    bins=30
)

plt.axvline(70, linestyle="--")

plt.axvline(180, linestyle="--")

plt.xlabel("Glucose (mg/dL)")
plt.ylabel("Frequency")

plt.title("Glucose Distribution")

plt.savefig(
    f"output/glucose_histogram_{patient_id}.png"
)

plt.show()

tbr = (df["Glucose"] < 70).mean() * 100

tar = (df["Glucose"] > 180).mean() * 100

labels = [
    "Below Range (<70)",
    "In Range (70-180)",
    "Above Range (>180)"
]

sizes = [tbr, tir, tar]

plt.figure(figsize=(7,7))

plt.pie(
    sizes,
    labels=labels,
    autopct="%1.1f%%"
)

plt.title("Time in Different Glucose Ranges")

plt.savefig(
    f"output/tir_pie_{patient_id}.png"
)

plt.show()

df["Date"] = df["Timestamp"].dt.date

daily_avg = (
    df.groupby("Date")["Glucose"]
    .mean()
)

plt.figure(figsize=(12,5))

plt.plot(
    daily_avg.index,
    daily_avg.values,
    marker="o"
)

plt.title("Daily Average Glucose")

plt.xlabel("Date")
plt.ylabel("Average Glucose (mg/dL)")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    f"output/daily_average_{patient_id}.png"
)

plt.show()
tar = (df["Glucose"] > 180).mean()*100
tbr = (df["Glucose"] < 70).mean()*100
std = df["Glucose"].std()
cv = (std / average) * 100
gmi = 3.31 + (0.02392 * average)

print(f"Time Above Range : {tar:.2f}%")
print(f"Time Below Range : {tbr:.2f}%")
print(f"Standard Deviation : {std:.2f}")
print(f"Coefficient of Variation : {cv:.2f}%")
print(f"Estimated GMI : {gmi:.2f}%")

df["TimeDiff"] = df["Timestamp"].diff()

print(df["TimeDiff"].max())

df["Date"] = df["Timestamp"].dt.date

daily_stats = (
    df.groupby("Date")["Glucose"]
    .agg(["mean", "max", "min"])
)

print(daily_stats)

with open(
    f"output/report_{patient_id}.txt",
    "w"
) as f:
    f.write("CGM ANALYSIS REPORT\n")
    f.write("="*40 + "\n")
    f.write(f"Average Glucose: {average:.2f}\n")
    f.write(f"Maximum Glucose: {maximum}\n")
    f.write(f"Minimum Glucose: {minimum}\n")
    f.write(f"Time In Range: {tir:.2f}%\n")
    f.write(f"Time Above Range: {tar:.2f}%\n")
    f.write(f"Time Below Range: {tbr:.2f}%\n")
    f.write(f"Standard Deviation: {std:.2f}\n")
    f.write(f"Coefficient of Variation: {cv:.2f}%\n")
    f.write(f"GMI: {gmi:.2f}%\n")

    print("Report saved successfully!")

#version 3 , meal analysis

#meal dataframe
meal_times = []
meal_types = []
meal_carbs = []

for meal in root.find("meal"):

    meal_times.append(
        meal.attrib["ts"]
    )

    meal_types.append(
        meal.attrib["type"]
    )

    meal_carbs.append(
        int(meal.attrib["carbs"])
    )

    meal_df = pd.DataFrame({
    "Timestamp": meal_times,
    "Meal Type": meal_types,
    "Carbs": meal_carbs
})
    
    meal_df["Timestamp"] = pd.to_datetime(
    meal_df["Timestamp"],
    format="%d-%m-%Y %H:%M:%S"
)
    
print("\nMeal Statistics")

print(
    "Total Meals:",
    len(meal_df)
)

print(
    "Average Carbs:",
    meal_df["Carbs"].mean()
)

#Meal type distribution

print(
    meal_df["Meal Type"]
    .value_counts()
)

#Daily carb intake

meal_df["Date"] = (
    meal_df["Timestamp"]
    .dt.date
)

daily_carbs = (
    meal_df
    .groupby("Date")
    ["Carbs"]
    .sum()
)

print("\nDaily Carbohydrate Intake")
print(daily_carbs)

#Visualisation

plt.figure(figsize=(12,5))

plt.plot(
    daily_carbs.index,
    daily_carbs.values,
    marker="o"
)

plt.title(
    "Daily Carbohydrate Intake"
)

plt.ylabel("Carbs (g)")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    f"output/carbs_{patient_id}.png"
)

plt.show()

#post meal glucose rise

meal_spikes = []
for _, meal in meal_df.iterrows():

    meal_time = meal["Timestamp"]

    future = df[
        (df["Timestamp"] >= meal_time)
        &
        (
            df["Timestamp"]
            <= meal_time
            + pd.Timedelta(hours=2)
        )
    ]

    if len(future) == 0:
        meal_spikes.append(None)
        continue

    start = future.iloc[0]["Glucose"]

    peak = future["Glucose"].max()

    rise = peak - start

    meal_spikes.append(rise)
    
#print(len(meal_df))
#print(len(meal_spikes))

meal_df["Spike"] = meal_spikes

print(
    meal_df[
        ["Meal Type",
         "Carbs",
         "Spike"]
    ]
)

#correlation

corr = (
    meal_df["Carbs"]
    .corr(
        meal_df["Spike"]
    )
)

print(
    "Carbs-Spike Correlation:",
    corr
)

#version 4
# 1 create lag features

df["lag1"] = df["Glucose"].shift(1)
df["lag2"] = df["Glucose"].shift(2)
df["lag3"] = df["Glucose"].shift(3)

df_ml = df.dropna()

#import
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from imblearn.over_sampling import SMOTE

#3 create x and y
X = df_ml[
    ["lag1","lag2","lag3"]
]

y = df_ml["Glucose"]

#4 split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    shuffle=False
)

#5 train model
model = LinearRegression()
model.fit(
    X_train,
    y_train
)

#6 predict
pred = model.predict(X_test)

#7 evaluate
mae = mean_absolute_error(
    y_test,
    pred
)

print(
    "\nPrediction MAE:",
    round(mae,2),
    "mg/dL"
)

#8 plot predictions vs actual
plt.figure(figsize=(12,5))

plt.plot(
    y_test.values[:300],
    label="Actual"
)

plt.plot(
    pred[:300],
    label="Predicted"
)

plt.legend()

plt.title(
    "Glucose Prediction"
)

plt.savefig(
    "output/prediction.png"
)

plt.show()

#version 4.1
#1 create future targets
df["target_30"] = df["Glucose"].shift(-6)

df["target_60"] = df["Glucose"].shift(-12)

#2 create clean datasets
df30 = df.dropna()

df60 = df.dropna()

#3 30 min prediction
X30 = df30[
    ["lag1","lag2","lag3"]
]

y30 = df30["target_30"]

X_train, X_test, y_train, y_test = train_test_split(
    X30,
    y30,
    test_size=0.2,
    shuffle=False
)

model30 = LinearRegression()

model30.fit(
    X_train,
    y_train
)

pred30 = model30.predict(X_test)

mae30 = mean_absolute_error(
    y_test,
    pred30
)

print(
    "\n30 min MAE:",
    round(mae30,2)
)

#4 60 min prediction
X60 = df60[
    ["lag1","lag2","lag3"]
]

y60 = df60["target_60"]

model60 = LinearRegression()

X_train60, X_test60, y_train60, y_test60 = train_test_split(
    X60,
    y60,
    test_size=0.2,
    shuffle=False
)

model60.fit(
    X_train60,
    y_train60
)

pred60 = model60.predict(
    X_test60
)

mae60 = mean_absolute_error(
    y_test60,
    pred60
)

print(
    "\n60 min MAE:",
    round(mae60,2)
)

#5 compare all models
print("\nPrediction Summary")

print("5 min MAE :", round(mae,2))

print("30 min MAE:", round(mae30,2))

print("60 min MAE:", round(mae60,2))

#6 plot all predictions
plt.figure(figsize=(12,5))

plt.plot(
    y_test.values[:300],
    label="Actual"
)

plt.plot(
    pred30[:300],
    label="30min Prediction"
)

plt.legend()

plt.title(
    "30 Minute Prediction"
)

plt.savefig(
    "output/prediction_30.png"
)

plt.show()

plt.figure(figsize=(12,5))

plt.plot(
    y_test60.values[:300],
    label="Actual"
)

plt.plot(
    pred60[:300],
    label="60min Prediction"
)

plt.legend()

plt.title(
    "60 Minute Prediction"
)

plt.savefig(
    "output/prediction_60.png"
)

plt.show()


#version 5
#create target variable
df["future_glucose"] = (
    df["Glucose"]
    .shift(-6)
)
df["Hypo_30"] = (
    df["future_glucose"] < 70
).astype(int)
#2 features
df["delta1"] = df["Glucose"].diff(1)

df["delta2"] = df["Glucose"].diff(2)

df["rolling_mean"] = (
    df["Glucose"]
    .rolling(3)
    .mean()
)

df["rolling_std"] = (
    df["Glucose"]
    .rolling(3)
    .std()
)

df["minimum"] = (
    df["Glucose"]
    .rolling(3)
    .min()
)
df=df.dropna()
X = df[
[
    "lag1",
    "lag2",
    "lag3",
    "delta1",
    "delta2",
    "rolling_mean",
    "rolling_std",
    "minimum"
]
]

df_hypo = df.dropna()

X = df_hypo[
    [
        "lag1",
        "lag2",
        "lag3",
        "delta1",
        "delta2",
        "rolling_mean",
        "rolling_std",
        "minimum"
    ]
]

y = df_hypo["Hypo_30"]

#3 train/test split
X_train, X_test, y_train, y_test = (
    train_test_split(
        X,
        y,
        test_size=0.2,
        shuffle=False
    )
)
#4classification model
from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(
    n_estimators=200,
    class_weight="balanced_subsample",
    random_state=42,
    max_depth=12,
    min_samples_leaf=5
)
sm = SMOTE(random_state=42,k_neighbors=3)
X_train, y_train = sm.fit_resample(X_train, y_train)

clf.fit(
    X_train,
    y_train
)
#5 predictions
pred = clf.predict(X_test)

#6 evaluation
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
)
acc = accuracy_score(
    y_test,
    pred
)

print(
    "\nHypoglycemia Prediction Accuracy:",
    round(acc*100,2),
    "%"
)

print(
    "\nConfusion Matrix"
)

print(
    confusion_matrix(
        y_test,
        pred
    )
)
#7 print
print(
    classification_report(
        y_test,
        pred
    )
)
#8 visualisation
import seaborn as sns

cm = confusion_matrix(
    y_test,
    pred
)

plt.figure(figsize=(5,5))

sns.heatmap(
    cm,
    annot=True,
    fmt="d"
)

plt.title(
    "Hypoglycemia Prediction"
)

plt.savefig(
    "output/hypo_confusion.png"
)

plt.show()

from sklearn.metrics import (
    recall_score,
    precision_score,
    f1_score
)

df["delta1"] = df["lag1"] - df["lag2"]

df["delta2"] = df["lag2"] - df["lag3"]

df["rolling_mean"] = (
    df[["lag1","lag2","lag3"]]
    .mean(axis=1)
)

df["rolling_std"] = (
    df[["lag1","lag2","lag3"]]
    .std(axis=1)
)

df["minimum"] = (
    df[["lag1","lag2","lag3"]]
    .min(axis=1)
)
X = df[
[
    "lag1",
    "lag2",
    "lag3",
    "delta1",
    "delta2",
    "rolling_mean",
    "rolling_std",
    "minimum"
]
]

#version 6
#1 daily risk score
risk = (
    (100 - tir) * 0.4
    + tbr * 2
    + cv * 0.5
)
if risk < 20:
    status = "Low Risk"

elif risk < 50:
    status = "Moderate Risk"

else:
    status = "High Risk"

print(
    f"\nRisk Score: {risk:.2f}"
)

print(
    f"Risk Category: {status}"
)


#2 glucose zone distribution plot
labels = [
    "Hypoglycemia",
    "Target Range",
    "Hyperglycemia"
]

sizes = [
    tbr,
    tir,
    tar
]

plt.figure(figsize=(7,7))

plt.pie(
    sizes,
    labels=labels,
    autopct="%1.1f%%"
)

plt.title(
    "Glucose Zone Distribution"
)

plt.savefig(
    "output/risk_pie.png"
)
plt.show()

#4 feature importance plot
importance = clf.feature_importances_

features = X.columns

plt.barh(
    features,
    importance
)
plt.xlabel("Importance")

plt.title(
    "Feature Importance"
)

plt.tight_layout()

plt.savefig(
    "output/feature_importance.png"
)
plt.show()


#DETAILED REPORT
with open("output/report.txt", "w") as f:
    f.write(f"Maximum Glucose : {maximum} mg/dL\n")
    f.write(f"Minimum Glucose : {minimum} mg/dL\n\n")

    f.write("CGM ANALYSIS REPORT\n")
    f.write("=" * 40 + "\n\n")

    f.write(f"Source File : {filename}\n")
    f.write(f"Patient ID : {filename.split('.')[0]}\n")
    f.write(f"Generated On : {pd.Timestamp.now()}\n\n")

    # General Statistics
    f.write("GENERAL STATISTICS\n")
    f.write("-" * 25 + "\n")
    f.write(f"Average Glucose : {average:.2f} mg/dL\n")

    # Time in Range
    f.write("TIME IN RANGES\n")
    f.write("-" * 25 + "\n")
    f.write(f"Time In Range (70-180) : {tir:.2f}%\n")
    f.write(f"Time Above Range : {tar:.2f}%\n")
    f.write(f"Time Below Range : {tbr:.2f}%\n\n")
    f.write(f"Standard Deviation : {std:.2f} mg/dL\n")
    f.write(f"Coefficient of Variation : {cv:.2f}%\n")
    f.write(f"Estimated GMI : {gmi:.2f}%\n\n")
    # Events
    f.write("EVENT COUNTS\n")
    f.write("-" * 25 + "\n")
    f.write(f"Hypoglycemia Events : {hypo}\n")
    f.write(f"Hyperglycemia Events : {hyper}\n\n")

    # Data Quality
    f.write("DATA QUALITY\n")
    f.write("-" * 25 + "\n")
    f.write(f"Maximum Gap : {df['Timestamp'].diff().max()}\n")
    f.write(f"Number of Large Gaps : {gaps.sum()}\n\n")

    # Meal Statistics
    f.write("MEAL ANALYSIS\n")
    f.write("-" * 25 + "\n")
    f.write(f"Total Meals : {len(meal_df)}\n")
    f.write(f"Average Carbs : {meal_df['Carbs'].mean():.2f} g\n")
    f.write(f"Carb-Spike Correlation : {corr:.3f}\n\n")

    # Prediction Results
    f.write("PREDICTION RESULTS\n")
    f.write("-" * 25 + "\n")
    f.write(f"5 min MAE : {mae:.2f} mg/dL\n")
    f.write(f"30 min MAE : {mae30:.2f} mg/dL\n")
    f.write(f"60 min MAE : {mae60:.2f} mg/dL\n\n")

    # Interpretation
    f.write("INTERPRETATION\n")
    f.write("-" * 25 + "\n")

    if tir >= 70:
        f.write("Excellent glucose control.\n")
    elif tir >= 50:
        f.write("Moderate glucose control.\n")
    else:
        f.write("Poor glucose control.\n")

    f.write(
        "Prediction error increases with longer prediction horizons.\n"
    )

    f.write("\nHYPOGLYCEMIA WARNING MODEL\n")
    f.write("=========================\n")
    f.write(f"Accuracy : {acc*100:.2f} %\n")
    f.write(f"Precision : "
    f"{precision_score(y_test, pred):.2f}\n")
    f.write(f"Recall : "f"{recall_score(y_test, pred):.2f}\n")
    f.write(f"F1 Score : "
    f"{f1_score(y_test, pred):.2f}\n")
    cm = confusion_matrix(y_test, pred)

    f.write("\nConfusion Matrix\n")
    f.write("----------------\n")
    f.write(str(cm))
    f.write("\n")

    # Interpretation
    tn, fp, fn, tp = cm.ravel()

    f.write("\nInterpretation\n")
    f.write("--------------\n")
    f.write(f"Detected hypo events : {tp}\n")
    f.write(f"Missed hypo events : {fn}\n")
    f.write(f"False alarms : {fp}\n")
    f.write(f"Detection Rate : "
    f"{tp/(tp+fn)*100:.2f}%\n")

    # Final insights
    f.write("\nKey Findings\n")
    f.write("------------\n")

    f.write("Prediction error increases with "
    "longer prediction horizons.\n")

    f.write("Carbohydrate intake alone shows "
    "weak correlation with glucose spikes.\n")

    f.write("Hypoglycemia model successfully "
    "detects most low glucose events.\n")

    # ==========================
    # RISK ASSESSMENT
    # ==========================

    f.write("\nRISK ASSESSMENT\n")
    f.write("=========================\n")

    f.write(
    f"Daily Risk Score : "
    f"{risk:.2f}\n"
    )

    f.write(
    f"Risk Category : "
    f"{status}\n"
    )

    f.write("\nInterpretation\n")
    f.write("-------------------------\n")

    if status == "Low Risk":

     f.write(
        "Patient demonstrates relatively "
        "stable glucose control.\n"
    )
    
    elif status == "Moderate Risk":

     f.write(
        "Patient shows moderate glycemic "
        "variability and may benefit from "
        "closer monitoring.\n"
    )

    else:
     f.write(
        "Patient exhibits high glucose "
        "variability and elevated risk of "
        "adverse glycemic events.\n"
    )

     f.write(
    "Risk score incorporates time in range, "
    "time below range, and glucose variability.\n"
    )
     f.write("\nCLINICAL RECOMMENDATIONS\n")
     f.write("========================\n")

    if status == "Low Risk":
     f.write("- Continue current therapy.\n")

    elif status == "Moderate Risk":
     f.write("- Increase monitoring frequency.\n")
     f.write("- Review insulin dosing patterns.\n")

    else:
     f.write("- Consider immediate clinical review.\n")
     f.write("- Investigate recurrent hypoglycemia.\n")

    confidence = recall_score(y_test, pred) * 100

    f.write(
    f"\nHypoglycemia Detection Confidence : "
    f"{confidence:.2f}%\n"
)

    f.write(
"\n====================================\n"
"Report generated automatically by\n"
"CGM Analyzer Version 6\n"
"Author: Sulabh Yadav\n"
"====================================\n"
)

print("Report saved successfully!")





