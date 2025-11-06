# System Architecture

## Overview

The ML-Powered Video Producer is a modular, scalable video processing system designed for offline, high-quality artistic style transfer with continual learning capabilities.

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACES                         │
├──────────────────────┬──────────────────────────────────────┤
│  Streamlit Web UI    │         CLI                          │
│  (Multi-page)        │   (scripts/cli.py)                   │
└──────────────────────┴──────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   CORE PROCESSING LAYER                      │
├──────────────────────┬──────────────────────────────────────┤
│  Pipeline Manager    │   Checkpoint Manager                 │
│  (Chunking, Resume)  │   (State Persistence)                │
├──────────────────────┼──────────────────────────────────────┤
│  Temporal Stabilizer │   Metrics Collector                  │
│  (EMA, Deflicker)    │   (SSIM, Edge, etc.)                 │
└──────────────────────┴──────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     STYLE PROCESSORS                         │
├───────────┬─────────┬─────────┬──────────┬─────────────────┤
│  Pencil   │ Cartoon │  Comic  │Cinematic │ Neural Style    │
│  (CPU)    │  (CPU)  │  (CPU)  │ (CPU/GPU)│    (ONNX GPU)   │
└───────────┴─────────┴─────────┴──────────┴─────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                       I/O LAYER                              │
├──────────────────────┬──────────────────────────────────────┤
│  VideoReader         │   VideoWriter                        │
│  (PyAV/FFmpeg)       │   (FFmpeg + NVENC)                   │
├──────────────────────┼──────────────────────────────────────┤
│  ColorSpaceManager   │   Hardware Manager                   │
│  (LUT, Gamma)        │   (GPU, NVENC detect)                │
└──────────────────────┴──────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  ML LEARNING SYSTEM                          │
├──────────────────────┬──────────────────────────────────────┤
│  AutoTuner           │   FineTuner                          │
│  (Param Search)      │   (PyTorch Training)                 │
├──────────────────────┼──────────────────────────────────────┤
│  MLSession           │   ONNX Exporter                      │
│  (ONNX Inference)    │   (PyTorch → ONNX)                   │
└──────────────────────┴──────────────────────────────────────┘
```

## Module Breakdown

### 1. User Interfaces

#### Streamlit UI (`app/`)
- **streamlit_app.py**: Main entry with navigation
- **pages/dashboard.py**: Processing configuration
- **pages/batch_queue.py**: Job monitoring
- **pages/style_lab.py**: A/B comparison and feedback
- **pages/trainer_page.py**: ML fine-tuning interface
- **pages/settings_page.py**: Hardware configuration

#### CLI (`scripts/cli.py`)
- Command-line interface for batch processing
- Commands: render, preview, train

### 2. Core Processing (`core/`)

#### Pipeline (`pipeline.py`)
- Orchestrates video processing
- Chunking logic (configurable duration)
- Resume capability via checkpoints
- Async frame flow (decode → process → encode)

#### I/O (`io.py`)
- **VideoProbe**: FFprobe metadata extraction
- **VideoReader**: Stream-based frame reading (PyAV)
- **VideoWriter**: Hardware-accelerated encoding (FFmpeg)
- NVENC detection and fallback

#### Temporal Stabilization (`temporal.py`)
- EMA-based frame smoothing
- Edge map stabilization
- Prevents flicker

#### Color Management (`color.py`)
- Color space conversions (RGB ↔ Linear)
- 3D LUT loading and application
- .cube file parser
- Trilinear interpolation

#### Metrics Collection (`metrics.py`)
- Per-frame SSIM, MSE, edge coherence, sharpness
- JSON logging for ML feedback
- Summary statistics

#### ML Session (`ml_session.py`)
- ONNX Runtime wrapper
- GPU (CUDA EP) and CPU providers
- Tiled inference for large images
- Feathering for seamless blending

#### Auto-tuning (`autotune.py`)
- Grid search over parameter spaces
- Metric-based evaluation
- Best parameter selection

#### Checkpoint Management (`checkpoint.py`)
- JSON-based state persistence
- Resume from last completed chunk
- Clear on success

#### Hardware Management (`hardware.py`)
- NVIDIA GPU detection (pynvml)
- VRAM, temperature, utilization monitoring
- NVENC availability check
- Codec recommendation

#### Presets (`presets.py`)
- Default presets (Speed/Balanced/Quality)
- Custom preset loading (YAML)
- Preset saving and management

#### Logging (`logging_config.py`)
- Daily rotating logs
- Structured logging (file + console)

### 3. Style Processors (`stylizers/`)

#### Pencil Sketch (`pencil.py`)
- Grayscale + invert + blur + color dodge
- Optional paper texture
- Temporal EMA

#### Cartoon (`cartoon.py`)
- Bilateral filter (edge-preserving)
- K-means color quantization
- Canny edge detection
- Black edge overlay

#### Comic/Halftone (`comic.py`)
- RGB to CMYK conversion
- Angle-based halftone dots
- Bold edge detection

#### Cinematic (`cinematic.py`)
- 3D LUT application
- S-curve tone mapping
- Bloom (bright area blur)
- Film grain (noise)
- Vignette (radial darkening)

#### Fast Neural Style (`fast_style.py`)
- ONNX model inference
- Tiled processing (512px + 32px overlap)
- GPU acceleration
- NHWC ↔ NCHW conversion

### 4. ML Learning System (`trainer/`)

#### Fine-tuning (`finetune.py`)
- PyTorch training loop
- Validation and early stopping
- Best model checkpointing
- MSE loss (customizable)

#### Dataset (`dataset.py`)
- Input/target pair loading
- Transforms
- PyTorch Dataset interface

#### ONNX Export (`export_onnx.py`)
- PyTorch to ONNX conversion
- Dynamic axes for batch/resolution
- Model validation

### 5. Utilities (`scripts/`)

#### CLI (`cli.py`)
- Command-line interface
- Render, preview, train commands

#### Probe (`probe.py`)
- Video metadata inspection
- JSON output

#### Benchmark (`benchmark.py`)
- Performance testing
- FPS measurements
- Hardware info

#### Demo (`demo.py`)
- Quick stylizer test
- Sample image generation
- Output verification

#### Model Downloader (`download_models.py`)
- Pre-trained ONNX model download
- Progress reporting

## Data Flow

### Processing Pipeline

```
Input Video
    │
    ├──> VideoProbe (metadata)
    │
    ├──> Chunk Calculation (GOP boundaries)
    │
    └──> For each chunk:
          │
          ├──> VideoReader (stream frames)
          │
          ├──> For each frame:
          │     │
          │     ├──> Apply Stylizer
          │     ├──> Temporal Stabilizer (optional)
          │     ├──> Collect Metrics (optional)
          │     └──> Queue for encoding
          │
          ├──> VideoWriter (FFmpeg + NVENC)
          │
          └──> Save Checkpoint
    │
    ├──> Stitch Chunks (if multiple)
    │
    └──> Output Video
```

### ML Feedback Loop

```
User Feedback
    │
    ├──> Style Lab (A/B comparison, ratings)
    │
    ├──> MetricsCollector (SSIM, edge, etc.)
    │
    └──> Feedback Log (JSON)
         │
         ├──> Training Data (approved pairs)
         │
         └──> Trainer Page:
              │
              ├──> FineTuner (PyTorch)
              │
              ├──> Validation
              │
              ├──> Export to ONNX
              │
              └──> Update MLSession (new model)
```

## Hardware Utilization

### GPU Tasks
- ONNX model inference (CUDAExecutionProvider)
- NVENC video encoding (h264_nvenc/hevc_nvenc)
- Optional: PyTorch training (fine-tuning)

### CPU Tasks
- Pencil, Cartoon, Comic stylizers (OpenCV)
- Cinematic LUT/effects (NumPy)
- Frame decoding (FFmpeg)
- Metric calculation

### Optimization Strategy
- **Single GPU job**: Prevents VRAM contention
- **Parallel CPU jobs**: Utilize multi-core
- **NVENC offload**: Minimal GPU compute usage
- **Bounded queues**: Back-pressure control

## Scalability

### Vertical (Single Machine)
- Chunked processing: No RAM limit
- Resume capability: Long-running jobs
- Async pipeline: Overlap decode/process/encode
- NVENC: Hardware acceleration

### Horizontal (Future)
- Job queue system (Redis/Celery)
- Distributed workers
- Shared storage (NFS/S3)
- Load balancing

## Error Handling

### Graceful Degradation
1. **No GPU**: Fallback to CPU encoding (libx264)
2. **No NVENC**: Use libx264 with preset medium
3. **Model missing**: Use fallback effect or skip
4. **Crash mid-process**: Resume from last checkpoint
5. **Out of VRAM**: Reduce tile size, queue size

### Monitoring
- GPU temperature warnings (>80°C)
- VRAM utilization tracking
- Disk space checks
- Error logging (daily files)

## Configuration Files

### Presets (YAML)
```yaml
codec: h264_nvenc
crf: 18
preset: p4
chunk_duration: 30
use_temporal: true
description: "Balanced quality"
```

### Checkpoints (JSON)
```json
{
  "last_frame": 1500,
  "total_frames": 3000,
  "chunks_completed": 1,
  "codec": "h264_nvenc",
  "crf": 18
}
```

### Metrics Log (JSON)
```json
[
  {
    "frame_idx": 0,
    "style": "pencil",
    "processing_time": 0.042,
    "edge_coherence": 0.23,
    "ssim": 0.87,
    "sharpness": 145.3
  }
]
```

## Testing Strategy

### Unit Tests
- Pixel parity (identity pass)
- Chunk stitching (seamless output)
- A/V sync (timing verification)

### Integration Tests
- Full pipeline (input → output)
- Resume functionality
- Multi-style processing

### Performance Tests
- Benchmark script
- FPS measurements
- Memory profiling

## Security Considerations

- **Local only**: No network access required
- **File permissions**: Respect user access controls
- **Resource limits**: VRAM guards, disk checks
- **Input validation**: Video format verification