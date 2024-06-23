import streamlit as st
import pandas as pd

# Load data from a CSV file
st.set_page_config(page_title="Contraceptive Care Recommendation", page_icon="🩷")

@st.cache_data
def load_data():
    df = pd.read_csv("/workspaces/contraceptive-care/contraceptive_data.csv")
    return df

df = load_data()

st.title("Personalized Contraceptive Care Advisor 🩷💊 ")
st.write(
    """
    Welcome to your personalized contraceptive care journey! This application helps you explore suitable 
    contraceptive options based on your unique medical profile. Let's find the best method for you.
    """
    """
    The following tool was created using [Summary Chart of U.S. Medical Eligibility Criteria for Contraceptive Use](https://www.cdc.gov/reproductivehealth/contraception/pdf/summary-chart-us-medical-eligibility-criteria_508tagged.pdf).
    """
)

# User input for medical conditions and subconditions
conditions = df['Condition'].unique()
conditions = [c for c in conditions if c.lower() != 'age']  # Exclude 'Age' from conditions
selected_condition = st.selectbox('What is your primary medical condition?', ['None'] + list(conditions))

if selected_condition != 'None':
    subconditions = df[df['Condition'] == selected_condition]['Sub-Condition'].unique()
    selected_subcondition = st.selectbox('Please specify the sub-condition:', ['None'] + list(subconditions))
else:
    selected_subcondition = 'None'

# Filter data based on user input
if selected_condition != 'None' and selected_subcondition != 'None':
    filtered_data = df[(df['Condition'] == selected_condition) & (df['Sub-Condition'] == selected_subcondition)]
else:
    filtered_data = pd.DataFrame(columns=df.columns)

# Function to interpret risk score
def interpret_score(score):
    if score == 1:
        return "✅ Safe to use"
    elif score == 2:
        return "🟨 Generally safe, consult doctor"
    elif score == 3:
        return "⚠️ Use with caution, consult doctor"
    elif score == 4:
        return "❌ Not recommended"
    else:
        return "ℹ️ Consult your doctor"

# Replace the Plotly visualization code with this:
if not filtered_data.empty:
    st.write("### Your Personalized Contraceptive Recommendations:")
    
    methods = ['Cu-IUD', 'LNG-IUD', 'Implant', 'DMPA', 'POP', 'CHC']
    scores = filtered_data[methods].iloc[0].astype(float)
    
    for method, score in scores.items():
        interpretation = interpret_score(score)
        st.write(f"**{method}:** {interpretation} (Risk Score: {score})")

    # Streamlit bar chart
    st.bar_chart(scores)

# Information about contraceptive methods
contraceptive_info = {
    "Cu-IUD": "A small, T-shaped device inserted into the uterus that releases copper to prevent pregnancy.",
    "LNG-IUD": "A hormonal intrauterine device that releases levonorgestrel to prevent pregnancy.",
    "Implant": "A small, flexible rod inserted under the skin of the upper arm that releases hormones.",
    "DMPA": "An injection given every three months to prevent pregnancy.",
    "POP": "A daily birth control pill that contains only progestin.",
    "CHC": "Combined hormonal contraceptives including pills, patches, and vaginal rings."
}

st.write("### Learn More About Contraceptive Methods:")
for method, info in contraceptive_info.items():
    with st.expander(f"{method}"):
        st.write(info)

# Add legend for risk scores
st.write(
    """
    ### Understanding Risk Scores:
    - **1:** ✅ No restriction (method can be used)
    - **2:** 🟨 Advantages generally outweigh theoretical or proven risks
    - **3:** ⚠️ Theoretical or proven risks usually outweigh the advantages
    - **4:** ❌ Unacceptable health risk (method not to be used)
    """
)

# Disclaimer
st.warning(
    """
    **Disclaimer:** This tool provides general guidance based on medical conditions. 
    It's crucial to consult with a healthcare professional for personalized advice 
    tailored to your individual health needs and circumstances.
    """
)

# Display additional guidance link
st.write(
    """
    For more detailed information, please visit the [CDC Contraception Guidance](https://www.cdc.gov/reproductivehealth/contraception/contraception_guidance.htm).
    """
)