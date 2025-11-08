"""Dashboard page - main processing interface."""

import streamlit as st
from pathlib import Path
import sys
import tempfile
import os

sys.path.append(str(Path(__file__).parent.parent.parent))

from core.presets import PresetManager
from core.hardware import HardwareManager


def show():
    st.markdown("<h1 class='main-header'>Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("Process videos with artistic styles powered by intelligent pattern learning")
    
    # Initialize managers
    preset_mgr = PresetManager()
    hw_mgr = HardwareManager()
    job_manager = st.session_state.job_manager
    
    # Two columns: Input | Preview
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📁 Input Configuration")
        
        # File upload options
        input_method = st.radio(
            "Input Method",
            ["📁 File Browser (Upload)", "📝 Enter Path", "🗂️ Folder Path"],
            horizontal=True
        )
        
        input_path = None
        
        if input_method == "📁 File Browser (Upload)":
            uploaded_file = st.file_uploader(
                "Choose a video file",
                type=['mp4', 'avi', 'mov', 'mkv', 'webm'],
                help="Upload a video file from your computer"
            )
            
            if uploaded_file:
                # Save uploaded file to temporary location
                temp_dir = Path(tempfile.gettempdir()) / "video_producer_uploads"
                temp_dir.mkdir(exist_ok=True)
                
                temp_path = temp_dir / uploaded_file.name
                with open(temp_path, 'wb') as f:
                    f.write(uploaded_file.getbuffer())
                
                input_path = str(temp_path)
                st.success(f"✅ Uploaded: {uploaded_file.name}")
                st.info(f"📍 Location: {input_path}")
        
        elif input_method == "📝 Enter Path":
            input_path = st.text_input(
                "Video Path",
                placeholder="/path/to/video.mp4 or C:\\Videos\\video.mp4",
                help="Enter the full path to your video file"
            )
        
        else:  # Folder Path
            input_path = st.text_input(
                "Folder Path",
                placeholder="/path/to/videos/ or C:\\Videos\\",
                help="Enter path to folder containing multiple videos"
            )
        
        st.markdown("---")
        
        # Style selection
        st.markdown("### 🎨 Style Selection")
        
        col_s1, col_s2 = st.columns(2)
        
        with col_s1:
            style_pencil = st.checkbox('✏️ Pencil Sketch', value=True)
            style_cartoon = st.checkbox('🎭 Cartoon', value=False)
            style_comic = st.checkbox('📰 Comic/Halftone', value=False)
        
        with col_s2:
            style_cinematic = st.checkbox('🎬 Cinematic', value=False)
            style_neural = st.checkbox('🧠 Neural Style', value=False)
        
        styles = {
            'Pencil Sketch': style_pencil,
            'Cartoon': style_cartoon,
            'Comic/Halftone': style_comic,
            'Cinematic': style_cinematic,
            'Fast Neural Style': style_neural
        }
        
        selected_styles = [k for k, v in styles.items() if v]
        
        st.markdown("---")
        
        # Effect Intensity Slider
        st.markdown("### 🎚️ Effect Intensity")
        effect_intensity = st.slider(
            "Adjust how strong the effect is applied",
            min_value=0.1,
            max_value=2.0,
            value=1.0,
            step=0.1,
            help="1.0 = Normal, < 1.0 = Subtle, > 1.0 = Strong"
        )
        
        intensity_label = "Subtle" if effect_intensity < 0.7 else "Normal" if effect_intensity <= 1.3 else "Strong"
        st.caption(f"Current intensity: **{intensity_label}** ({effect_intensity}x)")
        
        st.markdown("---")
        
        # Preset selection
        st.markdown("### ⚡ Quality Preset")
        preset_name = st.select_slider(
            "Preset",
            options=['Speed', 'Balanced', 'Quality'],
            value='Balanced',
            help="Speed = Fast processing | Balanced = Good quality & speed | Quality = Best output"
        )
        
        preset = preset_mgr.get_preset(preset_name)
        
        # Advanced settings (expandable)
        with st.expander("⚙️ Advanced Settings"):
            col_a, col_b = st.columns(2)
            
            with col_a:
                custom_crf = st.slider("CRF Quality", 10, 30, preset['crf'],
                                      help="Lower = Better quality, larger file")
                chunk_duration = st.slider("Chunk Duration (s)", 10, 120, preset['chunk_duration'],
                                          help="Duration of each processing chunk")
            
            with col_b:
                use_temporal = st.checkbox("Temporal Stabilization", preset['use_temporal'],
                                          help="Prevents flickering between frames")
                use_nvenc = st.checkbox("Use NVENC", hw_mgr.check_nvenc(),
                                       help="Use GPU hardware encoding if available")
        
        # Output path
        output_dir = st.text_input(
            "Output Directory",
            "/app/outputs/",
            help="Where processed videos will be saved"
        )
        
        # Process button
        st.markdown("---")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            preview_btn = st.button("🔍 Preview (5s)", use_container_width=True, type="secondary",
                                   help="Process first 5 seconds to preview result")
        with col_btn2:
            process_btn = st.button("🎬 Process Full Video", use_container_width=True, type="primary",
                                   help="Process the entire video")
    
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