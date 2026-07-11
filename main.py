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

    
