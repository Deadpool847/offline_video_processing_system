"""Batch queue page - job management."""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys
import time

sys.path.append(str(Path(__file__).parent.parent.parent))


def show():
    st.markdown("<h1 class='main-header'>Batch Queue</h1>", unsafe_allow_html=True)
    st.markdown("Monitor and manage processing jobs with real-time updates")
    
    # Get job manager
    job_manager = st.session_state.job_manager
    all_jobs = job_manager.get_all_jobs()
    
    if not all_jobs:
        st.info("📭 No jobs in queue. Go to **Dashboard** to create a new job.")
        
        st.markdown("---")
        st.markdown("### Quick Start")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**1️⃣ Upload Video**")
            st.caption("Go to Dashboard")
        with col2:
            st.markdown("**2️⃣ Select Styles**")
            st.caption("Choose artistic effects")
        with col3:
            st.markdown("**3️⃣ Process**")
            st.caption("Monitor here")
        return
    
    # Statistics
    stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
    
    with stats_col1:
        total = len(all_jobs)
        st.metric("📊 Total Jobs", total)
    
    with stats_col2:
        processing = len([j for j in all_jobs if j.status == 'Processing'])
        st.metric("🔄 Processing", processing)
    
    with stats_col3:
        completed = len([j for j in all_jobs if j.status == 'Completed'])
        st.metric("✅ Completed", completed)
    
    with stats_col4:
        failed = len([j for j in all_jobs if j.status in ['Failed', 'Cancelled']])
        st.metric("❌ Failed", failed)
    
    st.markdown("---")
    
    # Job controls
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🗑️ Clear Completed", use_container_width=True):
            job_manager.clear_completed()
            st.success("✅ Cleared completed jobs")
            time.sleep(0.5)
            st.rerun()
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    with col3:
        auto_refresh = st.checkbox("Auto-refresh (5s)", value=False)
    
    st.markdown("---")
    
    # Display jobs table
    st.markdown("### 📋 Active Jobs")
    
    # Create DataFrame
    job_data = []
    for job in all_jobs:
        job_data.append({
            'ID': job.id,
            'Input': Path(job.input_path).name if job.input_path else 'N/A',
            'Styles': ', '.join(job.styles[:2]) + ('...' if len(job.styles) > 2 else ''),
            'Status': job.status,
            'Progress': f"{job.progress:.1f}%",
            'FPS': f"{job.fps:.1f}" if job.fps > 0 else '-'
        })
    
    df = pd.DataFrame(job_data)
    
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