import streamlit as st
import plotly.graph_objects as go
from simulate import run_simulation
import os
import time

# Initialize session state keys if not present
if 'csv_path' not in st.session_state:
    st.session_state['csv_path'] = None
if 'source_message' not in st.session_state:
    st.session_state['source_message'] = ""
if 'uploader_seed' not in st.session_state:
    st.session_state['uploader_seed'] = 0

st.title("📈 C++ Trading Strategy Simulator")

# Place sidebar controls before main UI so short_window and long_window are defined
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

# Info panel at the top
st.markdown(
    """
    <div style='background-color: #f6f8fa; border: 1px solid #e1e4e8; border-radius: 8px; padding: 1.2rem 1.5rem; margin-bottom: 1.5rem; font-size: 1.08rem;'>
        <b>Welcome!</b> To get started, <b>upload your own CSV file</b> (see format preview below), or <b>load the sample data</b>.<br>
        Then, click <b>Run Simulation</b> to see your simple moving average strategy's profit and PnL over time.
    </div>
    """,
    unsafe_allow_html=True
)

# Example CSV preview
st.markdown(
    """
    <div style='background-color: #f6f8fa; border: 1px solid #e1e4e8; border-radius: 6px; padding: 1rem; margin-bottom: 1.2rem; font-family: monospace; font-size: 0.97rem;'>
    Timestamp,Price<br>
    100000001,101.5<br>
    100000002,101.7<br>
    100000003,101.8<br>
    ...
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns([3, 1], gap="medium")

# First, handle sample data load so uploader_seed updates before file_uploader is instantiated
with col2:
    st.markdown(
        "<div style='display: flex; justify-content: center; align-items: center; height: 100%;'>",
        unsafe_allow_html=True
    )
    load_sample = st.button(
        "🗂️ Load Sample Data",
        key="load_sample",
        help="Use built-in sample data",
        use_container_width=False,
        type="tertiary"
    )
    st.markdown("</div>", unsafe_allow_html=True)
    if load_sample:
        sample_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "Volatile_Price_Data.csv"
        )
        st.session_state['csv_path'] = sample_path
        st.session_state['source_message'] = "✅ Sample data loaded."
        # bump seed so uploader widget resets immediately
        st.session_state['uploader_seed'] += 1

# Then show file uploader, now with updated seed if sample was clicked
with col1:
    uploaded_file = st.file_uploader(
        "Upload your CSV file", type="csv",
        key=f"file_uploader_{st.session_state['uploader_seed']}",
        label_visibility="collapsed"
    )
    if uploaded_file is not None:
        csv_path = "uploaded_data.csv"
        with open(csv_path, "wb") as f:
            f.write(uploaded_file.read())
        st.session_state['csv_path'] = csv_path
        st.session_state['source_message'] = "✅ Custom file loaded."

# Show which data source is active (lowkey)
if st.session_state['source_message']:
    st.markdown(f"<div style='background-color: #f6f8fa; color: #222; border: 1px solid #e1e4e8; border-radius: 5px; padding: 0.5rem 1rem; font-size: 1rem; margin-bottom: 0.7rem;'>{st.session_state['source_message']}</div>", unsafe_allow_html=True)

# --- Run Simulation Button ---
run_disabled = st.session_state['csv_path'] is None
run_btn = st.button("🚀 Run Simulation", disabled=run_disabled, use_container_width=True)

if run_btn and st.session_state['csv_path']:
    with st.spinner("Running strategy..."):
        start_time = time.time()
        df, profit = run_simulation(st.session_state['csv_path'], short_window, long_window)
        elapsed = time.time() - start_time

    # Display metrics in a styled, emoji-rich panel
    st.markdown(
        f'''
<div style="background:#fff; border:1px solid #e1e4e8; border-radius:10px; padding:1.5rem; margin-bottom:2rem; box-shadow:0 4px 6px rgba(0,0,0,0.1);">
  <div style="text-align:center; margin-bottom:1rem;">
    <span style="font-size:1.4rem; font-weight:600;">🏁 Simulation Complete!</span>
  </div>
  <div style="display:flex; justify-content:space-around;">
    <div style="text-align:center;">
      <div style="font-size:1.6rem;">💰</div>
      <div style="font-size:0.85rem; color:#555;">Total Profit</div>
      <div style="font-size:1.3rem; font-weight:bold;">${profit:.2f}</div>
    </div>
    <div style="text-align:center;">
      <div style="font-size:1.6rem;">⏱️</div>
      <div style="font-size:0.85rem; color:#555;">Runtime</div>
      <div style="font-size:1.3rem; font-weight:bold;">{elapsed:.2f}s</div>
    </div>
    <div style="text-align:center;">
      <div style="font-size:1.6rem;">📊</div>
      <div style="font-size:0.85rem; color:#555;">Data Points</div>
      <div style="font-size:1.3rem; font-weight:bold;">{len(df)}</div>
    </div>
  </div>
</div>
''', unsafe_allow_html=True,
    )

    # Reduce space before the graph
    st.markdown("<div style='margin-top: -2rem'></div>", unsafe_allow_html=True)

    # Add a chart title above the plot
    st.markdown(
        """
        <div style='font-size: 1.1rem; font-weight: 700; color: #23234c; margin-bottom: 0.5rem; margin-top: 1.2rem;'>
            📈 Price & PnL Over Time
        </div>
        """,
        unsafe_allow_html=True
    )

    fig = go.Figure()
    fig.add_trace(go.Scatter(y=df['Price'], mode='lines', name='Price'))
    fig.add_trace(go.Scatter(y=df['PnL'], mode='lines', name='PnL'))
    fig.update_layout(
        xaxis_title='Time',
        yaxis_title='Value ($)'
    )
    st.plotly_chart(fig, use_container_width=True)
