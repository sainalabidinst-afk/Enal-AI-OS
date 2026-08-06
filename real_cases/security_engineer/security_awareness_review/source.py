import os
import logging

logger = logging.getLogger(__name__)

def login(username, password):
    # No rate limiting
    # No MFA
    logger.debug(f"Login attempt: {username} {password}")
    if authenticate(username, password):
        logger.info(f"User {username} logged in")
        return True
    return False

def process_payment(credit_card):
    # Logging sensitive data
    logger.info(f"Processing card: {credit_card}")
    charge(credit_card)

# Hardcoded training password
TRAINING_PASSWORD = "security123"