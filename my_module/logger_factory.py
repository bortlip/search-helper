import logging
import os

from datetime import datetime

def create_logger(name, level=logging.INFO, filename_prefix=None, base_log_dir="c:/log/gpt/"):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Create log directory based on date
    log_subdir = datetime.now().strftime("%Y-%m-%d")
    log_dir = os.path.join(base_log_dir, log_subdir)
    os.makedirs(log_dir, exist_ok=True)
   
    if filename_prefix:
        filename_suffix = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename= f"{filename_prefix}-{filename_suffix}.txt"
        log_file = os.path.join(log_dir, filename)
        fh = logging.FileHandler(log_file, encoding='utf-8')
        fh.setLevel(level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    else:
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger