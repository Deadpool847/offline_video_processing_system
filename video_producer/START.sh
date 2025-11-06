#!/bin/bash
# Quick start script for ML-Powered Video Producer

set -e

echo "==========================================" 
echo "ML-Powered Video Producer"
echo "HP OMEN Optimized"
echo "=========================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 not found"
    exit 1
fi

echo "Python: $(python3 --version)"

# Check FFmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "Warning: FFmpeg not found - video processing may fail"
else
    echo "FFmpeg: $(ffmpeg -version | head -n1)"
fi

echo ""
echo "==========================================" 
echo "Starting Streamlit UI..."
echo "=========================================="
echo ""
echo "Open browser at: http://localhost:8501"
echo "Press Ctrl+C to stop"
echo ""

# Start Streamlit
cd "$(dirname "$0")"
export PYTHONPATH="$(pwd):$PYTHONPATH"
streamlit run app/streamlit_app.py --server.port 8501 --server.address 0.0.0.0