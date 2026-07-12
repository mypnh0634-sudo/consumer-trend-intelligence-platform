import logging
import os
from datetime import datetime

def setup_logger(name: str = "platform_logger") -> logging.Logger:
    """Thiết lập hệ thống Logger ghi lại lịch sử hoạt động."""
    logger_obj = logging.getLogger(name)
    logger_obj.setLevel(logging.INFO)

    if logger_obj.handlers:
        return logger_obj

    os.makedirs("logs", exist_ok=True)

    formatter = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    current_date = datetime.now().strftime("%Y-%m-%d")
    file_handler = logging.FileHandler(f"logs/app_{current_date}.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger_obj.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger_obj.addHandler(stream_handler)

    return logger_obj

# Đảm bảo dòng này viết thường chính xác để file khác import
logger = setup_logger()