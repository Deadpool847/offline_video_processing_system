# Installation Guide

## System Requirements

### Minimum
- Python 3.10+
- 8 GB RAM
- FFmpeg

### Recommended (HP OMEN)
- Python 3.10+
- 16 GB RAM
- NVIDIA GPU (RTX series recommended)
- NVIDIA Driver 535+
- FFmpeg with NVENC support

## Installation Steps

### 1. Install System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install -y python3.10 python3-pip ffmpeg pkg-config
```

**Windows:**
```powershell
# Install Python 3.10+ from python.org
# Install FFmpeg
winget install FFmpeg
```

### 2. Install Python Dependencies

```bash
cd /app/video_producer

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows

# Install packages
pip install --upgrade pip
pip install -r requirements.txt
```

**Note:** If `av` (PyAV) fails to install:
```bash
# Ubuntu/Debian
sudo apt install -y libavformat-dev libavcodec-dev libavdevice-dev libavutil-dev libswscale-dev libavresample-dev

# Then retry
pip install av
```

### 3. Verify Installation

```bash
# Check FFmpeg
ffmpeg -version

# Check NVENC (GPU encoding)
ffmpeg -hide_banner -encoders | grep nvenc
# Should show: h264_nvenc, hevc_nvenc

# Check Python packages
python -c "import cv2, numpy, streamlit, onnxruntime; print('All imports OK')"
```

### 4. Download ONNX Models (Optional)

```bash
python scripts/download_models.py
```

Or manually place ONNX models in `assets/models/`

### 5. Test Installation

```bash
# Run demo
python scripts/demo.py

# Run benchmarks
python scripts/benchmark.py
```

## GPU Setup (NVIDIA)

### Check NVIDIA Driver

```bash
nvidia-smi
```

You should see:
- Driver version 535+
- CUDA version 12.0+
- GPU name and memory

### Install CUDA (if needed)

**Ubuntu:**
```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.0-1_all.deb
sudo dpkg -i cuda-keyring_1.0-1_all.deb
sudo apt update
sudo apt install -y cuda-toolkit-12-0
```

### Verify ONNX Runtime GPU

```bash
python -c "import onnxruntime as ort; print(ort.get_available_providers())"
# Should include: CUDAExecutionProvider
```

## Running the Application

### Streamlit UI (Recommended)

```bash
streamlit run app/streamlit_app.py
```

Open browser at: http://localhost:8501

### Command Line

```bash
# Render video
python -m scripts.cli render \
  --in /path/to/video.mp4 \
  --styles pencil,cartoon \
  --preset Balanced \
  --out /app/outputs/

# Preview
python -m scripts.cli preview \
  --in /path/to/video.mp4 \
  --style cinematic \
  --start 00:00:10 \
  --dur 8s
```

## Troubleshooting

### "NVENC not available"

**Solution:**
1. Update NVIDIA drivers to 535+
2. Reinstall FFmpeg with NVENC support
3. Verify: `ffmpeg -encoders | grep nvenc`

### "Out of memory"

**Solution:**
1. Reduce chunk size in Settings
2. Enable working resolution downscaling
3. Limit concurrent jobs to 1

### "PyAV installation failed"

**Solution:**
```bash
# Install system dependencies first
sudo apt install -y pkg-config libavformat-dev libavcodec-dev
pip install av
```

### "CUDA not found"

**Solution:**
- CUDA is optional for CPU processing
- For GPU acceleration, install CUDA Toolkit 12.0+
- Verify: `nvidia-smi`

## Performance Tips

### HP OMEN Optimization

1. **Enable NVENC** (Settings page)
2. **Set power limit** (optional):
   ```bash
   nvidia-smi -pl 150  # 150W limit
   ```
3. **Single GPU job** (default)
4. **Monitor temps** (Settings page)

### Best Practices

- Use **Balanced** preset for most cases
- Enable **temporal stabilization** for smooth output
- Process large videos with **chunking** (auto)
- Use **preview** before full render

## Uninstallation

```bash
# Remove Python packages
pip uninstall -r requirements.txt -y

# Remove virtual environment
rm -rf venv/

# Remove outputs
rm -rf outputs/ logs/ checkpoints/
```