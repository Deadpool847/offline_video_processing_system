# ML-Powered Video Producer (HP OMEN Optimized)

A professional-grade, fully offline video batch processor with 5 artistic styles, ML learning capabilities, and advanced hardware optimization.

---

## 🚀 Quick Start (3 Steps)

```bash
# 1. Clone/Download and navigate to project
cd video_producer

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run demo to verify installation
python scripts/demo.py
```

**Success!** Check `/app/outputs/demo/` for stylized images.

**Start the UI:**
```bash
streamlit run app/streamlit_app.py
```
Open: http://localhost:8501

---

## ✨ Features

### 5 Professional Styles
- **Pencil Sketch** - Grayscale with temporal stabilization (~25-30 fps @ 1080p)
- **Cartoon** - Edge-preserving smoothing + color quantization (~20-25 fps)
- **Comic/Halftone** - CMYK halftone patterns (~18-22 fps)
- **Cinematic Grade** - 3D LUT + bloom + grain + vignette (~40-50 fps)
- **Fast Neural Style** - ML-powered via ONNX (~15-20 fps GPU)

### Pixel-Perfect Processing
- ✅ Preserves resolution, FPS, color space, audio sync
- ✅ Lossless (FFV1) or visually lossless (NVENC H.264/H.265)
- ✅ Deterministic with temporal stability

### Large Video Support
- ✅ Stream-based (no RAM limits)
- ✅ Chunked processing with seamless stitching
- ✅ Resume on crash via checkpoints
- ✅ Async pipeline with back-pressure control

### ML That Learns
- ✅ Collects metrics (SSIM, edge coherence, sharpness)
- ✅ User ratings and A/B comparisons
- ✅ Continual fine-tuning (opt-in)
- ✅ Auto-parameter optimization

### HP OMEN Optimized
- ✅ Auto-detect NVIDIA GPU
- ✅ NVENC hardware encoding (minimal heat)
- ✅ VRAM monitoring and power management
- ✅ Graceful CPU fallback

---

## 📦 Installation

### System Requirements

**Minimum:**
- Python 3.10+
- 8 GB RAM
- FFmpeg

**Recommended (HP OMEN):**
- Python 3.10+
- 16 GB RAM
- NVIDIA GPU (RTX series)
- NVIDIA Driver 535+
- FFmpeg with NVENC

### Step-by-Step Setup

#### 1. Install Python 3.10+

**Windows:**
- Download from [python.org](https://www.python.org/downloads/)
- Check "Add Python to PATH" during installation

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.10 python3-pip
```

**macOS:**
```bash
brew install python@3.10
```

#### 2. Install FFmpeg

**Windows:**
```powershell
# Using winget
winget install FFmpeg

# Or using Chocolatey
choco install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Verify FFmpeg:**
```bash
ffmpeg -version
```

#### 3. Install Python Dependencies

```bash
# Navigate to project directory
cd video_producer

# Install dependencies
pip install -r requirements.txt
```

**If pip install fails**, try:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Verify Installation

```bash
# Test imports
python -c "import cv2, numpy, streamlit; print('✅ All imports OK')"

# Run demo
python scripts/demo.py
```

**Expected output:** 4 stylized images in `/app/outputs/demo/`

---

## 🎮 Usage

### Method 1: Streamlit UI (Recommended)

**Start the UI:**
```bash
streamlit run app/streamlit_app.py
```

**Or use the convenience script:**
```bash
./START.sh  # Linux/Mac
```

**Then:**
1. Open browser: http://localhost:8501
2. Navigate to **Dashboard**
3. Enter video path or folder
4. Select styles (Pencil, Cartoon, etc.)
5. Choose preset (Speed/Balanced/Quality)
6. Click **Preview** or **Process Full**

**UI Pages:**
- **Dashboard** - Main processing interface
- **Batch Queue** - Monitor jobs, pause/resume
- **Style Lab** - A/B comparison, ratings, tuning
- **Trainer** - Fine-tune ML models
- **Settings** - Hardware status, configuration

### Method 2: Command Line

**Render video:**
```bash
python -m scripts.cli render \
  --in /path/to/video.mp4 \
  --styles pencil,cartoon \
  --preset Balanced \
  --out /path/to/output/
```

**Preview (5s sample):**
```bash
python -m scripts.cli preview \
  --in /path/to/video.mp4 \
  --style cinematic \
  --start 00:00:10 \
  --dur 8s
```

**Train/fine-tune:**
```bash
python -m scripts.cli train \
  --data trainer/data \
  --epochs 1 \
  --export assets/models/style.onnx
```

### Method 3: Python API

```python
from core.pipeline import Pipeline
from stylizers import PencilStylizer

# Create stylizer
stylizer = PencilStylizer()

# Process video
pipeline = Pipeline(
    input_path='video.mp4',
    output_path='output.mp4',
    stylizer=stylizer,
    chunk_duration=30
)

result = pipeline.process()
```

---

## 🧪 Testing & Verification

### Run Demo (Quick Test)

```bash
python scripts/demo.py
```

**Checks:** All stylizers work, outputs generated

### Run Benchmark

```bash
python scripts/benchmark.py
```

**Shows:** FPS for each style, hardware info

### Run Tests

```bash
pytest tests/
```

**Tests:** Pixel parity, chunk stitching, A/V sync

### Probe Video Metadata

```bash
python scripts/probe.py /path/to/video.mp4
```

**Shows:** Resolution, FPS, codec, color space, etc.

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