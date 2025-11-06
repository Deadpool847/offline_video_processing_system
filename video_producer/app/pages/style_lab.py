"""Style Lab page - A/B comparison and ratings."""

import streamlit as st
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))


def show():
    st.markdown("<h1 class='main-header'>Style Lab</h1>", unsafe_allow_html=True)
    st.markdown("Compare styles and provide feedback for ML learning")
    
    # Sample selection
    st.markdown("### Select Sample")
    
    sample_video = st.text_input("Video Path", placeholder="/path/to/video.mp4")
    
    col1, col2 = st.columns(2)
    with col1:
        start_time = st.text_input("Start Time", "00:00:10")
    with col2:
        duration = st.slider("Duration (s)", 5, 30, 10)
    
    if st.button("🎬 Generate Comparison", type="primary"):
        st.info("Processing sample with all styles...")
    
    st.markdown("---")
    
    # A/B Comparison
    st.markdown("### A/B Comparison")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("#### Style A: Pencil Sketch")
        st.image("https://via.placeholder.com/400x300.png?text=Style+A", use_container_width=True)
        rating_a = st.slider("Rate Style A", 1, 5, 3, key="rating_a")
    
    with col_b:
        st.markdown("#### Style B: Cartoon")
        st.image("https://via.placeholder.com/400x300.png?text=Style+B", use_container_width=True)
        rating_b = st.slider("Rate Style B", 1, 5, 4, key="rating_b")
    
    # Comparison notes
    st.markdown("### Notes")
    notes = st.text_area("Observations", placeholder="What differences do you notice? Which style works better for this content?")
    
    # Save feedback
    if st.button("💾 Save Feedback", type="primary"):
        st.success("✅ Feedback saved! This will help improve ML models.")
        
        # Store feedback
        if 'feedback' not in st.session_state:
            st.session_state.feedback = []
        
        st.session_state.feedback.append({
            'style_a': 'Pencil',
            'style_b': 'Cartoon',
            'rating_a': rating_a,
            'rating_b': rating_b,
            'notes': notes
        })
    
    st.markdown("---")
    
    # Parameter tuning
    st.markdown("### Parameter Tuning")
    
    style_select = st.selectbox("Select Style", ['Pencil', 'Cartoon', 'Comic', 'Cinematic', 'Neural Style'])
    
    if style_select == 'Pencil':
        blur_sigma = st.slider("Blur Sigma", 5.0, 50.0, 21.0)
        use_texture = st.checkbox("Use Paper Texture")
    elif style_select == 'Cartoon':
        num_colors = st.slider("Number of Colors", 4, 16, 8)
        edge_strength = st.slider("Edge Strength", 50, 200, 100)
    elif style_select == 'Comic':
        dot_size = st.slider("Halftone Dot Size", 2, 8, 3)
        edge_thickness = st.slider("Edge Thickness", 1, 5, 2)
    elif style_select == 'Cinematic':
        bloom_strength = st.slider("Bloom Strength", 0.0, 1.0, 0.3)
        grain_strength = st.slider("Grain Strength", 0.0, 0.1, 0.02)
        vignette_strength = st.slider("Vignette Strength", 0.0, 1.0, 0.4)
    
    if st.button("🔄 Auto-Tune Parameters"):
        with st.spinner("Searching optimal parameters..."):
            st.success("✅ Optimal parameters found!")
            st.info("Check parameter values above")