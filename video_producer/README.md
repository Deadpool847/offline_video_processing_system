# ML-Powered Video Producer (HP OMEN Optimized)

A professional-grade, fully offline video batch processor with 5 artistic styles, ML learning capabilities, and advanced hardware optimization.

## Features

✨ **5 Professional Styles**
- Pencil Sketch (temporal stabilized)
- Cartoon (edge-preserving smoothing)
- Comic/Halftone (CMYK patterns)
- Cinematic Grade (3D LUT + bloom + grain)
- Fast Neural Style (ML-powered)

🎯 **Pixel-Perfect Processing**
- Preserves resolution, FPS, color space, audio sync
- Lossless (FFV1/ProRes) or visually lossless (NVENC H.264/H.265)
- Deterministic processing with temporal stability

🚀 **Large Video Support**
- Stream-based processing (no RAM limits)
- Chunked processing with seamless stitching
- Resume on crash/interruption
- Async pipeline with back-pressure control

🧠 **ML That Learns**
- Collects metrics (LPIPS, SSIM, edge coherence)
- User ratings and A/B comparisons
- Continual fine-tuning (opt-in)
- Auto-parameter optimization

💻 **HP OMEN Optimized**
- Auto-detect NVIDIA GPU
- NVENC hardware encoding (minimal heat)
- VRAM monitoring and power management
- Graceful CPU fallback

## Installation

### Prerequisites

**Windows (HP OMEN):**
```bash
# 1. Install Python 3.10+
# 2. Install NVIDIA drivers (535+ recommended)
# 3. Install FFmpeg with NVENC support
winget install FFmpeg
```

**Linux:**
```bash
sudo apt update
sudo apt install python3.10 python3-pip ffmpeg
```

### Setup

```bash
cd /app/video_producer
pip install -r requirements.txt
```

### Verify NVENC

```bash
ffmpeg -hide_banner -encoders | grep nvenc
# Should show: h264_nvenc, hevc_nvenc
```

## Usage

### Streamlit UI (Recommended)

```bash
streamlit run app/streamlit_app.py
```

Open browser at http://localhost:8501

### CLI

**Render:**
```bash
python -m scripts.cli render --in videos/ --styles pencil,comic --preset Balanced --out output/
```

**Preview:**
```bash
python -m scripts.cli preview --in video.mp4 --style cinematic --start 00:00:10 --dur 8s
```

**Train:**
```bash
python -m scripts.cli train --data trainer/data --epochs 1 --export assets/models/fast_style.onnx
```

## Architecture

```
video_producer/
├── app/                    # Streamlit multi-page UI
├── stylizers/             # 5 style processors
├── core/                  # Pipeline, I/O, ML, metrics
├── trainer/               # Fine-tuning system
├── assets/                # LUTs, textures, ONNX models
├── tests/                 # Unit tests
└── scripts/               # CLI and utilities
```

## Hardware Notes

**GPU Detection:**
- Auto-detects NVIDIA GPU via pynvml
- Enables NVENC if available
- Falls back to CPU gracefully

**Power Management (Optional):**
```bash
# Limit GPU power to reduce heat
nvidia-smi -pl 150  # 150W cap
```

**VRAM:**
- Monitors VRAM usage
- Backs off if memory pressure detected
- Configurable limits in Settings

## Testing

```bash
pytest tests/
```

**Key Tests:**
- `test_pixel_parity.py` - Identity pass validation
- `test_chunk_stitch.py` - Chunked vs single-pass comparison
- `test_timing_audio.py` - A/V sync verification

## Performance

**1080p @ 30fps (HP OMEN RTX 3070):**
- Pencil/Cartoon: ~25-30 fps (CPU)
- Comic: ~20-25 fps (CPU)
- Cinematic: ~40-50 fps (CPU/GPU LUT)
- Fast Neural Style: ~15-20 fps (ONNX GPU)
- Encoding (NVENC): ~200+ fps

## Troubleshooting

**"NVENC not available":**
- Update NVIDIA drivers
- Verify with: `ffmpeg -encoders | grep nvenc`
- Will auto-fallback to CPU (libx264)

**"Out of memory":**
- Reduce concurrent jobs in Settings
- Enable chunk processing
- Lower working resolution

**"Audio sync issues":**
- Check source video integrity
- Enable exact frame timing in Settings

## License

MIT License - Built for HP OMEN optimization

## Credits

- FFmpeg for robust video I/O
- ONNX Runtime for ML inference
- Streamlit for beautiful UI