import numpy as np
import logging

def detect_anomaly(data_point):
    # No statistical validation
    return data_point > 100

def process_user_input(user_input):
    # No input validation
    return eval(user_input)

def log_sensitive_data(data):
    # Logging sensitive data
    logger.info(f"Processing: {data['password']}")
    return True