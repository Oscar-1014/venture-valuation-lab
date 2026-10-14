
import streamlit as st
import pandas as pd
import plotly.express as px

from valuation import calculate_valuation

st.set_page_config(
    page_title="Venture Valuation Lab",
    page_icon="📈",
    layout="wide",
)

st.title("Venture Valuation Lab")
st.caption("VC / PE Exit Valuation & Investment Returns Simulator")
st.info("All default inputs are fictional and for educational use only.")

st.sidebar.header("Investment Assumptions")

net_income = st.sidebar.number_input(
    "Exit-year net income (million)",
    min_value=0.0,
    value=500.0,
    step=10.0,
)

exit_pe = st.sidebar.slider(
    "Exit P/E multiple", 5, 150, 50, 5
)

dilution = st.sidebar.slider(
    "Future ownership dilution (%)", 0, 80, 25, 5
) / 100

target_irr = st.sidebar.slider(
    "Target IRR (%)", 0, 80, 30, 5
) / 100

years = st.sidebar.slider(
    "Holding period (years)", 1, 10, 3
)

entry_valuation = st.sidebar.number_input(
    "Entry post-money valuation (million)",
    min_value=1.0,
    value=6000.0,
    step=100.0,
)

investment = st.sidebar.number_input(
    "Investment amount (million)",
    min_value=0.1,
    max_value=float(entry_valuation),
    value=min(100.0, float(entry_valuation)),
    step=10.0,
)

result = calculate_valuation(
    net_income=net_income,
    exit_pe=exit_pe,
    dilution=dilution,
    target_irr=target_irr,
    years=years,
    entry_valuation=entry_valuation,
    investment=investment,
)

st.subheader("Valuation Results")

a, b, c, d = st.columns(4)

a.metric(
    "Exit Equity Value",
    f"{result['exit_value']:,.1f} M",
)

b.metric(
    "Maximum Entry Post-money",
    f"{result['max_entry_valuation']:,.1f} M",
)

c.metric(
    "Investment MOIC",
    f"{result['moic']:.2f}x",
)

d.metric(
    "Expected IRR",
    f"{result['actual_irr']:.1%}",
)

if result["actual_irr"] >= target_irr:
    st.success("The investment meets the target IRR.")
else:
    st.warning("The investment does not meet the target IRR.")

st.divider()

st.subheader("P/E × Net Income Sensitivity Analysis")

pe_values = list(range(10, 151, 10))
income_factors = [0.5, 0.75, 1.0, 1.25, 1.5]

data = []

for factor in income_factors:
    row = []
    for pe in pe_values:
        adjusted_income = net_income * factor
        exit_value = adjusted_income * pe
        max_valuation = (
            exit_value * (1 - dilution)
            / (1 + target_irr) ** years
        )
        row.append(max_valuation)
    data.append(row)

df = pd.DataFrame(
    data,
    index=[f"{factor:.0%}" for factor in income_factors],
    columns=pe_values,
)

fig = px.imshow(
    df,
    labels={
        "x": "Exit P/E",
        "y": "Net Income vs. Base Case",
        "color": "Max Entry Valuation (M)",
    },
    aspect="auto",
    text_auto=".0f",
    color_continuous_scale="Blues",
)

st.plotly_chart(fig, use_container_width=True)

st.caption(
    "The model assumes a successful equity exit, "
    "fixed dilution and no interim cash flows."
)
