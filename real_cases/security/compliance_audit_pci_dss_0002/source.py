def transmit_payment(data):
    # No TLS 1.2+
    # No certificate validation
    return requests.post("http://payment-gateway.com/charge", json=data)

def log_transaction(transaction):
    # Logging sensitive data
    logger.info(f"Transaction: {transaction['card_number']} {transaction['cvv']}")