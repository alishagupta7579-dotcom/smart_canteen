
import streamlit as st
import pandas as pd

# Website settings
st.set_page_config(
    page_title="Smart Canteen",
    page_icon="🍽️",
    layout="wide"
)

st.title("🍽️ Smart Canteen")
st.subheader("Food Demand and Waste Predictor")
st.write("Analyze food sales and reduce food waste.")

# Load CSV dataset
try:
    df = pd.read_csv("canteen_data.csv")

    # Calculate waste
    df["Waste"] = df["Prepared"] - df["Sold"]

    # Dashboard
    st.header("📊 Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Food Prepared", int(df["Prepared"].sum()))
    col2.metric("Food Sold", int(df["Sold"].sum()))
    col3.metric("Food Waste", int(df["Waste"].sum()))

    # Show complete data
    st.header("📁 Canteen Data")
    st.dataframe(df, use_container_width=True)

    # Food selection
    st.header("🔍 Food Analysis")

    food_list = sorted(df["Food"].dropna().unique())
    food = st.selectbox("Select Food Item", food_list)

    selected = df[df["Food"] == food]

    st.write("###", food, "Analysis")
    st.write("Total Prepared:", int(selected["Prepared"].sum()))
    st.write("Total Sold:", int(selected["Sold"].sum()))
    st.write("Total Waste:", int(selected["Waste"].sum()))

    # Waste chart
    st.header("♻️ Waste by Food Item")
    st.bar_chart(df.groupby("Food")["Waste"].sum())

    # Simple demand estimate
    st.header("🤖 Demand Estimate")

    average_sales = selected["Sold"].mean()

    st.metric(
        "Estimated Demand",
        f"{average_sales:.0f} portions"
    )

    st.info(
        "This is a simple estimate based on average past sales, "
        "not a trained machine-learning prediction."
    )
   ( st.info(...))

    # Holiday records
    st.header("🎉 Holiday Records")

    holiday_data = df[
        df["Holiday"].astype(str).str.strip().str.lower() == "yes"
    ]

    st.dataframe(holiday_data, use_container_width=True)

    # Download processed data
    csv_file = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download Canteen Report",
        data=csv_file,
        file_name="canteen_report.csv",
        mime="text/csv"
    )

except FileNotFoundError:
    st.error(
        "canteen_data.csv not found. "
        "Upload the CSV file in the same project folder."
    )

except Exception as e:
    st.error(f"Something went wrong: {e}")
