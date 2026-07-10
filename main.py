print("start")
import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
import os

# -------------------------
# Load XML File
# -------------------------

tree = ET.parse("data/559-ws-training.xml")
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

plt.figure(figsize=(15,5))

plt.figure(figsize=(16,6))

# Plot only the first 500 readings
sample = df.iloc[:500]

plt.plot(
    sample["Timestamp"],
    sample["Glucose"],
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

plt.savefig("output/glucose_plot.png")

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