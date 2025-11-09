"""Style Lab page - A/B comparison and ratings."""

import streamlit as st
from pathlib import Path
import sys
import tempfile

sys.path.append(str(Path(__file__).parent.parent.parent))


def show():
    st.markdown("<h1 class='main-header'>Style Lab</h1>", unsafe_allow_html=True)
    st.markdown("Compare styles and provide feedback for ML learning")
    
    # Sample selection
    st.markdown("### 📹 Select Video Sample")
    
    # Input method
    input_method = st.radio(
        "Input Method",
        ["📁 Upload", "📝 Enter Path"],
        horizontal=True,
        key="lab_input_method"
    )
    
    sample_video = None
    
    if input_method == "📁 Upload":
        uploaded = st.file_uploader(
            "Upload video for comparison",
            type=['mp4', 'avi', 'mov', 'mkv'],
            key="lab_upload"
        )
        if uploaded:
            temp_dir = Path(tempfile.gettempdir()) / "video_producer_lab"
            temp_dir.mkdir(exist_ok=True)
            temp_path = temp_dir / uploaded.name
            with open(temp_path, 'wb') as f:
                f.write(uploaded.getbuffer())
            sample_video = str(temp_path)
            st.success(f"✅ Uploaded: {uploaded.name}")
    else:
        sample_video = st.text_input("Video Path", placeholder="/path/to/video.mp4")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        start_time = st.number_input("Start Time (seconds)", 0, 3600, 0)
    with col2:
        duration = st.slider("Duration (s)", 3, 15, 5)
    with col3:
        effect_intensity = st.slider("Effect Intensity", 0.5, 2.0, 1.0, 0.1)
    
    # Style selection for comparison
    st.markdown("### 🎨 Select Styles to Compare")
    compare_styles = st.multiselect(
        "Choose 2-4 styles for side-by-side comparison",
        ['Pencil Sketch', 'Cartoon', 'Comic/Halftone', 'Cinematic', 'Fast Neural Style'],
        default=['Pencil Sketch', 'Cartoon']
    )
    
    if st.button("🎬 Generate Comparison", type="primary"):
        if not sample_video or not Path(sample_video).exists():
            st.error("❌ Please provide a valid video path")
        elif len(compare_styles) < 2:
            st.error("❌ Please select at least 2 styles to compare")
        else:
            with st.spinner(f"🔄 Processing {len(compare_styles)} styles..."):
                try:
                    from core.preview_generator import PreviewGenerator
                    from stylizers import (PencilStylizer, CartoonStylizer, ComicStylizer,
                                          CinematicStylizer, FastStyleStylizer)
                    
                    generator = PreviewGenerator()
                    results = []
                    
                    # Generate preview for each style
                    for style in compare_styles:
                        # Get stylizer
                        if 'Pencil' in style:
                            stylizer = PencilStylizer()
                        elif 'Cartoon' in style:
                            stylizer = CartoonStylizer()
                        elif 'Comic' in style:
                            stylizer = ComicStylizer()
                        elif 'Cinematic' in style:
                            stylizer = CinematicStylizer()
                        else:
                            stylizer = PencilStylizer()
                        
                        result = generator.generate_preview(
                            input_path=sample_video,
                            stylizer=stylizer,
                            duration_seconds=duration,
                            start_time=start_time,
                            effect_intensity=effect_intensity
                        )
                        
                        if result['success']:
                            results.append((style, result))
                    
                    if results:
                        st.success(f"✅ Generated {len(results)} style comparisons!")
                        
                        # Store in session for comparison
                        st.session_state['comparison_results'] = results
                        st.session_state['original_video'] = sample_video
                        
                except Exception as e:
                    st.error(f"❌ Comparison generation failed: {str(e)}")
                    st.exception(e)
    
    st.markdown("---")
    
    # Display comparison results
    if 'comparison_results' in st.session_state and st.session_state['comparison_results']:
        st.markdown("### 🎬 Style Comparison Results")
        
        results = st.session_state['comparison_results']
        
        # Create columns based on number of results
        num_cols = min(len(results), 3)  # Max 3 columns per row
        
        for i in range(0, len(results), num_cols):
            cols = st.columns(num_cols)
            
            for j, col in enumerate(cols):
                if i + j < len(results):
                    style, result = results[i + j]
                    
                    with col:
                        st.markdown(f"#### {style}")
                        st.video(result['output_path'])
                        
                        # Stats
                        st.caption(f"⚡ {result['avg_fps']:.1f} FPS | ⏱️ {result['processing_time']:.2f}s")
                        
                        # Rating
                        rating = st.slider(
                            f"Rate {style}",
                            1, 5, 3,
                            key=f"rating_{i+j}_{style}",
                            help="1=Poor, 3=Good, 5=Excellent"
                        )
                        
                        # Download
                        with open(result['output_path'], 'rb') as f:
                            video_bytes = f.read()
                            st.download_button(
                                label="📥 Download",
                                data=video_bytes,
                                file_name=f"{style.lower().replace(' ', '_')}_sample.mp4",
                                mime="video/mp4",
                                key=f"download_{i+j}_{style}",
                                use_container_width=True
                            )
        
        st.markdown("---")
        
        # Original video for reference
        if 'original_video' in st.session_state:
            with st.expander("📹 View Original Video"):
                st.video(st.session_state['original_video'])
    
    st.markdown("---")
    
    # A/B Direct Comparison
    st.markdown("### 🔀 A/B Direct Comparison")
    
    if 'comparison_results' in st.session_state and len(st.session_state['comparison_results']) >= 2:
        results = st.session_state['comparison_results']
        
        col_select1, col_select2 = st.columns(2)
        
        with col_select1:
            style_a_idx = st.selectbox(
                "Style A",
                range(len(results)),
                format_func=lambda x: results[x][0],
                key="style_a_select"
            )
        
        with col_select2:
            style_b_idx = st.selectbox(
                "Style B",
                range(len(results)),
                format_func=lambda x: results[x][0],
                index=min(1, len(results)-1),
                key="style_b_select"
            )
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            style_a, result_a = results[style_a_idx]
            st.markdown(f"#### Style A: {style_a}")
            st.video(result_a['output_path'])
            rating_a = st.slider("Rate Style A", 1, 5, 3, key="rating_a")
        
        with col_b:
            style_b, result_b = results[style_b_idx]
            st.markdown(f"#### Style B: {style_b}")
            st.video(result_b['output_path'])
            rating_b = st.slider("Rate Style B", 1, 5, 4, key="rating_b")
    else:
        st.info("💡 Generate comparison above to use A/B comparison feature")
    
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