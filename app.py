import streamlit as st
import pandas as pd
from datetime import datetime, date
import os

# Setup
st.set_page_config(page_title="Mom's Health Tracker", layout="wide")
DATA_PATH = "data/daily_log.csv"
TODAY = str(date.today())
os.makedirs("data", exist_ok=True)

# Initialize CSV if not exist
if not os.path.exists(DATA_PATH):
    pd.DataFrame(columns=["date", "item", "status", "time", "checked_by"]).to_csv(DATA_PATH, index=False)

# Load CSV
df = pd.read_csv(DATA_PATH)

# Daily checklist
hydration_slots = [
    "Water - Morning (8-9 AM)",
    "Water - Mid Morning (10-11 AM)",
    "Water - Noon (12-1 PM)",
    "Water - Afternoon (2-3 PM)",
    "Water - Evening (4-5 PM)",
    "Water - Dusk (6-7 PM)",
    "Water - Night (8-9 PM)",
    "Water - Before Bed (10 PM)"
]

fruit_items = [
    "Banana (Morning)",
    "Carrot (Raw/Juice)",
    "Orange or Amla (Vitamin C)",
    "Papaya"
]

# UI
st.title("👁️ Mom's Daily Health Tracker")
st.markdown("### 🏥 For Early-Stage Motiabind Care")

username = st.text_input("👤 Who is checking today?", "")

if username:
    st.success(f"Welcome, **{username}**! Please check the completed items for today: {TODAY}")

    st.markdown("## 💧 Hydration Checklist")
    with st.container():
        cols = st.columns(2)
        for idx, item in enumerate(hydration_slots):
            col = cols[idx % 2]
            with col:
                already = df[(df["date"] == TODAY) & (df["item"] == item)]
                if already.empty:
                    if st.checkbox(item, key=item):
                        now = datetime.now().strftime("%H:%M:%S")
                        new_row = pd.DataFrame({
                            "date": [TODAY],
                            "item": [item],
                            "status": ["done"],
                            "time": [now],
                            "checked_by": [username]
                        })
                        df = pd.concat([df, new_row], ignore_index=True)
                        df.to_csv(DATA_PATH, index=False)
                        st.success(f"✅ Marked at {now}")
                else:
                    st.checkbox(item, value=True, key=item, disabled=True)
                    st.caption(f"✓ {already.iloc[0]['time']} by {already.iloc[0]['checked_by']}")

    st.markdown("---")
    st.markdown("## 🍎 Fruit Checklist")
    with st.container():
        cols = st.columns(2)
        for idx, item in enumerate(fruit_items):
            col = cols[idx % 2]
            with col:
                already = df[(df["date"] == TODAY) & (df["item"] == item)]
                if already.empty:
                    if st.checkbox(item, key=item + "_fruit"):
                        now = datetime.now().strftime("%H:%M:%S")
                        new_row = pd.DataFrame({
                            "date": [TODAY],
                            "item": [item],
                            "status": ["done"],
                            "time": [now],
                            "checked_by": [username]
                        })
                        df = pd.concat([df, new_row], ignore_index=True)
                        df.to_csv(DATA_PATH, index=False)
                        st.success(f"✅ Marked at {now}")
                else:
                    st.checkbox(item, value=True, key=item + "_fruit", disabled=True)
                    st.caption(f"✓ {already.iloc[0]['time']} by {already.iloc[0]['checked_by']}")

    st.markdown("## 📊 Summary for Today")

    water_df = df[(df["date"] == TODAY) & (df["item"].isin(hydration_slots))]
    fruit_df = df[(df["date"] == TODAY) & (df["item"].isin(fruit_items))]

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 💦 Water Intake Log")
        st.dataframe(water_df[["item", "time", "checked_by"]], use_container_width=True)

    with col2:
        st.markdown("#### 🍉 Fruits Log")
        st.dataframe(fruit_df[["item", "time", "checked_by"]], use_container_width=True)
else:
    st.warning("👆 Please enter your name above to begin.")
