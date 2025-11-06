"""Batch queue page - job management."""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))


def show():
    st.markdown("<h1 class='main-header'>Batch Queue</h1>", unsafe_allow_html=True)
    st.markdown("Monitor and manage processing jobs")
    
    # Initialize jobs if not exists
    if 'jobs' not in st.session_state:
        st.session_state.jobs = []
    
    if not st.session_state.jobs:
        st.info("No jobs in queue. Go to Dashboard to create a new job.")
        return
    
    # Job controls
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("⏸️ Pause All", use_container_width=True):
            st.info("All jobs paused")
    with col2:
        if st.button("▶️ Resume All", use_container_width=True):
            st.info("All jobs resumed")
    with col3:
        if st.button("🗑️ Clear Completed", use_container_width=True):
            st.session_state.jobs = [j for j in st.session_state.jobs if j['status'] != 'Completed']
            st.rerun()
    
    st.markdown("---")
    
    # Display jobs table
    st.markdown("### Active Jobs")
    
    # Create DataFrame
    df = pd.DataFrame(st.session_state.jobs)
    
    # Display with styling
    st.dataframe(
        df,
        use_container_width=True,
        column_config={
            'id': st.column_config.NumberColumn('Job ID', width='small'),
            'input': st.column_config.TextColumn('Input', width='large'),
            'styles': st.column_config.ListColumn('Styles', width='medium'),
            'preset': st.column_config.TextColumn('Preset', width='small'),
            'status': st.column_config.TextColumn('Status', width='small')
        },
        hide_index=True
    )
    
    # Job details (expandable)
    st.markdown("### Job Details")
    
    for job in st.session_state.jobs:
        with st.expander(f"Job {job['id']} - {job['status']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Input:** {job['input']}")
                st.markdown(f"**Styles:** {', '.join(job['styles'])}")
                st.markdown(f"**Preset:** {job['preset']}")
            
            with col2:
                st.markdown(f"**Status:** {job['status']}")
                
                # Mock progress
                if job['status'] == 'Processing':
                    progress = 0.65
                    st.progress(progress, text=f"{int(progress*100)}% complete")
                    st.markdown("**ETA:** 5 minutes")
                    st.markdown("**FPS:** 23.5")
                elif job['status'] == 'Completed':
                    st.success("✅ Completed successfully")
                
            # Action buttons
            btn_col1, btn_col2, btn_col3 = st.columns(3)
            
            with btn_col1:
                if job['status'] == 'Processing':
                    if st.button(f"⏸️ Pause", key=f"pause_{job['id']}"):
                        job['status'] = 'Paused'
                        st.rerun()
            
            with btn_col2:
                if job['status'] == 'Paused':
                    if st.button(f"▶️ Resume", key=f"resume_{job['id']}"):
                        job['status'] = 'Processing'
                        st.rerun()
            
            with btn_col3:
                if st.button(f"❌ Cancel", key=f"cancel_{job['id']}"):
                    st.session_state.jobs.remove(job)
                    st.rerun()