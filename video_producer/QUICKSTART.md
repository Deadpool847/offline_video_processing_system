# Quick Start Guide

## 5-Minute Setup

### 1. Install Dependencies

```bash
cd /app/video_producer
pip install -r requirements.txt
```

### 2. Run Demo

```bash
python scripts/demo.py
```

This creates sample stylized images in `/app/outputs/demo/`

### 3. Launch Streamlit UI

```bash
streamlit run app/streamlit_app.py
```

Open: http://localhost:8501

## Using the UI

### Dashboard (Main)

1. **Input**: Paste video path or select folder
2. **Styles**: Check styles to apply
   - ✅ Pencil Sketch
   - ✅ Cartoon
   - ✅ Comic/Halftone
   - ✅ Cinematic
   - ✅ Fast Neural Style
3. **Preset**: Choose Speed/Balanced/Quality
4. **Output**: Set output directory
5. **Preview** or **Process Full**

### Batch Queue

- Monitor jobs
- Pause/Resume/Cancel
- View progress and ETA

### Style Lab

- Compare styles A/B
- Rate outputs (1-5 stars)
- Auto-tune parameters
- Provide feedback for ML

### Trainer

- Fine-tune ML models
- Collect training data
- Export improved ONNX
- Rollback checkpoints

### Settings

- Check GPU/NVENC status
- Configure hardware
- Manage presets
- Power management

## CLI Quick Reference

### Render

```bash
python -m scripts.cli render \
  --in video.mp4 \
  --styles pencil,cartoon \
  --preset Balanced \
  --out outputs/
```

### Preview

```bash
python -m scripts.cli preview \
  --in video.mp4 \
  --style cinematic \
  --start 00:00:10 \
  --dur 8s
```

### Train

```bash
python -m scripts.cli train \
  --data trainer/data \
  --epochs 1 \
  --export assets/models/style.onnx
```

## Key Features

✅ **5 Artistic Styles**
- Pencil Sketch (temporal stabilized)
- Cartoon (edge-preserving)
- Comic/Halftone (CMYK patterns)
- Cinematic (LUT + bloom + grain)
- Fast Neural Style (ML-powered)

✅ **Pixel-Perfect**
- Preserves resolution, FPS, color space
- Lossless or visually lossless output
- Audio sync guaranteed

✅ **Large Videos**
- Stream-based processing
- Chunked with auto-resume
- No RAM limits

✅ **ML Learning**
- Collects metrics
- User feedback
- Continual fine-tuning
- Auto-parameter tuning

✅ **HP OMEN Optimized**
- NVENC hardware encoding
- GPU detection
- VRAM monitoring
- Power management

## Next Steps

1. **Process your first video** via Dashboard
2. **Compare styles** in Style Lab
3. **Tune parameters** for your content
4. **Provide feedback** to improve ML
5. **Run benchmarks** to check performance

## Getting Help

- Check `/app/video_producer/README.md`
- See `/app/video_producer/INSTALL.md` for setup issues
- Run: `python scripts/benchmark.py` for performance test
- Run: `python scripts/probe.py video.mp4` to inspect videos

## Tips

💡 Use **Balanced** preset for most cases
💡 Enable **NVENC** in Settings for speed
💡 **Preview** before full render
💡 **Temporal stabilization** prevents flicker
💡 Check **GPU temperature** during long jobs