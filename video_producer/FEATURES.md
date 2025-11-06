# Feature Specifications

## Core Features

### 1. Pixel-Perfect I/O

**Specification:**
- Preserve original resolution, FPS, and aspect ratio
- Maintain color space (bt601/bt709/bt2020)
- Preserve color transfer and range (full/limited)
- Audio sync within ±1ms
- Support lossless (FFV1/ProRes) and visually lossless (NVENC H.264/H.265)

**Implementation:**
- `core/io.py`: VideoProbe, VideoReader, VideoWriter
- `core/color.py`: ColorSpaceManager for color preservation
- FFmpeg-based with precise metadata extraction

**Validation:**
- `tests/test_pixel_parity.py`: Identity pass byte-exact check
- `tests/test_timing_audio.py`: A/V sync validation

---

### 2. Large Video Robustness

**Specification:**
- Stream-based frame processing (no full RAM decode)
- Chunked processing (configurable 10-120s chunks)
- Resume on crash with checkpoint files
- Async pipeline with back-pressure control
- Disk space preflight checks

**Implementation:**
- `core/pipeline.py`: Pipeline class with chunking
- `core/checkpoint.py`: CheckpointManager for resume
- PyAV for efficient streaming
- GOP boundary detection for seamless stitching

**Validation:**
- `tests/test_chunk_stitch.py`: Chunked vs single-pass comparison
- Checkpoint resume functionality

---

### 3. ML That Improves Over Time

**Specification:**
- Collect per-frame metrics (SSIM, LPIPS, edge coherence, sharpness)
- User ratings (1-5 stars) and A/B comparisons
- Continual learning with fine-tuning (opt-in)
- Auto-parameter search for style optimization
- Versioned checkpoints with rollback

**Implementation:**
- `core/metrics.py`: MetricsCollector for measurement
- `core/autotune.py`: AutoTuner for parameter search
- `trainer/finetune.py`: FineTuner for model updates
- `trainer/export_onnx.py`: PyTorch to ONNX export
- Style Lab UI for feedback collection

**Features:**
- Feedback logging (JSON)
- Training on approved pairs
- Metric-guided optimization
- Model versioning

---

### 4. Advanced Streamlit UI

**Specification:**
- Multi-page app (Dashboard, Queue, Lab, Trainer, Settings)
- File/folder upload with style multi-select
- Preset slider (Speed/Balanced/Quality)
- Live progress bars with ETA and FPS
- Preview on 5-10s clips
- A/B viewer with split/swipe comparison
- 5-star ratings and notes
- Job queue with pause/resume/cancel
- Hardware monitoring (GPU temp, VRAM, utilization)

**Implementation:**
- `app/streamlit_app.py`: Main app entry
- `app/pages/dashboard.py`: Processing interface
- `app/pages/batch_queue.py`: Job management
- `app/pages/style_lab.py`: Comparison and feedback
- `app/pages/trainer_page.py`: Fine-tuning UI
- `app/pages/settings_page.py`: Hardware config

**Features:**
- Real-time job monitoring
- Interactive parameter tuning
- Visual feedback collection
- Preset management

---

### 5. Hardware Optimization (HP OMEN)

**Specification:**
- Auto-detect NVIDIA GPU via NVML
- NVENC hardware encoding (h264_nvenc/hevc_nvenc)
- VRAM monitoring and backoff
- GPU temperature monitoring
- Power management hints (nvidia-smi -pl)
- Single GPU job + CPU jobs in parallel
- Graceful CPU fallback

**Implementation:**
- `core/hardware.py`: HardwareManager
- pynvml for GPU monitoring
- NVENC detection via FFmpeg
- Settings UI for configuration

**Features:**
- Real-time VRAM usage
- Temperature alerts
- Codec recommendation
- Power cap guidance

---

## Style Processors

### 1. Pencil Sketch

**Algorithm:**
1. Convert to grayscale
2. Invert image
3. Gaussian blur (sigma=21)
4. Color dodge blend
5. Optional paper texture overlay
6. Temporal EMA for stability

**Parameters:**
- `blur_sigma`: 5.0-50.0 (default 21.0)
- `use_texture`: boolean
- `texture_path`: optional

**Performance:** ~25-30 fps @ 1080p CPU

---

### 2. Cartoon

**Algorithm:**
1. Bilateral filter for edge-preserving smoothing
2. K-means color quantization (4-16 colors)
3. Canny edge detection
4. Edge dilation
5. Combine with black edges
6. Temporal EMA

**Parameters:**
- `bilateral_d`: 9
- `bilateral_sigma_color`: 75.0
- `bilateral_sigma_space`: 75.0
- `num_colors`: 4-16 (default 8)
- `edge_threshold1/2`: 50/150

**Performance:** ~20-25 fps @ 1080p CPU

---

### 3. Comic/Halftone

**Algorithm:**
1. Convert RGB to CMYK (approximation)
2. Create halftone patterns for each channel
3. Angle-based dot placement (C:15°, M:75°, Y:0°, K:45°)
4. Combine back to RGB
5. Add bold edges
6. Temporal EMA

**Parameters:**
- `dot_size`: 2-8 (default 3)
- `angles`: CMYK angles
- `edge_thickness`: 1-5 (default 2)

**Performance:** ~18-22 fps @ 1080p CPU

---

### 4. Cinematic

**Algorithm:**
1. Apply 3D LUT (.cube file)
2. S-curve tone adjustment
3. Bloom effect (bright area blur)
4. Film grain (Gaussian noise)
5. Vignette (radial gradient)

**Parameters:**
- `lut_path`: .cube file
- `bloom_strength`: 0.0-1.0 (default 0.3)
- `grain_strength`: 0.0-0.1 (default 0.02)
- `vignette_strength`: 0.0-1.0 (default 0.4)

**Performance:** ~40-50 fps @ 1080p CPU/GPU

---

### 5. Fast Neural Style

**Algorithm:**
1. Load ONNX style transfer model
2. Tiled inference for 4K+ (512px tiles, 32px overlap)
3. Feathering for seamless blending
4. NHWC↔NCHW format conversion
5. GPU acceleration via CUDA EP

**Parameters:**
- `model_path`: ONNX file
- `tile_size`: 512 (default)
- `overlap`: 32 (default)
- `use_gpu`: boolean

**Performance:** ~15-20 fps @ 1080p GPU, ~3-5 fps CPU

---

## Temporal Stability

**Implementation:**
- Exponential Moving Average (EMA) with alpha=0.3
- Applied to:
  - Full frames
  - Edge maps
  - Threshold values
- Optional optical flow deflicker (advanced)

**Benefits:**
- Eliminates frame-to-frame flicker
- Smooth transitions
- Stable edges

---

## File Format Support

**Input:**
- Video: MP4, AVI, MOV, MKV, WebM
- Codecs: H.264, H.265, VP9, ProRes

**Output:**
- Lossless: FFV1 (MKV), ProRes (MOV)
- Visually Lossless: H.264/H.265 NVENC (CRF 15-23)
- Fallback: libx264/libx265 (CPU)

**Audio:**
- Pass-through or re-encode (AAC 192kbps)
- Maintains sync

---

## Performance Benchmarks

**Test System: HP OMEN (RTX 3070, i7, 16GB RAM)**

| Style | 1080p FPS | 4K FPS | Device |
|-------|-----------|--------|--------|
| Pencil | 25-30 | 8-10 | CPU |
| Cartoon | 20-25 | 6-8 | CPU |
| Comic | 18-22 | 5-7 | CPU |
| Cinematic | 40-50 | 12-15 | CPU/GPU |
| Neural | 15-20 | 4-6 | GPU |
| Encoding (NVENC) | 200+ | 60+ | GPU |

**Notes:**
- CPU: Single-threaded OpenCV/NumPy
- GPU: ONNX Runtime with CUDA EP
- NVENC: Hardware encoder (minimal CPU/GPU load)

---

## API Reference

### Core Classes

```python
# Video I/O
from core.io import VideoReader, VideoWriter, VideoProbe

metadata = VideoProbe.probe('video.mp4')

with VideoReader('video.mp4') as reader:
    for frame in reader.read_frames():
        # Process frame
        pass

with VideoWriter('output.mp4', width, height, fps, codec='h264_nvenc') as writer:
    writer.write_frame(frame)

# Pipeline
from core.pipeline import Pipeline

pipeline = Pipeline(
    input_path='input.mp4',
    output_path='output.mp4',
    stylizer=stylizer_func,
    chunk_duration=30,
    use_temporal=True
)

result = pipeline.process(progress_callback=callback)

# Stylizers
from stylizers import PencilStylizer, CartoonStylizer

stylizer = PencilStylizer(blur_sigma=21.0)
result = stylizer.process(frame)
```

### CLI Commands

```bash
# Render
python -m scripts.cli render --in video.mp4 --styles pencil,cartoon --out outputs/

# Preview
python -m scripts.cli preview --in video.mp4 --style cinematic --start 00:00:10

# Train
python -m scripts.cli train --data trainer/data --epochs 1 --export model.onnx
```