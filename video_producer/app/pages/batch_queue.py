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
        hide_index=True
    )
    
    st.markdown("---")
    
    # Job details (expandable)
    st.markdown("### 📝 Job Details")
    
    for job in all_jobs:
        # Status emoji
        status_emoji = {
            'Queued': '⏳',
            'Processing': '🔄',
            'Completed': '✅',
            'Failed': '❌',
            'Cancelled': '🚫'
        }.get(job.status, '❓')
        
        with st.expander(f"{status_emoji} Job **{job.id}** - {job.status}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**📁 Input:** `{Path(job.input_path).name}`")
                st.markdown(f"**🎨 Styles:** {', '.join(job.styles)}")
                st.markdown(f"**⚙️ Preset:** {job.preset}")
                st.markdown(f"**🎚️ Intensity:** {job.effect_intensity}x")
            
            with col2:
                st.markdown(f"**📊 Status:** {job.status}")
                
                if job.status == 'Processing':
                    # Show progress
                    st.progress(job.progress / 100.0, text=f"{job.progress:.1f}% complete")
                    
                    # Show stats
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("FPS", f"{job.fps:.1f}")
                    with col_b:
                        if job.eta_seconds > 0:
                            eta_min = int(job.eta_seconds / 60)
                            eta_sec = int(job.eta_seconds % 60)
                            st.metric("ETA", f"{eta_min}m {eta_sec}s")
                        else:
                            st.metric("ETA", "Calculating...")
                    
                    st.caption(f"Frame {job.current_frame} / {job.total_frames}")
                
                elif job.status == 'Completed':
                    st.success("✅ Processing completed successfully!")
                    if job.completed_at:
                        st.caption(f"Completed: {job.completed_at}")
                
                elif job.status == 'Failed':
                    st.error(f"❌ Error: {job.error}")
                
                elif job.status == 'Queued':
                    st.info("⏳ Waiting in queue...")
            
            # Action buttons
            st.markdown("---")
            
            if job.status == 'Completed':
                # Show output files
                st.markdown("**📁 Output Files:**")
                
                # Find output files
                output_dir = Path(job.output_path)
                input_name = Path(job.input_path).stem
                
                output_files = []
                for style in job.styles:
                    style_slug = style.lower().replace(' ', '_')
                    expected_file = output_dir / f"{input_name}_{style_slug}.mp4"
                    if expected_file.exists():
                        output_files.append((style, str(expected_file)))
                
                if output_files:
                    for style, file_path in output_files:
                        col_file1, col_file2, col_file3 = st.columns([2, 1, 1])
                        
                        with col_file1:
                            file_size = Path(file_path).stat().st_size / (1024 * 1024)
                            st.markdown(f"**{style}** ({file_size:.1f} MB)")
                        
                        with col_file2:
                            # Video player
                            if st.button(f"▶️ Play", key=f"play_{job.id}_{style}", use_container_width=True):
                                st.session_state[f'playing_{job.id}_{style}'] = True
                        
                        with col_file3:
                            # Download button
                            try:
                                with open(file_path, 'rb') as f:
                                    video_bytes = f.read()
                                    st.download_button(
                                        label="📥 Download",
                                        data=video_bytes,
                                        file_name=Path(file_path).name,
                                        mime="video/mp4",
                                        key=f"download_{job.id}_{style}",
                                        use_container_width=True
                                    )
                            except Exception as e:
                                st.button(f"⚠️ Error", key=f"error_{job.id}_{style}", 
                                         disabled=True, use_container_width=True)
                        
                        # Show video if play button clicked
                        if st.session_state.get(f'playing_{job.id}_{style}', False):
                            st.video(file_path)
                            if st.button(f"⏹️ Close", key=f"close_{job.id}_{style}"):
                                st.session_state[f'playing_{job.id}_{style}'] = False
                                st.rerun()
                    
                    # Bulk actions for completed jobs
                    st.markdown("---")
                    bulk_col1, bulk_col2 = st.columns(2)
                    
                    with bulk_col1:
                        if st.button(f"📂 Open Folder", key=f"folder_{job.id}", use_container_width=True):
                            import subprocess
                            import platform
                            
                            try:
                                if platform.system() == 'Windows':
                                    subprocess.run(['explorer', str(output_dir)])
                                elif platform.system() == 'Darwin':
                                    subprocess.run(['open', str(output_dir)])
                                else:
                                    subprocess.run(['xdg-open', str(output_dir)])
                                st.success(f"✅ Opened folder: {output_dir}")
                            except Exception as e:
                                st.error(f"❌ Could not open folder: {e}")
                    
                    with bulk_col2:
                        if st.button(f"📦 Package All", key=f"package_{job.id}", use_container_width=True):
                            try:
                                from core.video_exporter import VideoExporter
                                
                                zip_path = output_dir / f"{input_name}_all_styles.zip"
                                file_paths = [fp for _, fp in output_files]
                                
                                if VideoExporter.package_outputs(file_paths, str(zip_path)):
                                    with open(zip_path, 'rb') as f:
                                        zip_bytes = f.read()
                                        st.download_button(
                                            label="📥 Download Package",
                                            data=zip_bytes,
                                            file_name=zip_path.name,
                                            mime="application/zip",
                                            key=f"download_zip_{job.id}"
                                        )
                                else:
                                    st.error("❌ Failed to create package")
                            except Exception as e:
                                st.error(f"❌ Packaging failed: {e}")
                else:
                    st.warning("⚠️ No output files found")
            
            # Control buttons
            st.markdown("---")
            btn_col1, btn_col2, btn_col3 = st.columns(3)
            
            with btn_col1:
                if job.status in ['Queued', 'Processing']:
                    if st.button(f"❌ Cancel", key=f"cancel_{job.id}", use_container_width=True):
                        job_manager.cancel_job(job.id)
                        st.success(f"✅ Job {job.id} cancelled")
                        time.sleep(0.5)
                        st.rerun()
            
            with btn_col2:
                if job.status == 'Completed':
                    if st.button(f"🔄 Process Again", key=f"reprocess_{job.id}", use_container_width=True):
                        new_job_id = job_manager.add_job(
                            input_path=job.input_path,
                            output_path=job.output_path,
                            styles=job.styles,
                            preset=job.preset,
                            effect_intensity=job.effect_intensity
                        )
                        st.success(f"✅ New job created: {new_job_id}")
                        time.sleep(0.5)
                        st.rerun()
            
            with btn_col3:
                if job.status in ['Completed', 'Failed', 'Cancelled']:
                    if st.button(f"🗑️ Remove", key=f"remove_{job.id}", use_container_width=True):
                        del job_manager.jobs[job.id]
                        st.success(f"✅ Job {job.id} removed")
                        time.sleep(0.5)
                        st.rerun()
    
    # Auto-refresh
    if auto_refresh:
        time.sleep(5)
        st.rerun()