import streamlit as st
import pandas as pd
import numpy as np
from datetime import date
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

st.set_page_config(
    page_title="Smart Mess, Zero Waste",
    page_icon="🌱",
    layout="wide"
)

# ---------------------------
# Generate illustrative data
# ---------------------------
@st.cache_resource
def train_model():
    rng = np.random.default_rng(42)
    dates = pd.date_range("2025-01-01", "2025-12-31")
    rows = []

    for d in dates:
        for meal in ["Lunch", "Dinner"]:
            weekend = int(d.dayofweek >= 5)
            exam = int(rng.random() < 0.15)
            holiday = int(rng.random() < 0.05)
            menu = rng.choice(["Regular", "Special", "Light"])

            attendance = 300 - 35 * weekend - 15 * exam - 100 * holiday
            attendance += 25 if menu == "Special" else 0
            attendance -= 15 if menu == "Light" else 0
            attendance -= 10 if meal == "Dinner" else 0
            attendance += rng.normal(0, 15)

            rows.append({
                "date": d,
                "day_type": "Weekend" if weekend else "Weekday",
                "meal": meal,
                "menu_type": menu,
                "exam_day": exam,
                "holiday": holiday,
                "month": d.month,
                "day_of_week": d.dayofweek,
                "actual_students": int(np.clip(attendance, 0, 500))
            })

    df = pd.DataFrame(rows)
    split = int(len(df) * 0.8)
    train = df.iloc[:split]
    test = df.iloc[split:]

    features = [
        "day_type", "meal", "menu_type",
        "exam_day", "holiday", "month", "day_of_week"
    ]
    cats = ["day_type", "meal", "menu_type"]
    nums = ["exam_day", "holiday", "month", "day_of_week"]

    prep = ColumnTransformer([
        ("cats", OneHotEncoder(handle_unknown="ignore"), cats),
        ("nums", "passthrough", nums)
    ])

    model = Pipeline([
        ("prep", prep),
        ("rf", RandomForestRegressor(
            n_estimators=100, random_state=42
        ))
    ])

    model.fit(train[features], train["actual_students"])
    error = mean_absolute_error(
        test["actual_students"], model.predict(test[features])
    )

    return model, error

model, demo_mae = train_model()

# ---------------------------
# App heading
# ---------------------------
st.title("🌱 Smart Mess, Zero Waste")
st.write(
    "AI-assisted meal planning to estimate attendance "
    "and help reduce avoidable food waste."
)
st.caption(
    "Demo version: predictions use synthetic sample data, "
    "not actual college attendance."
)

# ---------------------------
# Sidebar settings
# ---------------------------
st.sidebar.header("⚙️ Mess Settings")
portion = st.sidebar.number_input(
    "Prepared food per student (kg)",
    min_value=0.05,
    max_value=1.00,
    value=0.30,
    step=0.05
)
st.sidebar.caption("Adjust this assumption to match your mess.")

today = date.today()
day_type = "Weekend" if today.weekday() >= 5 else "Weekday"

st.sidebar.info(f"Date: {today.strftime('%d %b %Y')}")

# ---------------------------
# AI predictions
# ---------------------------
st.header("🍽️ Today's AI Food Planner")

col1, col2 = st.columns(2)

with col1:
    lunch_menu = st.selectbox(
        "Lunch menu",
        ["Regular", "Special", "Light"]
    )
    lunch_exam = st.checkbox("Exam day for lunch")
    lunch_holiday = st.checkbox("Holiday / low attendance for lunch")

with col2:
    dinner_menu = st.selectbox(
        "Dinner menu",
        ["Regular", "Special", "Light"],
        index=1
    )
    dinner_exam = st.checkbox("Exam day for dinner")
    dinner_holiday = st.checkbox("Holiday / low attendance for dinner")

if st.button("🔮 Predict attendance", type="primary"):
    inputs = pd.DataFrame([
        {
            "day_type": day_type, "meal": "Lunch",
            "menu_type": lunch_menu,
            "exam_day": int(lunch_exam),
            "holiday": int(lunch_holiday),
            "month": today.month, "day_of_week": today.weekday()
        },
        {
            "day_type": day_type, "meal": "Dinner",
            "menu_type": dinner_menu,
            "exam_day": int(dinner_exam),
            "holiday": int(dinner_holiday),
            "month": today.month, "day_of_week": today.weekday()
        }
    ])

    preds = np.clip(np.round(model.predict(inputs)), 0, 500).astype(int)

    st.session_state["predictions"] = {
        "Lunch": int(preds[0]),
        "Dinner": int(preds[1])
    }
    st.session_state["food_kg"] = {
        "Lunch": round(int(preds[0]) * portion, 1),
        "Dinner": round(int(preds[1]) * portion, 1)
    }

if "predictions" in st.session_state:
    p = st.session_state["predictions"]
    f = st.session_state["food_kg"]

    a, b, c = st.columns(3)
    a.metric("Lunch students", p["Lunch"])
    b.metric("Dinner students", p["Dinner"])
    c.metric("Estimated food", f["Lunch"] + f["Dinner"], "kg total")

    chart = pd.DataFrame({
        "Meal": ["Lunch", "Dinner"],
        "Predicted students": [p["Lunch"], p["Dinner"]]
    }).set_index("Meal")
    st.bar_chart(chart)

    st.subheader("Recommended preparation estimate")
    st.dataframe(pd.DataFrame({
        "Meal": ["Lunch", "Dinner"],
        "Predicted students": [p["Lunch"], p["Dinner"]],
        "Food estimate (kg)": [f["Lunch"], f["Dinner"]]
    }), use_container_width=True)

    st.caption(
        "Food estimates are calculated from your chosen portion assumption. "
        "Verify actual portions before using for kitchen decisions."
    )
else:
    st.info("Select meal details above and click Predict attendance.")

# ---------------------------
# Waste tracker
# ---------------------------
st.divider()
st.header("♻️ Daily Waste Tracker")
st.write("Record what was prepared and what remained after each meal.")

if "waste_records" not in st.session_state:
    st.session_state["waste_records"] = []

with st.form("waste_form"):
    meal = st.selectbox("Meal to record", ["Lunch", "Dinner"])
    prepared = st.number_input(
        "Food prepared (kg)", min_value=0.0, value=0.0, step=1.0
    )
    leftover = st.number_input(
        "Food left over (kg)", min_value=0.0, value=0.0, step=0.5
    )
    plate_waste = st.number_input(
        "Plate waste (kg), if measured",
        min_value=0.0, value=0.0, step=0.5
    )
    diners = st.number_input(
        "Actual students served", min_value=0, value=0, step=1
    )
    submitted = st.form_submit_button("Save waste record")

    if submitted:
        if leftover > prepared:
            st.error("Leftover food cannot exceed prepared food.")
        elif plate_waste > prepared:
            st.error("Plate waste cannot exceed prepared food.")
        else:
            st.session_state["waste_records"].append({
                "Date": str(today),
                "Meal": meal,
                "Prepared (kg)": prepared,
                "Leftover (kg)": leftover,
                "Plate waste (kg)": plate_waste,
                "Students served": diners
            })
            st.success("Record added for this session.")

if st.session_state["waste_records"]:
    waste_df = pd.DataFrame(st.session_state["waste_records"])
    st.dataframe(waste_df, use_container_width=True)

    total_leftover = waste_df["Leftover (kg)"].sum()
    st.metric("Recorded leftover food", f"{total_leftover:.1f} kg")

    csv = waste_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download waste records (CSV)",
        data=csv,
        file_name="mess_waste_records.csv",
        mime="text/csv"
    )
else:
    st.caption("No waste records entered yet.")

# ---------------------------
# Model information
# ---------------------------
with st.expander("About this AI model"):
    st.write(
        "Model: Random Forest Regressor. "
        "Inputs: meal, menu type, weekday/weekend, month, exam and holiday flags."
    )
    st.write(f"Demo test-set MAE: {demo_mae:.1f} students.")
    st.warning(
        "Both training and test data are synthetic. "
        "This metric does not establish real-world accuracy. "
        "Waste records are kept in session memory and may disappear "
        "when the app restarts. Use real records and persistent storage "
        "before relying on this for operational decisions."
    )
