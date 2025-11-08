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

# Initialize session state FIRST
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'Dashboard'
if 'job_manager' not in st.session_state:
    from core.job_manager import JobManager
    st.session_state.job_manager = JobManager()
if 'total_jobs' not in st.session_state:
    st.session_state.total_jobs = 0
if 'completed_jobs' not in st.session_state:
    st.session_state.completed_jobs = 0

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
    .stProgress > div > div > div > div {
        background-color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.markdown("<div class='main-header'>🎬 Video Producer</div>", unsafe_allow_html=True)
    st.markdown("### Navigation")
    
    # Page selection
    page = st.radio(
        "Select Page",
        ["Dashboard", "Batch Queue", "Style Lab", "Trainer", "Settings"],
        key="page_selector",
        index=["Dashboard", "Batch Queue", "Style Lab", "Trainer", "Settings"].index(st.session_state.current_page)
    )
    
    # Update current page
    st.session_state.current_page = page
    
    st.markdown("---")
    st.markdown("### Quick Stats")
    
    # Get real stats from job manager
    job_manager = st.session_state.job_manager
    all_jobs = job_manager.get_all_jobs()
    completed = len([j for j in all_jobs if j.status == 'Completed'])
    
    st.metric("Total Jobs", len(all_jobs))
    st.metric("Completed", completed)
    st.metric("Active", len([j for j in all_jobs if j.status == 'Processing']))
    
    st.markdown("---")
    st.markdown("""
    **HP OMEN Optimized**
    
    ✅ NVENC Hardware Encoding
    ✅ GPU-Accelerated ML
    ✅ Temporal Stability
    ✅ Resume on Crash
    ✅ Pattern Learning
    """)

# Dynamic import based on current page
import importlib

try:
    if page == "Dashboard":
        from pages import dashboard
        dashboard.show()
    elif page == "Batch Queue":
        from pages import batch_queue
        batch_queue.show()
    elif page == "Style Lab":
        from pages import style_lab
        style_lab.show()
    elif page == "Trainer":
        from pages import trainer_page
        trainer_page.show()
    elif page == "Settings":
        from pages import settings_page
        settings_page.show()
except Exception as e:
    st.error(f"Error loading page: {e}")
    st.exception(e)