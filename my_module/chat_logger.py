import logging
import json
import os

from datetime import datetime

class ChatLogger:

    def __init__(self, filename_prefix, base_log_dir="c:/log/gpt/"):
        self.transcript_logger = logging.getLogger('chat_transcript')
        self.transcript_logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S %p')

        filename_suffix = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"{filename_prefix}-{filename_suffix}"
        
        # Create log directory based on date
        log_subdir = datetime.now().strftime("%Y-%m-%d")
        log_dir = os.path.join(base_log_dir, log_subdir)
        os.makedirs(log_dir, exist_ok=True)

        # Update file paths to include the log directory
        transcript_file = os.path.join(log_dir, filename + ".txt")
        json_file = os.path.join(log_dir, filename + ".json")

        fh = logging.FileHandler(transcript_file, encoding='utf-8')
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
        self.transcript_logger.addHandler(fh)

        self.json_logger = logging.getLogger('chat_json')
        self.json_logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(message)s')
        fh = logging.FileHandler(json_file, encoding='utf-8')
        fh.setLevel(logging.INFO)
        fh.setFormatter(formatter)
        self.json_logger.addHandler(fh)

    def log_message(self, message):
        # Log to the transcript file
        self.transcript_logger.info(f'{message.role}: {message.content}')

        # Log to the JSON file
        message_json = json.dumps(message.__dict__)
        self.json_logger.info(message_json)
