import statistics

def detect_fraud(transaction):
    # No anomaly detection
    # No rule engine
    return transaction.amount > 10000

def check_user_behavior(user_id):
    # No behavioral analysis
    return get_user_history(user_id)

# Hardcoded threshold
THRESHOLD = 1000
API_KEY = "anomaly_api_key_12345"