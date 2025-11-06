# Troubleshooting Guide

**Solutions to common problems**

---

## Installation Issues

### Python Not Found

**Symptoms:**
```
'python' is not recognized as an internal or external command
```

**Solutions:**

**Windows:**
1. Reinstall Python from [python.org](https://www.python.org)
2. ✅ **Check "Add Python to PATH"** during installation
3. Restart terminal
4. Try: `python --version` or `py --version`

**Linux/macOS:**
```bash
# Use python3 instead
python3 --version

# Or create alias
echo "alias python=python3" >> ~/.bashrc
source ~/.bashrc
```

---

### FFmpeg Not Found

**Symptoms:**
```
ffmpeg: command not found
```

**Solutions:**

**Windows:**
```powershell
# Option 1: winget
winget install FFmpeg

# Option 2: Check PATH
# Search "Environment Variables" in Start Menu
# Add FFmpeg bin directory to PATH
# Example: C:\ffmpeg\bin
```

**Linux:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Verify:**
```bash
ffmpeg -version
```

---

### pip install fails

**Symptoms:**
```
ERROR: Could not find a version that satisfies the requirement...
```

**Solutions:**

**1. Upgrade pip:**
```bash
pip install --upgrade pip
```

**2. Install packages individually:**
```bash
pip install opencv-python
pip install numpy
pip install streamlit
pip install onnxruntime
# etc.
```

**3. Use Python 3.10+ (not 3.13+):**
```bash
python --version
# Should be 3.10.x, 3.11.x, or 3.12.x
```

**4. Check internet connection:**
```bash
ping pypi.org
```

---

### ModuleNotFoundError

**Symptoms:**
```
ModuleNotFoundError: No module named 'cv2'
```

**Solutions:**

**1. Verify installation:**
```bash
pip list | grep opencv
# Should show: opencv-python
```

**2. Reinstall:**
```bash
pip install opencv-python --force-reinstall
```

**3. Check virtual environment:**
```bash
# Make sure venv is activated
# Windows: .\venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
```

**4. Use correct Python:**
```bash
# Which python is pip using?
which pip  # Linux/Mac
where pip  # Windows

# Should point to venv if using virtual environment
```

---

## GPU/Hardware Issues

### NVENC Not Available

**Symptoms:**
- UI Settings shows "NVENC: Not available"
- Processing uses CPU encoding (slower)

**Solutions:**

**1. Check NVIDIA driver:**
```bash
nvidia-smi
```

**If command not found:**
- Download driver from [nvidia.com](https://www.nvidia.com/Download/index.aspx)
- Install and restart

**2. Verify FFmpeg NVENC:**
```bash
ffmpeg -encoders | grep nvenc
# Should show: h264_nvenc, hevc_nvenc
```

**If not shown:**
- Update NVIDIA driver to 535+
- Reinstall FFmpeg
- Check GPU supports NVENC (GTX 10-series and newer)

**3. Fallback to CPU:**
- System automatically uses libx264 (still works)
- Encoding slower but output quality identical

---

### GPU Not Detected

**Symptoms:**
- UI Settings shows "GPU: Not detected"

**Solutions:**

**1. Check NVIDIA driver:**
```bash
nvidia-smi
```

**2. Install pynvml:**
```bash
pip install pynvml
```

**3. Check GPU compatibility:**
- NVIDIA GPUs supported
- AMD/Intel GPUs: Use CPU mode (works fine)

**4. Continue without GPU:**
- All stylizers work on CPU
- Encoding uses CPU (libx264)
- Slightly slower but functional

---

### Out of Memory / VRAM

**Symptoms:**
```
CUDA out of memory
Out of memory error
```

**Solutions:**

**1. Reduce chunk size:**
- Settings → Chunk Duration: 60s or 90s

**2. Close other GPU apps:**
- Close games, browsers with GPU acceleration
- Check: `nvidia-smi` (shows GPU usage)

**3. Lower resolution:**
- Settings → Working Resolution: 720p

**4. Limit concurrent jobs:**
- Settings → Max Concurrent Jobs: 1

**5. Restart application:**
```bash
# Stop Streamlit (Ctrl+C)
# Start again
streamlit run app/streamlit_app.py
```

---

## Runtime Issues

### Port Already in Use

**Symptoms:**
```
OSError: [Errno 98] Address already in use
Port 8501 is already in use
```

**Solutions:**

**1. Use different port:**
```bash
streamlit run app/streamlit_app.py --server.port 8502
# Then open: http://localhost:8502
```

**2. Kill existing process:**

**Linux/macOS:**
```bash
# Find process
lsof -i :8501

# Kill it
kill -9 <PID>
```

**Windows:**
```powershell
# Find process
netstat -ano | findstr :8501

# Kill it
taskkill /PID <PID> /F
```

---

### Streamlit Not Loading

**Symptoms:**
- Browser shows "This site can't be reached"
- Blank page

**Solutions:**

**1. Check terminal for errors:**
- Look for error messages in terminal where you ran streamlit

**2. Try different URL:**
```
http://localhost:8501
http://127.0.0.1:8501
http://0.0.0.0:8501
```

**3. Try different browser:**
- Chrome, Firefox, Edge, Safari

**4. Disable browser extensions:**
- Try incognito/private mode

**5. Check firewall:**
- Allow Python/Streamlit through firewall

**6. Restart Streamlit:**
```bash
# Ctrl+C to stop
streamlit run app/streamlit_app.py
```

---

### Processing Too Slow

**Symptoms:**
- FPS < 5
- Processing takes hours

**Solutions:**

**1. Use Speed preset:**
- Dashboard → Preset: **Speed**

**2. Enable NVENC (if GPU):**
- Settings → Use NVENC: ✅

**3. Disable temporal stabilization:**
- Dashboard → Advanced → Temporal Stabilization: ☐

**4. Increase chunk size:**
- Settings → Chunk Duration: 60s+

**5. Select fewer styles:**
- Process one style at a time

**6. Lower resolution:**
- Settings → Working Resolution: 720p

**7. Check system resources:**
```bash
# CPU/RAM usage
top  # Linux/Mac
Task Manager  # Windows

# GPU usage (if NVIDIA)
nvidia-smi
```

---

### Audio Out of Sync

**Symptoms:**
- Audio doesn't match video
- Audio earlier/later than video

**Solutions:**

**1. Check source video:**
```bash
python scripts/probe.py input.mp4
# Check audio sample rate, codec
```

**2. Enable exact timing:**
- Settings → Exact Frame Timing: ✅

**3. Try different codec:**
- Settings → Codec: h264_nvenc or libx264

**4. Use audio passthrough:**
- Preserves original audio (no re-encoding)

**5. Check source integrity:**
```bash
# Play original video
# Check if audio already out of sync
```

---

### Output Quality Issues

**Symptoms:**
- Blocky/pixelated output
- Colors look wrong
- Output blurry

**Solutions:**

**1. Lower CRF (higher quality):**
- Dashboard → Advanced → CRF: 15 (instead of 18)
- Lower = better quality, larger file

**2. Use Quality preset:**
- Dashboard → Preset: **Quality**

**3. Check color space:**
- Settings → Preserve Color Space: ✅

**4. Use lossless:**
- Settings → Codec: FFV1 (lossless, large files)

**5. Compare with identity:**
```bash
# Process with no effects to check I/O quality
# If identity looks bad, issue is in I/O not stylizer
```

---

## Video Processing Issues

### Video Won't Process

**Symptoms:**
- "Failed to process video"
- Processing stuck at 0%

**Solutions:**

**1. Check video format:**
```bash
python scripts/probe.py video.mp4
# Check codec, resolution, FPS
```

**2. Convert video first:**
```bash
# Convert to standard format
ffmpeg -i input.mov -c:v libx264 -crf 18 output.mp4
```

**3. Check file path:**
- Use absolute path (full path from root)
- Avoid spaces in filename/path
- Use forward slashes: `/path/to/video.mp4`

**4. Check disk space:**
```bash
df -h  # Linux/Mac
# Windows: Check in File Explorer
```

**5. Check permissions:**
- Ensure read access to input
- Ensure write access to output directory

---

### Resume Not Working

**Symptoms:**
- Processing restarts from beginning after crash

**Solutions:**

**1. Check checkpoint directory:**
```bash
ls checkpoints/
# Should have .json files
```

**2. Enable checkpoints:**
- Settings → Auto-resume on crash: ✅

**3. Use same job ID:**
- Don't change video name/path mid-process

**4. Check logs:**
```bash
cat logs/$(date +%Y-%m-%d).log
# Look for checkpoint errors
```

---

## UI Issues

### Dashboard Not Showing Videos

**Symptoms:**
- Can't select files
- Path not working

**Solutions:**

**1. Use absolute paths:**
```
# ✅ Good
/home/user/Videos/video.mp4
C:\Users\User\Videos\video.mp4

# ❌ Bad
~/Videos/video.mp4
.\Videos\video.mp4
```

**2. Check file exists:**
```bash
ls /path/to/video.mp4  # Linux/Mac
dir C:\path\to\video.mp4  # Windows
```

**3. Use file picker (if available):**
- Some browsers support file upload widget

---

### Batch Queue Not Updating

**Symptoms:**
- Progress stuck
- Status not changing

**Solutions:**

**1. Refresh page:**
- Browser refresh (F5)

**2. Check logs:**
```bash
tail -f logs/$(date +%Y-%m-%d).log
```

**3. Restart Streamlit:**
```bash
# Ctrl+C to stop
streamlit run app/streamlit_app.py
```

---

### Style Lab Images Not Loading

**Symptoms:**
- Placeholder images only
- Comparison not working

**Solutions:**

**1. Process video first:**
- Need actual outputs to compare
- Dashboard → Process video

**2. Check output directory:**
```bash
ls /path/to/outputs/
# Should have processed videos
```

**3. Generate screenshots:**
- Currently uses placeholders
- Feature needs video frames extracted

---

## CLI Issues

### Command Not Found

**Symptoms:**
```
python: can't open file 'scripts/cli.py'
```

**Solutions:**

**1. Check current directory:**
```bash
pwd  # Should be in video_producer/
cd video_producer
```

**2. Use correct path:**
```bash
# From project root
python -m scripts.cli render --help

# Not: python scripts/cli.py
```

**3. Check Python path:**
```bash
echo $PYTHONPATH
# Should include project directory
```

---

### Arguments Not Working

**Symptoms:**
```
error: unrecognized arguments
```

**Solutions:**

**1. Check syntax:**
```bash
# ✅ Correct
python -m scripts.cli render --in video.mp4 --styles pencil --out outputs/

# ❌ Wrong
python -m scripts.cli render video.mp4 pencil outputs/
```

**2. Use quotes for paths with spaces:**
```bash
--in "/path/with spaces/video.mp4"
```

**3. Check help:**
```bash
python -m scripts.cli render --help
```

---

## Testing Issues

### Tests Failing

**Symptoms:**
```
FAILED tests/test_pixel_parity.py
```

**Solutions:**

**1. Install pytest:**
```bash
pip install pytest
```

**2. Run specific test:**
```bash
pytest tests/test_pixel_parity.py -v
```

**3. Check dependencies:**
```bash
pip list | grep -E "(pytest|opencv|numpy)"
```

**4. Update code:**
- Tests may need actual video files
- Currently use placeholders

---

## Performance Optimization

### Maximize Speed

```bash
# 1. Use Speed preset
# 2. Enable NVENC
# 3. Disable temporal stabilization
# 4. Increase chunk size to 90s
# 5. Process one style at a time
# 6. Close other applications
```

### Maximize Quality

```bash
# 1. Use Quality preset
# 2. Enable temporal stabilization
# 3. Set CRF to 15
# 4. Use smaller chunk size (20s)
# 5. Process at native resolution
# 6. Use lossless codec (FFV1) for archival
```

---

## Getting More Help

### Check Logs

```bash
# Daily log file
cat logs/$(date +%Y-%m-%d).log

# Real-time monitoring
tail -f logs/$(date +%Y-%m-%d).log
```

### System Information

```bash
# Python version
python --version

# FFmpeg version
ffmpeg -version

# GPU status (if NVIDIA)
nvidia-smi

# Installed packages
pip list

# Disk space
df -h  # Linux/Mac
# Windows: File Explorer → This PC
```

### Diagnostic Commands

```bash
# Test imports
python -c "import cv2, numpy, streamlit, onnxruntime; print('✅ All OK')"

# Run demo
python scripts/demo.py

# Run benchmark
python scripts/benchmark.py

# Probe video
python scripts/probe.py /path/to/video.mp4
```

---

## Still Having Issues?

1. **Check documentation:**
   - README.md
   - INSTALL.md
   - FEATURES.md

2. **Run diagnostics:**
   ```bash
   python scripts/demo.py
   python scripts/benchmark.py
   ```

3. **Check logs:**
   ```bash
   cat logs/$(date +%Y-%m-%d).log
   ```

4. **Try minimal example:**
   ```python
   # test_basic.py
   import cv2
   import numpy as np
   from stylizers import PencilStylizer
   
   # Create test image
   img = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
   
   # Apply style
   stylizer = PencilStylizer()
   result = stylizer.process(img)
   
   print("✅ Works!" if result is not None else "❌ Failed")
   ```

---

**Most issues are resolved by:**
1. Reinstalling dependencies
2. Updating drivers
3. Using absolute paths
4. Checking disk space
5. Restarting the application

Good luck! 🚀
