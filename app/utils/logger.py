"""
Logging utilities for GeoMask
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from app.config import settings


def setup_logger(name: str, level: str = None) -> logging.Logger:
    """
    Setup logger with consistent configuration
    
    Args:
        name: Logger name (usually __name__)
        level: Logging level (optional, uses settings if not provided)
        
    Returns:
        Configured logger instance
    """
    if level is None:
        level = settings.LOG_LEVEL
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )
    
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)
    
    # File handler for detailed logs
    try:
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"geomask_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(detailed_formatter)
        logger.addHandler(file_handler)
        
    except Exception as e:
        # If file logging fails, just log to console
        logger.warning(f"Could not setup file logging: {e}")
    
    # Error file handler
    try:
        error_log_file = log_dir / f"geomask_errors_{datetime.now().strftime('%Y%m%d')}.log"
        error_handler = logging.FileHandler(error_log_file)
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(detailed_formatter)
        logger.addHandler(error_handler)
        
    except Exception as e:
        logger.warning(f"Could not setup error file logging: {e}")
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


class LoggerMixin:
    """Mixin class to add logging capabilities to any class"""
    
    @property
    def logger(self) -> logging.Logger:
        """Get logger for this class"""
        return get_logger(self.__class__.__name__) 