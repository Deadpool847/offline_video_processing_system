# Complete Installation Guide

## System Requirements

### Minimum (CPU-only mode)
- **OS:** Windows 10/11, Ubuntu 20.04+, macOS 11+
- **Python:** 3.10 or higher
- **RAM:** 8 GB
- **Storage:** 2 GB free space
- **Software:** FFmpeg

### Recommended (HP OMEN / GPU mode)
- **OS:** Windows 10/11, Ubuntu 20.04+
- **Python:** 3.10 or higher
- **RAM:** 16 GB
- **GPU:** NVIDIA RTX series (3060+)
- **Driver:** NVIDIA Driver 535+
- **Storage:** 5 GB free space
- **Software:** FFmpeg with NVENC support

---

## Step-by-Step Installation

### Step 1: Install Python 3.10+

#### Windows

**Option A: Official Installer (Recommended)**
1. Download from [python.org/downloads](https://www.python.org/downloads/)
2. Run installer
3. ✅ **Important:** Check "Add Python to PATH"
4. Click "Install Now"

**Option B: Microsoft Store**
```powershell
# Search "Python 3.10" in Microsoft Store
# Click Install
```

**Verify:**
```powershell
python --version
# Should show: Python 3.10.x or higher
```

#### Linux (Ubuntu/Debian)

```bash
# Update package list
sudo apt update

# Install Python 3.10
sudo apt install -y python3.10 python3-pip python3-venv

# Verify
python3.10 --version
```

#### macOS

**Option A: Homebrew (Recommended)**
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.10

# Verify
python3 --version
```

**Option B: Official Installer**
1. Download from [python.org/downloads/macos](https://www.python.org/downloads/macos/)
2. Run .pkg installer
3. Follow prompts

---

### Step 2: Install FFmpeg

#### Windows

**Option A: winget (Windows 10 1809+)**
```powershell
winget install FFmpeg
```

**Option B: Chocolatey**
```powershell
# Install Chocolatey first (if not installed)
# Visit: chocolatey.org/install

# Then install FFmpeg
choco install ffmpeg
```

**Option C: Manual Installation**
1. Download from [ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Extract to `C:\ffmpeg`
3. Add to PATH:
   - Search "Environment Variables" in Start
   - Edit "Path" under System Variables
   - Add `C:\ffmpeg\bin`
   - Click OK

**Verify:**
```powershell
ffmpeg -version
```

#### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install -y ffmpeg

# Verify
ffmpeg -version
```

#### macOS

```bash
brew install ffmpeg

# Verify
ffmpeg -version
```

---

### Step 3: Clone/Download Project

**Option A: Git Clone**
```bash
git clone <repository-url>
cd video_producer
```

**Option B: Download ZIP**
1. Download project ZIP
2. Extract to desired location
3. Open terminal/command prompt
4. Navigate to extracted folder:
```bash
cd path/to/video_producer
```

---

### Step 4: Create Virtual Environment (Recommended)

**Why?** Isolates dependencies, prevents conflicts

#### Windows

```powershell
# Create virtual environment
python -m venv venv

# Activate
.\venv\Scripts\activate

# You should see (venv) in prompt
```

#### Linux/macOS

```bash
# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate

# You should see (venv) in prompt
```

**To deactivate later:**
```bash
deactivate
```

---

### Step 5: Install Python Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt
```

**This installs:**
- opencv-python (image processing)
- numpy (array operations)
- streamlit (web UI)
- onnxruntime (ML inference)
- PyYAML (config files)
- pandas (data handling)
- psutil (system monitoring)
- pynvml (GPU monitoring)
- scikit-image (image metrics)
- Pillow (image I/O)
- tqdm (progress bars)
- plotly (visualizations)
- pytest (testing)

**If installation fails:**
```bash
# Try installing one by one
pip install opencv-python numpy streamlit
pip install onnxruntime PyYAML pandas
pip install psutil pynvml scikit-image Pillow tqdm plotly pytest
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