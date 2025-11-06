# Local Machine Setup Guide

**Complete guide for running on your local computer (Windows, Linux, or Mac)**

---

## 🖥️ For Windows Users

### One-Time Setup

**1. Install Python 3.10+**
```powershell
# Download from python.org and run installer
# ✅ IMPORTANT: Check "Add Python to PATH" during installation
```

**2. Install FFmpeg**
```powershell
winget install FFmpeg
```

**3. Open PowerShell/Command Prompt**
```powershell
# Navigate to where you extracted the project
cd C:\Users\YourName\Downloads\video_producer
```

**4. Install Dependencies**
```powershell
pip install -r requirements.txt
```

**5. Run Demo (Verify)**
```powershell
python scripts\demo.py
```

**6. Start UI**
```powershell
streamlit run app\streamlit_app.py
```

**7. Open Browser**
- Go to: http://localhost:8501

### Processing Your Videos

**Location of your videos:**
- Example: `C:\Users\YourName\Videos\myvideo.mp4`

**In Dashboard:**
1. Paste full path: `C:\Users\YourName\Videos\myvideo.mp4`
2. Select styles
3. Output: `C:\Users\YourName\Desktop\output`
4. Click "Process Full"

**Check outputs:**
```powershell
explorer C:\Users\YourName\Desktop\output
```

---

## 🐧 For Linux Users (Ubuntu/Debian)

### One-Time Setup

**1. Install Dependencies**
```bash
# Update system
sudo apt update

# Install Python and FFmpeg
sudo apt install -y python3.10 python3-pip ffmpeg

# Verify
python3 --version
ffmpeg -version
```

**2. Navigate to Project**
```bash
cd ~/Downloads/video_producer
# or wherever you extracted the project
```

**3. Install Python Packages**
```bash
pip3 install -r requirements.txt
```

**4. Run Demo (Verify)**
```bash
python3 scripts/demo.py
```

**5. Start UI**
```bash
streamlit run app/streamlit_app.py
```

**6. Open Browser**
- Go to: http://localhost:8501

### Processing Your Videos

**Location of your videos:**
- Example: `/home/username/Videos/myvideo.mp4`

**In Dashboard:**
1. Paste full path: `/home/username/Videos/myvideo.mp4`
2. Select styles
3. Output: `/home/username/output`
4. Click "Process Full"

**Check outputs:**
```bash
xdg-open ~/output
```

---

## 🍎 For macOS Users

### One-Time Setup

**1. Install Homebrew (if not installed)**
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**2. Install Python and FFmpeg**
```bash
brew install python@3.10 ffmpeg

# Verify
python3 --version
ffmpeg -version
```

**3. Navigate to Project**
```bash
cd ~/Downloads/video_producer
# or wherever you extracted the project
```

**4. Install Python Packages**
```bash
pip3 install -r requirements.txt
```

**5. Run Demo (Verify)**
```bash
python3 scripts/demo.py
```

**6. Start UI**
```bash
streamlit run app/streamlit_app.py
```

**7. Open Browser**
- Go to: http://localhost:8501

### Processing Your Videos

**Location of your videos:**
- Example: `/Users/username/Movies/myvideo.mp4`

**In Dashboard:**
1. Paste full path: `/Users/username/Movies/myvideo.mp4`
2. Select styles
3. Output: `/Users/username/Desktop/output`
4. Click "Process Full"

**Check outputs:**
```bash
open ~/Desktop/output
```

---

## 🎮 HP OMEN Specific (NVIDIA GPU)

### Enable GPU Acceleration

**1. Check GPU**
```bash
nvidia-smi
# Should show your GPU (e.g., RTX 3070)
```

**If not working:**
- Download latest driver from [nvidia.com](https://www.nvidia.com/Download/index.aspx)
- Install and restart computer

**2. Verify NVENC**
```bash
ffmpeg -encoders | grep nvenc
# Should show: h264_nvenc, hevc_nvenc
```

**3. In UI Settings:**
- Go to "Settings" page
- Check GPU status (should show GPU name)
- Enable "Use NVENC" checkbox
- View temperature, VRAM usage

**4. Optional: Reduce Heat**
```bash
# Set power limit (150W for RTX 3070)
nvidia-smi -pl 150
```

**Performance with GPU:**
- Encoding: 200+ fps (vs 50-100 fps CPU)
- Neural styles: 15-20 fps GPU (vs 3-5 fps CPU)

---

## 📁 Organizing Your Workflow

### Recommended Folder Structure

```
Your Computer/
├── Videos/               # Input videos
│   ├── raw/             # Original footage
│   └── to_process/      # Ready to process
├── video_producer/      # This project
└── Outputs/             # Processed results
    ├── pencil/
    ├── cartoon/
    └── cinematic/
```

### Batch Processing Multiple Videos

**Option 1: Process Folder (UI)**
1. Dashboard → Input Type: **Folder**
2. Folder Path: `/path/to/Videos/to_process/`
3. Select styles
4. Process

**Option 2: CLI (Multiple videos)**
```bash
# Process all MP4 files in a folder
for video in /path/to/videos/*.mp4; do
  python -m scripts.cli render \
    --in "$video" \
    --styles pencil,cartoon \
    --preset Balanced \
    --out /path/to/outputs/
done
```

---

## 🚀 Performance Tips

### Speed Up Processing

**1. Use Faster Preset**
- Settings → Preset: **Speed** (instead of Balanced/Quality)

**2. Enable GPU Encoding**
- Settings → Use NVENC: ✅ (if NVIDIA GPU)

**3. Disable Temporal Stabilization**
- Dashboard → Advanced → Temporal Stabilization: ☐
- (Faster but may have slight flicker)

**4. Increase Chunk Size**
- Settings → Chunk Duration: 60s (instead of 30s)
- (Uses less overhead for large videos)

**5. Process at Lower Resolution**
- Settings → Working Resolution: 720p
- (Then upscale if needed)

### Quality Tips

**1. Use Quality Preset**
- Dashboard → Preset: **Quality**

**2. Enable Temporal Stabilization**
- Dashboard → Advanced → Temporal Stabilization: ✅

**3. Lower CRF Value**
- Dashboard → Advanced → CRF: 15 (instead of 18)
- (Lower = higher quality, larger file)

**4. Use Lossless Codec**
- Settings → Codec: FFV1 (lossless)
- (For archival, very large files)

---

## 🔍 Finding Video Paths

### Windows

**Method 1: File Explorer**
1. Navigate to video in File Explorer
2. Right-click video → Properties
3. Copy "Location" path
4. Add filename: `C:\Users\...\video.mp4`

**Method 2: Shift + Right-Click**
1. Hold Shift, right-click video
2. Click "Copy as path"
3. Paste in Dashboard

### Linux/Mac

**Method 1: Terminal**
```bash
# Navigate to video folder
cd ~/Videos

# Get full path
realpath myvideo.mp4
# Copy this path
```

**Method 2: GUI**
- **Linux:** Right-click → Properties → Location
- **Mac:** Right-click → Get Info → Where

---

## 📝 Example Workflows

### Workflow 1: Quick Test

```bash
# 1. Run demo to verify
python scripts/demo.py

# 2. Check outputs
ls /app/outputs/demo/
# Should see: original.png, pencil.png, cartoon.png, cinematic.png
```

### Workflow 2: Process Single Video

**UI:**
1. Start: `streamlit run app/streamlit_app.py`
2. Dashboard → Enter video path
3. Select: Pencil + Cartoon
4. Preset: Balanced
5. Process

**CLI:**
```bash
python -m scripts.cli render \
  --in /path/to/video.mp4 \
  --styles pencil,cartoon \
  --preset Balanced \
  --out /path/to/output/
```

### Workflow 3: Compare All Styles

1. Dashboard → Select **all 5 styles**
2. Preset: Balanced
3. Process
4. Go to "Style Lab"
5. Compare outputs side-by-side
6. Rate your favorites (helps ML learn)

### Workflow 4: Fine-tune for Your Content

1. Style Lab → Select style
2. Adjust parameters (blur, colors, etc.)
3. Click "Auto-Tune Parameters"
4. Use tuned settings for future videos

---

## ❓ Common Questions

**Q: Can I close the terminal while processing?**
- **UI:** No, keep Streamlit running
- **CLI:** Yes, add `&` at end of command

**Q: How do I stop processing?**
- **UI:** Batch Queue → Click "Cancel"
- **CLI:** Press Ctrl+C

**Q: Can I process multiple videos at once?**
- Yes, use Folder input or CLI loop

**Q: Where are outputs saved?**
- Location you specified in "Output Directory"
- Check Batch Queue for exact paths

**Q: How long does processing take?**
- Depends on video length and style
- Rough estimate: 1080p/30fps video
  - 1 minute video ≈ 2-5 minutes processing
  - GPU makes encoding faster (not stylizing)

**Q: Can I use this without internet?**
- Yes! Fully offline after installation

**Q: Does it work on old computers?**
- Yes, but slower
- CPU-only mode works fine
- Lower resolution if too slow

---

## 🆘 Quick Troubleshooting

**"Python not found"**
```bash
# Windows: Reinstall Python, check "Add to PATH"
# Linux/Mac: Use python3 instead of python
```

**"ffmpeg not found"**
```bash
# Install FFmpeg (see setup sections above)
# Verify: ffmpeg -version
```

**"Port 8501 already in use"**
```bash
# Use different port
streamlit run app/streamlit_app.py --server.port 8502
```

**"Out of memory"**
- Close other applications
- Settings → Reduce chunk size
- Process at lower resolution

**UI not loading?**
- Check terminal for errors
- Try: http://127.0.0.1:8501
- Try different browser

---

## 📞 Need More Help?

- **Installation issues:** See [INSTALL.md](INSTALL.md)
- **Feature details:** See [FEATURES.md](FEATURES.md)
- **Architecture:** See [ARCHITECTURE.md](ARCHITECTURE.md)

---

**Happy processing!** 🎬✨
