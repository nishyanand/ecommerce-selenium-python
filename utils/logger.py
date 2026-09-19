import logging

from pathlib import Path

# Ensure logs directory exists
LOG_DIR = Path(__file__).resolve().parents[1] / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "test_execution.log"

# Configure root logger only once
_logger = logging.getLogger()
if not _logger.handlers:
    _logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    # File handler
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)
    _logger.addHandler(file_handler)
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    _logger.addHandler(console_handler)

def get_logger(name: str = __name__) -> logging.Logger:
    """Return a logger with the configured handlers.

    Args:
        name: Name of the logger, typically ``__name__`` of the caller.
    """
    return logging.getLogger(name)
