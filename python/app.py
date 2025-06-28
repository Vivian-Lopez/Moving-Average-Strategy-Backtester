import streamlit as st
import plotly.graph_objects as go
from simulate import run_simulation

st.title("📈 C++ Trading Strategy Simulator")

st.sidebar.header("Strategy Settings")
st.sidebar.markdown(
    """
    <div style='background-color: #eafaf1; border: 1px solid #b7ebc6; border-radius: 6px; padding: 0.7rem; margin-bottom: 1.2rem; font-size: 0.98rem;'>
    Adjust the <b>Short Window</b> and <b>Long Window</b> sliders below to test different strategy settings and see which window sizes give you the highest profit!
    </div>
    """,
    unsafe_allow_html=True
)
short_window = st.sidebar.slider("Short Window", 1, 20, 3)
long_window = st.sidebar.slider("Long Window", 1, 50, 5)

# --- Data source selection with session state ---
if 'csv_path' not in st.session_state:
    st.session_state['csv_path'] = None
if 'source_message' not in st.session_state:
    st.session_state['source_message'] = None

# st.markdown("---")
# Example CSV box
st.markdown(
    """
    <div style='background-color: #f6f8fa; border: 1px solid #e1e4e8; border-radius: 6px; padding: 1rem; margin-top: 1rem; font-family: monospace; font-size: 0.95rem;'>
    <b>Example CSV format:</b><br>
    <span style='color:#555'># Left value: timestamp/tick, right value: price</span><br>
    100000001,101.5<br>
    100000002,101.7<br>
    100000003,101.8<br>
    </div>
    """,
    unsafe_allow_html=True
)

# Aligned row for uploader and sample button
col1, col2 = st.columns([3, 1], gap="medium")

with col1:
    uploaded_file = st.file_uploader("", type="csv", key="file_uploader")
    if uploaded_file is not None:
        csv_path = "uploaded_data.csv"
        with open(csv_path, "wb") as f:
            f.write(uploaded_file.read())
        st.session_state['csv_path'] = csv_path
        st.session_state['source_message'] = "✅ Custom file loaded."
with col2:
    st.markdown("<div style='height: 35px'></div>", unsafe_allow_html=True)  # Precise spacer for alignment
    if st.button("🗂️ Load Sample Data", key="load_sample", help="Use built-in sample data", use_container_width=True):
        st.session_state['csv_path'] = "../data/sample_data.csv"
        st.session_state['source_message'] = "✅ Sample data loaded."


# Show which data source is active
if st.session_state['source_message']:
    st.markdown(f"<div style='background-color: #f6f8fa; color: #222; border: 1px solid #e1e4e8; border-radius: 5px; padding: 0.5rem 1rem; font-size: 1rem; margin-bottom: 0.7rem;'>{st.session_state['source_message']}</div>", unsafe_allow_html=True)

# --- Run Simulation Button ---
run_disabled = st.session_state['csv_path'] is None
run_btn = st.button("🚀 Run Simulation", disabled=run_disabled)

if run_btn and st.session_state['csv_path']:
    with st.spinner("Running strategy..."):
        df, profit = run_simulation(st.session_state['csv_path'], short_window, long_window)

    st.success("Simulation complete!")
    st.metric("📊 Total Profit", f"${profit:.2f}")

    # Reduce space before the graph
    st.markdown("<div style='margin-top: -2rem'></div>", unsafe_allow_html=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(y=df['Close'], mode='lines', name='Price'))
    fig.add_trace(go.Scatter(y=df['PnL'], mode='lines', name='PnL'))
    st.plotly_chart(fig, use_container_width=True)
