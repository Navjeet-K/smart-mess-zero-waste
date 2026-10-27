Smart Mess, Zero Waste

AI-Powered Food Waste Reduction for College Messes

Smart Mess, Zero Waste** is an AI-based project designed to help college messes estimate student attendance, plan food preparation, and track food waste. The goal is to support better meal planning and reduce avoidable food waste.

🎯 Problem Statement

College messes often prepare food without knowing exactly how many students will attend each meal. This can lead to excess food preparation, leftover food, wasted resources, and unnecessary costs.

Smart Mess, Zero Waste aims to address this problem using machine learning and a simple food-waste tracking dashboard.

## 💡 Proposed Solution

The application provides the following features:

- **AI Attendance Prediction:** Estimates the number of students expected for lunch and dinner.
- **Food Quantity Estimation:** Calculates an estimated amount of food to prepare based on predicted attendance and a configurable portion size.
- **Food Waste Tracking:** Records prepared food, leftover food, plate waste, and the number of students served.
- **Waste Data Visualization:** Displays recorded waste information to help identify patterns.
- **CSV Export:** Allows users to download recorded waste data for further analysis.

## 🤖 AI and Technologies Used

- **Python** — Core programming language
- **Pandas** — Data processing and management
- **NumPy** — Numerical operations and sample data generation
- **Scikit-learn** — Machine learning model development
- **Random Forest Regressor** — Attendance prediction model
- **Streamlit** — Interactive web application
- **GitHub** — Source code management and version control
- **Streamlit Community Cloud** — Application deployment

## ⚙️ How It Works

1. The user selects meal details, including menu type, exam day, and holiday status.
2. The machine learning model predicts expected student attendance for lunch and dinner.
3. The application estimates food requirements using the selected portion size.
4. The user records prepared food, leftovers, plate waste, and actual attendance.
5. Waste records can be reviewed and downloaded as a CSV file.

## 🌍 Sustainable Development Goal

**UN SDG 12: Responsible Consumption and Production**

The project supports more responsible food preparation and resource use by helping kitchens make data-informed decisions and monitor food waste.

## 🚀 Live Demo

[Open Smart Mess, Zero Waste](https://smart-mess-zero-waste-dztycfdsbsueeudjbufydm.streamlit.app/)

Data Collection
      ↓
Data Preprocessing
      ↓
Random Forest Model Training
      ↓
Student Attendance Prediction
      ↓
Food Quantity Estimation
      ↓
Food Waste Tracking
      ↓
Streamlit Dashboard & CSV Reports
      ↓
Goal: Reduce Avoidable Food Waste

## 🛠️ Run the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/Navjeet-K/smart-mess-zero-waste.git
```

### 2. Open the project folder

```bash
cd smart-mess-zero-waste
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## 📂 Project Structure

```text
smart-mess-zero-waste/
├── app.py
├── requirements.txt
└── README.md
```

## ⚠️ Current Limitations

- The current demonstration model is trained on synthetic sample data rather than actual college mess records.
- Its test-set performance does not establish real-world prediction accuracy.
- Food quantity estimates depend on the portion-size assumption selected by the user.
- Waste records are stored in session memory and may be lost when the application restarts.

Real mess data, persistent storage, and real-world testing are needed before using the system for operational decisions.

## 🔮 Future Improvements

- Collect real student attendance and food-waste records.
- Improve attendance predictions using historical meal data.
- Add student meal booking or attendance confirmation.
- Store records in a persistent database.
- Add waste trend reports and food-cost estimates.
- Evaluate the system's impact through a pilot study.

## 👨‍💻 Project Information

**Project Name:** Smart Mess, Zero Waste  
**Domain:** Artificial Intelligence for Sustainability  
**Primary Goal:** Support food waste reduction through AI-assisted meal planning  
**SDG Alignment:** UN SDG 12 — Responsible Consumption and Production

---

*This project is a prototype demonstrating how machine learning and data tracking can support more sustainable food management.*
