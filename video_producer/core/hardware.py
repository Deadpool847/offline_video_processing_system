"""Hardware detection and optimization."""

import subprocess
import logging
from typing import Dict, Optional

try:
    import pynvml
    NVML_AVAILABLE = True
except ImportError:
    NVML_AVAILABLE = False
    pynvml = None

logger = logging.getLogger(__name__)


class HardwareManager:
    """Detect and manage hardware resources."""
    
    def __init__(self):
        self.gpu_available = False
        self.nvenc_available = False
        self.gpu_info = {}
        
        if NVML_AVAILABLE:
            self._init_nvml()
    
    def _init_nvml(self):
        """Initialize NVIDIA Management Library."""
        try:
            pynvml.nvmlInit()
            device_count = pynvml.nvmlDeviceGetCount()
            
            if device_count > 0:
                self.gpu_available = True
                handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                
                self.gpu_info = {
                    'name': pynvml.nvmlDeviceGetName(handle).decode('utf-8'),
                    'driver_version': pynvml.nvmlSystemGetDriverVersion().decode('utf-8'),
                    'cuda_version': pynvml.nvmlSystemGetCudaDriverVersion(),
                    'memory_total': pynvml.nvmlDeviceGetMemoryInfo(handle).total,
                    'compute_capability': pynvml.nvmlDeviceGetCudaComputeCapability(handle)
                }
                
                logger.info(f"GPU detected: {self.gpu_info['name']}")
            
        except Exception as e:
            logger.warning(f"NVML initialization failed: {e}")
    
    def check_nvenc(self) -> bool:
        """Check if NVENC is available."""
        try:
            result = subprocess.run(
                ['ffmpeg', '-hide_banner', '-encoders'],
                capture_output=True,
                text=True,
                check=True
            )
            self.nvenc_available = 'h264_nvenc' in result.stdout
            return self.nvenc_available
        except:
            return False
    
    def get_gpu_memory_usage(self) -> Optional[Dict]:
        """Get GPU memory usage."""
        if not NVML_AVAILABLE or not self.gpu_available:
            return None
        
        try:
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
            
            return {
                'total': mem_info.total,
                'used': mem_info.used,
                'free': mem_info.free,
                'utilization': (mem_info.used / mem_info.total) * 100
            }
        except Exception as e:
            logger.error(f"Failed to get GPU memory: {e}")
            return None
    
    def get_gpu_temperature(self) -> Optional[float]:
        """Get GPU temperature."""
        if not NVML_AVAILABLE or not self.gpu_available:
            return None
        
        try:
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
            return float(temp)
        except Exception as e:
            logger.error(f"Failed to get GPU temperature: {e}")
            return None
    
    def get_gpu_utilization(self) -> Optional[float]:
        """Get GPU utilization."""
        if not NVML_AVAILABLE or not self.gpu_available:
            return None
        
        try:
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            util = pynvml.nvmlDeviceGetUtilizationRates(handle)
            return float(util.gpu)
        except Exception as e:
            logger.error(f"Failed to get GPU utilization: {e}")
            return None
    
    def get_recommended_codec(self) -> str:
        """Get recommended codec based on hardware."""
        if self.check_nvenc():
            return 'h264_nvenc'
        else:
            logger.warning("NVENC not available, falling back to libx264")
            return 'libx264'
    
    def cleanup(self):
        """Cleanup NVML."""
        if NVML_AVAILABLE:
            try:
                pynvml.nvmlShutdown()
            except:
                pass