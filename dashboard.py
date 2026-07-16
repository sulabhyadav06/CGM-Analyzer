import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
st.title(
    "CGM Analyzer Dashboard"
)

uploaded_file = st.file_uploader(
    "Upload CGM File",
    type=["csv","xml"]
)
if uploaded_file:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)

    elif uploaded_file.name.endswith(".xml"):
       

     tree = ET.parse(uploaded_file)
     root = tree.getroot()



        # parsing code here

    rows = []
    glucose_section = root.find("glucose_level")

    for event in glucose_section.iter("event"):

     rows.append({
        "Timestamp": event.get("ts"),
        "Glucose": float(event.get("value"))
    })

    df = pd.DataFrame(rows)

    avg_glucose = df["Glucose"].mean()

    std_glucose = df["Glucose"].std()

    cov = (std_glucose / avg_glucose) * 100

    tir = (
    ((df["Glucose"] >= 70) &
     (df["Glucose"] <= 180))
    .mean() * 100
)

    tar = (
    (df["Glucose"] > 180)
    .mean() * 100
)

    tbr = (
    (df["Glucose"] < 70)
    .mean() * 100
)

    gmi = 3.31 + (0.02392 * avg_glucose)

    hyper_events = (
    (df["Glucose"] > 180)
    .astype(int)
    .diff()
    .eq(1)
    .sum()
)

    hypo_events = (
    (df["Glucose"] < 70)
    .astype(int)
    .diff()
    .eq(1)
    .sum()
)

    df["Timestamp"] = pd.to_datetime(
    df["Timestamp"],
    format="%d-%m-%Y %H:%M:%S"
)

    st.write(df.head())

    summary = pd.DataFrame({
    "Metric":[
        "Average Glucose",
        "Maximum Glucose",
        "Minimum Glucose",
        "TIR",
        "TAR",
        "TBR",
        "GMI",
        "CoV"
    ],
    "Value":[
        avg_glucose,
        df["Glucose"].max(),
        df["Glucose"].min(),
        f"{tir:.1f}%",
        f"{tar:.1f}%",
        f"{tbr:.1f}%",
        f"{gmi:.2f}%",
        f"{cov:.1f}%"
    ]
})

    st.subheader("Summary Metrics")
    st.dataframe(summary)
    col1,col2,col3 = st.columns(3)

    with col1:
      
     st.metric(
        "Average Glucose",
        f"{avg_glucose:.2f}"
    )

    with col2:
     st.metric(
        "TIR",
        f"{tir:.1f}%"
    )

    with col3:
     st.metric(
        "GMI",
        f"{gmi:.2f}%"
    )

    col4,col5,col6 = st.columns(3)

    with col4:
      
     st.metric(
        "TAR",
        f"{tar:.1f}%"
    )

    with col5:
      
     st.metric(
        "TBR",
        f"{tbr:.1f}%"
    )

    with col6:
     st.metric(
        "CoV",
        f"{cov:.1f}%"
    )

    st.metric(
    "Maximum Glucose",
    f"{df['Glucose'].max():.0f}"
)

    col7,col8 = st.columns(2)

    with col7:
     st.metric(
        "Hyper Events",
        hyper_events
    )

    with col8:
     st.metric(
        "Hypo Events",
        hypo_events
    )

    st.metric(
    "Minimum Glucose",
    f"{df['Glucose'].min():.0f}"
)

    col9,col10 = st.columns(2)

    with col9:
     st.metric(
        "Standard Deviation",
        f"{df['Glucose'].std():.2f}"
    )

    tir = (
    (df["Glucose"] >= 70)
    & (df["Glucose"] <= 180)
).mean()*100

    st.metric(
    "Time In Range",
    f"{tir:.1f}%"
)
    
    fig, ax = plt.subplots(figsize=(12,5))

    ax.plot(
    df["Timestamp"],
    df["Glucose"],
    linewidth=1
)
    ax.axhline(
    y=70,
    color="red",
    linestyle="--"
)

    ax.axhline(
    y=180,
    color="red",
    linestyle="--"
)

    ax.set_ylabel("Glucose (mg/dL)")
    ax.set_xlabel("Time")

    st.pyplot(fig)

    risk_score = df["Glucose"].std()
    if risk_score < 20:
        status = "Low Risk"
    elif risk_score < 50:
     status = "Moderate Risk"
    else:
     status = "High Risk"

     st.metric(
    "Risk Category",
    status
)
    st.subheader(
    "Clinical Interpretation"
)

    if tir > 70 and cov < 36:

     st.success(
        "Patient demonstrates relatively stable glucose control."
    )

    elif tir > 50:

     st.warning(
        "Patient shows moderate glycemic variability and may benefit from closer monitoring."
    )

    else:

     st.error(
        "Patient exhibits poor glucose control with elevated glucose variability."
    )

    report = f"""
    Average Glucose : {avg_glucose:.2f}
    Maximum Glucose : {df['Glucose'].max():.0f}
    Minimum Glucose : {df['Glucose'].min():.0f}

    TIR : {tir:.2f}%
    TAR : {tar:.2f}%
    TBR : {tbr:.2f}%

    GMI : {gmi:.2f}%
    CoV : {cov:.2f}%

    Hyper Events : {hyper_events}
    Hypo Events : {hypo_events}

    Risk Category : {status}
    """

    st.download_button(
    "Download Report",
    report,
    file_name=("cgm_report.txt"))