import logging
import os


def log(message):
    log_file = "log_file.log"
    log_dir = "log"
    previous_log = "previous.log"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file_path = os.path.join(log_dir, log_file)
    previous_log_path = os.path.join(log_dir, previous_log)
    if os.path.exists(previous_log_path):
        os.remove(previous_log_path)
    if os.path.exists(log_file_path):
        os.rename(log_file_path, previous_log_path)
    logging.basicConfig(filename=log_file_path, level=logging.INFO)
    logging.info(message)
    logging.shutdown()
