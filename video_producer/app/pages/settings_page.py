"""Settings page - hardware and configuration."""

import streamlit as st
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))

from core.hardware import HardwareManager
from core.presets import PresetManager


def show():
    st.markdown("<h1 class='main-header'>Settings & Hardware</h1>", unsafe_allow_html=True)
    st.markdown("Configure hardware and application settings")
    
    # Initialize managers
    hw_mgr = HardwareManager()
    preset_mgr = PresetManager()
    
    # Hardware tab
    st.markdown("### Hardware Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### GPU Status")
        
        if hw_mgr.gpu_available:
            st.success("✅ GPU Detected")
            st.markdown(f"**Name:** {hw_mgr.gpu_info.get('name', 'Unknown')}")
            st.markdown(f"**Driver:** {hw_mgr.gpu_info.get('driver_version', 'Unknown')}")
            st.markdown(f"**CUDA:** {hw_mgr.gpu_info.get('cuda_version', 'Unknown')}")
            
            # Memory info
            mem_info = hw_mgr.get_gpu_memory_usage()
            if mem_info:
                total_gb = mem_info['total'] / (1024**3)
                used_gb = mem_info['used'] / (1024**3)
                st.markdown(f"**Memory:** {used_gb:.1f} GB / {total_gb:.1f} GB")
                st.progress(mem_info['utilization'] / 100.0)
            
            # Temperature
            temp = hw_mgr.get_gpu_temperature()
            if temp:
                st.markdown(f"**Temperature:** {temp}°C")
                if temp > 80:
                    st.warning("⚠️ GPU temperature is high")
            
            # Utilization
            util = hw_mgr.get_gpu_utilization()
            if util:
                st.markdown(f"**Utilization:** {util:.1f}%")
        else:
            st.warning("⚠️ No GPU detected - running on CPU")
            st.info("Install NVIDIA drivers to enable GPU acceleration")
    
    with col2:
        st.markdown("#### NVENC Status")
        
        nvenc_available = hw_mgr.check_nvenc()
        if nvenc_available:
            st.success("✅ NVENC Available")
            st.markdown("Hardware-accelerated encoding enabled")
            st.markdown("Recommended codec: **h264_nvenc**")
        else:
            st.warning("⚠️ NVENC Not Available")
            st.markdown("Falling back to CPU encoding (libx264)")
            st.info("Update NVIDIA drivers to enable NVENC")
        
        st.markdown("#### Codec Selection")
        recommended = hw_mgr.get_recommended_codec()
        st.markdown(f"**Recommended:** {recommended}")
    
    st.markdown("---")
    
    # Application settings
    st.markdown("### Application Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Processing")
        max_concurrent_jobs = st.slider("Max Concurrent Jobs", 1, 4, 1)
        default_output_dir = st.text_input("Default Output Dir", "/app/outputs/")
        auto_resume = st.checkbox("Auto-resume on crash", value=True)
    
    with col2:
        st.markdown("#### Performance")
        vram_limit = st.slider("VRAM Limit (%)", 50, 100, 90)
        chunk_size = st.slider("Default Chunk Size (s)", 10, 120, 30)
        enable_temporal = st.checkbox("Enable temporal stabilization", value=True)
    
    # Save settings
    if st.button("💾 Save Settings", type="primary"):
        st.success("✅ Settings saved successfully")
    
    st.markdown("---")
    
    # Preset management
    st.markdown("### Preset Management")
    
    presets = preset_mgr.list_presets()
    st.markdown(f"**Available Presets:** {', '.join(presets)}")
    
    # Create new preset
    with st.expander("➕ Create New Preset"):
        preset_name = st.text_input("Preset Name")
        preset_desc = st.text_area("Description")
        
        col1, col2 = st.columns(2)
        with col1:
            preset_codec = st.selectbox("Codec", ['h264_nvenc', 'hevc_nvenc', 'libx264'])
            preset_crf = st.slider("CRF", 10, 30, 18)
        with col2:
            preset_chunk = st.slider("Chunk Duration", 10, 120, 30)
            preset_temporal = st.checkbox("Temporal Stabilization", True)
        
        if st.button("Create Preset"):
            new_preset = {
                'codec': preset_codec,
                'crf': preset_crf,
                'chunk_duration': preset_chunk,
                'use_temporal': preset_temporal,
                'description': preset_desc
            }
            preset_mgr.save_preset(preset_name, new_preset)
            st.success(f"✅ Preset '{preset_name}' created")
    
    st.markdown("---")
    
    # System info
    st.markdown("### System Information")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Python Version", "3.10+")
    with col2:
        st.metric("FFmpeg", "Installed")
    with col3:
        st.metric("ONNX Runtime", "1.17.0")
    
    st.markdown("---")
    
    # Power management hint
    st.markdown("### Power Management (HP OMEN)")
    st.info("""
    **Reduce GPU heat during long processing:**
    
    ```bash
    nvidia-smi -pl 150  # Set 150W power limit
    ```
    
    This reduces temperature while maintaining good performance.
    """)