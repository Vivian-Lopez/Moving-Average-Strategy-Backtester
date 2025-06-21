import streamlit as st
import plotly.graph_objects as go
from simulate import run_simulation

st.title("📈 C++ Trading Strategy Simulator")

st.sidebar.header("Strategy Settings")
short_window = st.sidebar.slider("Short Window", 1, 20, 3)
long_window = st.sidebar.slider("Long Window", 1, 50, 5)

uploaded_file = st.file_uploader("Upload price CSV", type="csv")

if uploaded_file is not None:
    csv_path = "uploaded_data.csv"
    with open(csv_path, "wb") as f:
        f.write(uploaded_file.read())

    if st.button("🚀 Run Simulation"):
        with st.spinner("Running strategy..."):
            df, profit = run_simulation(csv_path, short_window, long_window)

        st.success("Simulation complete!")
        st.metric("📊 Total Profit", f"${profit:.2f}")

        fig = go.Figure()
        fig.add_trace(go.Scatter(y=df['Close'], mode='lines', name='Price'))
        fig.add_trace(go.Scatter(y=df['PnL'], mode='lines', name='PnL'))
        st.plotly_chart(fig, use_container_width=True)
