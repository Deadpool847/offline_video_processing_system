"""Main Streamlit application - ML-Powered Video Producer."""

import streamlit as st
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

# Configure page
st.set_page_config(
    page_title="ML Video Producer",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .status-success {
        color: #10b981;
        font-weight: 600;
    }
    .status-processing {
        color: #3b82f6;
        font-weight: 600;
    }
    .status-error {
        color: #ef4444;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Import pages
from pages import dashboard, batch_queue, style_lab, trainer_page, settings_page

# Sidebar navigation
with st.sidebar:
    st.markdown("<div class='main-header'>🎬 Video Producer</div>", unsafe_allow_html=True)
    st.markdown("### Navigation")
    
    page = st.radio(
        "Select Page",
        ["Dashboard", "Batch Queue", "Style Lab", "Trainer", "Settings"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### Quick Stats")
    
    # Initialize session state
    if 'total_jobs' not in st.session_state:
        st.session_state.total_jobs = 0
    if 'completed_jobs' not in st.session_state:
        st.session_state.completed_jobs = 0
    
    st.metric("Total Jobs", st.session_state.total_jobs)
    st.metric("Completed", st.session_state.completed_jobs)
    
    st.markdown("---")
    st.markdown("""
    **HP OMEN Optimized**
    
    ✅ NVENC Hardware Encoding
    ✅ GPU-Accelerated ML
    ✅ Temporal Stability
    ✅ Resume on Crash
    """)

# Route to selected page
if page == "Dashboard":
    dashboard.show()
elif page == "Batch Queue":
    batch_queue.show()
elif page == "Style Lab":
    style_lab.show()
elif page == "Trainer":
    trainer_page.show()
elif page == "Settings":
    settings_page.show()