def process_medical_record(record_id):
    # No encryption
    # No access control
    record = get_record(record_id)
    logger.info(f"Processing medical record: {record}")
    return record

def transmit_phi(data):
    # No TLS
    # No audit log
    return requests.post("http://external.com/phi", json=data)