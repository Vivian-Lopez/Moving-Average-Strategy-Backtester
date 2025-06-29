import streamlit as st
import plotly.graph_objects as go
from simulate import run_simulation
import os
import time

# Add this at the top after imports
st.markdown(
    """
    <style>
    .frosted-panel {
        background: rgba(24, 26, 31, 0.92); /* darker gray, more opaque */
        border: 1.5px solid #35373e;
        border-radius: 10px;
        color: #23272f;
        box-shadow: 0 2px 8px rgba(0,0,0,0.13);
        padding: 1.2rem 1.5rem;
        margin-bottom: 1.5rem;
        font-size: 1.08rem;
        transition: background 0.2s, color 0.2s;
    }
    .frosted-panel.monospace { font-family: monospace; font-size: 0.97rem; }
    .frosted-panel.metrics-panel { display: block; padding: 1.5rem; }
    .frosted-panel .metrics-title { text-align: center; margin-bottom: 1rem; font-size: 1.4rem; font-weight: 600; }
    .frosted-panel .metrics-container { display: flex; justify-content: space-around; }
    .frosted-panel .metric-item { text-align: center; }
    .frosted-panel .metric-icon { font-size: 1.6rem; }
    .frosted-panel .metric-label { font-size: 0.85rem; color: #a3aab3; }
    .frosted-panel .metric-value { font-size: 1.3rem; font-weight: bold; }
    .frosted-panel .chart-title {
        font-size: 1.18rem;
        font-weight: 800;
        color: #c2c8f0;
        margin-bottom: 0.5rem;
        margin-top: 1.2rem;
        letter-spacing: 0.01em;
        text-shadow: 0 2px 8px rgba(0,0,0,0.18);
        display: flex;
        align-items: center;
        gap: 0.5em;
    }
    @media (prefers-color-scheme: light) {
        .frosted-panel {
            background: rgba(246, 248, 250, 0.85);
            color: #23272f;
            border: 1.5px solid #e1e4e8;
        }
        .frosted-panel .metric-label { color: #555; }
        .frosted-panel .chart-title {
            color: #23234c;
            text-shadow: none;
            font-weight: 700;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

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
    <style>
    .sidebar-info {
        background-color: #eafaf1;
        border: 1px solid #b7ebc6;
        border-radius: 6px;
        padding: 0.7rem;
        margin-bottom: 1.2rem;
        font-size: 0.98rem;
        color: #222;
    }
    @media (prefers-color-scheme: dark) {
        .sidebar-info {
            background-color: #2e3440 !important;
            border: 1px solid #444851 !important;
            color: #f3f6fa !important;
        }
    }
    </style>
    <div class="sidebar-info" data-testid="stSidebarContent">
    Adjust the <b>Short Window</b> and <b>Long Window</b> sliders below to test different strategy settings and see which window sizes give you the highest profit!
    </div>
    """,
    unsafe_allow_html=True
)
short_window = st.sidebar.slider("Short Window", 1, 20, 3)
long_window = st.sidebar.slider("Long Window", 1, 50, 11)

# Info panel at the top
st.markdown(
    """
    <div class='frosted-panel'>
        <b>Welcome!</b> To get started, <b>upload your own CSV file</b> (see format preview below), or <b>load the sample data</b>.<br>
        Then, click <b>Run Simulation</b> to see your simple moving average strategy's profit and PnL over time.
    </div>
    """,
    unsafe_allow_html=True
)

# Example CSV preview
st.markdown(
    """
    <div class="frosted-panel monospace">
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
            os.path.dirname(__file__), "..", "data", "more_volatile_prices.csv"
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
    st.markdown(f"""
    <div class="frosted-panel" style="padding: 0.5rem 1rem; font-size: 1rem; margin-bottom: 0.7rem;">
        {st.session_state['source_message']}
    </div>
    """, unsafe_allow_html=True)

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
<div class="frosted-panel metrics-panel">
  <div class="metrics-title">
    🏁 Simulation Complete!
  </div>
  <div class="metrics-container">
    <div class="metric-item">
      <div class="metric-icon">💰</div>
      <div class="metric-label">Total Profit</div>
      <div class="metric-value">${profit:.2f}</div>
    </div>
    <div class="metric-item">
      <div class="metric-icon">⏱️</div>
      <div class="metric-label">Runtime</div>
      <div class="metric-value">{elapsed:.2f}s</div>
    </div>
    <div class="metric-item">
      <div class="metric-icon">📊</div>
      <div class="metric-label">Data Points</div>
      <div class="metric-value">{len(df)}</div>
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
        <style>
        @media (prefers-color-scheme: dark) {
            .chart-title, .chart-title * {
                color: #fff !important;
                font-weight: 900 !important;
                text-shadow: 0 2px 8px rgba(0,0,0,0.18);
            }
        }
        @media (prefers-color-scheme: light) {
            .chart-title {
                color: #23234c !important;
                font-weight: 700;
                text-shadow: none;
            }
        }
        </style>
        <div class="chart-title" style="background: none; border: none; box-shadow: none; padding: 0; margin-bottom: 0.5rem; margin-top: 1.2rem; font-size: 1.18rem; font-weight: 900; display: flex; align-items: center; gap: 0.5em; letter-spacing: 0.01em;">
            📈 Price & PnL Over Time
        </div>
        """,
        unsafe_allow_html=True
    )

    fig = go.Figure()
    fig.add_trace(go.Scatter(y=df['Price'], mode='lines', name='Price', line=dict(width=2)))
    fig.add_trace(go.Scatter(y=df['PnL'], mode='lines', name='PnL', line=dict(width=2)))
    
    # Create dark mode compatible chart
    fig.update_layout(
        xaxis_title='Time',
        yaxis_title='Value ($)',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#f3f6fa'),
        xaxis=dict(
            gridcolor='rgba(80,80,80,0.2)',
            zerolinecolor='rgba(80,80,80,0.2)'
        ),
        yaxis=dict(
            gridcolor='rgba(80,80,80,0.2)',
            zerolinecolor='rgba(80,80,80,0.2)'
        ),
        margin=dict(l=10, r=10, t=10, b=10)
    )
    
    st.plotly_chart(fig, use_container_width=True)
