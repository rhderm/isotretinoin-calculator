import streamlit as st

# Function to calculate cumulative dose and compare to the target
def isotretinoin_calculator(weight_kg, dose_plan):
    target_dose = 120 * weight_kg  # Target dose (120 mg/kg)
    cumulative_dose = 0

    # Calculate cumulative dose from dose plan
    for dose, weeks in dose_plan:
        cumulative_dose += dose * 7 * weeks  # dose * days per week * number of weeks

    remaining_dose = target_dose - cumulative_dose  # How much is left to reach the target
    return cumulative_dose, target_dose, remaining_dose

# Streamlit UI
st.title('Isotretinoin Cumulative Dose Calculator')

# Input patient weight
weight_kg = st.number_input('Enter patient weight (kg):', min_value=1, max_value=200, value=60)

# Initialize session state to keep track of dose plan inputs
if 'dose_plan' not in st.session_state:
    st.session_state.dose_plan = [(20, 4)]  # Default values (1 dose of 20 mg for 4 weeks)

# Function to add a new dose line
def add_dose():
    st.session_state.dose_plan.append((20, 4))  # Add default dose and weeks

# Function to remove a specific dose line
def remove_dose(index):
    if len(st.session_state.dose_plan) > 1:  # Only remove if more than one row exists
        st.session_state.dose_plan.pop(index)

# Dynamic input for dose plans
st.subheader('Dose Plan')

# Display inputs for each dose plan
for i, (dose, weeks) in enumerate(st.session_state.dose_plan):
    cols = st.columns([2, 2, 1])  # Adjust column widths for dose, weeks, and delete button
    with cols[0]:
        new_dose = st.number_input(f'Daily dose (mg) for period {i + 1}:', min_value=1, max_value=100, value=dose, key=f'dose_{i}')
    with cols[1]:
        new_weeks = st.number_input(f'Duration in weeks for period {i + 1}:', min_value=1, max_value=52, value=weeks, key=f'weeks_{i}')
    
    # Add delete button only for rows beyond the initial one
    if i > 0:
        with cols[2]:
            if st.button('Remove', key=f'remove_{i}'):
                remove_dose(i)
                st.rerun()  # Use st.rerun to update the UI

    # Update session state with new values only if the row still exists
    if i < len(st.session_state.dose_plan):
        st.session_state.dose_plan[i] = (new_dose, new_weeks)

# Buttons for adding more doses and calculating
col1, col2 = st.columns([2, 1])
with col1:
    if st.button('Add another dose'):
        add_dose()
        st.rerun()  # Update the UI to show the new row

with col2:
    calculate_clicked = st.button('Calculate')

# Calculation and output
if calculate_clicked:
    st.markdown("<hr>", unsafe_allow_html=True)  # Optional horizontal line to separate output
    cumulative_dose, target_dose, remaining_dose = isotretinoin_calculator(weight_kg, st.session_state.dose_plan)

    # Display the results
    st.write(f"**Cumulative Dose:** {cumulative_dose} mg")
    st.write(f"**Target Dose (120 mg/kg):** {target_dose} mg")

    if remaining_dose > 0:
        st.write(f"**Remaining Dose to Target:** {remaining_dose} mg")
        
        # Calculate how many weeks it will take at the current dose to reach the target
        current_dose = st.session_state.dose_plan[-1][0]  # Get the current dose
        weeks_needed = remaining_dose / (current_dose * 7)
        st.write(f"**Weeks needed at current dose ({current_dose} mg) to reach target:** {round(weeks_needed, 1)} weeks")
    else:
        st.write("The cumulative dose has already exceeded the target dose.")

st.markdown("""
---
**Disclaimer:**  
The Isotretinoin Cumulative Dose Calculator is intended for educational purposes only. 
It is not intended to be used as a substitute for professional medical advice, diagnosis, or treatment. 
Please consult a healthcare provider for any medical concerns or decisions.
""")
