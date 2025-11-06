"""Logging configuration."""

import logging
from pathlib import Path
from datetime import datetime
import sys


def setup_logging(log_dir: str = "logs", level: int = logging.INFO):
    """Setup logging with daily rotation."""
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    
    # Daily log file
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = log_path / f"{today}.log"
    
    # Configure root logger
    logging.basicConfig(
        level=level,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized: {log_file}")


def get_logger(name: str) -> logging.Logger:
    """Get logger instance."""
    return logging.getLogger(name)