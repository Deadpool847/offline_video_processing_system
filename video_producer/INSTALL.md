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

---

### Step 6: Verify Installation

**Test Python imports:**
```bash
python -c "import cv2, numpy, streamlit, onnxruntime; print('✅ All core packages installed')"
```

**Test FFmpeg:**
```bash
ffmpeg -version
# Should show version info
```

**Check NVENC (GPU encoding):**
```bash
ffmpeg -hide_banner -encoders | grep nvenc
# Should show: h264_nvenc, hevc_nvenc (if NVIDIA GPU present)
# If not shown: CPU-only mode will be used (still works fine)
```

---

### Step 7: Run Demo (Verify Everything Works)

```bash
# Run demo script
python scripts/demo.py
```

**Expected output:**
```
======================================================================
ML-Powered Video Producer - Stylizer Demo
======================================================================

Hardware Status:
  ✅ GPU: NVIDIA RTX 3070  (or ⚠️ GPU: Not detected)
  NVENC: Available  (or Not available)

Output directory: /app/outputs/demo

Generating sample image...
  ✅ Saved: original.png

Processing styles...
  Processing pencil... ✅ Saved: pencil.png
  Processing cartoon... ✅ Saved: cartoon.png
  Processing comic... ✅ Saved: comic.png
  Processing cinematic... ✅ Saved: cinematic.png

======================================================================
Demo complete! Check outputs in: /app/outputs/demo
======================================================================
```

**Check outputs:**
```bash
# Windows
explorer /app/outputs/demo

# Linux
xdg-open /app/outputs/demo

# macOS
open /app/outputs/demo
```

You should see 4 stylized images!

---

### Step 8: Start the Application

**Option A: Streamlit UI (Recommended)**
```bash
streamlit run app/streamlit_app.py
```

**Or use convenience script:**
```bash
# Linux/macOS
./START.sh

# Windows
streamlit run app/streamlit_app.py
```

**Then open browser:** http://localhost:8501

**Option B: CLI**
```bash
# View help
python -m scripts.cli --help

# Render video
python -m scripts.cli render --in video.mp4 --styles pencil --out outputs/
```

---

## GPU Setup (NVIDIA - HP OMEN)

### Check Current Setup

```bash
# Check if NVIDIA driver installed
nvidia-smi
```

**Good output:**
```
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 535.xx       Driver Version: 535.xx       CUDA Version: 12.x   |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| ...
```

**If command not found:** Drivers not installed

### Install NVIDIA Drivers

#### Windows

1. Visit [nvidia.com/Download/index.aspx](https://www.nvidia.com/Download/index.aspx)
2. Select your GPU (e.g., RTX 3070)
3. Download **Game Ready Driver** or **Studio Driver**
4. Run installer
5. Restart computer
6. Verify: `nvidia-smi`

#### Linux (Ubuntu)

```bash
# Add NVIDIA PPA
sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt update

# Install driver (version 535 recommended)
sudo apt install nvidia-driver-535

# Reboot
sudo reboot

# After reboot, verify
nvidia-smi
```

### Verify NVENC Support

```bash
ffmpeg -hide_banner -encoders | grep nvenc
```

**Should show:**
```
h264_nvenc          NVIDIA NVENC H.264 encoder
hevc_nvenc          NVIDIA NVENC HEVC encoder
```

**If not shown but GPU detected:**
- Update NVIDIA drivers to latest
- Reinstall FFmpeg
- Check GPU compatibility (GTX 10-series and newer support NVENC)

---

## Advanced: CUDA for PyTorch (Optional)

**Only needed if you want to fine-tune ML models**

### Check CUDA Version

```bash
nvidia-smi
# Look for "CUDA Version: 12.x"
```

### Install PyTorch with CUDA

**Visit:** [pytorch.org/get-started](https://pytorch.org/get-started/locally/)

**Example (CUDA 12.1):**
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

**Verify:**
```python
python -c "import torch; print('CUDA available:', torch.cuda.is_available())"
# Should print: CUDA available: True
```

---

## Troubleshooting Installation

### Python Issues

**"Python not found"**
- **Windows:** Reinstall Python, check "Add to PATH"
- **Linux:** Use `python3` instead of `python`
- **macOS:** Use `python3` instead of `python`

**"pip not found"**
```bash
# Windows
python -m ensurepip --upgrade

# Linux/macOS
sudo apt install python3-pip  # Linux
brew install python  # macOS
```

### FFmpeg Issues

**"ffmpeg not found"**
- **Windows:** Check PATH includes FFmpeg bin folder
- **Linux:** `sudo apt install ffmpeg`
- **macOS:** `brew install ffmpeg`

**"NVENC not available"**
- Update NVIDIA drivers
- Check GPU supports NVENC (GTX 10-series+)
- System will fallback to CPU encoding (still works)

### Dependency Issues

**"opencv not found"**
```bash
pip install opencv-python
```

**"ModuleNotFoundError: numpy"**
```bash
pip install numpy
```

**"Cannot install scikit-image"**
```bash
# Try without version constraints
pip install --no-deps scikit-image
pip install -r requirements.txt
```

### Permission Issues

**Linux: "Permission denied"**
```bash
# Don't use sudo pip, use virtual environment instead
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Windows: "Access denied"**
- Run command prompt as Administrator
- Or use virtual environment (recommended)

---

## Uninstallation

### Remove Virtual Environment

```bash
# Deactivate if active
deactivate

# Remove folder
rm -rf venv  # Linux/macOS
rmdir /s venv  # Windows
```

### Remove Python Packages

```bash
pip uninstall -r requirements.txt -y
```

### Remove Project

```bash
# Delete project folder
rm -rf video_producer  # Linux/macOS
rmdir /s video_producer  # Windows
```

---

## Next Steps

1. ✅ **Verified installation** with demo
2. 🚀 **Start UI:** `streamlit run app/streamlit_app.py`
3. 📖 **Read QUICKSTART.md** for 5-minute tutorial
4. 🎬 **Process your first video** in Dashboard
5. ⚙️ **Check Settings** for hardware optimization

---

**Installation complete!** 🎉

For quick start guide, see [QUICKSTART.md](QUICKSTART.md)

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