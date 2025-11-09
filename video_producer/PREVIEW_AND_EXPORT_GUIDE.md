# Preview & Export Features Guide

## 🎬 5-Second Preview Feature

### What It Does
Generate a quick 5-second preview of any style to see results before processing the full video.

### How to Use

**From Dashboard:**

1. **Upload or Select Video**
   - Use File Browser to upload
   - Or enter video path manually

2. **Select Style** (at least one)
   - Pencil Sketch
   - Cartoon
   - Comic/Halftone
   - Cinematic
   - Neural Style

3. **Adjust Effect Intensity**
   - Slider: 0.1x to 2.0x
   - 1.0x = Normal strength

4. **Click "🔍 Preview (5s)"**

### What You Get

✅ **Instant Results:**
- Processes first 5 seconds of video
- Shows preview with video player
- Displays processing stats (FPS, time, frames)

✅ **Download Option:**
- Download preview as MP4
- Share for quick feedback
- Test before full processing

✅ **Time Estimation:**
- See estimated time for full video
- Based on actual preview performance

### Example Use Cases

1. **Test Multiple Intensities:**
   ```
   - Preview at 0.5x (subtle)
   - Preview at 1.0x (normal)  
   - Preview at 1.5x (strong)
   - Choose best intensity
   ```

2. **Quick Style Comparison:**
   ```
   - Preview Pencil style
   - Preview Cartoon style
   - Compare results
   - Process full video with winner
   ```

3. **Parameter Validation:**
   ```
   - Preview with Speed preset
   - Preview with Quality preset
   - Check visual difference
   - Decide on full processing settings
   ```

---

## 📁 Export & Download Features

### What It Does
Access, download, and manage all processed videos with multiple export options.

### Available Actions

#### 1. **Play Video** (▶️ Play)
- Stream video directly in browser
- No download needed for quick viewing
- Works for any completed style

**How:**
1. Go to **Batch Queue**
2. Expand completed job
3. Click "▶️ Play" next to any style
4. Video player appears inline
5. Click "⏹️ Close" when done

#### 2. **Download Single Video** (📥 Download)
- Download any stylized video
- Full quality MP4 file
- Original resolution preserved

**How:**
1. Go to **Batch Queue**
2. Find completed job
3. Click "📥 Download" for desired style
4. File saves to your Downloads folder

#### 3. **Open Output Folder** (📂 Open Folder)
- Opens folder with all processed videos
- Platform-specific (Windows Explorer, Mac Finder, Linux file manager)
- Quick access to all outputs

**How:**
1. Expand completed job
2. Click "📂 Open Folder"
3. Folder opens with all files

#### 4. **Package All Styles** (📦 Package All)
- Creates ZIP with all processed videos
- One download for all styles
- Perfect for sharing or archiving

**How:**
1. Expand completed job
2. Click "📦 Package All"
3. Wait for packaging
4. Click "📥 Download Package"
5. Get ZIP with all videos

#### 5. **Process Again** (🔄 Process Again)
- Re-process with same settings
- Try different intensity
- Refine results

**How:**
1. Expand completed job
2. Click "🔄 Process Again"
3. New job created in queue
4. Adjust settings if desired

### Export Features by Location

#### Dashboard
- Preview download (5s sample)
- Quick test downloads

#### Batch Queue
- All processed videos
- Individual downloads
- Bulk packaging
- Folder access

#### Style Lab
- Comparison samples download
- A/B test results
- Side-by-side videos

---

## 🎨 Style Lab Enhancements

### Generate Multi-Style Comparison

**Purpose:** Compare multiple styles side-by-side on same video sample

**How to Use:**

1. **Go to Style Lab**

2. **Upload or Enter Video Path**
   - File browser or manual path
   - Any supported format

3. **Set Sample Parameters**
   - Start Time: Where to begin (seconds)
   - Duration: 3-15 seconds
   - Effect Intensity: 0.5-2.0x

4. **Select Styles** (2-4 styles)
   - Pencil Sketch
   - Cartoon
   - Comic/Halftone
   - Cinematic
   - Neural Style

5. **Click "🎬 Generate Comparison"**

### What You Get

✅ **Side-by-Side Results:**
- All selected styles processed
- Displayed in columns
- Easy visual comparison

✅ **Individual Controls:**
- Rate each style (1-5 stars)
- Download any style
- See processing stats

✅ **A/B Direct Comparison:**
- Select any two styles
- View side-by-side
- Rate and compare directly

✅ **Original Reference:**
- View original video
- Compare against processed
- Validate results

### Example Workflow

**Finding Best Style for Your Video:**

```
1. Upload 10s sample clip
2. Select all 5 styles
3. Generate comparison
4. Rate each result
5. Download favorites
6. Process full video with winner
```

**Testing Effect Intensity:**

```
1. Same video sample
2. Generate at 0.5x intensity
3. Generate at 1.0x intensity
4. Generate at 1.5x intensity
5. Compare and choose best
```

---

## 🚀 Advanced Features

### Video Information Display

For each completed job:
- File size (MB)
- Resolution
- Duration
- FPS
- Processing time
- Average FPS during processing

### Automatic Cleanup

- Preview files auto-delete after 24 hours
- Saves disk space
- Configurable retention period

### Comparison Video Creation

Future feature: Create side-by-side comparison videos
- Original vs Processed
- Style A vs Style B
- Multiple styles in grid

### Format Conversion

Future feature: Convert to different formats
- MP4, AVI, MOV, WebM
- Different codecs
- Resolution scaling

---

## 💡 Pro Tips

### Preview Tips

1. **Test First 5s of Video:**
   - Representative sample
   - Quick feedback
   - Iterate on settings

2. **Use Preview for:**
   - Testing effect intensity
   - Comparing presets
   - Validating parameters

3. **Save Previews:**
   - Download interesting results
   - Share for feedback
   - Reference for full processing

### Export Tips

1. **Organize Downloads:**
   ```
   Downloads/
   ├── video1_pencil.mp4
   ├── video1_cartoon.mp4
   └── video1_all_styles.zip
   ```

2. **Use Package All:**
   - When processing multiple styles
   - For client delivery
   - For archival

3. **Open Folder:**
   - Quickly access all outputs
   - Batch rename if needed
   - Move to permanent storage

### Style Lab Tips

1. **Start with Extremes:**
   - Test very different styles first
   - Narrow down preferences
   - Then fine-tune intensity

2. **Use Short Samples:**
   - 5-10 seconds is enough
   - Faster iteration
   - Less storage used

3. **Rate Everything:**
   - Builds feedback data
   - Improves ML learning
   - Better auto-optimization

---

## ⚡ Performance Notes

### Preview Generation
- **Speed Preset:** ~30-50 FPS encoding
- **Balanced Preset:** ~20-30 FPS encoding
- **Quality Preset:** ~10-20 FPS encoding

**5s preview takes:**
- Speed: ~2-5 seconds
- Balanced: ~5-10 seconds
- Quality: ~10-15 seconds

### Export Performance
- **Download:** Instant (file already exists)
- **Package:** ~1-5 seconds per GB
- **Open Folder:** Instant

### Style Lab
- Multiple styles processed sequentially
- 3 styles on 5s = ~15-30 seconds
- Faster with GPU/NVENC

---

## 🆘 Troubleshooting

### Preview Issues

**"Preview failed":**
- Check video file exists
- Verify format supported (mp4, avi, mov, mkv)
- Ensure FFmpeg installed

**"No preview shown":**
- Check browser video codec support
- Try downloading and playing externally
- Update browser

### Export Issues

**"Download failed":**
- Check file exists in output folder
- Verify sufficient disk space
- Check file permissions

**"Open folder not working":**
- Manually navigate to output path
- Check path is correct
- Platform may not support auto-open

**"Package all failed":**
- Check all style files exist
- Verify disk space for ZIP
- Close any open video files

### Style Lab Issues

**"Comparison generation slow":**
- Reduce number of styles (2-3 max)
- Shorten duration (5s instead of 10s)
- Use Speed preset

**"Videos not playing":**
- Check browser video support
- Download and play externally
- Convert format if needed

---

## 📊 Feature Comparison

| Feature | Dashboard | Batch Queue | Style Lab |
|---------|-----------|-------------|-----------|
| 5s Preview | ✅ Yes | ❌ No | ❌ No |
| Download | ✅ Preview | ✅ Full | ✅ Samples |
| Play Inline | ✅ Preview | ✅ Full | ✅ Samples |
| Package All | ❌ No | ✅ Yes | ❌ No |
| A/B Compare | ❌ No | ❌ No | ✅ Yes |
| Multi-Style | ❌ No | ✅ Yes | ✅ Yes |
| Rating | ❌ No | ❌ No | ✅ Yes |

---

## 🎓 Learning Resources

### Video Processing Basics
- Understand FPS and resolution
- Learn about codecs (H.264, NVENC)
- Explore quality settings (CRF)

### Style Selection
- Pencil: Best for portraits, sketches
- Cartoon: Great for animations, bright scenes
- Comic: Perfect for bold, graphic look
- Cinematic: Ideal for films, dramatic effect
- Neural: Artistic, painterly results

### Effect Intensity
- 0.3-0.7x: Subtle, barely noticeable
- 0.8-1.2x: Natural, balanced
- 1.3-2.0x: Strong, dramatic

---

**Now you have full control over previewing, exporting, and comparing your stylized videos!** 🎉
