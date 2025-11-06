"""Dashboard page - main processing interface."""

import streamlit as st
from pathlib import Path
import sys
import json

sys.path.append(str(Path(__file__).parent.parent.parent))

from core.presets import PresetManager
from core.hardware import HardwareManager
from stylizers import *


def show():
    st.markdown("<h1 class='main-header'>Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("Process videos with artistic styles")
    
    # Initialize managers
    preset_mgr = PresetManager()
    hw_mgr = HardwareManager()
    
    # Two columns: Input | Preview
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Input Configuration")
        
        # File/Folder selection
        input_type = st.radio("Input Type", ["Single File", "Folder"], horizontal=True)
        
        if input_type == "Single File":
            input_path = st.text_input("Video Path", placeholder="/path/to/video.mp4")
        else:
            input_path = st.text_input("Folder Path", placeholder="/path/to/videos/")
        
        # Style selection
        st.markdown("### Style Selection")
        
        styles = {
            'Pencil Sketch': st.checkbox('Pencil Sketch', value=True),
            'Cartoon': st.checkbox('Cartoon'),
            'Comic/Halftone': st.checkbox('Comic/Halftone'),
            'Cinematic': st.checkbox('Cinematic'),
            'Fast Neural Style': st.checkbox('Fast Neural Style')
        }
        
        selected_styles = [k for k, v in styles.items() if v]
        
        # Preset selection
        st.markdown("### Quality Preset")
        preset_name = st.select_slider(
            "Preset",
            options=['Speed', 'Balanced', 'Quality'],
            value='Balanced'
        )
        
        preset = preset_mgr.get_preset(preset_name)
        
        # Advanced settings (expandable)
        with st.expander("⚙️ Advanced Settings"):
            col_a, col_b = st.columns(2)
            
            with col_a:
                custom_crf = st.slider("CRF Quality", 10, 30, preset['crf'])
                chunk_duration = st.slider("Chunk Duration (s)", 10, 120, preset['chunk_duration'])
            
            with col_b:
                use_temporal = st.checkbox("Temporal Stabilization", preset['use_temporal'])
                use_nvenc = st.checkbox("Use NVENC", hw_mgr.check_nvenc())
        
        # Output path
        output_dir = st.text_input("Output Directory", "/app/outputs/")
        
        # Process button
        st.markdown("---")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            preview_btn = st.button("🔍 Preview (5s)", use_container_width=True, type="secondary")
        with col_btn2:
            process_btn = st.button("🎬 Process Full", use_container_width=True, type="primary")
    
    with col2:
        st.markdown("### Preview & Info")
        
        if not selected_styles:
            st.warning("⚠️ Select at least one style")
        else:
            st.success(f"✅ {len(selected_styles)} style(s) selected")
            
            # Display selected styles
            for style in selected_styles:
                st.markdown(f"- **{style}**")
        
        # Hardware info
        st.markdown("### Hardware Status")
        
        if hw_mgr.gpu_available:
            st.markdown(f"**GPU:** {hw_mgr.gpu_info.get('name', 'Unknown')}")
            
            mem_info = hw_mgr.get_gpu_memory_usage()
            if mem_info:
                st.progress(mem_info['utilization'] / 100.0, text=f"VRAM: {mem_info['utilization']:.1f}%")
            
            temp = hw_mgr.get_gpu_temperature()
            if temp:
                st.metric("GPU Temperature", f"{temp}°C")
        else:
            st.info("Running on CPU (GPU not detected)")
        
        # Preset info
        st.markdown("### Preset Details")
        st.json(preset)
    
    # Handle buttons
    if preview_btn:
        if not input_path:
            st.error("Please provide an input path")
        elif not selected_styles:
            st.error("Please select at least one style")
        else:
            with st.spinner("Generating preview..."):
                st.info("Preview functionality - processing 5 seconds...")
                # TODO: Implement preview
                st.success("Preview ready! (Feature in development)")
    
    if process_btn:
        if not input_path:
            st.error("Please provide an input path")
        elif not selected_styles:
            st.error("Please select at least one style")
        else:
            # Add to queue
            st.session_state.total_jobs += 1
            st.success(f"✅ Job added to queue! Job ID: {st.session_state.total_jobs}")
            st.info("Check 'Batch Queue' page to monitor progress")
            
            # Store job info
            if 'jobs' not in st.session_state:
                st.session_state.jobs = []
            
            st.session_state.jobs.append({
                'id': st.session_state.total_jobs,
                'input': input_path,
                'styles': selected_styles,
                'preset': preset_name,
                'status': 'Queued'
            })