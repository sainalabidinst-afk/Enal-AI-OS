import logging

logger = logging.getLogger(__name__)

def login(username, password):
    # Sensitive data in logs
    logger.debug(f"Login attempt: {username} {password}")
    if authenticate(username, password):
        logger.info(f"User {username} logged in")
        return True
    return False

def process_payment(credit_card):
    # PCI-DSS violation
    logger.info(f"Processing payment for card: {credit_card}")
    pass

def api_call(endpoint, token):
    # Secret in log
    logger.debug(f"API call to {endpoint} with token {token}")
    response = requests.get(endpoint, headers={"Authorization": f"Bearer {token}"})
    return response