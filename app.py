import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="AI Medical Diagnosis Expert System",
    page_icon="🩺",
    layout="wide"
)

st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}

.stButton>button {
    width: 100%;
    border-radius: 10px;
    height: 3em;
    font-size: 16px;
}

.diagnosis-box {
    padding: 20px;
    border-radius: 15px;
    background-color: #ffffff;
    margin-bottom: 15px;
    box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
}

.big-font {
    font-size:20px !important;
    font-weight:bold;
}
</style>
""", unsafe_allow_html=True)

st.title("🩺 Intelligent Medical Diagnosis Expert System")
st.markdown("### Ontology-Based Knowledge Expert System with Forward Chaining")

# Sidebar
st.sidebar.title("Patient Information")

name = st.sidebar.text_input("Patient Name")
age = st.sidebar.number_input("Age", 1, 120, 25)
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])

st.sidebar.markdown("---")

st.sidebar.subheader("Vital Signs")

temperature = st.sidebar.slider("Temperature (°C)", 35.0, 42.0, 37.0)
oxygen = st.sidebar.slider("Oxygen Level (%)", 50, 100, 98)
heart_rate = st.sidebar.slider("Heart Rate (BPM)", 40, 180, 80)
blood_pressure = st.sidebar.slider("Blood Pressure", 80, 200, 120)
blood_sugar = st.sidebar.slider("Blood Sugar", 70, 300, 100)

st.sidebar.markdown("---")

st.header("Symptoms Selection")

col1, col2, col3 = st.columns(3)

symptoms = {}

with col1:
    symptoms["fever"] = st.checkbox("Fever")
    symptoms["cough"] = st.checkbox("Cough")
    symptoms["chest_pain"] = st.checkbox("Chest Pain")
    symptoms["shortness_of_breath"] = st.checkbox("Shortness of Breath")
    symptoms["headache"] = st.checkbox("Headache")

with col2:
    symptoms["fatigue"] = st.checkbox("Fatigue")
    symptoms["tachycardia"] = st.checkbox("Tachycardia")
    symptoms["wheezing"] = st.checkbox("Wheezing")
    symptoms["sore_throat"] = st.checkbox("Sore Throat")
    symptoms["loss_of_smell"] = st.checkbox("Loss of Smell")

with col3:
    symptoms["smoker"] = st.checkbox("Smoker")
    symptoms["obesity"] = st.checkbox("Obesity")
    symptoms["dizziness"] = st.checkbox("Dizziness")
    symptoms["chest_tightness"] = st.checkbox("Chest Tightness")
    symptoms["frequent_urination"] = st.checkbox("Frequent Urination")

facts = set()

for symptom, checked in symptoms.items():
    if checked:
        facts.add(symptom)

if temperature > 38:
    facts.add("fever")

if oxygen < 92:
    facts.add("oxygen_level_low")

if heart_rate > 100:
    facts.add("tachycardia")

if blood_pressure > 140:
    facts.add("high_blood_pressure")

if blood_sugar > 180:
    facts.add("high_blood_sugar")

rules = [
    ({"fever", "cough"}, "respiratory_infection"),
    ({"respiratory_infection", "oxygen_level_low"}, "severe_respiratory_condition"),
    ({"severe_respiratory_condition", "chest_pain"}, "possible_pneumonia"),
    ({"high_blood_sugar", "frequent_urination"}, "possible_diabetes"),
    ({"possible_diabetes"}, "diabetes_mellitus"),
    ({"high_blood_pressure", "headache"}, "hypertension"),
    ({"wheezing", "shortness_of_breath"}, "possible_asthma"),
    ({"possible_asthma", "chest_tightness"}, "asthma_attack"),
    ({"fever", "sore_throat"}, "viral_infection"),
    ({"viral_infection", "loss_of_smell"}, "possible_covid19"),
    ({"smoker", "chest_pain"}, "heart_risk"),
    ({"heart_risk", "tachycardia"}, "possible_heart_attack"),
    ({"oxygen_level_low", "tachycardia"}, "emergency_condition"),
    ({"possible_heart_attack", "emergency_condition"}, "acute_cardiac_emergency"),
]

reasoning_trace = []

new_fact_added = True

while new_fact_added:
    new_fact_added = False

    for conditions, conclusion in rules:
        if conditions.issubset(facts) and conclusion not in facts:
            facts.add(conclusion)

            reasoning_trace.append({
                "Conditions": ", ".join(conditions),
                "Conclusion": conclusion
            })

            new_fact_added = True

diagnoses = [
    fact for fact in facts
    if fact not in symptoms
]

st.markdown("---")

if st.button("Run Diagnosis"):

    st.header("Patient Summary")

    colA, colB, colC = st.columns(3)

    with colA:
        st.metric("Temperature", f"{temperature} °C")

    with colB:
        st.metric("Oxygen", f"{oxygen}%")

    with colC:
        st.metric("Heart Rate", f"{heart_rate} BPM")

    st.markdown("---")

    st.header("Diagnosis Results")

    if diagnoses:

        for diagnosis in diagnoses:

            if "emergency" in diagnosis:
                st.error(f"🚨 {diagnosis.replace('_', ' ').title()}")

            elif "heart" in diagnosis:
                st.warning(f"❤️ {diagnosis.replace('_', ' ').title()}")

            else:
                st.success(f"✅ {diagnosis.replace('_', ' ').title()}")

    else:
        st.info("No disease identified.")

    st.markdown("---")

    st.header("Recommended Actions")

    recommendations = []

    if "possible_pneumonia" in diagnoses:
        recommendations.append("Prescribe antibiotics")

    if "diabetes_mellitus" in diagnoses:
        recommendations.append("Recommend HbA1c test")

    if "hypertension" in diagnoses:
        recommendations.append("Recommend low-salt diet")

    if "acute_cardiac_emergency" in diagnoses:
        recommendations.append("Immediate ICU transfer required")

    if "possible_covid19" in diagnoses:
        recommendations.append("Recommend patient isolation")

    for rec in recommendations:
        st.write(f"• {rec}")

    st.markdown("---")

    st.header("Forward Chaining Reasoning Trace")

    trace_df = pd.DataFrame(reasoning_trace)

    if not trace_df.empty:
        st.dataframe(trace_df, use_container_width=True)

    st.markdown("---")

    st.header("Risk Analysis")

    risk_score = 0

    if "acute_cardiac_emergency" in diagnoses:
        risk_score += 50

    if "possible_heart_attack" in diagnoses:
        risk_score += 30

    if "possible_pneumonia" in diagnoses:
        risk_score += 20

    if "diabetes_mellitus" in diagnoses:
        risk_score += 15

    if oxygen < 90:
        risk_score += 25

    risk_df = pd.DataFrame({
        "Category": ["Risk Score"],
        "Value": [risk_score]
    })

    fig = px.bar(
        risk_df,
        x="Category",
        y="Value",
        title="Patient Risk Level"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    st.header("Medical Report")

    report = f"""
Patient Name: {name}
Age: {age}
Gender: {gender}

Diagnoses:
{', '.join(diagnoses)}

Recommendations:
{', '.join(recommendations)}

Risk Score:
{risk_score}
"""

    st.download_button(
        label="Download Medical Report",
        data=report,
        file_name="medical_report.txt",
        mime="text/plain"
    )

st.markdown("---")

st.caption("Knowledge-Based AI Medical Expert System")