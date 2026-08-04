def process_payment(card_data):
    # No PCI-DSS compliance
    # No encryption
    # Logging card data
    logger.info(f"Processing card: {card_data}")
    charge(card_data)

def store_card(card_number):
    # No encryption at rest
    db.insert("cards", {"number": card_number, "cvv": cvv})