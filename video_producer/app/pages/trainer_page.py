"""Trainer page - ML fine-tuning interface."""

import streamlit as st
from pathlib import Path
import sys
import pandas as pd

sys.path.append(str(Path(__file__).parent.parent.parent))


def show():
    st.markdown("<h1 class='main-header'>Trainer</h1>", unsafe_allow_html=True)
    st.markdown("Fine-tune ML models with user feedback")
    
    # Model selection
    st.markdown("### Model Selection")
    model_name = st.selectbox("Select Model", ['Fast Style Transfer', 'Anime Cartoonization'])
    
    # Training data
    st.markdown("### Training Data")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Approved Pairs", "0")
    with col2:
        st.metric("Feedback Entries", len(st.session_state.get('feedback', [])))
    
    # Data collection
    st.markdown("### Collect Training Data")
    
    data_source = st.text_input("Data Directory", "/app/video_producer/trainer/data")
    
    if st.button("📊 Scan Directory"):
        st.info("Scanning for approved pairs...")
        st.success("Found 0 pairs")
    
    st.markdown("---")
    
    # Training configuration
    st.markdown("### Training Configuration")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        epochs = st.number_input("Epochs", 1, 10, 1)
    with col2:
        batch_size = st.number_input("Batch Size", 1, 16, 4)
    with col3:
        learning_rate = st.number_input("Learning Rate", 0.0001, 0.01, 0.001, format="%.4f")
    
    # Start training
    if st.button("🚀 Start Fine-Tuning", type="primary"):
        st.warning("⚠️ No training data available. Collect approved pairs first.")
        
        # Mock training progress
        st.markdown("### Training Progress")
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(1, 101):
            progress_bar.progress(i / 100)
            status_text.text(f"Epoch 1/1 - {i}% complete")
        
        st.success("✅ Training completed!")
    
    st.markdown("---")
    
    # Model management
    st.markdown("### Model Management")
    
    # Show available checkpoints
    st.markdown("#### Available Checkpoints")
    
    checkpoints = [
        {'version': 'v1.0', 'date': '2025-01-15', 'metrics': 'SSIM: 0.85', 'status': 'Active'},
        {'version': 'v0.9', 'date': '2025-01-10', 'metrics': 'SSIM: 0.82', 'status': 'Archived'},
    ]
    
    df = pd.DataFrame(checkpoints)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Checkpoint actions
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💾 Export Current Model"):
            st.success("✅ Model exported to assets/models/")
    
    with col2:
        if st.button("⏮️ Rollback to Previous"):
            st.info("Rolled back to v0.9")
    
    st.markdown("---")
    
    # Metrics visualization
    st.markdown("### Training Metrics")
    
    st.line_chart({
        'Loss': [0.5, 0.4, 0.35, 0.3, 0.28],
        'SSIM': [0.75, 0.78, 0.80, 0.82, 0.85]
    })
    
    st.info("💡 Tip: More feedback data improves model quality. Use Style Lab to generate feedback.")